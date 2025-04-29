from fastapi import APIRouter
from app.api.endpoints.book.book import book_module
from app.api.endpoints.book.book import admin_book_module

book_router = APIRouter()

book_router.include_router(
    book_module,
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)

book_router.include_router(
    admin_book_module,
    prefix="/admin/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


