<template>
  <header class="flex flex-col md:flex-row justify-between items-center mb-6">
    <div class="text-center md:text-left">
      <h1 class="text-2xl md:text-3xl font-bold">
        SWARM ROBOTICS LABORATORY
      </h1>
      <p class="text-gray-400">Remote Control Interface</p>
    </div>
    <div class="mt-4 md:mt-0">
      <button @click="logout" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
        Logout
      </button>
    </div>
  </header>
</template>

<script>
export default {
  name: "AppHeader",
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('full_name');
      this.$router.push('/login');
    }
  }
};
</script>