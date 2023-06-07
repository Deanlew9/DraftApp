# ------------------------------------------------------------------- External Imports ----------------------------------------------------------------
from dynaconf import Dynaconf

# ------------------------------------------------------------------- Local Imports -------------------------------------------------------------------

# ------------------------------------------------------------------- Constants -----------------------------------------------------------------------

# ------------------------------------------------------------------- Classes -------------------------------------------------------------------------


settings = Dynaconf(
                settings_files=[
                    "application_service/config/settings.toml",
                    "application_service/config/local.settings.toml"
                ],
                environments=True
            )

default_settings = settings.from_env("default")
default_env = default_settings.ENV

AWS_ABSPATH = default_settings.AWS_CRED_PATH
