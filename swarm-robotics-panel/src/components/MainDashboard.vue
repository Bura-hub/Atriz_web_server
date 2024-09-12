<template>
  <div class="bg-gray-900 text-white font-sans">
    <div class="container mx-auto p-4">
      <AppHeader />
      <p v-if="fullName" class="welcome-message">
        <span>Bienvenido, </span>
        <span class="animated-name">{{ fullName }}</span>
      </p>
      <VideoStream />
      <div class="my-8"></div>
      <section class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <RobotDashboard />
        <BatterySensorData />
      </section>
      <PythonCode />
      <ExperimentResults />
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

export default {
  name: 'MainDashboard',
  components: {
    AppHeader,
    VideoStream,
    RobotDashboard,
    BatterySensorData,
    PythonCode,
    ExperimentResults,
    AppFooter
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
  font-family: 'Roboto', sans-serif; /* Asegúrate de que la fuente esté disponible */
  font-size: 1.5rem;
  font-weight: 700; /* Grosor de fuente más fuerte */
  color: #ffffff;
  margin-bottom: 1rem;
}

/* Estilo estático para "Bienvenido," */
.welcome-message span:first-of-type {
  color: #ffffff; /* Color blanco */
}

/* Nombre con animación de cambio de color */
.animated-name {
  font-family: 'Roboto', sans-serif; /* Asegúrate de que la fuente esté disponible */
  font-size: 1.5rem;
  font-weight: 700; /* Grosor de fuente más fuerte */
  color: #ffffff;
  animation: colorChange 3s infinite; /* Aplicar la animación de cambio de color */
}

/* Animación de cambio de color */
@keyframes colorChange {
  0% {
    color: #0b56ac; /* Color inicial blanco */
  }
  50% {
    color: #ffffff; /* Color intermedio amarillo */
  }
  100% {
    color: #0b56ac; /* Color final blanco */
  }
}
</style>