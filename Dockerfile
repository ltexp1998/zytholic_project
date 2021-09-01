FROM python:3.8.6-buster

COPY API/ API
COPY zytholic_project/ zytholic_project

COPY raw_data/ / raw_data/

COPY assets/ / assets/
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Execute compilation of similarity matrices 
# Saves files and dataframes using pickle
RUN python -m zytholic_project.base_model

CMD uvicorn API.api:app --host 0.0.0.0 --port $PORT
