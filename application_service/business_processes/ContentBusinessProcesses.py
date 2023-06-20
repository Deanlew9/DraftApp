# ------------------------------------------------------------------- External Imports ----------------------------------------------------------------
from typing import Any, List

# ------------------------------------------------------------------- Local Imports -------------------------------------------------------------------
from application_service.business_processes.BaseBusinessProcess import BaseBusinessProcess, BaseBusinessProcessesFactory
from application_service.data_classes.BaseDataClass import BaseDataClass
from application_service.data_classes.DataClasses import Draft, DraftComponent
from application_service.db.mongo.DraftsDAO import DraftsDAO


# ------------------------------------------------------------------- Constants -----------------------------------------------------------------------


class DraftResponses:
    DRAFT_CREATED = "Draft created!"
    DRAFT_COMPONENTS_UPDATED = "Draft components updated!"
    INVALID_DRAFT_PARAMETERS = "Invalid draft parameters..."
    FAILED_TO_INSERT_ITEM_INTO_DB = "Couldn't insert draft into db..."
    FAILED_FOR_SOME_REASON = "Failed for some reason..."


class DraftBusinessProcessNames:
    CREATE_DRAFT = "create_draft"
    UPDATE_DRAFT_COMPONENTS = "update_draft_components"


# ------------------------------------------------------------------- Classes -------------------------------------------------------------------------

class CreateDraftParams(Draft):
    pass

class UpdateDraftComponentsParams(BaseDataClass):
    draft_uuid: str
    draft_components: List[DraftComponent]

# ------------------------------------------------------------------- BaseBusinessProcesses -----------------------------------------------------------


# ------------------------------------------------------------------- BusinessProcesses ---------------------------------------------------------------


class CreateDraftBusinessProcess(BaseBusinessProcess):

    def _verify(self, params: dict) -> bool:
        if len(params[CreateDraftParams.field_names().draft_name]) == 0:
            self.response = DraftResponses.INVALID_DRAFT_PARAMETERS
            return False
        return True

    def _action(self, params: dict) -> Any:
        response = DraftsDAO().collection.insert_one(params)
        if not response:
            self.response = DraftResponses.FAILED_TO_INSERT_ITEM_INTO_DB
            self.success = False
            return
        self.response = DraftResponses.DRAFT_CREATED
        self.success = True


class UpdateDraftComponentsBusinessProcess(BaseBusinessProcess):

    def _verify(self, params: dict) -> bool:
        return True

    def _action(self, params: dict) -> Any:
        response = DraftsDAO().update_draft_component(params["draft_uuid"], params["components"])
        if not response:
            self.response = DraftResponses.FAILED_FOR_SOME_REASON
            self.success = False
            return
        self.response = DraftResponses.DRAFT_COMPONENTS_UPDATED
        self.success = True

# ------------------------------------------------------------------- Factory -------------------------------------------------------------------------


class ContentBusinessProcessesFactory(BaseBusinessProcessesFactory):

    def __init__(self):
        mapping = {
            DraftBusinessProcessNames.CREATE_DRAFT: CreateDraftBusinessProcess,
            DraftBusinessProcessNames.UPDATE_DRAFT_COMPONENTS: UpdateDraftComponentsBusinessProcess,
        }
        super().__init__(mapping)
