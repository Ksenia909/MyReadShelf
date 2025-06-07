from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.books import models
from apps.books.api import schemas
from apps.users.api.dependencies import get_current_user
from apps.users.models import User
from core.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.LibraryRead)
async def create_library(
        library_data: schemas.LibraryCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    library = models.Library(
        **library_data.model_dump(),
        user_id=current_user.id
    )
    db.add(library)
    try:
        await db.commit()
        await db.refresh(library, ["books"])
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Library with this name already exists for the user"
        )
    return library


@router.get("/{library_id}", response_model=schemas.LibraryRead)
async def get_library(
    library_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    library = await db.get(models.Library, library_id)
    if not library or library.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Library not found"
        )
    await db.refresh(library, ["books"])
    return library


@router.delete("/{library_id}")
async def delete_library(
    library_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    library = await db.get(models.Library, library_id)
    if not library or library.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Library not found"
        )
    await db.delete(library)
    await db.commit()
