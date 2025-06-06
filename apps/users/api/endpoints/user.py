from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from apps.users import models
from apps.users.api import schemas
from apps.users.api.dependencies import get_current_user
from core.database import get_db

router = APIRouter()


@router.get("/me", response_model=schemas.UserRead)
async def read_current_user(
        current_user: models.User = Depends(get_current_user)
):
    return current_user


@router.get("/me/libraries")
async def get_user_libraries(
        current_user: models.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.User)
        .options(selectinload(models.User.libraries))
        .where(models.User.id == current_user.id)
    )
    user_with_libraries = result.scalar_one()
    return user_with_libraries.libraries
