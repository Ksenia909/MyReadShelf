from fastapi import APIRouter

from .endpoints import user

router = APIRouter(prefix="/api/v1")

router.include_router(user.router, prefix="/users", tags=["users"])
