# ------------------------------------------------------------------- External-imports -----------------------------------------------
import boto3
import json
# --------------------------------------------- Local-imports -------------------------------------------------
from application_service.aws.constants import REGION_NAME
from application_service.config.Config import AWS_ABSPATH
from application_service.utils import Singleton
# ------------------------------------------------------------------- Constants ---------------------------------------------------

# ------------------------------------------------------------------- Classes ----------------------------------------------------

class BaseAWSClient(metaclass=Singleton):

    def __init__(self):
        self.creds = self._get_credentials()
        self.session = boto3.Session(
            aws_access_key_id=self.creds['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self.creds['AWS_SECRET_ACCESS_KEY'],
            region_name=REGION_NAME,
        )

    @staticmethod
    def _get_credentials():
        filepath = AWS_ABSPATH
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data

# ------------------------------------------------------------------- Functions ---------------------------------------------------