from fastapi import FastAPI
import uvicorn

app = FastAPI()

# define a root `/` endpoint
@app.get("/")
async def read_root():
    return {"Zytholic-project API" : True}

@app.get("/10_prefered_beers")
def beers(style):
    return {style}

@app.get("/taste")
def taste(taste):
    return {taste}

@app.get("/brewery")
def brewery(brewery):
    return {brewery}


@app.get("/test")
def test(test):
    result = int(test)*2
    return {result}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=2809)
