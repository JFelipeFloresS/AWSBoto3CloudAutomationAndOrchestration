import os


def get_aws_access_credentials():
    """
    Retrieve AWS access credentials from usercred.txt file.
    :return: dict with 'aws_access_key_id' and 'aws_secret_access_key'
    """
    credentials = {}
    cred_file_path = os.path.join(os.path.dirname(__file__), '../../usercred.txt')

    try:
        with open(cred_file_path, 'r') as cred_file:
            lines = cred_file.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                credentials[key] = value

        if 'AWS_ACCESS_KEY_ID' not in credentials:
            raise Exception("AWS_ACCESS_KEY_ID not found in credentials file.")
        if 'AWS_SECRET_ACCESS_KEY' not in credentials:
            raise Exception("AWS_SECRET_ACCESS_KEY not found in credentials file.")
    except FileNotFoundError:
        raise Exception(f"Credentials file not found at {cred_file_path}")
    except Exception as e:
        raise Exception(f"Error reading credentials: {str(e)}")

    return {
        'aws_access_key_id': credentials.get('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': credentials.get('AWS_SECRET_ACCESS_KEY')
    }


def get_rds_master_credentials():
    """
    Retrieve RDS master username and password from usercred.txt file.
    :return: dict with 'RDS_MASTER_USERNAME' and 'RDS_MASTER_PASSWORD'
    """
    credentials = {}
    cred_file_path = os.path.join(os.path.dirname(__file__), '../../usercred.txt')

    try:
        with open(cred_file_path, 'r') as cred_file:
            lines = cred_file.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                credentials[key] = value

        if 'RDS_MASTER_USERNAME' not in credentials:
            raise Exception("RDS_MASTER_USERNAME not found in credentials file.")
        if 'RDS_MASTER_PASSWORD' not in credentials:
            raise Exception("RDS_MASTER_PASSWORD not found in credentials file.")
    except FileNotFoundError:
        raise Exception(f"Credentials file not found at {cred_file_path}")
    except Exception as e:
        raise Exception(f"Error reading credentials: {str(e)}")

    return {
        'RDS_MASTER_USERNAME': credentials.get('RDS_MASTER_USERNAME'),
        'RDS_MASTER_PASSWORD': credentials.get('RDS_MASTER_PASSWORD')
    }
