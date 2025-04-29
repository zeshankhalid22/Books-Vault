import {create} from 'zustand';
import {persist} from 'zustand/middleware';
import type {User} from '~/types/user';
import apiClient from "~/utils/tokenUtils";

type AuthState = {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: string | null;
    token: string | null;

    // Actions
    login: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    verifyAuth: () => Promise<void>;
    clearError: () => void;
    refreshToken: () => Promise<string>;
};

export const useAuthStore = create<AuthState>()(
    persist(
        (set, get) => ({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
            token: null,

            // !TODO under the need
            refreshToken: async () => {
                try {
                    const currentToken = get().token;
                    const response = await apiClient.post(
                        '/refresh',
                        {},  // Usually nobody needed, token sent in headers
                        {
                            headers: {
                                'Authorization': `Bearer ${currentToken}`
                            }
                        }
                    );

                    const newToken = response.data.access_token;
                    // Update token in store
                    set({token: newToken});
                    // Update axios headers with new token

                    return newToken;
                } catch (error) {
                    console.error("Token refresh failed:", error);
                    // Clear auth state on refresh failure
                    set({
                        token: null,
                        isAuthenticated: false,
                        user: null
                    });
                    throw error;
                }
            },

            login: async (email: string, password: string) => {
                set({isLoading: true, error: null});
                try {
                    // Clear any previous Authorization header to avoid conflicts
                    delete apiClient.defaults.headers.common['Authorization'];

                    const response = await apiClient.post(
                        '/login',
                        {email, password},
                        {
                            headers: {
                                'Content-Type': 'application/json'
                            }
                        }
                    );

                    console.log('Login response:', response.data);

                    // Check if access_token exists in the response
                    if (!response.data.access_token) {
                        throw new Error('No access token in response');
                    }

                    // Store the token
                    const token = response.data.access_token;

                    // Setup default headers for future requests
                    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;

                    set({
                        user: response.data.user,
                        token: token,
                        isAuthenticated: true,
                        isLoading: false
                    });

                } catch (error: any) {
                    console.error("Login error:", error);
                    console.error("Response data:", error.response?.data);
                    console.error("Response status:", error.response?.status);
                    set({
                        error: error?.response?.data?.detail || 'Login failed',
                        isLoading: false,
                        user: null,
                        token: null,
                        isAuthenticated: false
                    });
                }
            },

            logout: async () => {
                set({isLoading: true});
                try {
                    console.log("TODO: define logout on backend");
                    await apiClient.post('/logout', {});
                } finally {
                    // Remove token and auth header
                    set({
                        user: null,
                        token: null,
                        isAuthenticated: false,
                        isLoading: false
                    });
                }
            },

            verifyAuth: async () => {
                set({isLoading: true});
                try {
                    const {token} = get();
                    if (!token) {
                        throw new Error('No token available');
                    }

                    // First just verify the token is valid
                    await apiClient.get('/verify-token', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    // Only if token is valid, fetch user data
                    const userResponse = await apiClient.get('/users/me', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    set({
                        user: userResponse.data,
                        isAuthenticated: true,
                        isLoading: false
                    });
                } catch (error: any) {
                    console.error("Auth check error:", error.response?.data);
                    set({
                        user: null,
                        isAuthenticated: false,
                        isLoading: false
                    });
                }
            },

            clearError: () => set({error: null})
        }),
        {
            name: 'auth-storage',
            partialize: (state) => ({
                isAuthenticated: state.isAuthenticated,
                token: state.token,
            }),
        }
    )
);

// Set up the interceptors only once on app initialization
const setupInterceptors = () => {
    const {logout, refreshToken} = useAuthStore.getState();
    import("~/utils/tokenUtils").then(({setupAuthInterceptors}) => {
        setupAuthInterceptors(logout, refreshToken);
    });
};

// Initialize auth token from persisted store and set up interceptors
const initializeAuth = () => {
    setupInterceptors();
};

// Call this after store hydration
initializeAuth();