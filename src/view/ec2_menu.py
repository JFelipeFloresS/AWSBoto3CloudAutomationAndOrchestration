from src.utils.list_utils import list_ec2_instances, EC2ListType
from src.utils.user_input_handler import get_user_input
from src.view.AbstractMenu import AbstractMenu
from src.controller.EC2Controller import EC2Controller
from src.model.Resources import Resource

class EC2Menu (AbstractMenu):
    def __init__(self):
        ec2_menu_options = \
            {1: "List instances",
             2: "Start instance",
             3: "Stop instance",
             4: "Launch new instance",
             5: "Terminate instance",
             9: "Main menu",
             99: "Exit"}

        super().__init__("EC2 Menu", ec2_menu_options)

        res = Resource()
        ec2_resource = res.ec2_resource()
        ec2_client = res.ec2_client()
        self.ec2_controller = EC2Controller(ec2_resource, ec2_client)

    def execute_choice(self, choice):
        if choice == 1:
            list_ec2_instances(self.ec2_controller, list_type=EC2ListType.SPLIT)
        elif choice == 2:
            self.start_instance()
        elif choice == 3:
            self.stop_instance()
        elif choice == 4:
            self.ec2_controller.launch_instance()
        elif choice == 5:
            self.terminate_instance()
        elif choice == 9:
            return False
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()

        return True

    def start_instance(self):
        """
        Start a stopped EC2 instance.
        :return: None
        """

        # get instance id
        instances = list_ec2_instances(self.ec2_controller, list_type=EC2ListType.STOPPED)
        # if no stopped instances, return
        if len(instances[EC2ListType.STOPPED]) == 0:
            print("No running EC2 instances found to start.")
            return
        instance_id = get_user_input("Enter the Instance ID to start", available_options=instances[EC2ListType.STOPPED])
        if not instance_id: return

        # start instance
        try:
            self.ec2_controller.start_instance(instance_id)
        except Exception as e:
            print(f"Error starting instance {instance_id}: {e}")

    def stop_instance(self):
        """
        Stop a running EC2 instance.
        :return: None
        """

        # get instance id
        instances = list_ec2_instances(self.ec2_controller, list_type=EC2ListType.RUNNING)
        # if no running instances, return
        if len(instances[EC2ListType.RUNNING]) == 0:
            print("No running EC2 instances found to stop.")
            return
        instance_id = get_user_input("Enter the Instance ID to stop", available_options=instances[EC2ListType.RUNNING])
        if not instance_id: return

        # stop instance
        try:
            self.ec2_controller.stop_instance(instance_id)
        except Exception as e:
            print(f"Error stopping instance {instance_id}: {e}")

    def terminate_instance(self):
        """
        Terminate an EC2 instance.
        :return: None
        """

        # get instance id
        instances = list_ec2_instances(self.ec2_controller, list_type=EC2ListType.ALL)
        # if no instances, return
        if len(instances) == 0:
            print("No EC2 instances found to terminate.")
            return
        instance_id = get_user_input("Enter the Instance ID to terminate", available_options=instances[EC2ListType.ALL])
        if not instance_id: return

        # terminate instance
        try:
            self.ec2_controller.terminate_instance(instance_id)
        except Exception as e:
            print(f"Error terminating instance {instance_id}: {e}")