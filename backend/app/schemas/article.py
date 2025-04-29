from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional

# Base schema for creating an article
class ArticleBase(BaseModel):
    title: str
    author: str
    genre: str
    abstract: str

# Schema for creating a new article
class ArticleCreate(ArticleBase):
    rating: Optional[Decimal] = Field(default=Decimal('0.00'), ge=0, le=5)

# Schema for updating an article
class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    abstract: Optional[str] = None
    rating: Optional[Decimal] = None

# Schema for article responses
class ArticleResponse(ArticleBase):
    id: int
    rating: Decimal
    uploaded_by: Optional[int] = None
    approved: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True