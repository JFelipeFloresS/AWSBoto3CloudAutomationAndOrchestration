import os


def get_aws_access_credentials():
    """
    Retrieve AWS access credentials from usercred.txt file.
    :return: dict with 'AWS_ACCESS_KEY_ID' and 'AWS_SECRET_ACCESS_KEY'
    """
    return get_req_credentials(['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'])


def get_rds_master_credentials():
    """
    Retrieve RDS master username and password from usercred.txt file.
    :return: dict with 'RDS_MASTER_USERNAME' and 'RDS_MASTER_PASSWORD'
    """
    return get_req_credentials(['RDS_MASTER_USERNAME', 'RDS_MASTER_PASSWORD'])


def get_ansible_credentials():
    """
    Retrieve Ansible-related credentials from usercred.txt file.
    :return: dict with 'MASTER_EC2_PUBLIC_DNS'
    """
    return get_req_credentials(['MASTER_EC2_PUBLIC_DNS'])


def get_req_credentials(credentials_list):
    """
    Retrieve specified credentials from usercred.txt file.
    :param credentials_list: List of credential keys to retrieve.
    :return: dict with requested credentials.
    """
    credentials = {}
    cred_file_path = os.path.join(os.path.dirname(__file__), '../../usercred.txt')

    try:
        with open(cred_file_path, 'r') as cred_file:
            lines = cred_file.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                if key in credentials_list:
                    credentials[key] = value

        for cred in credentials_list:
            if cred not in credentials:
                raise Exception(f"{cred} not found in credentials file.")
    except FileNotFoundError:
        raise Exception(f"Credentials file not found at {cred_file_path}")
    except Exception as e:
        raise Exception(f"Error reading credentials: {str(e)}")

    return credentials
