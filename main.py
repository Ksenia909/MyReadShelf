from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.books.api.router import router as books_router
from apps.users.api.router import router as users_router
from core.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="MyReadShelf", lifespan=lifespan)
app.include_router(books_router)
app.include_router(users_router)
