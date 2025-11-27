import axios from 'axios';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL, // Your backend base URL
  timeout: 100000, // 100 seconds
  headers: {
    'Content-Type': 'application/json',
  }
});

// // Optional: Add request interceptor
// apiClient.interceptors.request.use(
//   (config) => {
//     // You can add auth tokens here if needed
//     const token = localStorage.getItem('token');
//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`;
//     }
//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );

// // Optional: Add response interceptor
// apiClient.interceptors.response.use(
//   (response) => {
//     return response;
//   },
//   (error) => {
//     // Handle common errors globally
//     if (error.response?.status === 401) {
//       // Redirect to login if unauthorized
//       localStorage.removeItem('token');
//       window.location.href = '/login';
//     }
//     return Promise.reject(error);
//   }
// );

export default apiClient;