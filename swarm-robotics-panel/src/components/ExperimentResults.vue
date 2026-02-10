<template>
  <section class="card-panel card-panel--relative">
    <h2 class="section-title">Resultados de los experimentos</h2>

    <!-- Skeleton de carga inicial (simulado según docs) -->
    <div v-if="loadingResults" class="loading-overlay">
      <div class="loading-overlay__content">
        <div class="loading-overlay__spinner" aria-hidden="true"></div>
        <p class="loading-overlay__text">{{ loadingStep }}</p>
      </div>
      <div class="skeleton-block loading-overlay__skeleton">
        <div class="skeleton-line skeleton-line--title skeleton-line--short"></div>
        <div class="skeleton-line mt-2"></div>
        <div class="skeleton-line mt-1"></div>
        <div class="skeleton-line mt-1 w-3/4"></div>
      </div>
    </div>

    <div v-show="!loadingResults" id="results-container" class="results-placeholder">
      <div class="results-box">
        <h3 class="results-box__title">Estado</h3>
        <div v-if="resultLogs.length">
          <ul class="results-list list-disc pl-5 space-y-0 results-list--logs">
            <li v-for="(log, index) in resultLogs" :key="index" :class="logClass(log)" class="sim-step log-line">
              {{ log.text }}
            </li>
          </ul>
        </div>
        <p v-else class="results-box__empty">Los resultados de los experimentos (logs de sesiones, telemetría) se mostrarán aquí cuando haya experimentos ejecutados.</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "ExperimentResults",
  data() {
    return {
      loadingResults: true,
      loadingStep: "Cargando resultados…",
      resultLogs: [],
    };
  },
  mounted() {
    this.runInitialLoad();
  },
  methods: {
    logClass(log) {
      if (log.type === 'success') return 'text-green-600 dark:text-green-400';
      if (log.type === 'error') return 'text-red-600 dark:text-red-400';
      return 'text-gray-600 dark:text-gray-400';
    },
    async runInitialLoad() {
      this.resultLogs = [];
      this.loadingStep = "Consultando sesiones y telemetría…";
      await new Promise((r) => setTimeout(r, 400));
      this.loadingStep = "Procesando resultados…";
      await new Promise((r) => setTimeout(r, 350));
      this.loadingResults = false;
      this.resultLogs = [
        { text: "Listo. No hay resultados recientes. Ejecuta experimentos desde el panel de control para ver logs y telemetría aquí.", type: "success" },
      ];
    },
  },
};
</script>

<style scoped>
.card-panel--relative {
  position: relative;
}
.results-placeholder {
  min-height: 80px;
}
</style>
