from datetime import timedelta, datetime, timezone

from src.controller.CloudWatchController import CloudWatchController
from src.controller.EC2Controller import EC2Controller
from src.model.Resources import Resource
from src.utils.list_utils import list_ec2_instances, EC2ListType, list_ordered_list
from src.utils.user_input_handler import get_user_input, InputType
from src.view.AbstractMenu import AbstractMenu

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATETIME_COMPACT_FORMAT = '%Y%m%d%H%M%S'


class CloudWatchMenu(AbstractMenu):
    def __init__(self):
        cw_menu_options = \
            {1: "Get Metric Statistics",
             2: "Set DiskWriteBytes Alarm",
             9: "Main Menu",
             99: "Exit"}
        super().__init__("CloudWatch Menu", cw_menu_options)

        res = Resource()
        cw_client = res.cw_client()
        self.cw_controller = CloudWatchController(cw_client)

        ec2 = res.ec2_resource()
        ec2_client = res.ec2_client()
        self.ec2_controller = EC2Controller(ec2, ec2_client)

    def execute_choice(self, choice):
        if choice == 1:
            self.get_metrics_statistics()
        elif choice == 2:
            self.set_disk_write_bytes_alarm()
        elif choice == 9:
            return False
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()

        return True

    def get_metrics_statistics(self):
        """
        Retrieve and display statistics for a specific CloudWatch metric.
        :return: None
        """
        ec2_instances = list_ec2_instances(self.ec2_controller, list_type=EC2ListType.ALL)
        if not ec2_instances:
            print("No EC2 instances available to retrieve metrics.")
            return
        instance = get_user_input("Select an EC2 instance by ID to retrieve metrics for",
                                  available_options=ec2_instances[EC2ListType.ALL])
        if not instance: return

        namespace = "AWS/EC2"
        metric_names = ["DiskReadOps", "CPUCreditUsage"]
        dimensions = [{
            "Name": "InstanceId",
            "Value": instance
        }]

        time_range_minutes = get_user_input("Enter the time range in minutes to retrieve metrics for", default_value=30,
                                            input_type=InputType.INT)
        if not time_range_minutes: return

        # get current time
        from datetime import datetime, timezone
        utc = datetime.now(timezone.utc)

        # start_utc is time_range_minutes before current time
        start_time = utc - timedelta(minutes=time_range_minutes)
        end_time = utc
        period = 60 * time_range_minutes
        statistics = ["Average"]

        print(
            f"Querying metrics from {start_time.strftime(DATETIME_FORMAT)} to {end_time.strftime(DATETIME_FORMAT)} (UTC), period: {time_range_minutes} minutes.")

        for metric_name in metric_names:
            for stat in statistics:
                try:
                    datapoints = self.cw_controller.get_metrics_statistics(namespace, metric_name, dimensions,
                                                                           start_time,
                                                                           end_time, period, [stat])

                    if not datapoints:
                        print(
                            f"\n{metric_name}: No data points found for {stat} {metric_name} within the last {time_range_minutes} minutes for instance {instance}.")
                        continue

                    print(f"\n{metric_name}: Metric Statistics for {metric_name} ({stat}) for instance {instance}:")
                    for dp in sorted(datapoints, key=lambda x: x['Timestamp']):
                        timestamp = dp['Timestamp']
                        value = dp.get(stat)
                        print(f"Timestamp: {timestamp}, {stat}: {value}")
                except Exception as e:
                    print(f"\n{metric_name}: Error retrieving data for metric {metric_name} ({stat}): {e}")

    def set_disk_write_bytes_alarm(self):
        """
        Set a CloudWatch alarm for DiskWriteBytes metric on a selected EC2 instance.
        If DiskwriteBytes is greater than or equal to 9000 for 5 minutes the alarm will trigger.
        Once the alarm is triggered, the instance that triggered the alarm will be stopped.
        :return: None
        """

        # find ec2 instances already having the alarm set
        existing_alarms = self.cw_controller.cw_client.describe_alarms()
        alarmed_instances = set()
        for alarm in existing_alarms.get('MetricAlarms', []):
            for dimension in alarm.get('Dimensions', []):
                if dimension['Name'] == 'InstanceId':
                    alarmed_instances.add(dimension['Value'])

        print("EC2 Instances with existing DiskWriteBytes alarms:", alarmed_instances)

        ec2_instances = list_ec2_instances(self.ec2_controller, list_type=EC2ListType.ALL, skip_print=True)
        ec2_instances[EC2ListType.ALL] = list_ordered_list(
            [inst for inst in ec2_instances[EC2ListType.ALL] if inst not in alarmed_instances],
            "Available EC2 Instances for Alarm Setup:")
        if not ec2_instances[EC2ListType.ALL]:
            print("No EC2 instances available to set alarms.")
            return

        instance = get_user_input("Select an EC2 instance to set DiskWriteBytes alarm on",
                                  available_options=ec2_instances[EC2ListType.ALL])
        if not instance: return

        alarm_name = f"DiskWriteBytes_Alarm_CreatedOn_{datetime.now(timezone.utc).strftime(DATETIME_COMPACT_FORMAT)}"
        comparison_operator = "GreaterThanOrEqualToThreshold"
        metric_name = "DiskWriteBytes"
        statistic = "Average"
        threshold = 9000.0
        evaluation_periods = 1
        period = 300  # 5 minutes

        # add all existing instances as dimensions
        dimensions = [{
            "Name": "InstanceId",
            "Value": instance
        }]

        # Define the action to stop the instance when the alarm is triggered
        alarm_actions = [f"arn:aws:automate:{self.ec2_controller.ec2.meta.client.meta.region_name}:ec2:stop"]

        try:
            self.cw_controller.set_alarm(
                alarm_name,
                comparison_operator,
                metric_name,
                statistic,
                threshold,
                evaluation_periods,
                period,
                actions_enabled=True,
                alarm_actions=alarm_actions,
                dimensions=dimensions
            )
        except Exception as e:
            print(f"Error setting alarm '{alarm_name}': {e}")
