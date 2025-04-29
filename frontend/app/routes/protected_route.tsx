import { Navigate, Outlet } from 'react-router';
import { useEffect } from 'react';
import { useAuthStore } from '~/store/authStore';

export const Protected_route = () => {
  const { isAuthenticated, verifyAuth, isLoading, token } = useAuthStore();

  useEffect(() => {
    // Only check auth if we have a token but aren't authenticated yet
    if (token && !isAuthenticated && !isLoading) {
      verifyAuth();
    }
  }, [verifyAuth, isAuthenticated, isLoading, token]);

  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!isAuthenticated) {
    // Make sure path is correct - needs leading slash
    return <Navigate to="/users/auth" replace />;
  }

  return <Outlet />;
};