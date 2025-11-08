from src.utils.credentials_handler import get_rds_master_credentials


class RDSController:
    def __init__(self, rds_client):
        self.rds_client = rds_client
        self.credentials = get_rds_master_credentials()

    def list_db_instances(self):
        """
        List all RDS DB instances in the account.
        :return: List of RDS DB instance identifiers.
        """
        response = self.rds_client.describe_db_instances()
        return response['DBInstances']

    def create_db_instance(self, db_name, db_id, engine, availability_zone):
        """
        Create a new RDS DB instance.
        :param db_name: Name of the database.
        :param db_id: Identifier for the DB instance.
        :param engine: The database engine to use.
        :param availability_zone: The availability zone where the DB instance will be created.
        :return: The identifier of the created DB instance.
        """
        response = self.rds_client.create_db_instance(
            DBName=db_name,
            DBInstanceIdentifier=db_id,
            AllocatedStorage=20,
            DBInstanceClass="db.t4g.micro",
            Engine=engine,
            AvailabilityZone=availability_zone,
            MasterUsername=self.credentials["RDS_MASTER_USERNAME"],
            MasterUserPassword=self.credentials["RDS_MASTER_PASSWORD"],
            MultiAZ=False,
            PubliclyAccessible=True
        )
        return response['DBInstance']['DBInstanceIdentifier']

    def delete_db_instance(self, db_id):
        """
        Delete an RDS DB instance.
        :param db_id: Identifier of the DB instance to delete.
        :return: The identifier of the deleted DB instance.
        """
        response = self.rds_client.delete_db_instance(
            DBInstanceIdentifier=db_id,
            SkipFinalSnapshot=True
        )
        return response['DBInstance']['DBInstanceIdentifier']

    def reboot_db_instance(self, db_id):
        """
        Reboot an RDS DB instance.
        :param db_id: Identifier of the DB instance to reboot.
        :return: The identifier of the rebooted DB instance.
        """
        response = self.rds_client.reboot_db_instance(
            DBInstanceIdentifier=db_id
        )
        return response['DBInstance']['DBInstanceIdentifier']

    def list_db_snapshots(self):
        """
        List all RDS DB snapshots in the account.
        :return: List of RDS DB snapshot identifiers.
        """
        response = self.rds_client.describe_db_snapshots()
        return response['DBSnapshots']

    def create_db_snapshot(self, db_snapshot_id, db_instance_id):
        """
        Create a snapshot of an RDS DB instance.
        :param db_snapshot_id: Identifier for the DB snapshot.
        :param db_instance_id: Identifier of the DB instance to snapshot.
        :return: The identifier of the created DB snapshot.
        """
        response = self.rds_client.create_db_snapshot(
            DBSnapshotIdentifier=db_snapshot_id,
            DBInstanceIdentifier=db_instance_id
        )
        return response['DBSnapshot']['DBSnapshotIdentifier']

    def delete_db_snapshot(self, db_snapshot_id):
        """
        Delete an RDS DB snapshot.
        :param db_snapshot_id: Identifier of the DB snapshot to delete.
        :return: The identifier of the deleted DB snapshot.
        """
        response = self.rds_client.delete_db_snapshot(
            DBSnapshotIdentifier=db_snapshot_id
        )
        return response['DBSnapshot']['DBSnapshotIdentifier']

    def restore_db_instance_from_snapshot(self, db_snapshot_id, db_instance_id):
        """
        Restore an RDS DB instance from a snapshot.
        :param db_snapshot_id: Identifier of the DB snapshot to restore from.
        :param db_instance_id: Identifier for the new DB instance.
        :return: The identifier of the restored DB instance.
        """
        response = self.rds_client.restore_db_instance_from_db_snapshot(
            DBInstanceIdentifier=db_instance_id,
            DBSnapshotIdentifier=db_snapshot_id,
            MultiAZ=False,
            PubliclyAccessible=True
        )
        return response['DBInstance']['DBInstanceIdentifier']
