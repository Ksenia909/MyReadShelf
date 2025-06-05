from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.users import models
from apps.users.api import schemas
from apps.users.services.auth import authenticate_user, create_user
from core.config import settings
from core.database import get_db
from core.security import create_access_token

router = APIRouter()


@router.post("/register", response_model=schemas.UserRead)
async def register(
        user_data: schemas.UserCreate,
        db: AsyncSession = Depends(get_db)
):
    existing_email = await db.execute(
        select(models.User).where(models.User.email == user_data.email)
    )
    if existing_email.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    existing_username = await db.execute(
        select(models.User).where(models.User.username == user_data.username)
    )
    if existing_username.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    return await create_user(db, user_data)


@router.post("/login")
async def login(
        user_data: schemas.LoginRequest,
        db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(user_data.email, user_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes
    )
    return {
        "access_token": create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer"
    }
