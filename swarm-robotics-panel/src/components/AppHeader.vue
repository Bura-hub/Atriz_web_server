<template>
  <header class="app-header">
    <div class="app-header__brand">
      <h1 class="app-header__title">Laboratorio de Robótica de Enjambres (LRE-UDENAR)</h1>
      <p class="app-header__subtitle">Universidad de Nariño — Interfaz de control remoto</p>
    </div>
    <div class="app-header__actions">
      <a
        :href="apiDocsUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="app-header__link"
      >
        Documentación API
      </a>
      <button
        type="button"
        @click="logout"
        class="app-header__logout"
        aria-label="Cerrar sesión"
      >
        <span class="app-header__logout-text">Cerrar sesión</span>
      </button>
    </div>
  </header>
</template>

<script>
const apiUrl = process.env.VUE_APP_API_URL || 'http://localhost:5000/api';
const apiBase = apiUrl.replace(/\/api\/?$/, '') || 'http://localhost:5000';
export default {
  name: 'AppHeader',
  computed: {
    apiDocsUrl() {
      return `${apiBase}/admin/docs`;
    },
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('full_name');
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.app-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-default);
}

@media (min-width: 768px) {
  .app-header {
    flex-direction: row;
    align-items: flex-start;
  }
}

.app-header__brand {
  text-align: center;
}

@media (min-width: 768px) {
  .app-header__brand {
    text-align: left;
  }
}

.app-header__title {
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  line-height: 1.3;
}

@media (min-width: 768px) {
  .app-header__title {
    font-size: 1.5rem;
  }
}

.app-header__subtitle {
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.app-header__logout {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  background: var(--danger);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
}

.app-header__logout:hover {
  background: var(--danger-hover);
}

.app-header__logout:active {
  transform: scale(0.98);
}

.app-header__logout:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(225, 29, 72, 0.4);
}

.app-header__logout-text {
  display: inline-block;
}

.app-header__link {
  margin-right: 0.75rem;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--accent);
  background: transparent;
  border: 1px solid var(--accent);
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
}
.app-header__link:hover {
  background: var(--accent);
  color: white;
}
</style>
