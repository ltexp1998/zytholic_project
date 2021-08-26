from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import joblib
#import zytholic_project.style_rename

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

##### define endpoint

@app.get("/")
async def read_root():
    return {"Zytholic-project API" : True}

@app.get("/name_beer")
def beers(name):
    X = name
    pipeline = joblib.load('model_name.joblib')
    results_name = pipeline.predict(X)
    return {results_name}


@app.get("/10_prefered_beers")
def beers(style):
    X = style
    pipeline = joblib.load('model_style.joblib')
    results_style = pipeline.predict(X)
    return {results_style}


@app.get("/taste")
def taste(taste):
    X = taste
    pipeline = joblib.load('model_taste.joblib')
    results_taste = pipeline.predict(X)
    return {results_taste}


@app.get("/brewery")
def brewery(brewery):
    X = brewery
    pipeline = joblib.load('model_brewery.joblib')
    results_brewery = pipeline.predict(X)
    return {results_brewery}


@app.get("/test")
def test(test):
    result = int(test)*2
    return {result}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=2809)
