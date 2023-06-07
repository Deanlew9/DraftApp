# ------------------------------------------------------------------- External Imports ----------------------------------------------------------------
import abc
from typing import Any

from application_service.api.responses import ActionResponse


# ------------------------------------------------------------------- Local Imports -------------------------------------------------------------------

# ------------------------------------------------------------------- Constants -----------------------------------------------------------------------

# ------------------------------------------------------------------- Classes -------------------------------------------------------------------------


class BaseBusinessProcess:

    def __init__(self):
        self.success = False
        self.response = None

    def run(self, params):
        is_verified = self._verify(params)
        if is_verified:
            self._action(params)
        return ActionResponse(
            success = self.success,
            response = self.response
        )

    @abc.abstractmethod
    def _verify(self, params) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _action(self, params) -> Any:
        raise NotImplementedError


# ------------------------------------------------------------------- Factory -------------------------------------------------------------------------


class BaseBusinessProcessesFactory:

    def __init__(self, mapping: dict):
        self.MAPPING = mapping

    def get_business_process(self, name: str):
        return self.MAPPING[name]
