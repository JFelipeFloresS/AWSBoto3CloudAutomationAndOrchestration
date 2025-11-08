from src.utils.list_utils import EC2ListType, list_ordered_list
from src.utils.user_input_handler import get_user_input

EC2_KEY_PAIR_NAME = 'Cloud Automation and Orchestration'
WINDOWS_AMI_ID = 'ami-0c0dd5ec2d91c4221'
UBUNTU_AMI_ID = 'ami-049442a6cf8319180'

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
        self.OS_options = ["Windows", "Linux"]

    def get_ec2_instances(self, list_type: EC2ListType=EC2ListType.SPLIT):
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
        print("Stopping instance:", instance_id)
        instance = self.ec2.Instance(instance_id)
        response = instance.stop()
        print('Stop instance request response status:', response['ResponseMetadata']['HTTPStatusCode'])
        return response

    def start_instance(self, instance_id):
        """
        Start an EC2 instance by its ID.
        :param instance_id: The ID of the EC2 instance to start.
        :return: Response from the start_instances call.
        """
        print("Starting instance:", instance_id)
        instance = self.ec2.Instance(instance_id)
        response = instance.start()
        self.wait_for_instance_running(instance_id)
        print('Instance started successfully.')
        return response

    def launch_instance(self):
        """
        Launch a new EC2 instance with predefined parameters.
        :return: The launched EC2 instance object.
        """
        # request user input so user can enter windows or linux

        os_options = list_ordered_list(self.OS_options, "Available OS options:")
        user_input = get_user_input("Enter the OS for the new EC2 instance windows or linux", available_options=os_options).lower()
        if not user_input: return None
        ami_id = None
        if user_input == 'windows':
            ami_id = WINDOWS_AMI_ID
        elif user_input == 'linux':
            ami_id = UBUNTU_AMI_ID

        print("Launching a new EC2 instance...")
        try:
            instances = self.ec2.create_instances(
                ImageId=ami_id,
                MinCount=1,
                MaxCount=1,
                InstanceType='t3.micro',
                KeyName=EC2_KEY_PAIR_NAME
            )
            instance = instances[0]
            print(f'Launched EC2 Instance ID: {instance.id}')
            return instance
        except Exception as e:
            print(f"Error launching {user_input} instance: {e}")
            return None

    def terminate_instance(self, instance_id):
        """
        Terminate an EC2 instance by its ID.
        :param instance_id: The ID of the EC2 instance to terminate.
        :return: Response from the terminate_instances call.
        """
        instance = self.ec2.Instance(instance_id)
        response = instance.terminate()
        print('Terminate instance request response status:', response['ResponseMetadata']['HTTPStatusCode'])
        return response

    def wait_for_instance_running(self, instance_id):
        """
        Wait for an EC2 instance to reach the 'running' state.
        :param instance_id: The ID of the EC2 instance to wait for.
        :return: None
        """
        print(f"Waiting for instance {instance_id} to enter 'running' state...")
        waiter = self.ec2_client.get_waiter('instance_running')
        waiter.wait(
            InstanceIds=[instance_id]
        )
        print(f"Instance {instance_id} is now running.")
