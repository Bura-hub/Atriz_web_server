<template>
  <footer class="bg-gray-800 p-6 mt-6 rounded-lg flex flex-col md:flex-row justify-between items-center">
    <div class="text-center md:text-left">
      <p class="text-lg">Timer:</p>
      <p class="text-2xl font-bold">{{ timer }}</p>
    </div>
    <div class="mt-4 md:mt-0">
      <button class="bg-gray-700 p-4 rounded-full text-2xl" @click="refreshTimer">
        <i class="fas fa-sync-alt"></i>
      </button>
    </div>
  </footer>
</template>

<script>
export default {
  name: "AppFooter",
  data() {
    return {
      timer: this.getCurrentTime(),
    };
  },
  methods: {
    getCurrentTime() {
      const now = new Date();
      return now.toTimeString().slice(0, 8); // Formato HH:MM:SS
    },
    updateTimer() {
      this.timer = this.getCurrentTime();
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
/* Estilos opcionales para el footer */
</style>
