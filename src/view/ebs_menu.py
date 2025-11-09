from src.controller.EBSController import EBSController
from src.controller.EC2Controller import EC2Controller, EC2ListType
from src.model.Resources import Resource, DEFAULT_REGION
from src.utils.list_utils import list_ec2_instances, list_ordered_list
from src.utils.user_input_handler import get_user_input, InputType
from src.view.AbstractMenu import AbstractMenu


class EBSMenu(AbstractMenu):
    def __init__(self):
        ebs_menu_options = \
            {1: "List all existing volumes",
             2: "Create new volume",
             3: "Attach existing volume to EC2 instance",
             4: "Detach volume from instance",
             5: "Modify volume capacity",
             6: "Delete volume",
             7: "List snapshots",
             8: "Take snapshot of volume",
             9: "Create volume from snapshot",
             10: "Delete snapshot",
             11: "Main menu",
             99: "Exit"}
        super().__init__("EBS Menu", ebs_menu_options)

        self.volume_types = ['standard', 'io1', 'io2', 'gp2', 'sc1', 'st1', 'gp3']

        res = Resource()
        ec2 = res.ec2_resource()
        ec2_client = res.ec2_client()
        self.ebs_controller = EBSController(ec2, ec2_client)
        self.ec2_controller = EC2Controller(ec2, ec2_client)

    def execute_choice(self, choice):
        if choice == 1:
            self.list_volumes()
        elif choice == 2:
            self.create_volume()
        elif choice == 3:
            self.attach_volume_to_instance()
        elif choice == 4:
            self.detach_volume_from_instance()
        elif choice == 5:
            self.modify_volume_capacity()
        elif choice == 6:
            self.delete_volume()
        elif choice == 7:
            self.list_snapshots()
        elif choice == 8:
            self.take_snapshot_of_volume()
        elif choice == 9:
            self.create_volume_from_snapshot()
        elif choice == 10:
            self.delete_snapshot()
        elif choice == 11:
            return False
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()

        return True

    def list_volumes(self):
        """
        List all EBS volumes in the specified region.
        :return: List of all EBS volume IDs.
        """
        try:
            volumes = self.ebs_controller.list_existing_volumes()
            volume_ids = [v.id for v in volumes]
            return volume_ids
        except Exception as e:
            print(f"Error listing volumes: {e}")
            return []

    def create_volume(self):
        """
        Create a new EBS volume.
        :return: The created EBS volume Resource object.
        """

        # get availability zone
        availability_zone = get_user_input("Enter Availability Zone", default_value=DEFAULT_REGION + 'a')
        if not availability_zone: return

        # get volume size
        size = get_user_input("Enter Volume Size in GiB", InputType.INT, default_value=8)
        if not size: return

        # get volume type
        volume_types = list_ordered_list(self.volume_types, "Available EBS Volume Types:")
        volume_type = get_user_input(f"Enter Volume Type", default_value='gp2', available_options=volume_types)
        if not volume_type: return

        # create volume
        try:
            self.ebs_controller.create_volume(availability_zone, size, volume_type)
        except Exception as e:
            print(f"Error creating volume: {e}")

    def attach_volume_to_instance(self):
        """
        Attach an existing EBS volume to an EC2 instance.
        :return: None
        """

        # get volume id
        volumes = self.list_volumes()
        volume_id = get_user_input("Enter Volume ID to attach", available_options=volumes)
        if not volume_id: return

        # get instance id
        instances = list_ec2_instances(self.ec2_controller, list_type=EC2ListType.ALL)
        instance_id = get_user_input("Enter Instance ID to attach the volume to",
                                     available_options=instances[EC2ListType.ALL])
        if not instance_id: return

        # get device name
        device = get_user_input("Enter Device Name", default_value='/dev/sdf')
        if not device: return

        # attach volume
        try:
            self.ebs_controller.attach_volume_to_instance(volume_id, instance_id, device)
        except Exception as e:
            print(f"Error attaching volume: {e}")

    def detach_volume_from_instance(self):
        """
        Detach an EBS volume from an EC2 instance.
        :return: None
        """

        # get volume id
        volumes = self.list_volumes()
        volume_id = get_user_input("Enter Volume ID to detach", available_options=volumes)
        if not volume_id: return

        # get instance id
        instances = list_ec2_instances(self.ec2_controller, list_type=EC2ListType.ALL)
        instance_id = get_user_input("Enter Instance ID to detach the volume from",
                                     available_options=instances[EC2ListType.ALL])
        if not instance_id: return

        # detach volume
        try:
            self.ebs_controller.detach_volume_from_instance(volume_id, instance_id)
        except Exception as e:
            print(f"Error detaching volume: {e}")

    def modify_volume_capacity(self):
        """
        Modify the capacity of an existing EBS volume.
        :return: None
        """

        # get volume id
        volumes = self.list_volumes()
        volume_id = get_user_input("Enter Volume ID to modify", available_options=volumes)
        if not volume_id: return

        # get new size
        new_size = get_user_input("Enter new Volume Size in GiB", InputType.INT)
        if not new_size: return

        # modify volume capacity
        try:
            self.ebs_controller.modify_volume_capacity(volume_id, new_size)
        except Exception as e:
            print(f"Error modifying volume capacity: {e}")

    def delete_volume(self):
        """
        Delete an EBS volume.
        :return: None
        """

        # get volume id
        volumes = self.list_volumes()
        volume_id = get_user_input("Enter Volume ID to delete", available_options=volumes)
        if not volume_id: return

        # delete volume
        try:
            self.ebs_controller.delete_volume(volume_id)
        except Exception as e:
            print(f"Error deleting volume: {e}")

    def list_snapshots(self):
        """
        List all EBS snapshots in the specified region.
        :return: List of all EBS snapshot IDs.
        """
        try:
            snapshots = self.ebs_controller.list_snapshots()
            snapshot_ids = [s.id for s in snapshots]
            return snapshot_ids
        except Exception as e:
            print(f"Error listing snapshots: {e}")
            return []

    def take_snapshot_of_volume(self):
        """
        Take a snapshot of an existing EBS volume.
        :return: The created EBS snapshot Resource object.
        """

        # get volume id
        volumes = self.list_volumes()
        volume_id = get_user_input("Enter Volume ID to take snapshot of", available_options=volumes)
        if not volume_id: return

        # get description
        description = get_user_input("Enter Snapshot Description", default_value='Snapshot created by EBSMenu')
        if not description: return

        # take snapshot
        try:
            self.ebs_controller.take_snapshot_of_volume(volume_id, description)
        except Exception as e:
            print(f"Error taking snapshot of volume: {e}")

    def create_volume_from_snapshot(self):
        """
        Create a new EBS volume from an existing snapshot.
        :return:
        """

        # get snapshot id
        snapshots = self.list_snapshots()
        snapshot_id = get_user_input("Enter Snapshot ID", available_options=snapshots)
        if not snapshot_id: return

        # get availability zone
        availability_zone = get_user_input("Enter Availability Zone", default_value=DEFAULT_REGION + 'a')
        if not availability_zone: return

        # get volume type
        volume_types = list_ordered_list(self.volume_types, "Available EBS Volume Types:")
        volume_type = get_user_input(f"Enter Volume Type", default_value='gp2', available_options=volume_types)
        if not volume_type: return

        # create volume from snapshot
        try:
            self.ebs_controller.create_volume_from_snapshot(snapshot_id, availability_zone, volume_type)
        except Exception as e:
            print(f"Error creating volume from snapshot: {e}")

    def delete_snapshot(self):
        """
        Delete an EBS snapshot.
        :return: None
        """

        # get snapshot id
        snapshots = self.list_snapshots()
        snapshot_id = get_user_input("Enter Snapshot ID to delete", available_options=snapshots)
        if not snapshot_id: return

        # delete snapshot
        try:
            self.ebs_controller.delete_snapshot(snapshot_id)
        except Exception as e:
            print(f"Error deleting snapshot: {e}")
