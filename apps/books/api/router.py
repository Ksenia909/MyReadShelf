from fastapi import APIRouter

from .endpoints import book

router = APIRouter(prefix="/api/v1")

router.include_router(book.router, prefix="/books", tags=["books"])
# library_router = APIRouter(prefix="/library", tags=["library"])
