<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <label for="username">Username</label>
      <input type="text" id="username" v-model="username" required />
      <label for="password">Password</label>
      <input type="password" id="password" v-model="password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from '../utils/axios';
import qs from 'qs'; // Asegúrate de instalar qs

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        // Configura los datos del formulario en el formato correcto
        const response = await axios.post('/login', qs.stringify({
          username: this.username,
          password: this.password
        }), {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });
        localStorage.setItem('access_token', response.data.access_token);
        this.$router.push('/');
      } catch (error) {
        console.error('Login failed:', error);
        alert('Login failed. Please check your username and password.');
      }
    }
  }
};
</script>

<style scoped>
/* Estilos para el formulario de inicio de sesión */
.login-container {
  width: 300px;
  margin: auto;
  padding: 20px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
form {
  display: flex;
  flex-direction: column;
}
label {
  margin: 10px 0 5px;
}
input {
  margin-bottom: 15px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>
