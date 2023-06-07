# -------------------------------------------- External-imports -----------------------------------------------
import os
from logging import getLogger, INFO
# --------------------------------------------- Local-imports -------------------------------------------------
from application_service.config.Config import settings

# ----------------------------------------------- Constants ---------------------------------------------------

# ------------------------------------------------ Classes ----------------------------------------------------

class Logger:

    def __init__(self):
        self._logger = self._set_logger()

    def log_message(self, msg):
        self._set_level(INFO)
        self._logger.info(msg)

    @classmethod
    def _set_logger(cls):
        name = os.path.dirname(os.path.abspath(__file__)).split("/")[-3]
        try:
            if settings.logfile_name:
                name = settings.logfile_name
        except AttributeError:
            pass
        logger = getLogger(name)
        return logger

    def _set_level(self, lvl_name):
        self._logger.setLevel(lvl_name)

# ----------------------------------------------- Functions ---------------------------------------------------
