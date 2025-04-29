// responsible for making actual request on backend

import apiClient from "~/utils/tokenUtils";
import type { Book, UploadRequest } from "~/types/book";

const BOOKS_BASE_URL = "/books";
const UPLOAD_REQUEST_BASE_URL = "/upload_request";

export const booksApi = {
  // Fetch all books with pagination
  getAllBooks: async (page = 1, limit = 10): Promise<Book[]> => {
    try {
      const response = await apiClient.get(`${BOOKS_BASE_URL}/?page=${page}&limit=${limit}`);
      return response.data;
    } catch (error) {
      throw new Error("Failed to fetch books");
    }
  },

  // Fetch a single book by ID
  getBookById: async (id: number | string): Promise<Book> => {
    try {
      const response = await apiClient.get(`${BOOKS_BASE_URL}/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch book with ID ${id}`);
    }
  },

  // Search books by query
  searchBooks: async (query: string): Promise<Book[]> => {
    try {
      const response = await apiClient.get(`${BOOKS_BASE_URL}/search/?q=${encodeURIComponent(query)}`);
      return response.data;
    } catch (error) {
      throw new Error("Failed to search books");
    }
  },

  // Create a new upload request
  createUploadRequest: async (bookData: UploadRequest): Promise<void> => {
    try {
      await apiClient.post(`${UPLOAD_REQUEST_BASE_URL}/`, bookData);
    } catch (error) {
      throw new Error("Failed to create upload request");
    }
  },

  // Fetch all upload requests for the current user
  getUserUploadRequests: async (): Promise<UploadRequest[]> => {
    try {
      const response = await apiClient.get(`${UPLOAD_REQUEST_BASE_URL}/my`);
      return response.data;
    } catch (error) {
      throw new Error("Failed to fetch user upload requests");
    }
  }
};