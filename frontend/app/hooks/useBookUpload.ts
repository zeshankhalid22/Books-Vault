import {useState} from 'react';
import {booksApi} from '~/api/booksApi';
import {useAuthStore} from '~/store/authStore';

export const useBookUpload = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadRequests, setUploadRequests] = useState([]);
  const {isAuthenticated} = useAuthStore();

  const submitUploadRequest = async (bookData: any) => {
    if (!isAuthenticated) {
      setError("You must be logged in to submit upload requests");
      return false;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await booksApi.createUploadRequest(bookData);
      setIsLoading(false);
      return response.data;
    } catch (error: any) {
      console.error("Upload request error:", error);
      setError(error?.response?.data?.detail || "Failed to submit upload request");
      setIsLoading(false);
      return false;
    }
  };

  const fetchUserUploadRequests = async () => {
    if (!isAuthenticated) {
      setError("You must be logged in to view your upload requests");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await booksApi.getUserUploadRequests();
      setUploadRequests(response.data);
      setIsLoading(false);
    } catch (error: any) {
      console.error("Error fetching upload requests:", error);
      setError(error?.response?.data?.detail || "Failed to fetch your upload requests");
      setIsLoading(false);
    }
  };

  return {
    isLoading,
    error,
    uploadRequests,
    submitUploadRequest,
    fetchUserUploadRequests,
    clearError: () => setError(null)
  };
};