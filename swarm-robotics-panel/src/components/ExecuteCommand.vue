<template>
  <section class="card-panel">
    <h2 class="section-title">Ejecutar comando en Raspberry Pi</h2>

    <form @submit.prevent="executeCommand" class="space-y-4">
      <div>
        <label class="block text-sm font-medium label-muted mb-1">IP del robot</label>
        <input v-model="robotIp" type="text" placeholder="Ej: 192.168.20.39" required class="input-field" />
      </div>
      <div>
        <label class="block text-sm font-medium label-muted mb-1">Comando</label>
        <input v-model="command" type="text" placeholder="Comando a ejecutar" required class="input-field" />
      </div>
      <div class="flex flex-wrap gap-2">
        <button type="submit" class="btn-primary btn-press" :disabled="execLoading">
          <span v-if="execLoading" class="spinner-inline"></span>
          <span v-if="execLoading">Ejecutando…</span>
          <span v-else>Ejecutar comando</span>
        </button>
        <button type="button" @click="stopCommand" :disabled="!robotIp || execLoading" class="btn-danger btn-press">Detener</button>
      </div>
    </form>

    <p v-if="execStep" class="text-sm label-muted mb-2 sim-step">{{ execStep }}</p>

    <section v-if="commandOutput" class="mt-4">
      <h3 class="results-box__title">Salida del comando</h3>
      <pre class="output-block">{{ commandOutput }}</pre>
    </section>
  </section>
</template>
  
  <script>
  import axios from '../utils/axios';
  import qs from 'qs';

  export default {
    data() {
      return {
        robotIp: '',
        command: '',
        commandOutput: '',
        execLoading: false,
        execStep: '',
      };
    },
    methods: {
      async executeCommand() {
        this.execLoading = true;
        this.execStep = 'Conectando por SSH al robot…';
        await new Promise((r) => setTimeout(r, 350));
        this.execStep = 'Ejecutando comando en la Raspberry Pi…';
        try {
          const response = await axios.post('/robots/execute/', qs.stringify({
            robot_ip: this.robotIp,
            command: this.command
          }), {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
          });
          const data = response.data;
          this.execStep = 'Comando ejecutado. Recibiendo salida.';
          this.commandOutput = data.result != null ? data.result : (data.detail || JSON.stringify(data));
        } catch (error) {
          console.error('Error ejecutando el comando:', error);
          this.commandOutput = error.response?.data?.detail || error.message || 'Error al ejecutar el comando.';
        } finally {
          this.execLoading = false;
          this.execStep = '';
        }
      },
      async stopCommand() {
        try {
          const response = await axios.post('/robots/stop/', qs.stringify({ robot_ip: this.robotIp }), {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
          });
          const data = response.data;
          this.commandOutput = data.message != null ? data.message : (data.detail || JSON.stringify(data));
        } catch (error) {
          console.error('Error deteniendo el comando:', error);
          this.commandOutput = error.response?.data?.detail || error.message || 'Error al detener el comando.';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .button-container {
    display: flex;
    gap: 10px; /* Espacio entre botones */
  }
  </style>
  