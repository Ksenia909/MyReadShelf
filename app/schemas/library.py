from typing import List

from pydantic import BaseModel

from app.schemas.library_books import LibraryBookRead


class LibraryRead(BaseModel):
    id: int
    books: List[LibraryBookRead]

    class Config:
        orm_mode = True
