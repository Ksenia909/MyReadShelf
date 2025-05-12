from fastapi import APIRouter

from .books import router as books_router
# from .users import router as users_router
# from .library import router as library_router


router = APIRouter()
router.include_router(books_router, prefix="/books", tags=["books"])
# router.include_router(users_router, prefix="/users", tags=["users"])
# router.include_router(library_router, prefix="/library", tags=["library"])

__all__ = ["router"]
