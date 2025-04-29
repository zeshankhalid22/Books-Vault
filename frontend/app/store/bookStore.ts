import {create} from 'zustand';
import {booksApi} from '~/api/booksApi';
import type {Book} from '~/types/book';

type BooksState = {
  books: Book[];
  currentBook: Book | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchBooks: (page?: number, limit?: number) => Promise<void>;
  fetchBookById: (id: number | string) => Promise<void>;
  searchBooks: (query: string) => Promise<void>;
  clearError: () => void;
};

export const useBooksStore = create<BooksState>()((set) => ({
  books: [],
  currentBook: null,
  isLoading: false,
  error: null,

  fetchBooks: async (page = 1, limit = 10) => {
    set({isLoading: true, error: null});
    try {
      const response = await booksApi.getAllBooks(page, limit);
      set({books: response.data, isLoading: false});
    } catch (error: any) {
      console.error("Error fetching books:", error);
      set({
        error: error?.response?.data?.detail || 'Failed to fetch books',
        isLoading: false
      });
    }
  },

  fetchBookById: async (id) => {
    set({isLoading: true, error: null});
    try {
      const response = await booksApi.getBookById(id);
      set({currentBook: response.data, isLoading: false});
    } catch (error: any) {
      console.error("Error fetching book:", error);
      set({
        error: error?.response?.data?.detail || `Failed to fetch book ${id}`,
        isLoading: false
      });
    }
  },

  searchBooks: async (query) => {
    set({isLoading: true, error: null});
    try {
      const response = await booksApi.searchBooks(query);
      set({books: response.data, isLoading: false});
    } catch (error: any) {
      console.error("Error searching books:", error);
      set({
        error: error?.response?.data?.detail || 'Search failed',
        isLoading: false
      });
    }
  },

  clearError: () => set({error: null})
}));

