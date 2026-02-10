<template>
  <div class="login-wrapper">
    <div class="login-card">
      <h1 class="login-card__title">SW-LRE-UDENAR</h1>
      <p class="login-card__subtitle">Plataforma Atriz — Inicio de sesión</p>
      <form @submit.prevent="login" class="login-form">
        <div class="input-group">
          <label for="username">Nombre de usuario</label>
          <input
            id="username"
            v-model="username"
            type="text"
            class="input-field"
            placeholder="Introduzca su usuario"
            required
            autocomplete="username"
            :disabled="loading"
          />
        </div>
        <div class="input-group">
          <label for="password">Contraseña</label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="input-field"
            placeholder="Introduzca su contraseña"
            required
            autocomplete="current-password"
            :disabled="loading"
          />
        </div>
        <button type="submit" class="login-card__btn" :disabled="loading">
          <span v-if="loading" class="login-card__btn-spinner"></span>
          <span v-else>Acceder</span>
        </button>
        <p v-if="error" class="login-card__error" role="alert">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from '../utils/axios';
import qs from 'qs';

export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      error: null,
      loading: false,
    };
  },
  methods: {
    async login() {
      this.error = null;
      this.loading = true;
      try {
        const response = await axios.post(
          '/login',
          qs.stringify({ username: this.username, password: this.password }),
          { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
        );
        const accessToken = response.data.access_token;
        localStorage.setItem('access_token', accessToken);
        const payload = JSON.parse(atob(accessToken.split('.')[1]));
        localStorage.setItem('full_name', payload.full_name || this.username);
        this.$router.push('/');
      } catch (err) {
        const status = err.response?.status;
        const detail = err.response?.data?.detail;
        if (status === 401 || (detail && typeof detail === 'string' && detail.toLowerCase().includes('password'))) {
          this.error = 'Usuario o contraseña incorrectos. Inténtelo de nuevo.';
        } else if (err.message === 'Network Error') {
          this.error = 'No se pudo conectar al servidor. Compruebe la conexión.';
        } else {
          this.error = detail || 'Error al iniciar sesión. Inténtelo de nuevo.';
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.login-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 1.5rem;
  background: url('../assets/login-background_1.jpg') no-repeat center center fixed;
  background-size: cover;
}

.login-wrapper::before {
  content: '';
  position: fixed;
  inset: 0;
  background: rgba(11, 15, 26, 0.72);
  backdrop-filter: blur(8px);
  z-index: 0;
}

.login-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  background: var(--bg-surface);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-default);
  box-shadow: var(--shadow-lg);
}

.login-card__title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  text-align: center;
  margin-bottom: 0.25rem;
  letter-spacing: -0.02em;
}

.login-card__subtitle {
  font-size: 1rem;
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 1.5rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.input-group {
  margin-bottom: 1rem;
  text-align: left;
}

.input-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 0.375rem;
}

.login-card__btn {
  width: 100%;
  margin-top: 0.5rem;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: white;
  background: var(--accent);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 0.2s, transform 0.1s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
}

.login-card__btn:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 14px var(--accent-glow);
}

.login-card__btn:active:not(:disabled) {
  transform: translateY(0);
}

.login-card__btn:disabled {
  opacity: 0.8;
  cursor: not-allowed;
}

.login-card__btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px var(--accent-glow);
}

.login-card__btn-spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: login-spin 0.7s linear infinite;
}

@keyframes login-spin {
  to {
    transform: rotate(360deg);
  }
}

.login-card__error {
  margin-top: 1rem;
  padding: 0.75rem;
  font-size: 0.875rem;
  color: #fda4af;
  background: var(--danger-muted);
  border-radius: var(--radius-md);
  border: 1px solid rgba(225, 29, 72, 0.35);
}
</style>
