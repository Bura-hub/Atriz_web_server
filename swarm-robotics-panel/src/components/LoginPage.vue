<template>
  <div class="login-wrapper">
    <div
      class="login-card"
      :class="{
        'login-card--loading': loading,
        'login-card--success': loginSuccess,
        'login-card--enter': cardEnter
      }"
    >
      <div v-if="loginSuccess" class="login-success">
        <span class="login-success__icon" aria-hidden="true">✓</span>
        <p class="login-success__text">Sesión iniciada</p>
        <p class="login-success__sub">Redirigiendo al panel…</p>
      </div>
      <template v-else>
        <div class="login-card__header">
          <img src="/logo.png" alt="Logo Plataforma Atriz" class="login-card__logo" />
          <div class="login-card__titles">
            <h1 class="login-card__title">SW-LRE-UDENAR</h1>
            <p class="login-card__subtitle">Plataforma Atriz — Inicio de sesión</p>
          </div>
        </div>
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
        <button type="submit" class="login-card__btn btn-press" :disabled="loading">
          <span v-if="loading" class="login-card__btn-spinner"></span>
          <span v-else>Acceder</span>
        </button>
        <p v-if="error" class="login-card__error" role="alert">{{ error }}</p>
      </form>
      </template>
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
      loginSuccess: false,
      cardEnter: false,
    };
  },
  mounted() {
    requestAnimationFrame(() => {
      this.cardEnter = true;
    });
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
        this.loading = false;
        this.loginSuccess = true;
        setTimeout(() => {
          this.$router.push('/');
        }, 900);
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
}

.login-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 520px;
  padding: 2rem;
  background: var(--bg-surface);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-default);
  box-shadow: var(--shadow-lg);
  transition: opacity 0.25s ease, transform 0.35s ease;
  opacity: 0;
  transform: translateY(24px) scale(0.96);
}

.login-card--enter {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.login-card--loading {
  opacity: 0.92;
  pointer-events: none;
}

.login-card--success {
  text-align: center;
  padding: 2.5rem 2rem;
}

.login-success {
  animation: login-success-in 0.4s ease;
}

.login-success__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
  margin-bottom: 1rem;
  font-size: 2rem;
  font-weight: 700;
  color: white;
  background: var(--success);
  border-radius: 50%;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
}

.login-success__text {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.login-success__sub {
  font-size: 0.9375rem;
  color: var(--text-secondary);
}

@keyframes login-success-in {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.login-card__header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.login-card__logo {
  width: 160px;
  height: 160px;
  object-fit: contain;
  flex-shrink: 0;
}

.login-card__titles {
  flex: 1;
  min-width: 0;
}

.login-card__title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  text-align: left;
  margin-bottom: 0.25rem;
  letter-spacing: -0.02em;
}

.login-card__subtitle {
  font-size: 1rem;
  color: var(--text-secondary);
  text-align: left;
  margin-bottom: 0;
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
