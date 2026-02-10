<template>
  <div class="card-panel">
    <h2 class="section-title">Datos de batería y sensores</h2>
    <div class="mb-4">
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
        sensorStatuses: [
          { name: 'Sensor 1', active: true },
          { name: 'Sensor 2', active: false },
        ],
      };
    },
  };
  </script>
  