# ------------------------------------------------------------------- External Imports ----------------------------------------------------------------
import argparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ------------------------------------------------------------------- Local Imports -------------------------------------------------------------------
from application_service.api.rest import router as webapp_router
# ------------------------------------------------------------------- Constants -----------------------------------------------------------------------

# ------------------------------------------------------------------- Classes -------------------------------------------------------------------------

app = FastAPI(
    title="Draft App Server"
)

app.include_router(webapp_router)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Mono-server main Application!')
    parser.add_argument('-p', '--port', help='The internal port to run the app on', required=True)
    args = vars(parser.parse_args())

    uvicorn.run(app, host="0.0.0.0", port=int(args["port"]))  # Todo: pass host somehow...
