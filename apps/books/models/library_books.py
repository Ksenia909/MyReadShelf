from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from core.enum import ReadingStatus


class LibraryBook(Base):
    __tablename__ = "library_books"

    id: Mapped[int] = mapped_column(primary_key=True)
    library_id: Mapped[int] = mapped_column(ForeignKey("libraries.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    status: Mapped[ReadingStatus] = mapped_column(
        Enum(ReadingStatus), default=ReadingStatus.to_read
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    library: Mapped["Library"] = relationship(back_populates="books")
    book: Mapped["Book"] = relationship(back_populates="in_libraries")
