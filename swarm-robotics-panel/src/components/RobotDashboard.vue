<template>
  <div class="card-panel">
    <h2 class="section-title">Panel de control de robots</h2>

    <!-- Botón para cargar lista de experimentos -->
    <div class="mb-4">
      <button type="button" @click="fetchScripts" class="btn-primary">
        Leer experimentos
      </button>
    </div>

    <!-- Selector de experimentos -->
    <div class="mb-4" v-if="scripts.length">
      <label for="experiment" class="block mb-2 text-sm font-medium label-muted">Seleccionar experimento</label>
      <select id="experiment" v-model="selectedScript" class="input-field w-full p-2">
        <option v-for="script in scripts" :key="script" :value="script">
          {{ script }}
        </option>
      </select>
    </div>

    <!-- Panel de robots -->
    <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
      <div v-for="robot in robots" :key="robot.id" class="robot-card">
        <img :src="robot.imgSrc" :alt="`Robot ${robot.name}`" class="mb-2 mx-auto" />
        <p class="text-center">{{ robot.name }}</p>
      </div>
    </div>

    <!-- Parada de emergencia (E-Stop) -->
    <div class="emergency-stop-block mb-4">
      <label for="robot-ip-estop" class="block mb-2 text-sm font-medium label-muted">IP del robot (parada de emergencia)</label>
      <div class="flex flex-col sm:flex-row gap-2 align-end">
        <input
          id="robot-ip-estop"
          v-model="robotIpEstop"
          type="text"
          class="input-field flex-1"
          placeholder="ej. 10.20.50.231"
        />
        <button
          type="button"
          @click="emergencyStop"
          class="btn-estop"
          :disabled="estopLoading || !robotIpEstop?.trim()"
        >
          <span v-if="estopLoading">Enviando…</span>
          <span v-else><i class="fas fa-stop-circle" aria-hidden="true"></i> Parada de emergencia</span>
        </button>
      </div>
    </div>

    <!-- Botones de control (manual: iniciar, detener y reiniciar) -->
    <div class="flex flex-col sm:flex-row gap-2">
      <button type="button" @click="startExperiment" class="btn-success flex-1">
        Iniciar
      </button>
      <button type="button" @click="stopExperiment" class="btn-danger flex-1">
        Detener
      </button>
      <button type="button" @click="restartExperiment" class="btn-primary flex-1" :disabled="!selectedScript || restartLoading">
        <span v-if="restartLoading">Reiniciando…</span>
        <span v-else>Reiniciar</span>
      </button>
    </div>

    <!-- Área de visualización de resultados -->
    <div class="results-box">
      <h3 class="results-box__title">Resultados en tiempo real</h3>
      <div v-if="results.length">
        <ul>
          <li v-for="(result, index) in results" :key="index" class="text-white">
            {{ result }}
          </li>
        </ul>
      </div>
      <p v-else class="results-box__empty">Aún no hay resultados para mostrar.</p>
    </div>
  </div>
</template>

<script>
import axios from '../utils/axios';

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
      robotIpEstop: '',
      estopLoading: false,
      restartLoading: false,
    };
  },
  methods: {
    async fetchScripts() {
      try {
        const response = await axios.get("/list-scripts");
        const data = response.data;
        const scriptsByHost = data.scripts || {};
        // Unir listas de todos los hosts y quitar duplicados, o usar el primer host disponible
        const firstHostScripts = Object.values(scriptsByHost)[0];
        this.scripts = Array.isArray(firstHostScripts) ? firstHostScripts : [];
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
        const response = await axios.post("/start-experiment", { script_name: this.selectedScript });
        const data = response.data;
        const allOk = Array.isArray(data) && data.every((r) => r.status === "success");
        if (allOk) {
          alert("Experimento iniciado correctamente.");
        } else {
          const firstError = Array.isArray(data) ? data.find((r) => r.status !== "success") : null;
          alert(firstError ? `Error: ${firstError.message || firstError.details}` : "Error al iniciar el experimento.");
        }
      } catch (error) {
        console.error("Error al iniciar el experimento:", error);
        alert(error.response?.data?.detail || "Error al iniciar el experimento.");
      }
    },
    async stopExperiment() {
      if (!this.selectedScript) {
        alert("Selecciona un experimento para detener.");
        return;
      }
      try {
        const response = await axios.post("/stop-script", { script_name: this.selectedScript });
        const data = response.data;
        const allOk = Array.isArray(data) && data.every((r) => r.status === "success" || r.status === "not_found");
        if (allOk) {
          alert("Experimento detenido correctamente.");
        } else {
          const firstError = Array.isArray(data) ? data.find((r) => r.status === "error") : null;
          alert(firstError ? `Error: ${firstError.message}` : "Error al detener el experimento.");
        }
      } catch (error) {
        console.error("Error al detener el experimento:", error);
        alert(error.response?.data?.detail || "Error al detener el experimento.");
      }
    },
    async restartExperiment() {
      if (!this.selectedScript) {
        alert("Selecciona un experimento para reiniciar.");
        return;
      }
      this.restartLoading = true;
      try {
        await axios.post("/stop-script", { script_name: this.selectedScript });
        await new Promise((r) => setTimeout(r, 800));
        const response = await axios.post("/start-experiment", { script_name: this.selectedScript });
        const data = response.data;
        const allOk = Array.isArray(data) && data.every((r) => r.status === "success");
        if (allOk) {
          alert("Experimento reiniciado correctamente.");
        } else {
          const firstError = Array.isArray(data) ? data.find((r) => r.status !== "success") : null;
          alert(firstError ? `Error: ${firstError.message || firstError.details}` : "Error al reiniciar.");
        }
      } catch (error) {
        console.error("Error al reiniciar el experimento:", error);
        alert(error.response?.data?.detail || "Error al reiniciar el experimento.");
      } finally {
        this.restartLoading = false;
      }
    },
    async emergencyStop() {
      const ip = this.robotIpEstop?.trim();
      if (!ip) {
        alert("Indica la IP del robot para la parada de emergencia.");
        return;
      }
      this.estopLoading = true;
      try {
        const form = new FormData();
        form.append("robot_ip", ip);
        const response = await axios.post("/robots/emergency-stop/", form);
        if (response.data?.status === "success") {
          alert("Parada de emergencia enviada correctamente.");
        } else {
          alert(response.data?.message || "Parada de emergencia enviada.");
        }
      } catch (error) {
        const detail = error.response?.data?.detail;
        alert(detail || "No se pudo enviar la parada de emergencia. Comprueba la IP y la conexión.");
      } finally {
        this.estopLoading = false;
      }
    },
  },
};
</script>

