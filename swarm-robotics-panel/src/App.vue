<template>
  <div class="app-root">
    <router-view v-slot="{ Component }">
      <transition name="session" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
import './assets/styles.css';

export default {
  name: 'App',
};
</script>

<style>
.app-root {
  position: relative;
  min-height: 100vh;
  background: url('./assets/login-background_1.jpg') no-repeat center center fixed;
  background-size: cover;
}

.app-root::before {
  content: '';
  position: fixed;
  inset: 0;
  background: rgba(11, 15, 26, 0.72);
  backdrop-filter: blur(8px);
  z-index: 0;
}

.app-root > * {
  position: relative;
  z-index: 1;
}

/* Animaciones de apertura y cierre de sesión */
.session-enter-active,
.session-leave-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}
.session-leave-to {
  opacity: 0;
  transform: scale(0.98) translateY(-10px);
}
.session-enter-from {
  opacity: 0;
  transform: scale(0.98) translateY(12px);
}
.session-enter-to,
.session-leave-from {
  opacity: 1;
  transform: scale(1) translateY(0);
}
</style>
