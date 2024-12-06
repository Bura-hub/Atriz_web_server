<template>
    <div class="bg-gray-800 p-6 rounded-lg">
      <h2 class="text-xl md:text-2xl mb-4">Robot Control Dashboard</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
        <div v-for="robot in robots" :key="robot.id" class="bg-gray-700 p-4 rounded-md">
          <img :src="robot.imgSrc" :alt="`Robot ${robot.name}`" class="mb-2 mx-auto" />
          <p class="text-center">{{ robot.name }}</p>
        </div>
      </div>
      <div class="flex flex-col md:flex-row justify-between">
        <button class="bg-green-500 p-3 rounded-md mb-2 md:mb-0">
          Start
        </button>
        <button class="bg-red-500 p-3 rounded-md mb-2 md:mb-0">
          Stop
        </button>
        <button class="bg-blue-500 p-3 rounded-md">
          Reset
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "RobotDashboard",
    data() {
      return {
        robots: [
          { id: 1, name: 'Robot 1', imgSrc: 'https://placehold.co/100x100' },
          { id: 2, name: 'Robot 2', imgSrc: 'https://placehold.co/100x100' },
          { id: 3, name: 'Robot 3', imgSrc: 'https://placehold.co/100x100' },
        ],
      };
    },
  };
  </script>
  