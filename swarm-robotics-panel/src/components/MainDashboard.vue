<template>
  <div class="bg-gray-900 text-white font-sans">
    <div class="container mx-auto p-4">
      <AppHeader />
      <p v-if="fullName" class="welcome-message">
        <span>Bienvenido, </span>
        <span class="animated-name">{{ fullName }}</span>
      </p>

      <!-- Stream de video -->
      <VideoStream />
      <div class="my-8"></div>

      <!-- Sección de dashboards y datos -->
      <section class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <RobotDashboard />
        <BatterySensorData />
      </section>

      <!-- Sección para ejecutar comandos en la Raspberry Pi -->
      <section class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <PythonCode />
        <ExecuteCommand /> <!-- Aquí integramos el componente de ejecución de comandos -->
      </section>

      <!-- Código Python y Resultados de Experimentos -->
      <ExperimentResults />

      <!-- Footer de la aplicación -->
      <AppFooter />
    </div>
  </div>
</template>

<script>
import AppHeader from './AppHeader.vue';
import VideoStream from './VideoStream.vue';
import RobotDashboard from './RobotDashboard.vue';
import BatterySensorData from './BatterySensorData.vue';
import PythonCode from './PythonCode.vue';
import ExperimentResults from './ExperimentResults.vue';
import AppFooter from './AppFooter.vue';
import ExecuteCommand from './ExecuteCommand.vue'; // Importa el nuevo componente

export default {
  name: 'MainDashboard',
  components: {
    AppHeader,
    VideoStream,
    RobotDashboard,
    BatterySensorData,
    PythonCode,
    ExperimentResults,
    AppFooter,
    ExecuteCommand // Registra el nuevo componente
  },
  data() {
    return {
      fullName: localStorage.getItem('full_name') || 'Unknown User'
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('full_name');
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
/* Estilos del Dashboard */
.welcome-message {
  font-family: 'Roboto', sans-serif; 
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 1rem;
}

/* Estilo estático para "Bienvenido," */
.welcome-message span:first-of-type {
  color: #ffffff;
}

/* Nombre con animación de cambio de color */
.animated-name {
  font-family: 'Roboto', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  animation: colorChange 3s infinite;
}

/* Animación de cambio de color */
@keyframes colorChange {
  0% {
    color: #0b56ac;
  }
  50% {
    color: #ffffff;
  }
  100% {
    color: #0b56ac;
  }
}
</style>
