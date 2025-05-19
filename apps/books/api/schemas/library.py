from typing import List

from pydantic import BaseModel

from apps.books.api.schemas.library_books import LibraryBookRead


class LibraryRead(BaseModel):
    id: int
    books: List[LibraryBookRead]

    class Config:
        orm_mode = True
