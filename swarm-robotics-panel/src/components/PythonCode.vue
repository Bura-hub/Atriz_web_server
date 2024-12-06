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

    <!-- Botón para subir script -->
    <section class="space-y-2">
      <button @click="uploadScript" class="bg-blue-500 p-2 rounded-md w-full">
        Upload Script
      </button>
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
    };
  },
  methods: {
    uploadScript() {
      // Simular selección de archivo (esto puede abrir el diálogo de archivos del navegador)
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = '.py'; // Aceptar solo archivos Python
      input.click(); // Simular el clic para abrir el selector de archivos

      input.onchange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.editableCode = e.target.result;
            this.updateCode(); // Resaltar el código cargado
          };
          reader.readAsText(selectedFile);
        }
      };
    },
    updateCode() {
      this.highlightedCode = Prism.highlight(this.editableCode, Prism.languages.python, 'python');
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
</style>
