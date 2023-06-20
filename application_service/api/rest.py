# ------------------------------------------------------------------- External Imports ----------------------------------------------------------------
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter

# ------------------------------------------------------------------- Local Imports -------------------------------------------------------------------
from application_service.api.rest_router_decorators import rest_api_request_wrapper
from application_service.managers.DataManager import DataManager

# ------------------------------------------------------------------- Constants -----------------------------------------------------------------------

router = APIRouter()

# ------------------------------------------------------------------- Classes -------------------------------------------------------------------------

@router.get("/users/{user_id}/drafts")
@rest_api_request_wrapper
def get_user_drafts(user_id: str):
    res = DataManager.get_user_drafts(user_id)
    return JSONResponse(jsonable_encoder(res))

@router.get("/drafts/{draft_uuid}/components")
@rest_api_request_wrapper
def get_draft_components(draft_uuid: str, user_id: str):
    res = DataManager.get_draft_components(draft_uuid, user_id)
    return JSONResponse(jsonable_encoder(res))

@router.post("/drafts")
@rest_api_request_wrapper
def create_draft(payload: dict, user_id: str):
    res = DataManager.create_draft(payload["draft_name"], payload["draft_description"], payload["user_id"])
    return JSONResponse(jsonable_encoder(res))

@router.put("/drafts/{draft_uuid}/components")
@rest_api_request_wrapper
def update_draft_components(draft_uuid: str, payload: dict, user_id: str):
    res = DataManager.update_draft_components(draft_uuid, payload["components"])
    return JSONResponse(jsonable_encoder(res))


@router.post("/drafts/{draft_uuid}/components/{component_uuid}/audio")
@rest_api_request_wrapper
def save_audio_recording(draft_uuid: str, component_uuid: str, payload: dict, user_id: str):
    res = DataManager.save_audio(draft_uuid, component_uuid, user_id, payload["uint8array"])
    return JSONResponse(jsonable_encoder(res))
