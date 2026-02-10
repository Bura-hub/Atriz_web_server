<template>
  <div class="dashboard">
    <div class="dashboard__inner">
      <AppHeader />
      <div class="welcome-block">
        <p class="welcome-message">
          <span>Bienvenido, </span>
          <span class="welcome-message__name">{{ fullName }}</span>
        </p>
      </div>

      <!-- Manual: Control de experimentos y vídeo -->
      <section class="dashboard-section" aria-labelledby="sec-exp-video">
        <h2 id="sec-exp-video" class="dashboard-section__heading">Control de experimentos y vídeo</h2>
        <div class="grid grid-cols-1 gap-6">
          <VideoStream />
          <RobotDashboard />
        </div>
      </section>

      <!-- Manual: Envío de código a robots y sensores -->
      <section class="dashboard-section" aria-labelledby="sec-codigo-sensores">
        <h2 id="sec-codigo-sensores" class="dashboard-section__heading">Envío de código a robots y sensores</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <PythonCode />
          <ExecuteCommand />
          <BatterySensorData />
        </div>
      </section>

      <!-- Apartado de resultados (manual: respuesta de los prototipos) -->
      <section class="dashboard-section" aria-labelledby="sec-resultados">
        <h2 id="sec-resultados" class="dashboard-section__heading">Resultados</h2>
        <ExperimentResults />
      </section>

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
import ExecuteCommand from './ExecuteCommand.vue';

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
    ExecuteCommand
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
.dashboard {
  @apply text-gray-100 font-sans;
}

.dashboard__inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem 1rem 2rem;
}

@media (min-width: 768px) {
  .dashboard__inner {
    padding: 2rem 1.5rem 3rem;
  }
}

.welcome-block {
  margin-bottom: 1.5rem;
}

.welcome-message {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.welcome-message__name {
  color: var(--accent);
  font-weight: 700;
}

.dashboard-section {
  margin-bottom: 2rem;
}

.dashboard-section__heading {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-default);
}
</style>
