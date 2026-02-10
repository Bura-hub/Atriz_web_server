<template>
  <div class="card-panel card-panel--relative">
    <h2 class="section-title">Datos de batería y sensores</h2>
    <p class="text-sm label-muted mb-2">Según el driver: estado de batería (getBatteryPercentage) y sensor streaming (IMU, odometría).</p>

    <!-- Overlay de carga durante consulta -->
    <div v-if="consultLoading" class="loading-overlay">
      <div class="loading-overlay__content">
        <div class="loading-overlay__spinner" aria-hidden="true"></div>
        <p class="loading-overlay__text">{{ consultStep }}</p>
      </div>
      <div class="skeleton-block loading-overlay__skeleton">
        <div class="skeleton-line skeleton-line--short"></div>
        <div class="skeleton-line mt-2"></div>
      </div>
    </div>

    <div class="mb-3">
      <button type="button" @click="consultSensors" class="btn-primary btn-press" :disabled="consultLoading">
        <span v-if="consultLoading" class="spinner-inline"></span>
        <span v-if="consultLoading">Consultando…</span>
        <span v-else>Consultar batería y sensores</span>
      </button>
    </div>
    <div class="mb-4" :class="{ 'battery-track--pulse': consultLoading }">
      <p class="text-sm font-medium label-muted mb-2">Nivel de batería</p>
      <div class="battery-track">
        <div
          class="battery-fill"
          :style="{ width: batteryLevel + '%' }"
        ></div>
      </div>
    </div>

    <!-- Resultados en tiempo real (logs) -->
    <div class="results-box mb-4">
      <h3 class="results-box__title">Resultados en tiempo real</h3>
      <div v-if="consultLogs.length">
        <ul class="results-list list-disc pl-5 space-y-0 results-list--logs">
          <li v-for="(log, index) in consultLogs" :key="index" :class="logClass(log)" class="sim-step log-line">
            {{ log.text }}
          </li>
        </ul>
      </div>
      <p v-else class="results-box__empty">Pulsa «Consultar batería y sensores» para ver el flujo (conexión → getBatteryPercentage → sensores).</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
      <div
        v-for="sensor in sensorStatuses"
        :key="sensor.name"
        class="sensor-card"
        :class="{ 'sensor-card--updated': sensor.justUpdated }"
      >
        <p class="font-medium sensor-card__name">{{ sensor.name }}</p>
        <p :class="sensor.active ? 'status-active' : 'status-inactive'" class="text-sm mt-1">
          {{ sensor.active ? 'Activo' : 'Inactivo' }}
        </p>
      </div>
    </div>
  </div>
</template>
  
  <script>
  export default {
    name: "BatterySensorData",
    data() {
      return {
        batteryLevel: 75,
        consultLoading: false,
        consultStep: '',
        consultLogs: [],
        sensorStatuses: [
          { name: 'IMU (9 DoF)', active: true, justUpdated: false },
          { name: 'Odometría', active: true, justUpdated: false },
          { name: 'Color / Luz', active: false, justUpdated: false },
        ],
      };
    },
    methods: {
      pushLog(text, type = 'pending') {
        this.consultLogs.push({ text, type });
      },
      logClass(log) {
        if (log.type === 'success') return 'text-green-600 dark:text-green-400';
        if (log.type === 'error') return 'text-red-600 dark:text-red-400';
        return 'text-gray-600 dark:text-gray-400';
      },
      async consultSensors() {
        this.consultLoading = true;
        this.consultLogs = [];
        this.consultStep = 'Conectando al robot…';
        this.pushLog('[1/4] Conectando al robot (driver/API)…', 'pending');
        await new Promise((r) => setTimeout(r, 280));
        this.pushLog('[1/4] Conexión establecida.', 'success');
        this.consultStep = 'Leyendo getBatteryPercentage…';
        this.pushLog('[2/4] Leyendo getBatteryPercentage (driver RVR)…', 'pending');
        await new Promise((r) => setTimeout(r, 320));
        this.batteryLevel = Math.min(100, this.batteryLevel + (Math.random() * 10 - 3) | 0);
        this.batteryLevel = Math.max(5, this.batteryLevel);
        this.pushLog(`[2/4] Batería: ${this.batteryLevel}%.`, 'success');
        this.consultStep = 'Consultando sensores (IMU, odometría)…';
        this.pushLog('[3/4] Consultando sensores (IMU, odometría, color/luz)…', 'pending');
        await new Promise((r) => setTimeout(r, 250));
        this.sensorStatuses = this.sensorStatuses.map((s, i) => ({
          ...s,
          active: i < 2 || Math.random() > 0.4,
          justUpdated: true,
        }));
        this.pushLog('[3/4] Sensores actualizados.', 'success');
        this.consultStep = 'Listo.';
        this.pushLog('[4/4] Consulta completada. Datos mostrados arriba.', 'success');
        this.consultLoading = false;
        this.consultStep = '';
        setTimeout(() => {
          this.sensorStatuses = this.sensorStatuses.map(s => ({ ...s, justUpdated: false }));
        }, 600);
      },
    },
  };
</script>

<style scoped>
.card-panel--relative {
  position: relative;
}
</style>
