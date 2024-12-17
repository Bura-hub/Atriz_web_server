<template>
  <div class="bg-gray-800 p-6 rounded-lg">
    <h2 class="text-xl md:text-2xl mb-4">Panel de control de robots</h2>

    <!-- Botón para cargar lista de experimentos -->
    <div class="mb-4">
      <button @click="fetchScripts" class="bg-blue-500 p-3 rounded-md">
        Leer experimentos
      </button>
    </div>

    <!-- Selector de experimentos -->
    <div class="mb-4" v-if="scripts.length">
      <label for="experiment" class="block mb-2">Seleccionar Experimento:</label>
      <select id="experiment" v-model="selectedScript" class="w-full p-2 rounded-md bg-gray-700">
        <option v-for="script in scripts" :key="script" :value="script">
          {{ script }}
        </option>
      </select>
    </div>

    <!-- Panel de robots -->
    <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
      <div v-for="robot in robots" :key="robot.id" class="bg-gray-700 p-4 rounded-md">
        <img :src="robot.imgSrc" :alt="`Robot ${robot.name}`" class="mb-2 mx-auto" />
        <p class="text-center">{{ robot.name }}</p>
      </div>
    </div>

    <!-- Botones de control -->
    <div class="flex flex-col md:flex-row justify-between">
      <button @click="startExperiment" class="bg-green-500 p-3 rounded-md mb-2 md:mb-0">
        Iniciar
      </button>
      <button @click="stopExperiment" class="bg-red-500 p-3 rounded-md mb-2 md:mb-0">
        Detener
      </button>
    </div>

    <!-- Área de visualización de resultados -->
    <div class="mt-4 bg-gray-700 p-4 rounded-md">
      <h3 class="text-lg">Resultados en tiempo real:</h3>
      <div v-if="results.length">
        <ul>
          <li v-for="(result, index) in results" :key="index" class="text-white">
            {{ result }}
          </li>
        </ul>
      </div>
      <p v-else class="text-gray-400">Aún no hay resultados para mostrar.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "RobotDashboard",
  data() {
    return {
      robots: [
        { id: 1, name: "Robot 1", imgSrc: "https://placehold.co/100x100" },
        { id: 2, name: "Robot 2", imgSrc: "https://placehold.co/100x100" },
        { id: 3, name: "Robot 3", imgSrc: "https://placehold.co/100x100" },
      ],
      scripts: [],
      selectedScript: null,
      results: [],
    };
  },
  methods: {
    async fetchScripts() {
      try {
        const response = await fetch("/api/list-scripts");
        const data = await response.json();
        this.scripts = data.scripts["10.20.50.29"] || []; // Cambia según el host requerido
        if (this.scripts.length === 0) {
          alert("No se encontraron experimentos disponibles.");
        }
      } catch (error) {
        console.error("Error al obtener los scripts:", error);
        alert("No se pudieron cargar los experimentos.");
      }
    },
    async startExperiment() {
      if (!this.selectedScript) {
        alert("Selecciona un experimento primero.");
        return;
      }
      try {
        const response = await fetch(`/api/start-experiment`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ script_name: this.selectedScript }),
        });
        const data = await response.json();
        if (data.status === "success") {
          alert("Experimento iniciado correctamente.");
        } else {
          alert(`Error al iniciar el experimento: ${data.details}`);
        }
      } catch (error) {
        console.error("Error al iniciar el experimento:", error);
        alert("Ejecutado.");
      }
    },
    async stopExperiment() {
      if (!this.selectedScript) {
        alert("Selecciona un experimento para detener.");
        return;
      }
      try {
        const response = await fetch(`/api/stop-script`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ script_name: this.selectedScript }), // Enviar el nombre del script
        });
        const data = await response.json();
        if (data.status === "success") {
          alert("Experimento detenido correctamente.");
        } else {
          alert(`Error al detener el experimento: ${data.details}`);
        }
      } catch (error) {
        console.error("Error al detener el experimento:", error);
        alert("Hubo un error al intentar detener el experimento.");
      }
    },
  },
};
</script>

<style scoped>
.bg-gray-800 {
  background-color: #2d3748;
}
.bg-gray-700 {
  background-color: #4a5568;
}
</style>
