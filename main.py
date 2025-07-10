from fastapi import APIRouter, FastAPI

from core.router_register import register_all_service_routers

app = FastAPI(title="MyReadShelf")
router = APIRouter(prefix="/api/v1")
register_all_service_routers(router)
app.include_router(router)
