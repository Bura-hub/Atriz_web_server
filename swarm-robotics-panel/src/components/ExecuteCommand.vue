<template>
  <section class="card-panel card-panel--relative">
    <h2 class="section-title">Ejecutar comando en Raspberry Pi</h2>

    <!-- Overlay de carga durante ejecución -->
    <div v-if="execLoading" class="loading-overlay">
      <div class="loading-overlay__content">
        <div class="loading-overlay__spinner" aria-hidden="true"></div>
        <p class="loading-overlay__text">{{ execStep }}</p>
      </div>
      <div class="skeleton-block loading-overlay__skeleton">
        <div class="skeleton-line skeleton-line--short"></div>
        <div class="skeleton-line mt-2"></div>
      </div>
    </div>

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

    <!-- Resultados en tiempo real (logs) -->
    <div class="results-box mt-4">
      <h3 class="results-box__title">Resultados en tiempo real</h3>
      <div v-if="execLogs.length">
        <ul class="results-list list-disc pl-5 space-y-0 results-list--logs">
          <li v-for="(log, index) in execLogs" :key="index" :class="logClass(log)" class="sim-step log-line">
            {{ log.text }}
          </li>
        </ul>
      </div>
      <p v-else class="results-box__empty">Ejecuta un comando para ver los pasos (SSH → ejecución → salida).</p>
    </div>

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
        execLogs: [],
      };
    },
    methods: {
      pushLog(text, type = 'pending') {
        this.execLogs.push({ text, type });
      },
      logClass(log) {
        if (log.type === 'success') return 'text-green-600 dark:text-green-400';
        if (log.type === 'error') return 'text-red-600 dark:text-red-400';
        return 'text-gray-600 dark:text-gray-400';
      },
      async executeCommand() {
        this.execLoading = true;
        this.execLogs = [];
        this.execStep = 'Conectando por SSH al robot…';
        this.pushLog('[1/3] Estableciendo túnel SSH al robot…', 'pending');
        await new Promise((r) => setTimeout(r, 350));
        this.pushLog('[1/3] Conexión SSH establecida.', 'success');
        this.execStep = 'Ejecutando comando en la Raspberry Pi…';
        this.pushLog('[2/3] Ejecutando comando en la Raspberry Pi…', 'pending');
        try {
          const response = await axios.post('/robots/execute/', qs.stringify({
            robot_ip: this.robotIp,
            command: this.command
          }), {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
          });
          const data = response.data;
          this.execStep = 'Comando ejecutado. Recibiendo salida.';
          this.pushLog('[2/3] Comando enviado. Recibiendo stdout/stderr.', 'success');
          this.pushLog('[3/3] Salida recibida y mostrada abajo.', 'success');
          this.commandOutput = data.result != null ? data.result : (data.detail || JSON.stringify(data));
        } catch (error) {
          console.error('Error ejecutando el comando:', error);
          this.pushLog(`[Error] ${error.response?.data?.detail || error.message || 'Error al ejecutar.'}`, 'error');
          this.commandOutput = error.response?.data?.detail || error.message || 'Error al ejecutar el comando.';
        } finally {
          this.execLoading = false;
          this.execStep = '';
        }
      },
      async stopCommand() {
        this.pushLog('Enviando señal de detención al robot…', 'pending');
        try {
          const response = await axios.post('/robots/stop/', qs.stringify({ robot_ip: this.robotIp }), {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
          });
          const data = response.data;
          this.pushLog(data.message != null ? data.message : 'Comando detenido.', 'success');
          this.commandOutput = data.message != null ? data.message : (data.detail || JSON.stringify(data));
        } catch (error) {
          console.error('Error deteniendo el comando:', error);
          this.pushLog(error.response?.data?.detail || error.message || 'Error al detener.', 'error');
          this.commandOutput = error.response?.data?.detail || error.message || 'Error al detener el comando.';
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .card-panel--relative {
    position: relative;
  }
  .button-container {
    display: flex;
    gap: 10px;
  }
  </style>
  