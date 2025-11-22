from src.utils.config import EC2_KEY_PAIR_NAME, DEFAULT_EC2_INSTANCE_TYPE
from src.utils.list_utils import EC2ListType


class EC2Controller:
    def __init__(self, ec2, ec2_client):
        """
        Initialise the EC2Controller with a boto3 EC2 resource.
        :param ec2: Boto3 EC2 resource object.
        :param ec2_client: Boto3 EC2 client object.
        :return: None
        """
        self.ec2 = ec2
        self.ec2_client = ec2_client
        self.list_options = {
            1: "All Instances",
            2: "Running Instances",
            3: "Stopped Instances"
        }

    def get_ec2_instances(self, list_type: EC2ListType = EC2ListType.SPLIT):
        """
        List all EC2 instances in the specified region.
        :param list_type: EC2ListType indicating which instances to list (ALL, SPLIT, RUNNING, STOPPED).
        :return: List of all EC2 instances Resource objects.
        """

        if list_type == EC2ListType.ALL:
            return {EC2ListType.ALL: list(self.ec2.instances.all())}

        running_instances = []
        other_instances = []
        for instance in self.ec2.instances.all():
            if instance.state['Name'] == 'running':
                running_instances.append(instance)
            else:
                other_instances.append(instance)

        return {
            EC2ListType.RUNNING: running_instances,
            EC2ListType.STOPPED: other_instances
        }

    def stop_instance(self, instance_id):
        """
        Stop an EC2 instance by its ID.
        :param instance_id: The ID of the EC2 instance to stop.
        :return: Response from the stop_instances call.
        """
        instance = self.ec2.Instance(instance_id)
        response = instance.stop()
        return response

    def start_instance(self, instance_id):
        """
        Start an EC2 instance by its ID.
        :param instance_id: The ID of the EC2 instance to start.
        :return: Response from the start_instances call.
        """
        instance = self.ec2.Instance(instance_id)
        response = instance.start()
        print(f"Waiting for instance {instance_id} to enter 'running' state...")
        self.wait_for_instance_running(instance_id)
        return response

    def launch_instance(self, ami_id):
        instances = self.ec2.create_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=DEFAULT_EC2_INSTANCE_TYPE,
            KeyName=EC2_KEY_PAIR_NAME
        )
        instance = instances[0]
        return instance

    def terminate_instance(self, instance_id):
        """
        Terminate an EC2 instance by its ID.
        :param instance_id: The ID of the EC2 instance to terminate.
        :return: Response from the terminate_instances call.
        """
        instance = self.ec2.Instance(instance_id)
        response = instance.terminate()
        return response

    def wait_for_instance_running(self, instance_id):
        """
        Wait for an EC2 instance to reach the 'running' state.
        :param instance_id: The ID of the EC2 instance to wait for.
        :return: None
        """
        waiter = self.ec2_client.get_waiter('instance_running')
        waiter.wait(
            InstanceIds=[instance_id]
        )
