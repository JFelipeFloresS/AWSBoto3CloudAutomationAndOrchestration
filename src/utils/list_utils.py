from enum import Enum


class EC2ListType(Enum):
    ALL = 1
    SPLIT = 2
    RUNNING = 3
    STOPPED = 4


def list_ec2_instances(ec2_controller, list_type: EC2ListType = EC2ListType.SPLIT, skip_print: bool = False):
    """
    List EC2 instances based on the specified type.
    :param ec2_controller: EC2Controller instance.
    :param list_type: EC2ListType indicating which instances to list (ALL, SPLIT, RUNNING, STOPPED).
    :param skip_print: If True, skip printing the instances to console.
    :return: dict containing lists of EC2 instances.
    {EC2ListType.RUNNING: [...], EC2ListType.STOPPED: [...]}
    """
    try:
        region_name = ec2_controller.ec2.meta.client.meta.region_name
        instances = ec2_controller.get_ec2_instances(list_type=list_type)

        i = 1

        if list_type == EC2ListType.ALL:
            if len(instances[EC2ListType.ALL]) == 0:
                if not skip_print: print("No EC2 instances found.")
            else:
                if not skip_print: print("EC2 Instances:")
                for instance in instances[EC2ListType.ALL]:
                    if not skip_print: print(ec2_to_string(instance, region_name, i))
                    i += 1
            instances[EC2ListType.ALL] = [instance.id for instance in instances[EC2ListType.ALL]]
            return instances
        elif list_type == EC2ListType.RUNNING or list_type == EC2ListType.STOPPED:
            key = list_type
            if len(instances[key]) > 0:
                if not skip_print: print(f"{list_type.name.capitalize()} EC2 Instances:")
                for instance in instances[key]:
                    if not skip_print: print(ec2_to_string(instance, region_name, i))
                    i += 1

            instances[key] = [instance.id for instance in instances[key]]
            return instances
        elif list_type == EC2ListType.SPLIT:
            if len(instances[EC2ListType.RUNNING]) == 0:
                if not skip_print: print("No running EC2 instances found.")
            else:
                if not skip_print: print("Running EC2 Instances:")
                for instance in instances[EC2ListType.RUNNING]:
                    if not skip_print: print(ec2_to_string(instance, region_name, i))
                    i += 1

            if len(instances[EC2ListType.STOPPED]) == 0:
                if not skip_print: print("No stopped EC2 instances found.")
            else:
                if not skip_print: print("Stopped EC2 Instances:")
                for instance in instances[EC2ListType.STOPPED]:
                    if not skip_print: print(ec2_to_string(instance, region_name, i))
                    i += 1

        instances[EC2ListType.RUNNING] = [instance.id for instance in instances[EC2ListType.RUNNING]]
        instances[EC2ListType.STOPPED] = [instance.id for instance in instances[EC2ListType.STOPPED]]

        return instances
    except Exception as e:
        print(f"Error listing EC2 instances: {e}")
        return {}


def list_ordered_list(input_list, list_title):
    print(list_title)
    for i, item in enumerate(input_list, start=1):
        print(f"{i}. {item}")
    return input_list


def ec2_to_string(instance, region_name, index):
    """
    Convert an EC2 instance object to a string representation.
    :param index: Index number for display.
    :param region_name:
    :param instance: Boto3 EC2 instance object.
    :return: String representation of the EC2 instance.
    """
    return (f"{index}. Instance ID: {instance.id}, "
            f"{("Name: " + instance.tags[0]['Value']) if instance.tags and instance.tags[0]['Value'] != '' else 'Unnamed'}, "
            f"State: {instance.state['Name']}, "
            f"Instance Type: {instance.instance_type}, "
            f"Region: {region_name}, "
            f"Launch Time: {instance.launch_time}"
            f"Public IP: {instance.public_ip_address if instance.public_ip_address else 'N/A'}")
