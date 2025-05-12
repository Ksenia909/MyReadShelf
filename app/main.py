from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.database import Base, engine
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="MyReadShelf", lifespan=lifespan)
app.include_router(router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
