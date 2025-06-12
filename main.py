from fastapi import FastAPI

from core.router_register import register_all_service_routers

app = FastAPI(title="MyReadShelf")

register_all_service_routers(app)
