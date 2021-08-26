FROM python:3.8.6-buster

COPY API/ API
COPY zytholic_project/ zytholic_project
# COPY model.joblib /model.joblib
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn API.api:app --host 0.0.0.0 --port $PORT