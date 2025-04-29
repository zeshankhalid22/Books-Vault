from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.content import Content

class Article(Base):
    __tablename__ = 'articles'

    id: Mapped[int] = mapped_column(ForeignKey('content.id', ondelete='CASCADE'), primary_key=True)
    abstract: Mapped[str] = mapped_column()
    content: Mapped["Content"] = relationship("Content", back_populates="article", lazy="joined")