# ------------------------------------------------------------------- External Imports ----------------------------------------------------------------
from fastapi import FastAPI
import uvicorn
import argparse

# ------------------------------------------------------------------- Local Imports -------------------------------------------------------------------
from application_service.api.rest import router as webapp_router
# ------------------------------------------------------------------- Constants -----------------------------------------------------------------------

# ------------------------------------------------------------------- Classes -------------------------------------------------------------------------

app = FastAPI(
    title="Draft App Server"
)

app.include_router(webapp_router)  # Todo: import this from somewhere...


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Mono-server main Application!')
    parser.add_argument('-p', '--port', help='The internal port to run the app on', required=True)
    args = vars(parser.parse_args())

    uvicorn.run(app, host="0.0.0.0", port=int(args["port"]))  # Todo: pass host somehow...
