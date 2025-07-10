from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from apps.books import models
from apps.books.api import schemas
from core.database import SessionDep

router = APIRouter()


@router.get("/", response_model=list[schemas.BookRead])
async def list_books(session: SessionDep):
    result = await session.execute(select(models.Book))
    return result.scalars().all()


@router.get("/{book_id}", response_model=schemas.BookRead)
async def get_book(book_id: int, session: SessionDep):
    result = await session.execute(
        select(models.Book).filter(models.Book.id == book_id)
    )
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=schemas.BookRead)
async def create_book(book: schemas.BookCreate, session: SessionDep):
    result = await session.execute(select(models.Book).filter(
        models.Book.title == book.title, models.Book.author == book.author
    ))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Book already exists")
    new_book = models.Book(**book.model_dump())
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book


@router.delete("/{book_id}")
async def delete_book(book_id: int, session: SessionDep):
    result = await session.execute(
        select(models.Book).filter(models.Book.id == book_id)
    )
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    await session.delete(book)
    await session.commit()
    return {"detail": "Book deleted"}
