from typing import Optional

from pydantic import BaseModel

from app.core import ReadingStatus
from app.schemas.book import BookRead


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
