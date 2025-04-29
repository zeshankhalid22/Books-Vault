import React from 'react';
import type { Book } from '~/types/book';
import BookCard from './BookCard';

interface BookListProps {
  books: Book[];
}

const BookList: React.FC<BookListProps> = ({ books }) => {
  if (!books || books.length === 0) {
    return <div>No books available</div>;
  }

  return (
    <div className="grid grid-cols-4 gap-6 p-4">
      {books.map((book) => (
        <BookCard key={book.id} book={book} />
      ))}
    </div>
  );
};

export default BookList;