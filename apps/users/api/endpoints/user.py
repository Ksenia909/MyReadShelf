from fastapi import APIRouter, Depends

from apps.users import models
from apps.users.api import schemas
from apps.users.api.dependencies import get_current_user

router = APIRouter()


@router.get("/me", response_model=schemas.UserRead)
async def read_current_user(
        current_user: models.User = Depends(get_current_user)
):
    return current_user

@router.get("/me/libraries")
async def get_user_libraries(
        current_user: models.User = Depends(get_current_user)
):
    return current_user.libraries
