# ------------------------------------------------------------------- External-imports -----------------------------------------------
from datetime import datetime
from enum import Enum
from typing import Optional, List

# ------------------------------------------------------------------- Local-imports ---------------------------------------------------
from application_service.data_classes.BaseDataClass import BaseDataClass

# ------------------------------------------------------------------- Constants -------------------------------------------------------

# ------------------------------------------------------------------- Classes ---------------------------------------------------------

class DraftComponentTypes(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"

class DraftComponent(BaseDataClass):
    draft_component_uuid: str
    draft_uuid: str
    user_uuid: str
    draft_component_type: DraftComponentTypes  # todo: is this how you do it?
    text: Optional[str]
    transcribed_text: Optional[str]

class Draft(BaseDataClass):
    draft_uuid: str
    draft_name: str
    draft_description: Optional[str]
    user_uuid: str
    created_datetime: datetime
    last_updated_datetime: datetime
    draft_components: List[DraftComponent]

class User(BaseDataClass):
    user_id: str
    created_datetime: datetime
