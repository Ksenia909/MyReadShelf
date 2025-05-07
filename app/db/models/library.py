import enum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.models import Book


class ReadingStatus(str, enum.Enum):
    to_read = "to_read"
    reading = "reading"
    read = "read"


class LibraryItem(Base):
    __tablename__ = "library"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    status: Mapped[ReadingStatus] = mapped_column(
        Enum(ReadingStatus), default=ReadingStatus.to_read
    )
    notes: Mapped[str | None] = mapped_column(String, nullable=True)

    book: Mapped["Book"] = relationship("Book")
