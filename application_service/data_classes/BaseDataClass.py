# -------------------------------------------- External-imports -----------------------------------------------
from collections import namedtuple
from pydantic import BaseModel
# --------------------------------------------- Local-imports -------------------------------------------------

# ----------------------------------------------- Constants ---------------------------------------------------

# ------------------------------------------------ Classes ----------------------------------------------------

class BaseDataClass(BaseModel):

    @classmethod
    def field_names(cls) -> namedtuple:
        name_tup = namedtuple(f"{cls.__name__}", [field for field in cls.__fields__.keys()])
        return name_tup(*cls.__fields__.keys())
    