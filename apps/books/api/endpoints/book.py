from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.books import models
from apps.books.api import schemas
from core.database import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.BookRead])
async def list_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Book))
    return result.scalars().all()


@router.get("/{book_id}", response_model=schemas.BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Book).filter(models.Book.id == book_id)
    )
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=schemas.BookRead)
async def create_book(
        book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Book).filter(
        models.Book.title == book.title, models.Book.author == book.author
    ))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Book already exists")
    new_book = models.Book(**book.dict())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book
