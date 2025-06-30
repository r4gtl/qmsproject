import axios from 'axios';

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  withCredentials: true, // se usi cookie
});

// Aggiungi Authorization header se presente
instance.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor per refresh automatico
instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Se riceviamo 401 e non abbiamo già provato il refresh
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      localStorage.getItem('refreshToken')
    ) {
      originalRequest._retry = true;
      try {
        const response = await axios.post(
          `${
            import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
          }/token/refresh/`,
          {
            refresh: localStorage.getItem('refreshToken'),
          }
        );

        const newAccessToken = response.data.access;
        localStorage.setItem('accessToken', newAccessToken);

        // aggiorna header e riprova richiesta originale
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return instance(originalRequest);
      } catch (err) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login'; // o usa navigate()
        return Promise.reject(err);
      }
    }

    return Promise.reject(error);
  }
);

export default instance;
