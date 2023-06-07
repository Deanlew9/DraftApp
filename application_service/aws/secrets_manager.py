# ------------------------------------------------------------------- External-imports -----------------------------------------------
import base64
import json
from botocore.exceptions import ClientError

# ------------------------------------------------------------------- Local-imports -------------------------------------------------
from application_service.aws.constants import AWSServiceNames, REGION_NAME
from application_service.utils import Singleton
from application_service.logging.logger import Logger

# ------------------------------------------------------------------- Constants ---------------------------------------------------

# ------------------------------------------------------------------- Classes ----------------------------------------------------

class SecretsManager(metaclass=Singleton):

    def __init__(self, aws_session):
        super().__init__()
        self.session = aws_session
        self.client = self.session.client(
            service_name=AWSServiceNames.SECRET_MANAGER,
            region_name=REGION_NAME,
        )
        self.secrets = {}

    def get_secret(self, secret_name: str, return_json: bool = False) -> dict:
        if secret_name in self.secrets:
            secret = self.secrets[secret_name]
        else:
            secret = self.fetch_secret(secret_name, return_json)
            self.secrets[secret_name] = secret
        return secret

    def fetch_secret(self, secret_name: str, return_json: bool) -> dict:
        Logger().log_message(f"fetching secret - {secret_name}")
        try:
            secret_value_response = self.client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                Logger().log_message(f"The requested secret {secret_name} was not found")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                Logger().log_message(f"The request was invalid due to: {e}")
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                Logger().log_message(f"The request had invalid params: {e}")
            elif e.response['Error']['Code'] == 'DecryptionFailure':
                Logger().log_message(f"The requested secret can't be decrypted using the provided KMS key: {e}")
            elif e.response['Error']['Code'] == 'InternalServiceError':
                Logger().log_message(f"An error occurred on service side: {e}")
        else:
            if 'SecretString' in secret_value_response:
                text_secret_data = secret_value_response['SecretString']
                secrets_obj = json.loads(text_secret_data) if not return_json else text_secret_data
            else:
                binary_secret_data = secret_value_response['SecretBinary']
                secrets_obj = base64.b64decode(binary_secret_data)
            return secrets_obj

# ------------------------------------------------------------------- Functions ---------------------------------------------------
