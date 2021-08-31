from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import joblib
import pandas as pd
#import zytholic_project.style_rename
from zytholic_project.apicall import get_most_similar_beers, get_most_similar_beers_ibu_abv
from zytholic_project.apicall import get_similar_style

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
    """Enter a beer name, return most similar beers"""
    results_name = get_most_similar_beers(name)
    return results_name

@app.get("/filter_abv_ibu")
def filter(name, abv=None, ibu=None):
    """Enter a beer name, maximum alcohol content wanted (ABV),
    and maximum bitterness wanted (IBU):
    return most similar beers"""
    results_name = get_most_similar_beers_ibu_abv(name, float(ibu), float(abv))
    return results_name

@app.get("/style_search")
def style_beers(style, abv=None, ibu=None):
    if abv is not None: abv = float(abv)
    if ibu is not None: ibu = float(ibu)
    return get_similar_style(style, abv, ibu)


# @app.get("/taste")
# def taste(taste):
#     X = taste
#     pipeline = joblib.load('model_taste.joblib')
#     results_taste = pipeline.predict(X)
#     return {results_taste}


# @app.get("/brewery")
# def brewery(brewery):
#     X = brewery
#     pipeline = joblib.load('model_brewery.joblib')
#     results_brewery = pipeline.predict(X)
#     return {results_brewery}


# @app.get("/test")
# def test(test):
#     result = int(test)*2
#     return {result}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=2809)
