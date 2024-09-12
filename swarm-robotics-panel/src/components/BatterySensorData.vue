<template>
    <div class="bg-gray-800 p-6 rounded-lg">
      <h2 class="text-xl md:text-2xl mb-4">Battery & Sensor Data</h2>
      <div class="mb-4">
        <p class="mb-2">Battery Level</p>
        <div class="bg-gray-700 w-full h-4 rounded-full overflow-hidden">
          <div class="bg-blue-500 h-full" :style="{ width: batteryLevel + '%' }"></div>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="sensor in sensorStatuses" :key="sensor.name" class="bg-gray-700 p-4 rounded-md">
          <p>{{ sensor.name }}</p>
          <p :class="sensor.active ? 'text-green-400' : 'text-red-400'">
            {{ sensor.active ? 'Active' : 'Inactive' }}
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
  