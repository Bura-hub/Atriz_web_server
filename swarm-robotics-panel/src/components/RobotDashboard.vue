<template>
  <div class="card-panel">
    <h2 class="section-title">Panel de control de robots</h2>

    <!-- Botón para cargar lista de experimentos (manual: control de experimentos) -->
    <div class="mb-4">
      <button type="button" @click="fetchScripts" class="btn-primary btn-press" :disabled="scriptsLoading">
        <span v-if="scriptsLoading" class="spinner-inline"></span>
        <span v-if="scriptsLoading">Leyendo experimentos…</span>
        <span v-else>Leer experimentos</span>
      </button>
    </div>

    <!-- Zona selector: pantalla de carga o lista (según docs) -->
    <div class="scripts-list-wrapper relative mb-4">
      <!-- Pantalla de carga al leer experimentos (animación + skeleton) -->
      <div v-if="scriptsLoading" class="loading-overlay">
        <div class="loading-overlay__content">
          <div class="loading-overlay__spinner" aria-hidden="true"></div>
          <p class="loading-overlay__text">{{ loadingStep }}</p>
        </div>
        <div class="skeleton-block loading-overlay__skeleton">
          <div class="skeleton-line skeleton-line--title skeleton-line--short"></div>
          <div class="skeleton-select mt-2"></div>
        </div>
      </div>
      <!-- Selector de experimentos (manual: iniciar, detener, reiniciar) -->
      <transition name="scripts-list">
        <div class="mb-0 scripts-list-block" v-if="scripts.length && !scriptsLoading">
          <p v-if="isDemoScripts" class="text-sm label-muted mb-2 scripts-list-block__demo">
            <i class="fas fa-info-circle" aria-hidden="true"></i> Experimentos de demostración (según documentación).
          </p>
          <label for="experiment" class="block mb-2 text-sm font-medium label-muted">Seleccionar experimento</label>
          <select id="experiment" v-model="selectedScript" class="input-field w-full p-2 scripts-list__select">
            <option value="" disabled>— Elige un experimento —</option>
            <option v-for="script in scripts" :key="script" :value="script">
              {{ script }}
            </option>
          </select>
        </div>
      </transition>
    </div>

    <!-- Panel de robots (imágenes por defecto: prototipos) -->
    <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
      <div v-for="robot in robots" :key="robot.id" class="robot-card">
        <img :src="robot.imgSrc" :alt="`Robot ${robot.name}`" class="robot-card__img mb-2 mx-auto" />
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
          class="btn-estop btn-press"
          :disabled="estopLoading || !robotIpEstop?.trim()"
        >
          <span v-if="estopLoading" class="spinner-inline"></span>
          <span v-if="estopLoading">Enviando…</span>
          <span v-else><i class="fas fa-stop-circle" aria-hidden="true"></i> Parada de emergencia</span>
        </button>
      </div>
    </div>

    <!-- Botones de control (manual: iniciar, detener y reiniciar) -->
    <div class="flex flex-col sm:flex-row gap-2">
      <button type="button" @click="startExperiment" class="btn-success btn-press flex-1" :disabled="startLoading">
        <span v-if="startLoading" class="spinner-inline"></span>
        <span v-if="startLoading">Iniciando…</span>
        <span v-else>Iniciar</span>
      </button>
      <button type="button" @click="stopExperiment" class="btn-danger btn-press flex-1" :disabled="stopLoading">
        <span v-if="stopLoading" class="spinner-inline"></span>
        <span v-if="stopLoading">Deteniendo…</span>
        <span v-else>Detener</span>
      </button>
      <button type="button" @click="restartExperiment" class="btn-primary btn-press flex-1" :disabled="!selectedScript || restartLoading">
        <span v-if="restartLoading" class="spinner-inline"></span>
        <span v-if="restartLoading">Reiniciando…</span>
        <span v-else>Reiniciar</span>
      </button>
    </div>

    <!-- Área de visualización de resultados (manual: respuesta de los prototipos) -->
    <div class="results-box">
      <h3 class="results-box__title">Resultados en tiempo real</h3>
      <div v-if="results.length">
        <ul class="results-list list-disc pl-5 space-y-0 results-list--logs">
          <li v-for="(result, index) in results" :key="index" :class="resultClass(result)" class="sim-step log-line">
            {{ result.text }}
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
        { id: 1, name: "Robot 1", imgSrc: "/img/robot-placeholder.svg" },
        { id: 2, name: "Robot 2", imgSrc: "/img/robot-placeholder.svg" },
        { id: 3, name: "Robot 3", imgSrc: "/img/robot-placeholder.svg" },
      ],
      scripts: [],
      demoScripts: [
        'experimento_movimiento_basico.py',
        'seguimiento_linea.py',
        'evitar_obstaculos.py',
        'formacion_enjambre.py',
        'calibracion_sensores.py',
      ],
      selectedScript: null,
      isDemoScripts: false,
      results: [],
      robotIpEstop: '',
      estopLoading: false,
      restartLoading: false,
      scriptsLoading: false,
      startLoading: false,
      stopLoading: false,
      loadingStep: 'Conectando al servidor…',
    };
  },
  methods: {
    pushResult(text, type = 'pending') {
      this.results.push({ text, type });
    },
    resultClass(item) {
      if (item.type === 'success') return 'sim-step--success';
      if (item.type === 'error') return 'sim-step--error';
      return 'sim-step--pending';
    },
    async fetchScripts() {
      this.scriptsLoading = true;
      this.loadingStep = 'Conectando al servidor…';
      this.pushResult('[1/4] Conectando al servidor (API)…', 'pending');
      await new Promise((r) => setTimeout(r, 400));
      this.loadingStep = 'Consultando directorio remoto en robots…';
      this.pushResult('[2/4] Consultando lista de experimentos (SSH / directorio remoto)…', 'pending');
      await new Promise((r) => setTimeout(r, 350));
      this.loadingStep = 'Procesando lista de scripts…';
      this.pushResult('[3/4] Procesando scripts .py disponibles…', 'pending');
      try {
        const response = await axios.get("/list-scripts");
        const data = response.data;
        const scriptsByHost = data.scripts || {};
        const allLists = Object.values(scriptsByHost).filter((v) => Array.isArray(v));
        const merged = [...new Set(allLists.flat())].sort();
        this.scripts = merged.length ? merged : this.demoScripts;
        this.isDemoScripts = merged.length === 0 || Boolean(data.demo);
        this.loadingStep = 'Listo.';
        this.pushResult(`[4/4] Experimentos cargados: ${this.scripts.length} disponible(s). ${this.isDemoScripts ? 'Modo demostración (según documentación).' : 'Listados desde los robots.'}`, 'success');
      } catch (error) {
        console.error("Error al obtener los scripts:", error);
        this.loadingStep = 'Error.';
        this.pushResult('[4/4] Error al cargar desde el servidor. Mostrando experimentos de demostración.', 'error');
        this.scripts = this.demoScripts;
        this.isDemoScripts = true;
      } finally {
        this.scriptsLoading = false;
      }
    },
    async startExperiment() {
      if (!this.selectedScript) {
        alert("Selecciona un experimento primero.");
        return;
      }
      this.startLoading = true;
      this.pushResult(`[Inicio] Enviando comando para "${this.selectedScript}"…`, 'pending');
      await new Promise((r) => setTimeout(r, 300));
      this.pushResult('[Inicio] Conexión SSH / rosrun sphero_rvr_pkg script_executor.py…', 'pending');
      try {
        const response = await axios.post("/start-experiment", { script_name: this.selectedScript });
        const data = response.data;
        const allOk = Array.isArray(data) && data.every((r) => r.status === "success");
        if (allOk) {
          this.pushResult('[Inicio] Experimento en curso. Driver publicando /cmd_vel, script en ejecución.', 'success');
          alert("Experimento iniciado correctamente.");
        } else {
          const firstError = Array.isArray(data) ? data.find((r) => r.status !== "success") : null;
          this.pushResult(firstError ? `[Inicio] Error: ${firstError.message || firstError.details}` : '[Inicio] Error al iniciar.', 'error');
          alert(firstError ? `Error: ${firstError.message || firstError.details}` : "Error al iniciar el experimento.");
        }
      } catch (error) {
        console.error("Error al iniciar el experimento:", error);
        this.pushResult(`[Inicio] ${error.response?.data?.detail || "Error al iniciar el experimento."}`, 'error');
        alert(error.response?.data?.detail || "Error al iniciar el experimento.");
      } finally {
        this.startLoading = false;
      }
    },
    async stopExperiment() {
      if (!this.selectedScript) {
        alert("Selecciona un experimento para detener.");
        return;
      }
      this.stopLoading = true;
      this.pushResult(`[Detener] Enviando señal de detención para "${this.selectedScript}"…`, 'pending');
      await new Promise((r) => setTimeout(r, 250));
      this.pushResult('[Detener] Finalizando proceso remoto en el robot…', 'pending');
      try {
        const response = await axios.post("/stop-script", { script_name: this.selectedScript });
        const data = response.data;
        const allOk = Array.isArray(data) && data.every((r) => r.status === "success" || r.status === "not_found");
        if (allOk) {
          this.pushResult('[Detener] Experimento detenido. Proceso remoto finalizado.', 'success');
          alert("Experimento detenido correctamente.");
        } else {
          const firstError = Array.isArray(data) ? data.find((r) => r.status === "error") : null;
          this.pushResult(firstError ? `[Detener] ${firstError.message}` : '[Detener] Error al detener.', 'error');
          alert(firstError ? `Error: ${firstError.message}` : "Error al detener el experimento.");
        }
      } catch (error) {
        console.error("Error al detener el experimento:", error);
        this.pushResult(`[Detener] ${error.response?.data?.detail || "Error al detener."}`, 'error');
        alert(error.response?.data?.detail || "Error al detener el experimento.");
      } finally {
        this.stopLoading = false;
      }
    },
    async restartExperiment() {
      if (!this.selectedScript) {
        alert("Selecciona un experimento para reiniciar.");
        return;
      }
      this.restartLoading = true;
      this.pushResult(`[Reiniciar] Paso 1/3: Deteniendo "${this.selectedScript}"…`, 'pending');
      try {
        await axios.post("/stop-script", { script_name: this.selectedScript });
        await new Promise((r) => setTimeout(r, 400));
        this.pushResult('[Reiniciar] Paso 2/3: Esperando liberación del proceso…', 'pending');
        await new Promise((r) => setTimeout(r, 300));
        this.pushResult('[Reiniciar] Paso 3/3: Iniciando de nuevo el experimento…', 'pending');
        const response = await axios.post("/start-experiment", { script_name: this.selectedScript });
        const data = response.data;
        const allOk = Array.isArray(data) && data.every((r) => r.status === "success");
        if (allOk) {
          this.pushResult('[Reiniciar] Experimento reiniciado. Ejecución en curso.', 'success');
          alert("Experimento reiniciado correctamente.");
        } else {
          const firstError = Array.isArray(data) ? data.find((r) => r.status !== "success") : null;
          this.pushResult(firstError ? `[Reiniciar] ${firstError.message || firstError.details}` : '[Reiniciar] Error.', 'error');
          alert(firstError ? `Error: ${firstError.message || firstError.details}` : "Error al reiniciar.");
        }
      } catch (error) {
        console.error("Error al reiniciar el experimento:", error);
        this.pushResult(`[Reiniciar] ${error.response?.data?.detail || "Error al reiniciar."}`, 'error');
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
      this.pushResult(`[E-Stop] Publicando en /rvr/emergency_stop (robot ${ip})…`, 'pending');
      await new Promise((r) => setTimeout(r, 200));
      this.pushResult('[E-Stop] Actualizando State Buffer a velocidad cero (driver)…', 'pending');
      try {
        const form = new FormData();
        form.append("robot_ip", ip);
        const response = await axios.post("/robots/emergency-stop/", form);
        if (response.data?.status === "success") {
          this.pushResult('[E-Stop] Parada de emergencia enviada. Velocidad a cero, failsafe activado.', 'success');
          alert("Parada de emergencia enviada correctamente.");
        } else {
          this.pushResult(`[E-Stop] ${response.data?.message || "Parada de emergencia enviada."}`, 'success');
          alert(response.data?.message || "Parada de emergencia enviada.");
        }
      } catch (error) {
        const detail = error.response?.data?.detail;
        this.pushResult(`[E-Stop] ${detail || "No se pudo enviar la parada de emergencia."}`, 'error');
        alert(detail || "No se pudo enviar la parada de emergencia. Comprueba la IP y la conexión.");
      } finally {
        this.estopLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.scripts-list-enter-active,
.scripts-list-leave-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}
.scripts-list-enter-from,
.scripts-list-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
.scripts-list-block__demo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.scripts-list-block__demo i {
  color: var(--accent);
}
.scripts-list__select {
  animation: scripts-select-fade 0.4s ease;
}
@keyframes scripts-select-fade {
  from { opacity: 0; }
  to { opacity: 1; }
}
.scripts-list-wrapper {
  position: relative;
  min-height: 100px;
}
.robot-card__img {
  width: 100px;
  height: 100px;
  object-fit: contain;
}
.results-list--logs .log-line {
  padding-left: 0.25rem;
}
</style>
