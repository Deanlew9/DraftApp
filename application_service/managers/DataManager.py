# ------------------------------------------------------------------- External Imports ----------------------------------------------------------------
from datetime import datetime
from typing import Optional
from uuid import uuid4

# ------------------------------------------------------------------- Local Imports -------------------------------------------------------------------
from application_service.api.responses import ActionResponse
from application_service.business_processes.ContentBusinessProcesses import ContentBusinessProcessesFactory, DraftBusinessProcessNames
from application_service.data_classes.DataClasses import Draft, DraftComponent, DraftComponentTypes
from application_service.db.mongo.DraftsDAO import DraftsDAO
from application_service.db.s3.S3Buckets import AudioBucket


# ------------------------------------------------------------------- Constants -----------------------------------------------------------------------

# ------------------------------------------------------------------- Classes -------------------------------------------------------------------------

class DataManager:

    @classmethod
    def get_user_drafts(cls, user_id: str) -> Optional[list]:
        drafts = DraftsDAO().get_user_drafts(user_id)
        return drafts

    @classmethod
    def get_draft_components(cls, draft_uuid: str, user_id: str) -> Optional[list]:
        components = DraftsDAO().get_draft_components(draft_uuid)
        if not components:
            return None
        component_type_key = DraftComponent.field_names().draft_component_type
        for component in components:
            if component[component_type_key] == DraftComponentTypes.AUDIO:
                component["pre_signed_url"] = cls.get_audio_pre_signed_url(draft_uuid, component[DraftComponent.field_names().draft_component_uuid], user_id)
            elif component[component_type_key] == DraftComponentTypes.IMAGE:
                # Attach image from S3
                pass
            elif component[component_type_key] == DraftComponentTypes.VIDEO:
                # Attach video from S3
                pass
        return components

    @classmethod
    def create_draft(cls, draft_name: str, draft_description: Optional[str], user_id: str) -> ActionResponse:
        now_dt = datetime.now()
        draft = Draft(
            draft_uuid=str(uuid4()),
            draft_name=draft_name,
            draft_description=draft_description,
            user_id=user_id,
            created_datetime=now_dt,
            last_updated_datetime=now_dt,
            draft_components=[]
        )
        response = ContentBusinessProcessesFactory().get_business_process(DraftBusinessProcessNames.CREATE_DRAFT)().run(draft.dict())
        return response

    @classmethod
    def update_draft_components(cls, draft_uuid: str, components: list) -> ActionResponse:
        params = {"draft_uuid": draft_uuid, "components": components}
        response = ContentBusinessProcessesFactory().get_business_process(DraftBusinessProcessNames.UPDATE_DRAFT_COMPONENTS)().run(params)
        return response

    @classmethod
    def save_audio(cls, draft_uuid: str, component_uuid: str, user_id: str, uint8array: dict):
        audio_bytes = bytearray(uint8array.values())
        AudioBucket().put_audio(component_uuid, f"{user_id}/{draft_uuid}", audio_bytes)
        return cls.get_audio_pre_signed_url(draft_uuid, component_uuid, user_id)

    @classmethod
    def get_audio_pre_signed_url(cls, draft_uuid: str, component_uuid: str, user_id: str):
        return AudioBucket().create_presigned_url(f"{user_id}/{draft_uuid}/{component_uuid}")