from fastapi import APIRouter

from .endpoints import book, library

router = APIRouter()

router.include_router(book.router, prefix="/books", tags=["books"])
router.include_router(library.router, prefix="/libraries", tags=["libraries"])
