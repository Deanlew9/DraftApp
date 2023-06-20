# -------------------------------------------- External-imports -----------------------------------------------
from botocore.exceptions import ClientError

# --------------------------------------------- Local-imports -------------------------------------------------
from application_service.aws.constants import AWSServiceNames
from application_service.globals import Globals
from application_service.logging.logger import Logger
from application_service.utils import Singleton


# ----------------------------------------------- Constants ---------------------------------------------------

# ------------------------------------------------ Classes ----------------------------------------------------

class BaseS3Bucket:

    BASE_URL = "https://drafts-media.s3.us-east-1.amazonaws.com/"

    def __init__(self, bucket_name):
        self.session = Globals().aws_client.session
        self.s3 = self.session.resource(AWSServiceNames.S3)
        self.client = self.session.client(AWSServiceNames.S3)
        self.bucket = self.s3.Bucket(bucket_name)
        self.bucket_name = bucket_name

    def remove_file(self, path_to_file):
        self.s3.Object(self.bucket_name, path_to_file).delete()

    def put(self, file_name, folder_path, file_object, content_type, storage_class="STANDARD_IA"):
        key = f"{folder_path}/{file_name}"
        self.bucket.put_object(
            ACL="authenticated-read",
            Key=key,
            ContentType=content_type,
            Body=file_object,
            StorageClass=storage_class,
        )
        return key

    def get(self, file_name, folder_path):
        try:
            obj = self.s3.Object(self.bucket_name, f"{folder_path}/{file_name}")
            data = obj.get()["Body"].read()
        except:
            data = None
        return data

    def create_presigned_url(self, file_name, expiration=3600):
        """
        Generate a presigned URL to share an S3 object
        :param file_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """
        params = {'Bucket': self.bucket_name, 'Key': file_name}
        try:
            response = self.client.generate_presigned_url('get_object', Params=params, ExpiresIn=expiration)
        except ClientError as e:
            Logger().log_message(e)
            return None

        # The response contains the presigned URL
        return response

class AudioBucket(BaseS3Bucket, metaclass=Singleton):
    def __init__(self, bucket_name="drafts-media"):
        BaseS3Bucket.__init__(self, bucket_name)

    def put_audio(self, file_name, folder_path, file_object, storage_class="STANDARD_IA"):
        key = self.put(
            file_name,
            folder_path,
            file_object,
            content_type="audio/x-wav",
            storage_class=storage_class,
        )

        return key

# ----------------------------------------------- Functions ---------------------------------------------------
