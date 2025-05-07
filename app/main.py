from fastapi import FastAPI

app = FastAPI(title="MyReadShelf")


@app.get("/")
async def read_root():
    return {"Hello": "World"}
