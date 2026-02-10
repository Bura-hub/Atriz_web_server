<template>
  <section class="card-panel">
    <h2 class="section-title">Código Python</h2>

    <div class="mb-4">
      <label class="block text-sm font-medium label-muted mb-1">Seleccionar archivo Python</label>
      <input type="file" accept=".py" @change="handleFile" class="input-field block w-full text-sm file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-[var(--accent)] file:text-white file:font-medium file:cursor-pointer" />
    </div>

    <div class="flex flex-wrap gap-2 mb-4">
      <button v-if="selectedFile" type="button" @click="openEditor" class="btn-success">
        Visualizar y editar script
      </button>
      <button type="button" @click="uploadScript" class="btn-primary">
        Subir script
      </button>
    </div>

    <section v-if="commandOutput" class="mt-4">
      <h3 class="results-box__title">Resultado de la operación</h3>
      <pre class="output-block">{{ commandOutput }}</pre>
    </section>

    <!-- Editor modal (Monaco, según documento de desarrollo) -->
    <div v-if="isEditorOpen" class="modal-overlay" @click.self="closeEditor">
      <div class="modal-panel modal-panel--with-monaco">
        <div class="modal-header">
          <h3 class="modal-title">Editar script (Monaco)</h3>
          <button type="button" @click="closeEditor" class="modal-close" aria-label="Cerrar">&#x2715;</button>
        </div>
        <div ref="monacoContainer" class="monaco-container"></div>
        <div class="modal-footer">
          <button type="button" @click="closeEditor" class="btn-secondary">Cancelar</button>
          <button type="button" @click="saveChanges" class="btn-success">Guardar cambios</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from '../utils/axios';
import * as monaco from 'monaco-editor';

export default {
  name: "PythonCode",
  data() {
    return {
      selectedFile: null,
      fileContent: "",
      commandOutput: "",
      isEditorOpen: false,
      monacoEditor: null,
    };
  },
  methods: {
    handleFile(event) {
      this.selectedFile = event.target.files[0];
      this.readFileContent();
    },
    readFileContent() {
      if (this.selectedFile) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.fileContent = e.target.result;
        };
        reader.readAsText(this.selectedFile);
      }
    },
    openEditor() {
      if (!this.selectedFile) {
        alert("Por favor, selecciona un archivo primero.");
        return;
      }
      this.isEditorOpen = true;
      this.$nextTick(() => this.initMonaco());
    },
    initMonaco() {
      const container = this.$refs.monacoContainer;
      if (!container || this.monacoEditor) return;
      this.monacoEditor = monaco.editor.create(container, {
        value: this.fileContent,
        language: 'python',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 14,
        scrollBeyondLastLine: false,
      });
    },
    disposeMonaco() {
      if (this.monacoEditor) {
        this.monacoEditor.dispose();
        this.monacoEditor = null;
      }
    },
    closeEditor() {
      this.disposeMonaco();
      this.isEditorOpen = false;
    },
    saveChanges() {
      if (this.monacoEditor) {
        this.fileContent = this.monacoEditor.getValue();
      }
      this.disposeMonaco();
      this.isEditorOpen = false;
      alert("Cambios guardados exitosamente.");
    },
    async uploadScript() {
      if (!this.fileContent) {
        alert("Por favor, carga y edita un archivo primero.");
        return;
      }

      const formData = new FormData();
      const file = new Blob([this.fileContent], { type: "text/plain" });
      formData.append("file", file, this.selectedFile.name);

      try {
        const response = await axios.post("/upload-script", formData);
        const data = response.data;

        if (data.status === "success") {
          this.commandOutput = "Archivo enviado exitosamente a las Raspberry Pi.";
        } else {
          this.commandOutput = `Error: ${data.details || data.detail || "desconocido"}`;
        }
      } catch (error) {
        console.error("Error al enviar el archivo:", error);
        this.commandOutput = error.response?.data?.detail || error.message || "Error al intentar subir el archivo.";
      }
    },
  },
  beforeUnmount() {
    this.disposeMonaco();
  },
};
</script>

<style scoped>
/* Sobrescribe los estilos globales aplicados a code y pre */
code[class*="language-"], pre[class*="language-"] {
  color: #ffffff !important;
  background-color: #15181e !important;
  text-shadow: none !important;
  font-family: "Fira Code", "Consolas", "Monaco", "Ubuntu Mono", monospace !important;
  font-size: 1em;
  line-height: 1.6;
  white-space: pre-wrap;
}

.code-block {
  border-radius: 10px;
  color: #ffffff;
  padding: 15px;
  background-color: #00000000;
}

.output-block {
  background-color: #1a1a1a;
  border-radius: 8px;
}

.monaco-container {
  width: 100%;
  height: 400px;
  min-height: 300px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
}

.modal-panel--with-monaco .modal-panel {
  max-width: 90vw;
}
</style>
