FROM python:3.10.1

EXPOSE 3001

COPY application_service application_service
COPY aws_credentials.json aws_credentials.json

RUN pip install -r application_service/requirements.txt

RUN pip install urllib3==2.0.3

CMD uvicorn application_service.app:app --host 0.0.0.0 --port 3001
