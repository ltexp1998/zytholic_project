from fastapi import FastAPI
import socket
import sys
import uvicorn

app = FastAPI()

hostname = socket.gethostname()
version = f"{sys.version_info.major}.{sys.version_info.minor}"

# define a root `/` endpoint
@app.get("/")
async def read_root():
    return {
        "name":"Zytholic-project",
        "host": hostname,
        "version":
        f"Hello world! From FastAPI running on Uvicorn. Using Python {version}"
    }


@app.get("/10_prefered_beers")
def index():
    return {"Zytholic API : return 10 beers": True}

@app.get("/brewery")
def index():
    return {"Zytholic API : return brewery next to you": True}

@app.get("/test")
def index(test):
    return { test*2 }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2809)
