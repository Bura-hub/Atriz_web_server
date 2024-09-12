<template>
  <div class="login-wrapper">
    <div class="login-container">
      <h1 class="app-title">Atriz RVR</h1>
      <h2>Sign In</h2>
      <form @submit.prevent="login">
        <div class="input-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" placeholder="Enter your username" required />
        </div>
        <div class="input-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" placeholder="Enter your password" required />
        </div>
        <button type="submit" class="btn">Login</button>
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from '../utils/axios';
import qs from 'qs';

export default {
  data() {
    return {
      username: '',
      password: '',
      error: null
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/login', qs.stringify({
          username: this.username,
          password: this.password
        }), {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });

        const accessToken = response.data.access_token;
        localStorage.setItem('access_token', accessToken);

        // Decodificar el token para obtener el nombre completo del usuario
        const userInfo = JSON.parse(atob(accessToken.split('.')[1]));
        localStorage.setItem('full_name', userInfo.full_name);

        this.$router.push('/'); // Redirige al dashboard
      } catch (error) {
        this.error = 'Login failed. Please check your username and password.';
        console.error('Login failed:', error);
      }
    }
  }
};
</script>

<style scoped>
/* Flexbox for centering and responsiveness */
.login-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: url('../assets/login-background.jpg') no-repeat center center fixed;
  background-size: cover;
}

/* Styled container for the login box */
.login-container {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

/* New App Title style */
.app-title {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #007bff;
  font-family: 'Roboto', sans-serif;
}

/* Enhancing the form header */
h2 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #333;
  font-family: 'Roboto', sans-serif;
}

/* Input group styles for consistency */
.input-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

label {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  background-color: #fafafa;
  transition: border-color 0.3s ease;
}

input:focus {
  border-color: #007bff;
  outline: none;
}

/* Button with hover and transition effects */
.btn {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #0056b3;
}

/* Error message styling */
.error-message {
  margin-top: 1rem;
  color: #d9534f;
  font-weight: bold;
}
</style>