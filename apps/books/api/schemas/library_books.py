from typing import Optional

from pydantic import BaseModel

from apps.books.api.schemas.book import BookRead
from core.enum import ReadingStatus


class LibraryBookBase(BaseModel):
    book_id: int
    status: ReadingStatus = ReadingStatus.to_read
    notes: Optional[str] = None


class LibraryBookCreate(LibraryBookBase):
    pass


class LibraryBookRead(LibraryBookBase):
    id: int
    book: BookRead

    class Config:
        orm_mode = True
