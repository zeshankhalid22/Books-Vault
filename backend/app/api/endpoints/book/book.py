import os
import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, Query, HTTPException, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.config import settings
from app.core.dependencies import get_db, admin_role_check
from app.schemas.book import BookResponse, BookCreate
from . import functions

book_module = APIRouter()
admin_book_module = APIRouter()


@book_module.get("/", response_model=List[BookResponse])
async def read_all_books(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
):
    books = await functions.get_all_books(db, skip, limit)
    return books


@book_module.get("/search/", response_model=List[BookResponse])
async def search_books(
        q: str = Query(..., min_length=1, description="Search query string"),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
):
    """Search for books by title, author, or genre"""
    books = await functions.search_books(db, q, skip, limit)
    return books


@book_module.get("/{book_id}", response_model=BookResponse)
async def get_book_by_id(book_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific book by ID"""
    book = await functions.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# --- Admin routes ---

@admin_book_module.post("/", response_model=BookResponse)
async def create_book(
        title: str = Form(...),
        author: str = Form(...),
        genre: str = Form(None),
        rating: float = Form(0.0),
        cover_image: UploadFile = File(None),
        db: AsyncSession = Depends(get_db),
        current_user=Depends(admin_role_check)
):
    # Create book data with default cover image from schema
    book_data = BookCreate(
        title=title,
        author=author,
        genre=genre,
        rating=Decimal(str(rating)),
    )

    # If cover image provided by user
    if cover_image and cover_image.filename:
        # Create unique filename
        file_extension = os.path.splitext(cover_image.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Save file using consistent path
        file_path = os.path.join(settings.BOOK_COVER_IMAGE_DIR.lstrip("/"), unique_filename)
        try:
            with open(file_path, "wb") as image_file:
                content = await cover_image.read()
                image_file.write(content)
        except IOError:
            raise HTTPException(status_code=500, detail="Failed to save cover image")

        # Path for database should match schema format
        book_data.cover_image = f"{settings.BOOK_COVER_IMAGE_DIR}/{unique_filename}"

    new_book = await functions.create_book(db, book_data, current_user.id)
    return new_book

@admin_book_module.delete("/{book_id}", status_code=204)
async def delete_book(
        book_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(admin_role_check)
):

    success = await functions.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
