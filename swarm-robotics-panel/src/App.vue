<template>
  <div>
    <!-- Mostrar la vista principal si el usuario está autenticado -->
    <div v-if="isAuthenticated" class="bg-gray-900 text-white font-sans">
      <div class="container mx-auto p-4">
        <AppHeader />
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
    <!-- Mostrar la página de inicio de sesión si el usuario no está autenticado -->
    <div v-else>
      <LoginPage />
    </div>
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue';
import VideoStream from './components/VideoStream.vue';
import RobotDashboard from './components/RobotDashboard.vue';
import BatterySensorData from './components/BatterySensorData.vue';
import PythonCode from './components/PythonCode.vue';
import ExperimentResults from './components/ExperimentResults.vue';
import AppFooter from './components/AppFooter.vue';
import LoginPage from './components/LoginPage.vue';

export default {
  name: "App",
  components: {
    AppHeader,
    VideoStream,
    RobotDashboard,
    BatterySensorData,
    PythonCode,
    ExperimentResults,
    AppFooter,
    LoginPage
  },
  computed: {
    isAuthenticated() {
      // Comprobar si hay un token de acceso en el almacenamiento local
      return !!localStorage.getItem('access_token');
    }
  }
};
</script>

<style scoped>
/* Añade estilos generales aquí si es necesario */
</style>
