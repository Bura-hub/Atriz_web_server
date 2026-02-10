<template>
  <div class="card-panel">
    <h2 class="section-title">Datos de batería y sensores</h2>
    <p class="text-sm label-muted mb-2">Según el driver: estado de batería (getBatteryPercentage) y sensor streaming (IMU, odometría).</p>
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
        sensorStatuses: [
          { name: 'IMU (9 DoF)', active: true, justUpdated: false },
          { name: 'Odometría', active: true, justUpdated: false },
          { name: 'Color / Luz', active: false, justUpdated: false },
        ],
      };
    },
    methods: {
      async consultSensors() {
        this.consultLoading = true;
        await new Promise((r) => setTimeout(r, 800));
        this.batteryLevel = Math.min(100, this.batteryLevel + (Math.random() * 10 - 3) | 0);
        this.batteryLevel = Math.max(5, this.batteryLevel);
        this.sensorStatuses = this.sensorStatuses.map((s, i) => ({
          ...s,
          active: i < 2 || Math.random() > 0.4,
          justUpdated: true,
        }));
        this.consultLoading = false;
        setTimeout(() => {
          this.sensorStatuses = this.sensorStatuses.map(s => ({ ...s, justUpdated: false }));
        }, 600);
      },
    },
  };
  </script>
  