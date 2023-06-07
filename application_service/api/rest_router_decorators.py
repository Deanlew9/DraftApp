# ------------------------------------------------------------------- External Imports ----------------------------------------------------------------
import functools

from application_service.logging.logger import Logger


# ------------------------------------------------------------------- Local Imports -------------------------------------------------------------------

# ------------------------------------------------------------------- Constants -----------------------------------------------------------------------

# ------------------------------------------------------------------- Classes -------------------------------------------------------------------------


def filter_args_to_print(kwargs: dict) -> dict:
    args_to_print = {}
    for k, v in kwargs.items():
        if isinstance(v, (bytes, str)):
            v = v[:50]
        if k == 'payload':
            for body_key, body_val in v.items():
                if isinstance(body_val, (bytes, str)):
                    body_val = body_val[:50]
                args_to_print[body_key] = body_val
            continue
        args_to_print[k] = v
    return args_to_print


def rest_api_request_wrapper(function):
    @functools.wraps(function)
    def wrapper_log_api_request(*args, **kwargs):
        user_id = kwargs["user_id"]
        args_to_print = filter_args_to_print(kwargs)
        msg = f"[user_id: {user_id}] Got request {function.__name__} with params: {args_to_print}"
        Logger().log_message(msg)
        return function(*args, **kwargs)
    return wrapper_log_api_request
