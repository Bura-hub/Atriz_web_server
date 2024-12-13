<template>
  <section class="bg-gray-800 p-6 rounded-lg mt-6 space-y-6">
    <!-- Título para el editor de código -->
    <h2 class="text-xl md:text-2xl mb-4">Código Python</h2>

    <!-- Subir archivo desde el sistema local -->
    <div class="mb-4">
      <label class="block mb-2">Seleccionar archivo Python</label>
      <input type="file" @change="handleFile" class="bg-gray-700 w-full p-2 rounded-md border border-gray-600" />
    </div>

    <!-- Botón para previsualizar y editar el archivo -->
    <section class="space-y-2">
      <button v-if="selectedFile" @click="openEditor" class="bg-green-500 p-2 rounded-md w-full">
        Visualizar y Editar Script
      </button>
    </section>

    <!-- Botón para subir y ejecutar script -->
    <section class="space-y-2">
      <button @click="uploadScript" class="bg-blue-500 p-2 rounded-md w-full">
        Subir Script
      </button>
    </section>

    <!-- Mostrar resultado de la ejecución -->
    <section v-if="commandOutput" class="output-block mt-4">
      <h3 class="text-xl">Resultado de la operación:</h3>
      <pre class="bg-gray-700 p-4 rounded-md text-white">{{ commandOutput }}</pre>
    </section>

    <!-- Editor modal -->
    <div v-if="isEditorOpen" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="bg-gray-900 w-11/12 md:w-2/3 lg:w-1/2 rounded-lg shadow-lg overflow-hidden">
        <div class="flex justify-between items-center bg-gray-700 p-4">
          <h3 class="text-lg font-semibold text-white">Editar Script</h3>
          <button @click="closeEditor" class="text-white">&#x2715;</button>
        </div>
        <textarea v-model="fileContent" class="w-full h-96 bg-gray-800 text-white p-4 font-mono"></textarea>
        <div class="flex justify-end p-4">
          <button @click="closeEditor" class="bg-red-500 text-white px-4 py-2 rounded-md mr-2">Cancelar</button>
          <button @click="saveChanges" class="bg-green-500 text-white px-4 py-2 rounded-md">Guardar Cambios</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "PythonCode",
  data() {
    return {
      selectedFile: null,
      fileContent: "",
      commandOutput: "",
      isEditorOpen: false,
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
      if (this.fileContent) {
        this.isEditorOpen = true;
      } else {
        alert("Por favor, selecciona un archivo primero.");
      }
    },
    closeEditor() {
      this.isEditorOpen = false;
    },
    saveChanges() {
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
        const response = await fetch("/api/upload-script", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();

        if (data.status === "success") {
          this.commandOutput = "Archivo enviado exitosamente a las Raspberry Pi.";
        } else {
          this.commandOutput = `Error: ${data.details}`;
        }
      } catch (error) {
        console.error("Error al enviar el archivo:", error);
        this.commandOutput = "Error al intentar subir el archivo.";
      }
    },
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
</style>
