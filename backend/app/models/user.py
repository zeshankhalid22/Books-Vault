from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TIMESTAMP, Boolean, String
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from app.core.db.base import Base

if TYPE_CHECKING:
    from app.models.content import Content
    from app.models.upload_request import UploadRequest
    from app.models.lists import ReadingList, Wishlist

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]]
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str]
    profile_image_url: Mapped[Optional[str]]
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[str] = mapped_column(String(50), default='reader')
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Define relationships
    contents: Mapped[List["Content"]] = relationship("Content", back_populates="uploader")
    upload_requests: Mapped[List["UploadRequest"]] = relationship("UploadRequest", back_populates="user")

    # In User model
    reading_list: Mapped[List["ReadingList"]] = relationship(
        "ReadingList",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"  # Use selectin for collections
    )

    wishlist: Mapped[List["Wishlist"]] = relationship(
        "Wishlist",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"  # Use selectin for collections
    )

