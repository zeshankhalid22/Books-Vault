from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from datetime import datetime
from app.core.db.base import Base
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from app.models.book import Book
    from app.models.article import Article
    from app.models.lists import ReadingList, Wishlist
    from app.models.user import User

class Content(Base):
    __tablename__ = 'content'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column()
    rating: Mapped[DECIMAL] = mapped_column(DECIMAL(3, 2), default=DECIMAL(0))
    uploaded_by: Mapped[Optional[int]] = mapped_column(ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    approved: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    # ? Will adding type improve database speed
    type: Mapped[str] = mapped_column()

    # One-to-one relationships
    book: Mapped[Optional["Book"]] = relationship(
        "Book", back_populates="content",
        uselist=False, lazy="selectin",
        cascade="all, delete-orphan"
    )
    article: Mapped[Optional["Article"]] = relationship("Article", back_populates="content", uselist=False, lazy="selectin")

    # User who uploaded the content
    uploader: Mapped[Optional["User"]] = relationship("User", back_populates="contents")

    # Many-to-many relationships
    in_reading_lists: Mapped[List["ReadingList"]] = relationship("ReadingList", back_populates="content")
    in_wishlists: Mapped[List["Wishlist"]] = relationship("Wishlist", back_populates="content")