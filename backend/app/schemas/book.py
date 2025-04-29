# In app/schemas/book.py
from decimal import Decimal
from typing import Optional, Any, Dict

from pydantic import BaseModel,  model_validator

from app.core.config import settings

class BookBase(BaseModel):
    title: str
    author: str
    genre: str | None = None
    rating: Decimal | None = Decimal('0.0')
    cover_image: str = f"{settings.BOOK_COVER_IMAGE_DIR}/default_cover.png"

class BookCreate(BookBase):
    pass


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: Optional[str] = None
    rating: Optional[Decimal] = None
    cover_image: str
    uploaded_by: Optional[str] = "ADMIN"

    class Config:
        from_attributes = True

    @model_validator(mode='before')
    @classmethod
    def extract_nested_content(cls, data: Any) -> Dict[str, Any]:
        # Initialize with default value
        uploaded_by = "ADMIN"

        if hasattr(data, 'content') and data.content is not None:
            # Convert uploaded_by to string explicitly
            if getattr(data.content, 'uploaded_by', None) is not None:
                uploaded_by = str(data.content.uploaded_by)

            return {
                'id': data.id,
                'cover_image': data.cover_image,
                'title': data.content.title,
                'author': data.content.author,
                'genre': getattr(data.content, 'genre', None),
                'rating': getattr(data.content, 'rating', None),
                'uploaded_by': uploaded_by,
            }
        return data
