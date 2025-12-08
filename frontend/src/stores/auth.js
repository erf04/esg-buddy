import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import apiClient from '@/plugins/axios';

export const useAuthStore = defineStore('auth', () => {
  // State - using sessionStorage for persistence across reloads
  const token = ref(sessionStorage.getItem('token'));
  const user = ref(null);
  const isLoading = ref(false);

  // Getters
  const isAuthenticated = computed(() => !!token.value);
  const getUser = computed(() => user.value);

  // Actions
  const setToken = (newToken) => {
    token.value = newToken;
    if (newToken) {
      sessionStorage.setItem('token', newToken);
    } else {
      sessionStorage.removeItem('token');
    }
  };

  const setUser = (userData) => {
    user.value = userData;
  };

  const login = async (email, password) => {
    isLoading.value = true;
    try {
      const response = await apiClient.post('/auth/login/', {
        email,
        password
      });
      
      if (response.data.token) {
        setToken(response.data.token);
        setUser(response.data.user);
        return { success: true, data: response.data };
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  };

  const signup = async (firstName,lastName,email, password) => {
    isLoading.value = true;
    try {
      const response = await apiClient.post('/auth/register/', {
        first_name:firstName,
        last_name:lastName,
        email:email,
        password:password
      });
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    // Clear session storage for this tab
    sessionStorage.removeItem('token');
  };

  // Initialize store - check if we have a token in sessionStorage
  const initialize = () => {
    const savedToken = sessionStorage.getItem('token');
    if (savedToken) {
      token.value = savedToken;
      console.log('Restored token from sessionStorage');
    }
  };

  return {
    token,
    user,
    isLoading,
    isAuthenticated,
    getUser,
    setToken,
    setUser,
    login,
    signup,
    logout,
    initialize
  };
});