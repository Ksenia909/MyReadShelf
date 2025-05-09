from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.db import Base


class Library(Base):
    __tablename__ = "libraries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="library")
    books: Mapped[list["LibraryItem"]] = relationship(
        back_populates="library", cascade="all, delete-orphan"
    )
