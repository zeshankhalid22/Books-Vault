from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum

class RequestType(str, Enum):
    BOOK = "book"
    ARTICLE = "article"

class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class UploadRequestBase(BaseModel):
    title: str
    author: str
    type: RequestType
    genre: Optional[str] = None
    rating: Optional[float] = Field(default=0.0, ge=0.0, le=5.0)
    cover_image: Optional[str] = None  # Only for books
    abstract: Optional[str] = None  # Only for articles

class UploadRequestCreate(UploadRequestBase):
    @field_validator('cover_image', 'abstract', mode='after')
    def validate_fields(cls, value, info):
        data = info.data
        field_name = info.field_name

        if data.get('type') == RequestType.BOOK and field_name == 'abstract' and value:
            raise ValueError('Abstract should not be provided for book uploads')
        if data.get('type') == RequestType.ARTICLE and field_name == 'cover_image' and value:
            raise ValueError('Cover image should not be provided for article uploads')

        return value

class UploadRequestUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    cover_image: Optional[str] = None
    abstract: Optional[str] = None
    status: Optional[RequestStatus] = None

class UploadRequestResponse(UploadRequestBase):
    id: int
    requested_by: Optional[int] = None
    status: RequestStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True