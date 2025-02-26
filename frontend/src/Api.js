import axios from 'axios';

// Configuration de base pour Axios
const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // URL de base de votre backend
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token JWT aux requêtes
api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('access');
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepteur pour gérer le rafraîchissement du token en cas d'expiration
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Si l'erreur est 401 (non autorisé) et que la requête n'a pas déjà été réessayée
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Marquer la requête comme réessayée
      const refreshToken = localStorage.getItem('refresh');

      if (refreshToken) {
        try {
          // Rafraîchir le token d'accès
          const response = await axios.post('http://localhost:8000/api/token/refresh/', {
            refresh: refreshToken,
          });
          localStorage.setItem('access', response.data.access); // Mettre à jour le token d'accès
          originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`; // Mettre à jour l'en-tête
          return api(originalRequest); // Réessayer la requête originale
        } catch (refreshError) {
          console.error('Échec du rafraîchissement du token :', refreshError);
          // Rediriger vers la page de connexion en cas d'échec
          window.location.href = '/login';
        }
      } else {
        // Rediriger vers la page de connexion si aucun token de rafraîchissement n'est disponible
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default api;