from application_service.aws.base_client import BaseAWSClient
from application_service.aws.secrets_manager import SecretsManager
from application_service.db.mongo.BaseMongoClient import MongoClient
from application_service.utils import Singleton


class Globals(metaclass=Singleton):

    def __init__(self):
        self.aws_client = BaseAWSClient()
        self.secrets_manager = SecretsManager(self.aws_client.session)
        self.mongo_client = MongoClient(self.secrets_manager)
