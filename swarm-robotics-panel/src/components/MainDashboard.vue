<template>
  <div class="dashboard-container">
    <h1>Main Dashboard</h1>
    <p>Welcome to the dashboard!</p>
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
export default {
  name: 'MainDashboard',
  methods: {
    logout() {
      localStorage.removeItem('access_token');
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #0056b3;
}
</style>
