# Configuration constants for AWS resources

## Regions and Availability Zones
DEFAULT_REGION = 'eu-west-1'
DEFAULT_AVAILABILITY_ZONE = 'eu-west-1a'

## EC2 Key Pair
EC2_KEY_PAIR_NAME = 'Cloud Automation and Orchestration'

## EC2 AMI IDs and Instance Types
WINDOWS_AMI_ID = 'ami-0c0dd5ec2d91c4221'
UBUNTU_AMI_ID = 'ami-049442a6cf8319180'
DEFAULT_EC2_INSTANCE_TYPE = 't3.micro'

## EBS Volume and Snapshot Defaults
DEFAULT_VOLUME_TYPE = 'gp2'
DEFAULT_VOLUME_SIZE_GIB = 8

## Device Names and Snapshot Defaults
DEFAULT_DEVICE_NAME = '/dev/sdf'
DEFAULT_SNAPSHOT_NAME = 'Created from EBSController'

## CloudWatch Defaults
DEFAULT_NAMESPACE = 'AWS/EC2'

## RDS Defaults
DEFAULT_RDS_DB_INSTANCE_CLASS = 'db.t4g.micro'
DEFAULT_DB_STORAGE_GIB = 20

## DateTime Formats
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATETIME_COMPACT_FORMAT = '%Y%m%d%H%M%S'

## Security Group Defaults
DEFAULT_SECURITY_GROUP_NAME = 'default'
