import axios from 'axios';

// Configuración de Axios
const instance = axios.create({
  // baseURL: 'http://atriz-project.duckdns.org/api', // Ajusta la URL base a tu configuración
  baseURL: 'http://10.20.50.228/api', // Ajusta la URL base a tu configuración
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

// Función para enviar datos de formulario
instance.postForm = (url, data) => {
  return instance.post(url, data, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });
};

export default instance;
