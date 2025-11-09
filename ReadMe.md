# AWS Management Console CLI

#### Jose Felipe Flores da Silva

#### Student number: R00293192

#### [GitHub Repository](https://github.com/JFelipeFloresS/AWSBoto3CloudAutomationAndOrchestration)

## DEPENDENCIES

This project requires the Python packages listed in [requirements.txt](requirements.txt).

To install the required packages, run one of the commands (depending on your Python installation) in your terminal:

- ```
    pip install -r requirements.txt
    ```
- ```
    pip3 install -r requirements.txt
    ```

## ENVIRONMENT VARIABLES

The file [usercred.txt](usercred.txt) contains the user credentials in the following format:

```
AWS_ACCESS_KEY_ID={your_aws_access_key_id}
AWS_SECRET_ACCESS_KEY={your_aws_secret_access_key}
EC2_RDP_PASSWORD={your_ec2_rdp_password} # this is not actually used in the code
RDS_MASTER_USERNAME={your_rds_master_username}
RDS_MASTER_PASSWORD={your_rds_master_password}
```

The utility [credentials_handler](src/utils/credentials_handler.py) provides access to these environment variables.

## RUNNING THE APPLICATION

To run the code, execute one of the following commands in your terminal (depending on your Python installation):

- ```
    python src/main.py
    ```
- ```
    python3 src/main.py
    ```

Make sure you have the required packages installed and the [usercred.txt](usercred.txt) file properly configured before
running the
code.

## USER INPUT

This is a command-line application that requires user input during execution. Follow the prompts in the terminal to
provide the necessary information.

When a list is provided, you can either type the value directly or select from the numbered options displayed.
For example, if prompted to select an option from a list:

```
Select an option:
1. Option A
2. Option B
3. Option C
```

You can either type "Option A" or just "1" to select it.

If a default value is provided in the prompt, you can simply press Enter to accept the default.
For example, if prompted:

```
Enter your name [Default: John Doe]:
```

Pressing Enter without typing anything will select "John Doe" as the input.

You can cancel any operation at any time by typing "cancel" and pressing Enter. This will abort the current process and
return you to the main menu or exit the application, depending on the context.

On any inner menu, typing "Main menu" or the corresponding number for the main menu option will take you back to the
main menu.

On any menu, typing "exit" or the corresponding number for the exit option will terminate the application.

## DEFAULT REGION

The default region for all services is `eu-west-1`. You can change the region in the code if needed by changing the
constant `DEFAULT_REGION` in [Resources](src/model/Resources.py).

## FEATURES

![img.png](assets/read_me_imgs/img.png)

The application provides the following features:

- Elastic Compute Cloud (EC2) Management
    - ![img_1.png](assets/read_me_imgs/img_1.png)
- Elastic Block Store (EBS) Management
    - ![img_10.png](assets/read_me_imgs/img_10.png)
- Simple Storage Service (S3) Management
    - ![img_29.png](assets/read_me_imgs/img_29.png)
- CloudWatch Monitoring and Alarms
    - ![img_40.png](assets/read_me_imgs/img_40.png)
- Relational Database Service (RDS) Management
    - ![img_43.png](assets/read_me_imgs/img_43.png)

### EC2 Management

The EC2 Management feature allows you to:

- List all EC2 instances
    - ![img_2.png](assets/read_me_imgs/img_2.png)
- Start an EC2 instance
    - ![img_3.png](assets/read_me_imgs/img_3.png)
    - ![img_4.png](assets/read_me_imgs/img_4.png)
- Stop an EC2 instance
    - ![img_5.png](assets/read_me_imgs/img_5.png)
- Launch a new EC2 instance
    - ![img_6.png](assets/read_me_imgs/img_6.png)
    - ![img_7.png](assets/read_me_imgs/img_7.png)
- Terminate an EC2 instance
    - ![img_8.png](assets/read_me_imgs/img_8.png)
    - ![img_9.png](assets/read_me_imgs/img_9.png)

### EBS Management

The EBS Management feature allows you to:

- List all existing EC2 volumes
    - ![img_11.png](assets/read_me_imgs/img_11.png)
- Create a new EC2 volume
    - ![img_12.png](assets/read_me_imgs/img_12.png)
    - ![img_13.png](assets/read_me_imgs/img_13.png)
- Attach existing EC2 volume to an EC2 instance
    - ![img_14.png](assets/read_me_imgs/img_14.png)
    - ![img_15.png](assets/read_me_imgs/img_15.png)
- Detach an EC2 volume from an EC2 instance
    - ![img_16.png](assets/read_me_imgs/img_16.png)
    - ![img_17.png](assets/read_me_imgs/img_17.png)
- Modify an EC2 volume's capacity
    - ![img_18.png](assets/read_me_imgs/img_18.png)
    - ![img_19.png](assets/read_me_imgs/img_19.png)
- Delete an EC2 volume
    - ![img_20.png](assets/read_me_imgs/img_20.png)
    - ![img_21.png](assets/read_me_imgs/img_21.png)
- List all EC2 volume snapshots
    - ![img_22.png](assets/read_me_imgs/img_22.png)
- Take snapshot of an EC2 volume
    - ![img_23.png](assets/read_me_imgs/img_23.png)
    - ![img_24.png](assets/read_me_imgs/img_24.png)
- Create a new EC2 volume from an EC2 volume snapshot
    - ![img_25.png](assets/read_me_imgs/img_25.png)
    - ![img_26.png](assets/read_me_imgs/img_26.png)
- Delete an EC2 volume snapshot
    - ![img_27.png](assets/read_me_imgs/img_27.png)
    - ![img_28.png](assets/read_me_imgs/img_28.png)

### S3 Management

The S3 Management feature allows you to:

- List all S3 buckets
    - ![img_30.png](assets/read_me_imgs/img_30.png)
- List all objects in a given S3 bucket
    - ![img_31.png](assets/read_me_imgs/img_31.png)
- Upload an object to an S3 bucket
    - ![img_32.png](assets/read_me_imgs/img_32.png)
    - ![img_33.png](assets/read_me_imgs/img_33.png)
- Download an object from an S3 bucket
    - ![img_34.png](assets/read_me_imgs/img_34.png)
    - ![img_35.png](assets/read_me_imgs/img_35.png)
- Delete an S3 bucket
    - ![img_38.png](assets/read_me_imgs/img_38.png)
    - ![img_39.png](assets/read_me_imgs/img_39.png)
- Create a new S3 bucket
    - ![img_36.png](assets/read_me_imgs/img_36.png)
    - ![img_37.png](assets/read_me_imgs/img_37.png)

### CloudWatch Monitoring and Alarms

The CloudWatch Monitoring and Alarms feature allows you to:

- Get DiskReadOps and CPUCreditUsage performance metrics for an EC2 instance
    - ![img_41.png](assets/read_me_imgs/img_41.png)
- Set a DiskWriteBytes Alarm for an EC2 instance so that the instance is stopped when the alarm is triggered
    - ![img_42.png](assets/read_me_imgs/img_42.png)

### RDS Management

The RDS Management feature allows you to:

- List all RDS DB instances
    - ![img_44.png](assets/read_me_imgs/img_44.png)
- Create a new RDS DB instance (takes a while to complete)
    - ![img_45.png](assets/read_me_imgs/img_45.png)
    - ![img_47.png](assets/read_me_imgs/img_47.png)
- Delete an RDS DB instance
    - ![img_48.png](assets/read_me_imgs/img_48.png)
    - ![img_49.png](assets/read_me_imgs/img_49.png)
- Reboot an RDS DB instance (takes a while to complete)
    - ![img_50.png](assets/read_me_imgs/img_50.png)
- List all snapshots of RDS DB instances
    - ![img_51.png](assets/read_me_imgs/img_51.png)
- Create a snapshot from an RDS DB instance (takes a while to complete)
    - ![img_52.png](assets/read_me_imgs/img_52.png)
    - ![img_53.png](assets/read_me_imgs/img_53.png)
- Delete a snapshot of an RDS DB instance
    - ![img_54.png](assets/read_me_imgs/img_54.png)
    - ![img_55.png](assets/read_me_imgs/img_55.png)
- Restore an RDS DB instance from a snapshot of an RDS DB instance
    - ![img_56.png](assets/read_me_imgs/img_56.png)
    - ![img_57.png](assets/read_me_imgs/img_57.png)