from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from apps.books import models
from apps.books.api import schemas
from apps.users.api.dependencies import get_current_user
from apps.users.models import User
from core.database import SessionDep

router = APIRouter()


@router.post("/", response_model=schemas.LibraryRead)
async def create_library(
        library_data: schemas.LibraryCreate,
        session: SessionDep,
        current_user: User = Depends(get_current_user)
):
    library = models.Library(
        **library_data.model_dump(),
        user_id=current_user.id
    )
    session.add(library)
    try:
        await session.commit()
        await session.refresh(library, ["books"])
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Library with this name already exists for the user"
        )
    return library


@router.get("/{library_id}", response_model=schemas.LibraryRead)
async def get_library(
    library_id: int,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    library = await session.get(models.Library, library_id)
    if not library or library.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Library not found"
        )
    await session.refresh(library, ["books"])
    return library


@router.delete("/{library_id}")
async def delete_library(
    library_id: int,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    library = await session.get(models.Library, library_id)
    if not library or library.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Library not found"
        )
    await session.delete(library)
    await session.commit()
