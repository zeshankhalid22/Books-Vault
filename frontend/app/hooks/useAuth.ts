import { useNavigate } from 'react-router';
import { useAuthStore } from '~/store/authStore';

export const useAuth = () => {
  const navigate = useNavigate();
  const auth = useAuthStore();

  return {
    ...auth,
    login: async (email: string, password: string) => {
      console.log(`!Checking for ${email} and ${password}`)
      await auth.login(email, password);
      if (auth.isAuthenticated) {
        navigate('/');
      }
    },
    logout: async () => {
      await auth.logout();
      navigate('/users/auth');
    }
  };
}