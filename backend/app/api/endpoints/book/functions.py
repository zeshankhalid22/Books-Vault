from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book as BookModel, Book
from app.schemas.book import BookCreate
from app.models.content import Content as ContentModel

async def get_all_books(db: AsyncSession, skip: int = 0, limit: int = 10):
    """Retrieve all books with pagination"""
    query = (
        select(BookModel)
        .options(joinedload(BookModel.content))
        .limit(limit)
        .offset(skip)
    )
    result = await db.execute(query)
    return result.scalars().all()

async def search_books(
    db: AsyncSession,
    query: str,
    skip: int = 0,
    limit: int = 10
):
    """Search books by title, author, or genre"""
    from sqlalchemy import or_
    from app.models.content import Content

    search_query = f"%{query}%"

    stmt = (
        select(BookModel)
        .join(BookModel.content)
        .options(joinedload(BookModel.content))
        .filter(
            or_(
                Content.title.ilike(search_query),
                Content.author.ilike(search_query),
                Content.genre.ilike(search_query)
            )
        )
        .limit(limit)
        .offset(skip)
    )

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_book_by_id(db: AsyncSession, book_id: int):
    """Retrieve a specific book by its ID"""
    query = (
        select(BookModel)
        .options(joinedload(BookModel.content))
        .where(BookModel.id == book_id)
    )
    result = await db.execute(query)
    return result.scalars().first()

# --- Admin functions ---

async def create_book(db: AsyncSession, book_data: BookCreate, admin_id: int):
    # Create content record
    new_content = ContentModel(
        title=book_data.title,
        author=book_data.author,
        genre=book_data.genre,
        rating=book_data.rating,
        type="book",
        uploaded_by=admin_id,
        approved=True
    )
    db.add(new_content)
    await db.flush()  # Get the ID

    # Create book record
    new_book = BookModel(
        id=new_content.id,
        cover_image=book_data.cover_image
    )
    db.add(new_book)
    await db.commit()

    # IMPORTANT: Explicitly reload with joined relationship
    stmt = select(BookModel).options(joinedload(BookModel.content)).where(BookModel.id == new_book.id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def delete_book(db: AsyncSession, book_id: int) -> bool:
    # First check if the book exists
    book = await db.execute(
        select(Book).where(Book.id == book_id)
    )
    book = book.scalar_one_or_none()

    if not book:
        # Book doesn't exist
        return False

    # Book exists, proceed with deletion
    await db.execute(delete(Book).where(Book.id == book_id))
    await db.commit()
    return True