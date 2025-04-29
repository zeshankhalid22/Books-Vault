import axios, {type AxiosInstance} from 'axios';

// Create the single Axios instance to be used throughout the app
const apiClient: AxiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000',
});


// Setup axios interceptors for token refresh
export const setupAuthInterceptors = (
    onLogout: () => void,
    refreshTokenFn: () => Promise<string>
) => {
    // In setupAuthInterceptors function in tokenUtils.ts
    apiClient.interceptors.response.use(
        (response) => response,
        async (error) => {
            const originalRequest = error.config;

            // Only try token refresh for 401 errors, not 422
            if (error.response?.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true;

                try {
                    const newToken = await refreshTokenFn();
                    // Update the Authorization header with the new token
                    originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
                    return apiClient(originalRequest);
                } catch (refreshError) {
                    onLogout();
                    return Promise.reject(refreshError);
                }
            }

            return Promise.reject(error);
        }
    );
};

export default apiClient;