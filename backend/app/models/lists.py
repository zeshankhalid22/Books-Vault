from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.content import Content

class ReadingList(Base):
    __tablename__ = 'reading_list'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    content_id: Mapped[int] = mapped_column(ForeignKey('content.id', ondelete='CASCADE'))

    # Define relationships
    # In ReadingList and Wishlist models
    user: Mapped["User"] = relationship(
        "User",
        back_populates="reading_list",  # or "wishlist"
        lazy="joined"  # Use joined for single objects
    )
    content: Mapped["Content"] = relationship("Content", back_populates="in_reading_lists")

    # Define composite primary key
    __table_args__ = (PrimaryKeyConstraint('user_id', 'content_id'),)

class Wishlist(Base):
    __tablename__ = 'wishlist'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    content_id: Mapped[int] = mapped_column(ForeignKey('content.id', ondelete='CASCADE'))

    # Define relationships
    # In ReadingList and Wishlist models
    user: Mapped["User"] = relationship(
        "User",
        back_populates="wishlist",  # or "wishlist"
        lazy="joined"  # Use joined for single objects
    )
    content: Mapped["Content"] = relationship("Content", back_populates="in_wishlists")

    # Define composite primary key
    __table_args__ = (PrimaryKeyConstraint('user_id', 'content_id'),)