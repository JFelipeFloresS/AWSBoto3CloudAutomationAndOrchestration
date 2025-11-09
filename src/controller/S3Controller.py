from src.model.Resources import DEFAULT_REGION


class S3Controller:
    def __init__(self, s3_service):
        self.s3_service = s3_service

    def list_buckets(self):
        """
        List all S3 buckets in the account.
        :return: List of S3 bucket names.
        """
        buckets = self.s3_service.buckets.all()
        bucket_names = [bucket.name for bucket in buckets]
        return bucket_names

    def list_objects(self, bucket_name):
        """
        List all objects in a specified S3 bucket.
        :param bucket_name: The name of the S3 bucket.
        :return: List of object keys in the bucket.
        """
        bucket = self.s3_service.Bucket(bucket_name)
        objects = bucket.objects.all()
        object_keys = [obj.key for obj in objects]
        return object_keys

    def upload_object(self, bucket_name, object_key, file_path):
        """
        Upload an object to a specified S3 bucket.
        :param bucket_name: The name of the S3 bucket.
        :param object_key: The key (name) for the uploaded object.
        :param file_path: The local file path of the object to upload.
        :return: None
        """
        bucket = self.s3_service.Bucket(bucket_name)
        bucket.upload_file(file_path, object_key)
        print(f"Uploaded {file_path} to {bucket_name}/{object_key}")

    def download_object(self, bucket_name, object_key, download_path, file_extension):
        """
        Download an object from a specified S3 bucket.
        :param bucket_name: The name of the S3 bucket.
        :param object_key: The key (name) of the object to download.
        :param download_path: The local file path to save the downloaded object.
        :param file_extension: The file extension to append to the downloaded file.
        :return: None
        """
        bucket = self.s3_service.Bucket(bucket_name)
        file_extension = '.' + file_extension if not file_extension.startswith('.') else file_extension
        bucket.download_file(object_key, download_path + '/' + object_key + file_extension)
        print(f"Downloaded {bucket_name}/{object_key} to {download_path}")

    def delete_bucket(self, bucket_name):
        """
        Delete a specified S3 bucket.
        :param bucket_name: The name of the S3 bucket to delete.
        :return: None
        """
        bucket = self.s3_service.Bucket(bucket_name)
        # First, delete all objects in the bucket
        bucket.objects.all().delete()
        # Then, delete the bucket itself
        bucket.delete()
        print(f"Deleted bucket: {bucket_name}")

    def create_bucket(self, bucket_name, region: str = DEFAULT_REGION):
        """
        Create a new S3 bucket.
        :param bucket_name: The name of the S3 bucket to create.
        :param region: The AWS region to create the bucket in.
        :return: None
        """
        if region is None:
            self.s3_service.create_bucket(Bucket=bucket_name)
        else:
            self.s3_service.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"Created bucket: {bucket_name} in region: {region}")
