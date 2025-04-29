import { useEffect, useState } from "react";
import { useBooksStore } from "~/store/bookStore";
import BookList from "~/components/BookList";
import SearchInput from "~/components/SearchInput";

export default function BooksIndex() {
  const { books, isLoading, error, fetchBooks, searchBooks } = useBooksStore();
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    if (!searchQuery) {
      fetchBooks(); // Fetch all books if no search query
    }
  }, [fetchBooks, searchQuery]);

  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    if (query.trim()) {
      await searchBooks(query); // Perform search
    } else {
      fetchBooks(); // Reset to all books if query is empty
    }
  };

  if (isLoading) {
    return <div className="flex justify-center p-8">Loading books...</div>;
  }

  if (error) {
    return <div className="text-red-500 p-4">{error}</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Books Library</h1>
      <SearchInput onSearch={handleSearch} />
      <BookList books={books} />
    </div>
  );
}