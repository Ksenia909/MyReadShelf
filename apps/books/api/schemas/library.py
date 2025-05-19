from typing import List, Optional

from pydantic import BaseModel


class LibraryBase(BaseModel):
    name: str
    genre: Optional[str] = None
    description: Optional[str] = None


class LibraryCreate(LibraryBase):
    pass


class LibraryRead(LibraryBase):
    id: int
    user_id: int
    books: List["LibraryBookRead"] = []

    class Config:
        from_attributes = True


from .library_books import LibraryBookRead

LibraryRead.model_rebuild()
