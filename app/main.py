from fastapi import FastAPI

from app.core import load_config

app = FastAPI(title="MyReadShelf")
config = load_config()


@app.get("/")
async def read_root():
    return {"Hello": "World"}
