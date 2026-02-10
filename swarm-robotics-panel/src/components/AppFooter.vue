<template>
  <footer class="app-footer">
    <div class="app-footer__time">
      <p class="app-footer__label">Hora local</p>
      <p class="app-footer__value">{{ dateFormatted }}</p>
      <p class="app-footer__value app-footer__value--clock">{{ timeFormatted }}</p>
    </div>
    <button
      type="button"
      class="app-footer__refresh"
      @click="refreshTimer"
      aria-label="Actualizar hora"
    >
      <i class="fas fa-sync-alt" aria-hidden="true"></i>
    </button>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter',
  data() {
    return {
      now: new Date(),
    };
  },
  computed: {
    dateFormatted() {
      return this.now.toLocaleDateString('es-ES', {
        weekday: 'short',
        day: 'numeric',
        month: 'short',
      });
    },
    timeFormatted() {
      return this.now.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      });
    },
  },
  methods: {
    updateTimer() {
      this.now = new Date();
    },
    refreshTimer() {
      this.updateTimer();
    },
  },
  mounted() {
    this.timerInterval = setInterval(this.updateTimer, 1000);
  },
  beforeUnmount() {
    clearInterval(this.timerInterval);
  },
};
</script>

<style scoped>
.app-footer {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  margin-top: 2rem;
  padding: 1.25rem 1.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-default);
  background: var(--bg-surface);
}

.app-footer__time {
  text-align: left;
}

.app-footer__label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}

.app-footer__value {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
}

.app-footer__value--clock {
  font-size: 1.5rem;
  font-variant-numeric: tabular-nums;
  color: var(--text-primary);
}

.app-footer__refresh {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  padding: 0;
  color: var(--text-secondary);
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: 50%;
  cursor: pointer;
  transition: color 0.2s, background 0.2s;
}

.app-footer__refresh:hover {
  color: var(--text-primary);
  background: var(--bg-surface-hover);
}

.app-footer__refresh:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--accent-glow);
}
</style>
