<template>
  <section class="bg-gray-800 p-6 rounded-lg mt-6 space-y-6">
    <!-- Título para el editor de código -->
    <h2 class="text-xl md:text-2xl mb-4">Código Python</h2>

    <!-- Editor de Código -->
    <textarea 
      v-model="editableCode"
      @input="updateCode"
      class="w-full h-64 bg-gray-900 text-white p-4 rounded-lg"
      placeholder="Escribe o pega tu código Python aquí..."
    ></textarea>

    <!-- Título para el código interpretado -->
    <h2 class="text-xl md:text-2xl mb-4">Código Interpretado</h2>
    
    <!-- Código Python con resaltado de sintaxis -->
    <section class="bg-gray-800 p-4 rounded-lg">
      <pre class="code-block language-python">
        <code class="language-python" v-html="highlightedCode"></code>
      </pre>
    </section>

    <!-- Input para la IP del robot -->
    <div class="mb-4">
      <label class="block mb-2">IP del Robot</label>
      <input v-model="robotIp" type="text" placeholder="Ej: 192.168.1.100" required class="bg-gray-700 w-full p-2 rounded-md border border-gray-600" />
    </div>

    <!-- Botón para subir y ejecutar script -->
    <section class="space-y-2">
      <button @click="uploadAndExecuteScript" class="bg-blue-500 p-2 rounded-md w-full">
        Subir y Ejecutar Script
      </button>
    </section>

    <!-- Mostrar resultado de la ejecución -->
    <section v-if="commandOutput" class="output-block mt-4">
      <h3 class="text-xl">Salida del Script:</h3>
      <pre class="bg-gray-700 p-4 rounded-md text-white">{{ commandOutput }}</pre>
    </section>
  </section>
</template>

<script>
import Prism from 'prismjs';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css';

export default {
  name: "PythonCode",
  data() {
    return {
      editableCode: '',
      highlightedCode: '',
      robotIp: '',
      commandOutput: '',
    };
  },
  methods: {
    updateCode() {
      this.highlightedCode = Prism.highlight(this.editableCode, Prism.languages.python, 'python');
    },
    async uploadAndExecuteScript() {
      const blob = new Blob([this.editableCode], { type: 'text/plain' });
      const formData = new FormData();
      formData.append('file', blob, 'script.py'); // Nombramos el archivo como 'script.py'
      formData.append('robot_ip', this.robotIp);

      try {
        const response = await fetch('/api/scripts/upload/', {
          method: 'POST',
          body: formData
        });
        const data = await response.json();
        
        if (data.status === 'success') {
          this.commandOutput = data.result;
        } else {
          this.commandOutput = data.detail || 'Error desconocido';
        }
      } catch (error) {
        console.error('Error al subir y ejecutar el script:', error);
      }
    }
  },
  watch: {
    editableCode: 'updateCode'
  },
};
</script>

<style scoped>
/* Sobrescribe los estilos globales aplicados a code y pre */
code[class*="language-"], pre[class*="language-"] {
  color: #ffffff !important; /* Cambia el color del texto */
  background-color: #15181e !important; /* Fondo oscuro */
  text-shadow: none !important; /* Elimina el efecto de sombra de texto */
  font-family: "Fira Code", "Consolas", "Monaco", "Ubuntu Mono", monospace !important;
  font-size: 1em; /* Ajusta el tamaño de fuente */
  line-height: 1.6; /* Ajusta la altura de línea */
  white-space: pre-wrap; /* Permite que el texto se ajuste */
}

.code-block {
  border-radius: 10px;
  color: #ffffff;
  padding: 15px;
  background-color: #00000000; /* Fondo gris oscuro */
}

.output-block {
  background-color: #1a1a1a; /* Fondo oscuro para la salida */
  border-radius: 8px;
}
</style>
