# In app/models/book.py
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db.base import Base

if TYPE_CHECKING:
    from app.models import Content


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(ForeignKey('content.id', ondelete='CASCADE'), primary_key=True)
    cover_image: Mapped[str] = mapped_column()
    content: Mapped["Content"] = relationship(
        "Content",
        back_populates="book",
        lazy="joined",
        passive_deletes=True
    )