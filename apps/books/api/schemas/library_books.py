from typing import Optional

from pydantic import BaseModel

from core.enum import ReadingStatus


class LibraryBookBase(BaseModel):
    book_id: int
    status: ReadingStatus = ReadingStatus.to_read
    notes: Optional[str] = None


class LibraryBookCreate(LibraryBookBase):
    pass


class LibraryBookRead(LibraryBookBase):
    id: int
    book: 'BookRead'

    class Config:
        from_attributes = True


from .book import BookRead

LibraryBookRead.model_rebuild()
