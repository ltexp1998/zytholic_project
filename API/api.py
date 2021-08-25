from fastapi import FastAPI

app = FastAPI()

# define a root `/` endpoint
@app.get("/")
def index():
    return {"Zytholic API : running": True}

@app.get("/10_prefered_beers")
def index():
    return {"Zytholic API : return 10 beers": True}

@app.get("/brewery")
def index():
    return {"Zytholic API : return brewery next to you": True}

@app.get("/test")
def index():
    return {"Zytholic API : test": True}
