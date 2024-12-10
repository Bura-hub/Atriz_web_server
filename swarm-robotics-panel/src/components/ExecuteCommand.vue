<template>
    <section class="bg-gray-800 p-6 rounded-lg mt-6 space-y-6">
      <h2 class="text-xl md:text-2xl mb-4">Ejecutar Comando en Raspberry Pi</h2>
  
      <!-- Formulario para ingresar IP y comando -->
      <form @submit.prevent="executeCommand" class="space-y-4">
        <div class="mb-4">
          <label class="block mb-2">IP del Robot</label>
          <input v-model="robotIp" type="text" placeholder="Ej: 192.168.20.39" required class="bg-gray-700 w-full p-2 rounded-md border border-gray-600" />
        </div>
  
        <div class="mb-4">
          <label class="block mb-2">Comando</label>
          <input v-model="command" type="text" placeholder="Comando a ejecutar" required class="bg-gray-700 w-full p-2 rounded-md border border-gray-600" />
        </div>
  
        <div class="button-container flex gap-4">
          <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md">Ejecutar Comando</button>
          <button type="button" @click="stopCommand" :disabled="!robotIp" class="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-md">Detener</button>
        </div>
      </form>
  
      <!-- Mostrar resultado de la ejecución -->
      <section v-if="commandOutput" class="output-block mt-4">
        <h3 class="text-xl">Salida del Comando:</h3>
        <pre class="bg-gray-700 p-4 rounded-md text-white">{{ commandOutput }}</pre>
      </section>
    </section>
  </template>
  
  <script>
  export default {
    data() {
      return {
        robotIp: '',
        command: '',
        commandOutput: ''
      };
    },
    methods: {
      async executeCommand() {
        try {
          const response = await fetch('/api/robots/execute/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
              robot_ip: this.robotIp,
              command: this.command
            })
          });
          const data = await response.json();
          this.commandOutput = data.result;
        } catch (error) {
          console.error('Error ejecutando el comando:', error);
        }
      },
      async stopCommand() {
        try {
          const response = await fetch('/api/robots/stop/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
              robot_ip: this.robotIp
            })
          });
          const data = await response.json();
          this.commandOutput = data.message;
        } catch (error) {
          console.error('Error deteniendo el comando:', error);
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
  