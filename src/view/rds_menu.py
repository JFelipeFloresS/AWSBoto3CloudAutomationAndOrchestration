from src.controller.RDSController import RDSController
from src.model.Resources import Resource
from src.utils.list_utils import list_ordered_list
from src.utils.user_input_handler import get_user_input
from src.view.AbstractMenu import AbstractMenu


class RDSMenu(AbstractMenu):
    def __init__(self):
        rds_menu_options = \
            {1: "List DB instances",
             2: "Create DB instance",
             3: "Delete DB instance",
             4: "Reboot DB instance",
             5: "List DB snapshots",
             6: "Create DB snapshot",
             7: "Delete DB snapshot",
             8: "Restore DB instance from snapshot",
             9: "Main menu",
             99: "Exit"}
        super().__init__("RDS Menu", rds_menu_options)

        res = Resource()
        rds = res.rds_client()
        self.rds_controller = RDSController(rds)

        self.valid_engines = ["mysql", "postgres", "mariadb"]

    def execute_choice(self, choice):
        if choice == 1:
            self.list_db_instances()
        elif choice == 2:
            self.create_db_instance()
        elif choice == 3:
            self.delete_db_instance()
        elif choice == 4:
            self.reboot_db_instance()
        elif choice == 5:
            self.list_db_snapshots()
        elif choice == 6:
            self.create_db_snapshot()
        elif choice == 7:
            self.delete_db_snapshot()
        elif choice == 8:
            self.restore_db_instance_from_snapshot()
        elif choice == 9:
            return False
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()

        return True

    def list_db_instances(self):
        """
        List all RDS DB instances in the account.
        :return: List of RDS DB instance identifiers.
        """
        try:
            db_instances = self.rds_controller.list_db_instances()
            db_string_list = [
                f"{db_instance['DBName']} ({db_instance['DBInstanceIdentifier']} - {db_instance['Engine']}): {db_instance['DBInstanceStatus']}"
                for db_instance in db_instances
            ]
            list_ordered_list(db_string_list, "RDS DB Instances:")
            return [db_instances['DBInstanceIdentifier'] for db_instances in db_instances]
        except Exception as e:
            print(f"Error listing DB instances: {e}")
            return []

    def create_db_instance(self):
        """
        Create a new RDS DB instance.
        :return: The identifier of the created DB instance.
        """

        # get db name
        db_name = get_user_input("Enter the database name")
        if not db_name: return None

        # get db instance identifier
        db_id = get_user_input("Enter the DB instance identifier (to be unique)")
        if not db_id: return None

        # get db engine
        valid_db_engines = list_ordered_list(self.valid_engines, "Available DB engines:")
        db_engine = get_user_input("Enter the DB engine", available_options=valid_db_engines)
        if not db_engine: return None

        # get availability zone
        availability_zone = get_user_input("Enter the availability zone", default_value="eu-west-1a")
        if not availability_zone: return None

        try:
            db_instance_id = self.rds_controller.create_db_instance(db_name, db_id, db_engine, availability_zone)
            # wait for db instance to be available
            print("Waiting for DB instance to be available...")
            waiter = self.rds_controller.rds_client.get_waiter('db_instance_available')
            waiter.wait(DBInstanceIdentifier=db_instance_id)
            print(f"DB instance '{db_instance_id}' created successfully.")
            return db_instance_id
        except Exception as e:
            print(f"Error creating DB instance: {e}")
            return None

    def delete_db_instance(self):
        """
        Delete an existing RDS DB instance.
        :return: The identifier of the deleted DB instance.
        """

        # get db instance id
        db_instances = self.list_db_instances()
        if not db_instances:
            print("No DB instances available to delete.")
            return None
        db_instance_id = get_user_input("Enter the DB instance identifier to delete", available_options=db_instances)
        if not db_instance_id: return None

        # delete db instance
        try:
            db_instance_id = self.rds_controller.delete_db_instance(db_instance_id)
            print(f"DB instance '{db_instance_id}' deleted successfully.")
            return db_instance_id
        except Exception as e:
            print(f"Error deleting DB instance: {e}")
            return None

    def reboot_db_instance(self):
        """
        Reboot an existing RDS DB instance.
        :return: The identifier of the rebooted DB instance.
        """

        # get db instance id
        db_instances = self.list_db_instances()
        if not db_instances:
            print("No DB instances available to reboot.")
            return None
        db_instance_id = get_user_input("Enter the DB instance identifier to reboot", available_options=db_instances)
        if not db_instance_id: return None

        # reboot db instance
        try:
            db_instance_id = self.rds_controller.reboot_db_instance(db_instance_id)
            print("Waiting for DB instance to reboot...")
            # wait for db instance to be available
            waiter = self.rds_controller.rds_client.get_waiter('db_instance_available')
            waiter.wait(DBInstanceIdentifier=db_instance_id)
            print(f"DB instance '{db_instance_id}' rebooted successfully.")
            return db_instance_id
        except Exception as e:
            print(f"Error rebooting DB instance: {e}")
            return None

    def list_db_snapshots(self, print_list: bool = True, deletable_only: bool = False):
        """
        List all RDS DB snapshots in the account.
        :param print_list: Whether to print the list.
        :param deletable_only: If True, only list snapshots that can be deleted (manual).
        :return: List of RDS DB snapshot identifiers.
        """
        try:
            db_snapshots = self.rds_controller.list_db_snapshots()
            if deletable_only:
                db_snapshots = [
                    snap for snap in db_snapshots
                    if snap.get('SnapshotType', 'manual') == 'manual'
                ]
            if print_list:
                db_snapshot_list = [
                    f"{db_snapshot['DBSnapshotIdentifier']}"
                    for db_snapshot in db_snapshots
                ]
                list_ordered_list(db_snapshot_list, "RDS DB Snapshots:")
            return [db_snapshot['DBSnapshotIdentifier'] for db_snapshot in db_snapshots]
        except Exception as e:
            print(f"Error listing DB snapshots: {e}")
            return []

    def create_db_snapshot(self):
        """
        Create a snapshot of an existing RDS DB instance.
        :return: The identifier of the created DB snapshot.
        """

        # get db instance id
        db_instances = self.list_db_instances()
        if not db_instances:
            print("No DB instances available to create a snapshot.")
            return None
        db_instance_id = get_user_input("Enter the DB instance identifier to create a snapshot",
                                        available_options=db_instances)
        if not db_instance_id: return None

        # find snapshot ids for the selected db instance
        existing_snapshots = self.list_db_snapshots(print_list=False)
        existing_snapshot_ids = [snap for snap in existing_snapshots if snap.startswith(db_instance_id)]
        snapshot_id = f"{db_instance_id}-snapshot-{len(existing_snapshot_ids) + 1}"

        try:
            self.rds_controller.create_db_snapshot(snapshot_id, db_instance_id)
            # wait for db snapshot to be available
            print("Waiting for DB snapshot to be available...")
            waiter = self.rds_controller.rds_client.get_waiter('db_snapshot_available')
            waiter.wait(DBSnapshotIdentifier=snapshot_id)
            print(f"DB snapshot '{snapshot_id}' created successfully.")
            return snapshot_id
        except Exception as e:
            print(f"Error creating DB snapshot: {e}")
            return None

    def delete_db_snapshot(self):
        """
        Delete an existing RDS DB snapshot.
        :return: The identifier of the deleted DB snapshot.
        """

        # get db snapshot id (only manual/deletable)
        db_snapshots = self.list_db_snapshots(deletable_only=True)
        if not db_snapshots:
            print("No deletable DB snapshots available to delete.")
            return None
        db_snapshot_id = get_user_input("Enter the DB snapshot identifier to delete", available_options=db_snapshots)
        if not db_snapshot_id: return None

        # delete db snapshot
        try:
            db_snapshot_id = self.rds_controller.delete_db_snapshot(db_snapshot_id)
            # wait for db snapshot to be deleted
            print("Waiting for DB snapshot to be deleted...")
            waiter = self.rds_controller.rds_client.get_waiter('db_snapshot_deleted')
            waiter.wait(DBSnapshotIdentifier=db_snapshot_id)
            print(f"DB snapshot '{db_snapshot_id}' deleted successfully.")
            return db_snapshot_id
        except Exception as e:
            print(f"Error deleting DB snapshot: {e}")
            return None

    def restore_db_instance_from_snapshot(self):
        """
        Restore an RDS DB instance from an existing snapshot.
        :return: The identifier of the restored DB instance.
        """

        # get db snapshot id
        db_snapshots = self.list_db_snapshots()
        if not db_snapshots:
            print("No DB snapshots available to restore from.")
            return None
        db_snapshot_id = get_user_input("Enter the DB snapshot identifier to restore from",
                                        available_options=db_snapshots)
        if not db_snapshot_id: return None

        # db instance id
        db_instance_id = get_user_input("Enter the new DB instance identifier for the restored instance")
        if not db_instance_id: return None

        try:
            restored_db_instance_id = self.rds_controller.restore_db_instance_from_snapshot(db_snapshot_id,
                                                                                            db_instance_id)
            print(f"DB instance '{restored_db_instance_id}' restored successfully from snapshot '{db_snapshot_id}'.")
            return restored_db_instance_id
        except Exception as e:
            print(f"Error restoring DB instance from snapshot: {e}")
            return None
