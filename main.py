from contextlib import asynccontextmanager

from fastapi import FastAPI

import apps.books.models
import apps.users.models
from core.database import Base, engine
from core.router_register import register_all_service_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="MyReadShelf", lifespan=lifespan)

register_all_service_routers(app)
