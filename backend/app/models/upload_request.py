from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db.base import Base
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User

class UploadRequest(Base):
    __tablename__ = 'upload_requests'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    author: Mapped[str]
    type: Mapped[str]  # Discriminator field ('book' or 'article')
    genre: Mapped[Optional[str]]
    rating: Mapped[Optional[float]] = mapped_column(default=0.0)
    cover_image: Mapped[Optional[str]]  # Only for books
    abstract: Mapped[Optional[str]]  # Only for articles
    requested_by: Mapped[Optional[int]] = mapped_column(ForeignKey('user.id', ondelete='SET NULL'))
    status: Mapped[str] = mapped_column(default='pending')
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define relationships
    user: Mapped["User"] = relationship("User", back_populates="upload_requests")

    # Add check constraints
    __table_args__ = (
        CheckConstraint("type IN ('book', 'article')", name="type_check"),
        CheckConstraint("status IN ('pending', 'approved', 'rejected')", name="status_check"),
    )
    # Methods
    def to_content_dict(self):
        """Convert UploadRequest to a dictionary"""
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "rating": self.rating,
            "uploaded_by": self.requested_by,
            "approved": True
        }

    def build_book(self, content_id: int):
        from app.models.book import Book

        return Book(
            id=content_id,  # Foreign key to Content table
            cover_image=self.cover_image
        )

    def build_article(self, content_id: int):
        """Creates an Article object from the request data"""
        from app.models.article import Article

        return Article(
            id=content_id,  # Foreign key to Content table
            abstract=self.abstract
        )
