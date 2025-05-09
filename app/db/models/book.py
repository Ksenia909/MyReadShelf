from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    author: Mapped[str] = mapped_column(String, index=True)

    library_items: Mapped[list["LibraryBook"]] = relationship(back_populates="book")
