import boto3

from src.utils.config import DEFAULT_REGION
from src.utils.credentials_handler import get_aws_access_credentials

aws_access_credentials = get_aws_access_credentials()


class Resource:
    def __init__(self, region=None):
        # use default region if
        if region is None:
            self.region = DEFAULT_REGION
        else:
            self.region = region
        self.access_key_id = aws_access_credentials['AWS_ACCESS_KEY_ID']
        self.secret_access_key = aws_access_credentials['AWS_SECRET_ACCESS_KEY']

    def ec2_resource(self):
        return boto3.resource('ec2',
                              aws_access_key_id=self.access_key_id,
                              aws_secret_access_key=self.secret_access_key,
                              region_name=self.region)

    def ec2_client(self):
        return boto3.client('ec2',
                            aws_access_key_id=self.access_key_id,
                            aws_secret_access_key=self.secret_access_key,
                            region_name=self.region)

    def s3_resource(self):
        return boto3.resource('s3',
                              aws_access_key_id=self.access_key_id,
                              aws_secret_access_key=self.secret_access_key,
                              region_name=self.region)

    def cw_client(self):
        return boto3.client('cloudwatch',
                            aws_access_key_id=self.access_key_id,
                            aws_secret_access_key=self.secret_access_key,
                            region_name=self.region)

    def rds_client(self):
        return boto3.client('rds',
                            aws_access_key_id=self.access_key_id,
                            aws_secret_access_key=self.secret_access_key,
                            region_name=self.region)
