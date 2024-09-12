<template>
  <div class="bg-gray-900 text-white font-sans">
    <div class="container mx-auto p-4">
      <AppHeader />
      <button @click="logout" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
        Logout
      </button>
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
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
/* Estilos del Dashboard */
</style>
