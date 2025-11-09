from src.controller.S3Controller import S3Controller
from src.model.Resources import Resource
from src.utils.list_utils import list_ordered_list
from src.utils.user_input_handler import get_user_input
from src.view.AbstractMenu import AbstractMenu


class S3Menu(AbstractMenu):
    def __init__(self):
        s3_menu_options = \
            {1: "List buckets",
             2: "List objects in bucket",
             3: "Upload object",
             4: "Download object",
             5: "Delete bucket",
             6: "Create bucket",
             9: "Main menu",
             99: "Exit"}
        super().__init__("S3 Menu", s3_menu_options)

        res = Resource()
        s3 = res.s3_resource()
        self.s3_controller = S3Controller(s3)

    def execute_choice(self, choice):
        if choice == 1:
            self.list_buckets()
        elif choice == 2:
            self.list_objects_in_bucket()
        elif choice == 3:
            self.upload_object()
        elif choice == 4:
            self.download_object()
        elif choice == 5:
            self.delete_bucket()
        elif choice == 6:
            self.create_bucket()
        elif choice == 9:
            return False
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()

        return True

    def list_buckets(self):
        """
        List all S3 buckets in the account.
        :return: List of S3 bucket names.
        """
        try:
            buckets = self.s3_controller.list_buckets()
            if not buckets:
                print("No S3 buckets found.")
            else:
                list_ordered_list(buckets, "S3 Buckets:")
            return buckets
        except Exception as e:
            print(f"Error listing buckets: {e}")
            return []

    def list_objects_in_bucket(self, bucket_name=None):
        """
        List all objects in a specified S3 bucket.
        :param bucket_name: The name of the S3 bucket.
        :return: List of object keys in the bucket.
        """
        try:
            # if bucket_name is not provided, prompt the user to select one
            if not bucket_name:
                buckets = self.list_buckets()

                # if no buckets are available, return as we can't list objects
                if not buckets or len(buckets) == 0:
                    print("No buckets available to list objects from.")
                    return []
                bucket_name = get_user_input("Enter the bucket name", available_options=buckets)
                if not bucket_name: return []

            # get objects in the specified bucket
            objects = self.s3_controller.list_objects(bucket_name)
            if not objects:
                print(f"No objects found in bucket '{bucket_name}'.")
            else:
                list_ordered_list(objects, f"Objects in bucket '{bucket_name}':")
            return objects
        except Exception as e:
            print(f"Error listing objects in bucket: {e}")
            return []

    def upload_object(self):
        """
        Upload an object to a specified S3 bucket.
        :return: None
        """

        # get bucket name
        buckets = self.list_buckets()
        if not buckets or len(buckets) == 0:
            print("No buckets available to upload objects to.")
            return
        bucket_name = get_user_input("Enter the bucket name", available_options=buckets)
        if not bucket_name: return

        # get object name to be uploaded as
        object_key = get_user_input("Enter the object key (name)")
        if not object_key: return

        # get local file path to upload
        file_path = get_user_input("Enter the local file path to upload")
        if not file_path: return

        # upload object
        try:
            print(f"Uploading {file_path} to {bucket_name}/{object_key}...")
            self.s3_controller.upload_object(bucket_name, object_key, file_path)
            print(f"Uploaded {file_path} to {bucket_name}/{object_key}")
        except Exception as e:
            print(f"Error uploading object: {e}")

    def download_object(self):
        """
        Download an object from a specified S3 bucket.
        :return: None
        """

        # get bucket name
        buckets = self.list_buckets()
        if not buckets or len(buckets) == 0:
            print("No buckets available to download objects from.")
            return
        bucket_name = get_user_input("Enter the bucket name", available_options=buckets)
        if not bucket_name: return

        # get object name to download
        objects = self.list_objects_in_bucket(bucket_name)
        if not objects or len(objects) == 0:
            print("No objects available to download.")
            return
        object_key = get_user_input("Enter the object key (name)", available_options=objects)
        if not object_key: return

        # get local file path to save the downloaded object
        download_path = get_user_input(
            "Enter the local file path to save the downloaded object (specify only the directory, e.g., /home/user/downloads)")
        if not download_path: return

        # get file extension
        file_extension = get_user_input("Enter the file extension for the downloaded file (e.g., txt, jpg)",
                                        default_value="")
        if not file_extension: return

        # download object
        try:
            print(f"Downloading {bucket_name}/{object_key} to {download_path} as .{file_extension}")
            self.s3_controller.download_object(bucket_name, object_key, download_path, file_extension)
            print(f"Downloaded {bucket_name}/{object_key} to {download_path} as .{file_extension}")
        except Exception as e:
            print(f"Error downloading object: {e}")

    def delete_bucket(self):
        """
        Delete a specified S3 bucket.
        :return: None
        """

        # get bucket name
        buckets = self.list_buckets()
        if not buckets or len(buckets) == 0:
            print("No buckets available to delete.")
            return
        bucket_name = get_user_input("Enter the bucket name to delete", available_options=buckets)
        if not bucket_name: return

        # delete bucket
        try:
            print(f"Deleting bucket '{bucket_name}'")
            self.s3_controller.delete_bucket(bucket_name)
            print(f"Deleted bucket: {bucket_name}")
        except Exception as e:
            print(f"Error deleting bucket: {e}")

    def create_bucket(self):
        """
        Create a new S3 bucket.
        :return: None
        """

        # get bucket name
        bucket_name = get_user_input("Enter the name for the new bucket")
        if not bucket_name: return

        # create bucket
        try:
            print(f"Creating bucket '{bucket_name}'")
            self.s3_controller.create_bucket(bucket_name)
            print(f"Created bucket: {bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")
