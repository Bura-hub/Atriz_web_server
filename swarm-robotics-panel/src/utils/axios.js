import axios from 'axios';

// API base URL (incluye /api). Local: localhost:5000; producción: definir VUE_APP_API_URL
const apiBaseURL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api';

const instance = axios.create({
  baseURL: apiBaseURL,
});

// Interceptor para añadir el token a cada solicitud
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// Interceptor de respuesta: 401 → cerrar sesión y redirigir a login
instance.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('full_name');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Función para enviar datos de formulario
instance.postForm = (url, data) => {
  return instance.post(url, data, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });
};

export default instance;
