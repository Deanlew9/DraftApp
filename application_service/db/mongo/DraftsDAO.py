# ------------------------------------------------------------------- External-imports -----------------------------------------------
from typing import Optional
import bson

# ------------------------------------------------------------------- Local-imports --------------------------------------------------
from application_service.db.mongo.BaseCollectionDAO import BaseCollection
from application_service.data_classes.DataClasses import Draft
from application_service.db.mongo.constants import DatabaseNames, CollectionNames


# ------------------------------------------------------------------- Constants ------------------------------------------------------

# ------------------------------------------------------------------- Classes --------------------------------------------------------

class DraftsDAO(BaseCollection):

    class Item(Draft):
        _id: Optional[bson.ObjectId]

    DATABASE_NAME = DatabaseNames.MAIN
    COLLECTION_NAME = CollectionNames.USER_DRAFTS
    FIELD_NAMES = Item.field_names()
    INDEXES = [(FIELD_NAMES.draft_uuid, -1), (FIELD_NAMES.user_id, -1)]

    def get_user_drafts(self, user_id: str) -> Optional[list]:
        drafts = self.collection.find({self.FIELD_NAMES.user_id: user_id}, {"_id": 0})
        return list(drafts) if drafts else None

    def get_draft_components(self, draft_uuid: str) -> Optional[list]:
        draft = self.get_item({self.FIELD_NAMES.draft_uuid: draft_uuid}, {self.FIELD_NAMES.draft_components: 1})
        if not draft:
            return None
        return draft.get(self.FIELD_NAMES.draft_components, [])

    def update_draft_component(self, draft_uuid: str, components: list):
        return self.collection.update_one({self.FIELD_NAMES.draft_uuid: draft_uuid}, {"$set": {self.FIELD_NAMES.draft_components: components}})
