import os

from src.utils.config import EC2_KEY_PAIR_NAME
from src.utils.credentials_handler import get_ansible_credentials

instance_user_id = 'ubuntu'
MASTER_EC2_PUBLIC_DNS = get_ansible_credentials()['MASTER_EC2_PUBLIC_DNS']


def ssh_to_instance(target_address):
    """
    SSH into the master EC2 instance using the specified key pair and user ID.
    :return: None
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    key_path = os.path.join(base_dir, f"../\"{EC2_KEY_PAIR_NAME}.pem\"")
    ssh_command = f"ssh -i {key_path} {instance_user_id}@{target_address}"
    os.system(ssh_command)


if __name__ == "__main__":
    ssh_to_instance(MASTER_EC2_PUBLIC_DNS)
