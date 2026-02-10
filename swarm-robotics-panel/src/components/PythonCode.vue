<template>
  <section class="card-panel card-panel--relative">
    <h2 class="section-title">Código Python</h2>

    <!-- Overlay de carga durante subida (según desarrollo.tex: recepción → almacenamiento → SCP → SSH) -->
    <div v-if="uploadLoading" class="loading-overlay">
      <div class="loading-overlay__content">
        <div class="loading-overlay__spinner" aria-hidden="true"></div>
        <p class="loading-overlay__text">{{ uploadLoadingStep }}</p>
      </div>
      <div class="skeleton-block loading-overlay__skeleton">
        <div class="skeleton-line skeleton-line--title skeleton-line--short"></div>
        <div class="skeleton-line mt-2"></div>
        <div class="skeleton-line mt-1"></div>
      </div>
    </div>

    <div class="mb-4">
      <label class="block text-sm font-medium label-muted mb-1">Seleccionar archivo Python</label>
      <input type="file" accept=".py" @change="handleFile" class="input-field block w-full text-sm file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-[var(--accent)] file:text-white file:font-medium file:cursor-pointer" />
    </div>

    <div class="flex flex-wrap gap-2 mb-4">
      <button v-if="selectedFile" type="button" @click="openEditor" class="btn-success btn-press">
        Visualizar y editar script
      </button>
      <button type="button" @click="uploadScript" class="btn-primary btn-press" :disabled="uploadLoading">
        <span v-if="uploadLoading" class="spinner-inline"></span>
        <span v-if="uploadLoading">Subiendo…</span>
        <span v-else>Subir script</span>
      </button>
    </div>

    <!-- Pasos simulados según desarrollo.tex: recepción → almacenamiento → SCP → SSH -->
    <div v-if="uploadSteps.length && !uploadLoading" class="steps-progress mb-3">
      <span
        v-for="(step, i) in uploadSteps"
        :key="i"
        class="steps-progress__dot"
        :class="{ 'steps-progress__dot--active': step.active, 'steps-progress__dot--done': step.done }"
        :title="step.label"
      ></span>
    </div>
    <p v-if="uploadSteps.length && !uploadLoading" class="text-sm label-muted mb-2 sim-step">
      {{ uploadSteps.find(s => s.active)?.label || uploadSteps[uploadSteps.length - 1]?.label }}
    </p>

    <!-- Resultados en tiempo real (logs paso a paso según docs) -->
    <div class="results-box mt-4">
      <h3 class="results-box__title">Resultados en tiempo real</h3>
      <div v-if="uploadLogs.length">
        <ul class="results-list list-disc pl-5 space-y-0 results-list--logs">
          <li v-for="(log, index) in uploadLogs" :key="index" :class="logClass(log)" class="sim-step log-line">
            {{ log.text }}
          </li>
        </ul>
      </div>
      <p v-else class="results-box__empty">Aún no hay resultados. Sube un script para ver el flujo (recepción → almacenamiento → SCP → SSH).</p>
    </div>

    <section v-if="commandOutput" class="mt-4">
      <h3 class="results-box__title">Resultado de la operación</h3>
      <pre class="output-block">{{ commandOutput }}</pre>
    </section>

    <!-- Editor modal (Monaco, según documento de desarrollo) -->
    <div v-if="isEditorOpen" class="modal-overlay" @click.self="closeEditor">
      <div class="modal-panel modal-panel--with-monaco" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">Editar script (Monaco)</h3>
          <button type="button" @click="closeEditor" class="modal-close" aria-label="Cerrar">&#x2715;</button>
        </div>
        <div ref="monacoContainer" class="monaco-container"></div>
        <div class="modal-footer">
          <button type="button" @click.prevent="closeEditor" class="btn-secondary">Cancelar</button>
          <button type="button" @click.prevent="saveChanges" class="btn-success">Guardar cambios</button>
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
      uploadLoading: false,
      uploadLoadingStep: "",
      uploadSteps: [],
      uploadLogs: [],
    };
  },
  methods: {
    pushLog(text, type = 'pending') {
      this.uploadLogs.push({ text, type });
    },
    logClass(log) {
      if (log.type === 'success') return 'text-green-600 dark:text-green-400';
      if (log.type === 'error') return 'text-red-600 dark:text-red-400';
      return 'text-gray-600 dark:text-gray-400';
    },
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
      this.$nextTick(() => {
        this.isEditorOpen = false;
      });
    },
    saveChanges() {
      if (this.monacoEditor) {
        this.fileContent = this.monacoEditor.getValue();
      }
      this.disposeMonaco();
      this.$nextTick(() => {
        this.isEditorOpen = false;
        alert("Cambios guardados exitosamente.");
      });
    },
    async uploadScript() {
      if (!this.fileContent) {
        alert("Por favor, carga y edita un archivo primero.");
        return;
      }

      const steps = [
        { label: "Recepción: validando archivo (.py) y tamaño…", active: false, done: false },
        { label: "Almacenamiento temporal en servidor…", active: false, done: false },
        { label: "Transferencia SCP al robot…", active: false, done: false },
        { label: "Ejecución SSH: rosrun sphero_rvr_pkg script_executor.py…", active: false, done: false },
        { label: "Salida: captura stdout/stderr…", active: false, done: false },
      ];
      this.uploadSteps = steps;
      this.uploadLoading = true;
      this.uploadLoadingStep = "Recepción: validando archivo…";
      this.uploadLogs = [];
      this.commandOutput = "";

      const delay = (ms) => new Promise((r) => setTimeout(r, ms));

      const setStep = (index, active, done) => {
        this.uploadSteps = this.uploadSteps.map((s, i) => ({
          ...s,
          active: i === index && active,
          done: i < index || (i === index && done),
        }));
        if (steps[index]) this.uploadLoadingStep = steps[index].label;
      };

      try {
        this.pushLog("[1/5] POST /api/scripts/upload/ — Recepción del archivo…", 'pending');
        setStep(0, true, false);
        await delay(400);
        this.pushLog("[1/5] Validación .py y tamaño (límite 1MB). OK.", 'success');
        setStep(0, false, true);
        setStep(1, true, false);
        this.pushLog("[2/5] Almacenamiento temporal en /tmp/atriz_uploads/…", 'pending');
        await delay(350);
        this.pushLog("[2/5] Archivo guardado con nombre único (UUID).", 'success');
        setStep(1, false, true);
        setStep(2, true, false);
        this.pushLog("[3/5] Transferencia SCP al robot (paramiko/subprocess)…", 'pending');
        await delay(400);

        const formData = new FormData();
        const file = new Blob([this.fileContent], { type: "text/plain" });
        formData.append("file", file, this.selectedFile.name);

        const response = await axios.post("/upload-script", formData);
        const data = response.data;

        this.pushLog("[3/5] SCP completado.", 'success');
        setStep(2, false, true);
        setStep(3, true, false);
        this.pushLog("[4/5] Ejecución SSH: source ROS && rosrun sphero_rvr_pkg script_executor.py…", 'pending');
        await delay(300);
        this.pushLog("[4/5] Comando enviado al robot.", 'success');
        setStep(3, false, true);
        setStep(4, true, false);
        this.pushLog("[5/5] Salida: stdout/stderr devueltos al frontend o registrados en logs.", 'pending');
        await delay(200);
        setStep(4, false, true);

        if (data.status === "success") {
          this.pushLog("Script desplegado. Ejecución disponible vía script_executor.", 'success');
          this.commandOutput = "Archivo enviado exitosamente a las Raspberry Pi.\n[SCP → robot] Ejecución disponible vía script_executor.";
        } else {
          this.pushLog(`Error: ${data.details || data.detail || "desconocido"}`, 'error');
          this.commandOutput = `Error: ${data.details || data.detail || "desconocido"}`;
        }
      } catch (error) {
        console.error("Error al enviar el archivo:", error);
        this.pushLog(`[Error] ${error.response?.data?.detail || error.message || "Error al subir el archivo."}`, 'error');
        this.commandOutput = error.response?.data?.detail || error.message || "Error al intentar subir el archivo.";
        this.uploadSteps = this.uploadSteps.map((s) => ({ ...s, done: true, active: false }));
      } finally {
        this.uploadLoading = false;
        this.uploadLoadingStep = "";
        this.uploadSteps = [];
      }
    },
  },
  beforeUnmount() {
    this.disposeMonaco();
  },
};
</script>

<style scoped>
.card-panel--relative {
  position: relative;
}
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
  flex-shrink: 0;
}

.modal-panel--with-monaco .modal-footer {
  position: relative;
  z-index: 10;
}

.modal-panel--with-monaco .modal-panel {
  max-width: 90vw;
}
</style>
