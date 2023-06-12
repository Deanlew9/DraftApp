# DraftApp (BE)

As a songwriter, it's essential for me to record my ideas whenever inspiration strikes throughout the day. This could involve jotting down lyrics, recording myself humming a melody or playing an instrument while singing, or even capturing photos or videos as a creative outlet.

Here's a server side of an app for organizing my ideas and drafts as notes.
Each note/draft contains components that could be one of 4: text, audio, image, video.

Setting up:

1. Clone this repository.
2. Set a python env with version 3.10
3. In the main directory of this repo run: `$ pip install -r application_service/requirements.txt`
4. Create an AWS user.
5. Add the AWS credentials to `~/.cred/draft_app_aws.json`
6. Create a MongoDB cluster.
7. Add the MongoDB password to SecretsManager in AWS under secret name "mongo_dev" as an object `{"password", <password>}` (replace <password> with the password).
8. Run `$ touch application_service/config/local.settings.toml` and add this code to it:
  ```
[default]
env = "dev"
#AWS
aws_cred_path = "~/.cred/draft_app_aws.json"
[dev]
# mongo
mongo_user = <mongo_user>
mongo_address = <mongo_address>
  ```
9. Run `$ uvicorn application_service.app:app --port 3001`
  
Your all set!
