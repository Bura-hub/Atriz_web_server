<template>
  <div class="app-root">
    <router-view />
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
  min-height: 100vh;
  background: linear-gradient(165deg, var(--bg-base) 0%, var(--bg-base-alt) 45%, var(--bg-surface) 100%);
}
</style>
