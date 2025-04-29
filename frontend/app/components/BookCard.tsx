import React from 'react';
import type { Book } from '~/types/book';

interface BookCardProps {
  book: Book;
}

const BookCard: React.FC<BookCardProps> = ({ book }) => {
  return (
    <div className="border rounded-lg overflow-hidden shadow-md">
      <img src={book.cover_image} alt={book.title} className="w-full h-48 object-cover" />
      <div className="p-4">
        <h2 className="text-lg font-bold">{book.title}</h2>
        <p className="text-gray-700">{book.author}</p>
        {book.genre && <p className="text-gray-600">{book.genre}</p>}
        {book.rating && <p className="text-yellow-500">Rating: {book.rating}</p>}
      </div>
    </div>
  );
};

export default BookCard;