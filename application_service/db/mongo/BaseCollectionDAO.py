# ------------------------------------------------------------------- External-imports -----------------------------------------------
from typing import Optional
from pymongo.collection import Collection
from pymongo.database import Database

# ------------------------------------------------------------------- Local-imports --------------------------------------------------
from application_service.globals import Globals
from application_service.logging.logger import Logger

# ------------------------------------------------------------------- Constants ------------------------------------------------------

# ------------------------------------------------------------------- Classes --------------------------------------------------------

class BaseCollection:
    DATABASE_NAME = None
    COLLECTION_NAME = None
    INDEXES = []

    def __init__(self, mongo_client=Globals().mongo_client, db_name=None, collection_name=None):
        self.mongo_client = mongo_client
        self.db = self._init_database(db_name)
        self.collection = self._init_collection(collection_name)
        self._fields = None

    def _init_database(self, db_name) -> Database:
        if db_name is not None:
            db = self.mongo_client.client[db_name]
        elif self.DATABASE_NAME is not None:
            db = self.mongo_client.client[self.DATABASE_NAME]
        else:
            raise ValueError("db name missing")
        return db

    def _init_collection(self, collection_name) -> Collection:
        if collection_name is None and self.COLLECTION_NAME is None:
            raise ValueError("self.COLLECTION_NAME missing!")
        if collection_name is not None:
            collection = self.db.get_collection(collection_name)
        else:
            collection = self.db.get_collection(self.COLLECTION_NAME)
        self._create_indexes_for_collection(collection)
        return collection

    def _create_indexes_for_collection(self, collection: Collection):
        coll_indexes = collection.index_information()
        for idx in self.INDEXES:
            if isinstance(idx, tuple):
                name, direction = idx
                idx_name = f"{name}_{direction}"
                idx = [idx]
            elif isinstance(idx, list):
                idx_name = "_".join([f"{name}_{direction}" for name, direction in idx])
            else:
                return
            if idx_name not in coll_indexes:
                Logger().log_message(f"Creating index '{idx_name}' in MongoDB collection {collection.name}!")
                collection.create_index(idx, background=True)

    def get_item(self, query: dict, fields_to_keep: Optional[dict] = None) -> Optional[dict]:
        projection = {"_id": 0}
        if fields_to_keep:
            projection.update({field: 1 for field in fields_to_keep})
        return self.collection.find_one(query, projection)

    def count(self) -> int:
        return self.collection.count_documents({})

# ----------------------------------------------- Functions ---------------------------------------------------
