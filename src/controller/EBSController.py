from src.model.Resources import DEFAULT_REGION


class EBSController:
    def __init__(self, ec2, ec2_client):
        """
        Initialise the EBSController with a boto3 EBS service client.
        :param ec2: Boto3 EC2 resource object.
        """
        self.ec2 = ec2
        self.ec2_client = ec2_client

    def list_existing_volumes(self):
        """
        List all existing EBS volumes in the specified region.
        :return: List of all EBS volumes Resource objects.
        """
        volumes = self.ec2.volumes.all()
        volume_list = []
        for volume in volumes:
            volume_list.append(volume)
        return volume_list

    def create_volume(self, size, availability_zone: str = DEFAULT_REGION, volume_type: str = 'gp2'):
        """
        Create a new EBS volume.
        :param size: Size of the volume in GiB.
        :param availability_zone: The Availability Zone in which to create the volume.
        :param volume_type: The type of the volume (default is 'gp2').
        :return: The created volume's information.
        """
        response = self.ec2.create_volume(
            Size=size,
            AvailabilityZone=availability_zone,
            VolumeType=volume_type
        )
        return response

    def attach_volume_to_instance(self, volume_id, instance_id, device: str = '/dev/sdf'):
        """
        Attach an EBS volume to an EC2 instance.
        :param volume_id: The ID of the EBS volume to attach.
        :param instance_id: The ID of the EC2 instance to attach the volume to.
        :param device: The device name to expose to the instance (e.g., '/dev/sdf').
        :return: Response from the attach_volume call.
        """
        response = self.ec2.Instance(instance_id).attach_volume(
            VolumeId=volume_id,
            Device=device
        )
        return response

    def detach_volume_from_instance(self, volume_id, instance_id):
        """
        Detach an EBS volume from an EC2 instance.
        :param volume_id: The ID of the EBS volume to detach.
        :param instance_id: The ID of the EC2 instance to detach the volume from.
        :return: Response from the detach_volume call.
        """
        response = self.ec2.Instance(instance_id).detach_volume(
            VolumeId=volume_id
        )
        return response

    def modify_volume_capacity(self, volume_id, new_size: int):
        """
        Modify the size of an existing EBS volume.
        :param volume_id: The ID of the EBS volume to modify.
        :param new_size: The new size of the volume in GiB.
        :return: Response from the modify_volume call.
        """
        response = self.ec2_client.modify_volume(
            VolumeId=volume_id,
            Size=new_size
        )
        return response

    def delete_volume(self, volume_id):
        """
        Delete an EBS volume.
        :param volume_id: The ID of the EBS volume to delete.
        :return: Response from the delete_volume call.
        """
        response = self.ec2.Volume(volume_id).delete()
        return response

    def list_snapshots(self):
        """
        List all EBS snapshots in the specified region.
        :return: List of all EBS snapshots Resource objects.
        """
        snapshots = self.ec2.snapshots.filter(OwnerIds=['self'])
        snapshot_list = []
        for snapshot in snapshots:
            snapshot_list.append(snapshot)
        return snapshot_list

    def take_snapshot_of_volume(self, volume_id, description: str = 'Created from EBSController'):
        """
        Take a snapshot of an EBS volume.
        :param volume_id: The ID of the EBS volume to snapshot.
        :param description: Description for the snapshot.
        :return: The created snapshot's information.
        """
        response = self.ec2.Volume(volume_id).create_snapshot(Description=description)
        return response

    def create_volume_from_snapshot(self, snapshot_id, availability_zone, volume_type: str = 'gp2'):
        """
        Create a new EBS volume from an existing snapshot.
        :param snapshot_id: The ID of the snapshot to create the volume from.
        :param availability_zone: The Availability Zone in which to create the volume.
        :param volume_type: The type of the volume (default is 'gp2').
        :return: The created volume's information.
        """
        response = self.ec2.create_volume(
            SnapshotId=snapshot_id,
            AvailabilityZone=availability_zone,
            VolumeType=volume_type
        )
        return response

    def delete_snapshot(self, snapshot_id):
        """
        Delete an EBS snapshot.
        :param snapshot_id: The ID of the EBS snapshot to delete.
        :return: Response from the delete_snapshot call.
        """
        response = self.ec2.Snapshot(snapshot_id).delete()
        return response

    def create_snapshot(self, volume_id, description: str = 'Created from EBSController'):
        """
        Take a snapshot of an EBS volume.
        :param volume_id: The ID of the EBS volume to snapshot.
        :param description: Description for the snapshot.
        :return: The created snapshot's information.
        """
        response = self.ec2.create_snapshot(
            VolumeId=volume_id,
            Description=description
        )
        return response
