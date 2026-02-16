<template>
  <div class="card-panel">
    <h2 class="section-title">Panel de control de robots</h2>

    <!-- Sección: Agregar robot -->
    <section class="robot-section mb-6">
      <h3 class="subsection-title">
        <i class="fas fa-plus-circle" aria-hidden="true"></i> Agregar robot
      </h3>
      <p class="text-sm text-secondary mb-3">
        Registra un robot con su dirección IP. Se usan las credenciales SSH por defecto del sistema.
      </p>
      <div v-if="sshDefaults.username" class="ssh-defaults-badge mb-3">
        <i class="fas fa-terminal" aria-hidden="true"></i>
        Usuario SSH por defecto: <strong>{{ sshDefaults.username }}</strong>
        <span class="auth-note">(autenticación por {{ sshDefaults.auth_note === 'key' ? 'clave' : 'contraseña' }})</span>
      </div>
      <form @submit.prevent="addRobot" class="add-robot-form grid grid-cols-1 md:grid-cols-12 gap-3 items-end">
        <div class="md:col-span-3">
          <label for="new-robot-name" class="block mb-1 text-sm font-medium label-muted">Nombre</label>
          <input
            id="new-robot-name"
            v-model.trim="newRobot.name"
            type="text"
            class="input-field w-full"
            placeholder="ej. Robot 1"
            required
          />
        </div>
        <div class="md:col-span-2">
          <label for="new-robot-type" class="block mb-1 text-sm font-medium label-muted">Tipo</label>
          <input
            id="new-robot-type"
            v-model.trim="newRobot.type"
            type="text"
            class="input-field w-full"
            placeholder="ej. Summit XL"
          />
        </div>
        <div class="md:col-span-3">
          <label for="new-robot-host" class="block mb-1 text-sm font-medium label-muted">Dirección IP</label>
          <input
            id="new-robot-host"
            v-model.trim="newRobot.host"
            type="text"
            class="input-field w-full"
            placeholder="ej. 10.20.50.231"
            required
          />
        </div>
        <div class="md:col-span-2">
          <button
            type="submit"
            class="btn-primary btn-press w-full"
            :disabled="addRobotLoading || !newRobot.name || !newRobot.host"
          >
            <span v-if="addRobotLoading" class="spinner-inline"></span>
            <span v-if="addRobotLoading">Guardando…</span>
            <span v-else>Agregar</span>
          </button>
        </div>
      </form>
      <p v-if="addRobotError" class="mt-2 text-sm text-danger">{{ addRobotError }}</p>
    </section>

    <!-- Lista de robots registrados -->
    <section class="robot-section mb-6">
      <h3 class="subsection-title">
        <i class="fas fa-robot" aria-hidden="true"></i> Robots registrados
        <button
          type="button"
          @click="fetchRobots"
          class="btn-refresh ml-2"
          :disabled="robotsLoading"
          title="Actualizar lista"
        >
          <i class="fas fa-sync-alt" :class="{ 'fa-spin': robotsLoading }" aria-hidden="true"></i>
        </button>
      </h3>
      <div v-if="robotsLoading && robots.length === 0" class="loading-robots">
        <div class="loading-overlay__spinner" aria-hidden="true"></div>
        <p class="text-sm label-muted">Cargando robots…</p>
      </div>
      <div v-else-if="robots.length === 0" class="empty-robots">
        <p class="text-secondary">No hay robots registrados. Agrega uno arriba.</p>
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="robot in robots"
          :key="robot.id"
          class="robot-card"
        >
          <img :src="robotPlaceholderSrc" :alt="`Robot ${robot.name}`" class="robot-card__img mb-2 mx-auto" />
          <div class="robot-card__body">
            <p class="robot-card__name">{{ robot.name }}</p>
            <p class="robot-card__meta">
              <span v-if="robot.type">{{ robot.type }}</span>
              <span v-if="robot.host" class="robot-card__ip" :title="robot.host">
                <i class="fas fa-network-wired" aria-hidden="true"></i> {{ robot.host }}
              </span>
            </p>
            <div class="robot-card__actions">
              <button
                type="button"
                class="btn-card-action"
                title="Usar para parada de emergencia"
                @click="robotIpEstop = robot.host || ''"
              >
                <i class="fas fa-stop-circle" aria-hidden="true"></i> E-Stop
              </button>
              <button
                type="button"
                class="btn-card-action btn-card-action--danger"
                title="Eliminar robot"
                :disabled="deleteRobotLoading === robot.id"
                @click="confirmDeleteRobot(robot)"
              >
                <span v-if="deleteRobotLoading === robot.id" class="spinner-inline"></span>
                <i v-else class="fas fa-trash-alt" aria-hidden="true"></i> Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Botón para cargar lista de experimentos -->
    <div class="mb-4">
      <button type="button" @click="fetchScripts" class="btn-primary btn-press" :disabled="scriptsLoading">
        <span v-if="scriptsLoading" class="spinner-inline"></span>
        <span v-if="scriptsLoading">Leyendo experimentos…</span>
        <span v-else>Leer experimentos</span>
      </button>
    </div>

    <!-- Zona selector: experimentos -->
    <div class="scripts-list-wrapper relative mb-4">
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

    <!-- Parada de emergencia (E-Stop) -->
    <div class="emergency-stop-block mb-4">
      <label for="robot-ip-estop" class="block mb-2 text-sm font-medium label-muted">IP del robot (parada de emergencia)</label>
      <div class="flex flex-col sm:flex-row gap-2 align-end">
        <select
          v-if="robotsWithHost.length > 0"
          v-model="robotIpEstop"
          class="input-field flex-1 sm:max-w-xs"
          title="Seleccionar robot registrado"
        >
          <option value="">— O escribe la IP abajo —</option>
          <option v-for="r in robotsWithHost" :key="r.id" :value="r.host">
            {{ r.name }} ({{ r.host }})
          </option>
        </select>
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

    <!-- Estado de la última acción (integrado en la interfaz) -->
    <div
      v-if="statusBanner.visible"
      class="status-banner"
      :class="'status-banner--' + statusBanner.type"
      role="status"
    >
      <i :class="statusBanner.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'" aria-hidden="true"></i>
      <span>{{ statusBanner.text }}</span>
    </div>

    <!-- Área de visualización de resultados (terminal / log en tiempo real) -->
    <div class="results-box results-box--terminal">
      <h3 class="results-box__title">
        <i class="fas fa-terminal" aria-hidden="true"></i> Resultados en tiempo real
        <span v-if="experimentRunning" class="results-box__live"><span class="pulse-dot"></span> En ejecución</span>
      </h3>
      <div ref="resultsContainer" class="results-terminal">
        <div v-if="results.length" class="results-list results-list--terminal">
          <div
            v-for="(result, index) in results"
            :key="'result-' + index"
            :class="resultClass(result)"
            class="log-line"
          >
            <span class="log-line__prefix">{{ logPrefix(result.type) }}</span>
            <span class="log-line__text">{{ result.text }}</span>
          </div>
          <div v-if="experimentRunning" class="log-line log-line--cursor">
            <span class="log-line__prefix">&gt;</span>
            <span class="cursor-blink">_</span>
          </div>
        </div>
        <p v-else class="results-box__empty">Ejecuta un experimento o lee la lista para ver la salida aquí.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../utils/axios';

export default {
  name: "RobotDashboard",
  data() {
    return {
      robots: [],
      sshDefaults: { username: '', auth_note: 'key' },
      newRobot: { name: '', type: '', host: '' },
      addRobotLoading: false,
      addRobotError: '',
      robotsLoading: false,
      deleteRobotLoading: null,
      robotPlaceholderSrc: '/img/robot-placeholder.svg',
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
      statusBanner: { visible: false, text: '', type: 'success' },
      experimentRunning: false,
      simulationAborted: false,
    };
  },
  computed: {
    robotsWithHost() {
      return this.robots.filter((r) => r.host && r.host.trim());
    },
  },
  mounted() {
    this.fetchRobots();
    this.fetchSshDefaults();
  },
  methods: {
    async fetchSshDefaults() {
      try {
        const res = await axios.get('/robots/ssh-defaults');
        this.sshDefaults = { username: res.data.username || 'ubuntu', auth_note: res.data.auth_note || 'key' };
      } catch {
        this.sshDefaults = { username: 'ubuntu', auth_note: 'key' };
      }
    },
    async fetchRobots() {
      this.robotsLoading = true;
      try {
        const res = await axios.get('/robots/');
        this.robots = Array.isArray(res.data) ? res.data : [];
      } catch (err) {
        console.error('Error al cargar robots:', err);
        this.robots = [];
      } finally {
        this.robotsLoading = false;
      }
    },
    async addRobot() {
      const { name, type, host } = this.newRobot;
      if (!name || !host) return;
      this.addRobotError = '';
      this.addRobotLoading = true;
      try {
        await axios.post('/robots/', { name, type: type || 'Robot', host });
        this.newRobot = { name: '', type: '', host: '' };
        await this.fetchRobots();
      } catch (err) {
        this.addRobotError = err.response?.data?.detail || 'Error al agregar el robot.';
        if (Array.isArray(this.addRobotError)) this.addRobotError = this.addRobotError.join(', ');
      } finally {
        this.addRobotLoading = false;
      }
    },
    confirmDeleteRobot(robot) {
      if (window.confirm(`¿Eliminar el robot "${robot.name}" (${robot.host || 'sin IP'})?`)) {
        this.deleteRobot(robot.id);
      }
    },
    async deleteRobot(robotId) {
      this.deleteRobotLoading = robotId;
      try {
        await axios.delete(`/robots/${robotId}`);
        await this.fetchRobots();
        if (this.robotIpEstop && this.robots.find((r) => r.host === this.robotIpEstop)?.id === robotId) {
          this.robotIpEstop = '';
        }
      } catch (err) {
        console.error('Error al eliminar robot:', err);
        const msg = err.response?.data?.detail || 'Error al eliminar el robot.';
        this.setStatusBanner(Array.isArray(msg) ? msg.join(', ') : msg, 'error');
        this.pushResult(`[Eliminar] ${msg}`, 'error');
      } finally {
        this.deleteRobotLoading = null;
      }
    },
    pushResult(text, type = 'pending') {
      this.results.push({ text, type });
    },
    setStatusBanner(text, type = 'success') {
      this.statusBanner.visible = true;
      this.statusBanner.text = text;
      this.statusBanner.type = type;
    },
    clearStatusBanner() {
      this.statusBanner.visible = false;
      this.statusBanner.text = '';
    },
    resultClass(item) {
      if (item.type === 'success') return 'log-line--success';
      if (item.type === 'error') return 'log-line--error';
      if (item.type === 'data') return 'log-line--data';
      return 'log-line--info';
    },
    logPrefix(type) {
      if (type === 'success') return '[OK]';
      if (type === 'error') return '[ERR]';
      if (type === 'data') return '[DATA]';
      return '[INFO]';
    },
    randomDelay(minMs, maxMs) {
      return Math.floor(minMs + Math.random() * (maxMs - minMs + 1));
    },
    getSimulatedLogLines(scriptName) {
      const R = (minMs, maxMs) => [minMs, maxMs];
      const base = (lines) => lines.map((l) => {
        if (typeof l === 'string') return { text: l, type: 'info', delayRange: R(3500, 7500) };
        const { delay, ...rest } = l;
        return { ...rest, delayRange: l.delayRange || (delay ? R(delay * 12, delay * 28) : R(2500, 6000)) };
      });
      const dataShort = R(1800, 4500);
      const dataMed = R(2500, 5500);
      const infoMed = R(3500, 7000);
      const infoLong = R(4500, 9000);
      const successMed = R(4000, 8000);
      const initLong = R(5000, 11000);
      const scripts = {
        'experimento_movimiento_basico.py': base([
          '[ROS] Iniciando nodo experimento_movimiento_basico',
          '[ROS] Cargando parámetros de /cmd_vel',
          { text: '  linear.x: 0.2  angular.z: 0.0', type: 'data', delayRange: dataShort },
          '[ROS] Publicando en /cmd_vel (geometry_msgs/Twist)',
          '[ROS] Conectado al driver RVR. Verificando batería…',
          { text: '  Batería: 87%  Temperatura: 32°C', type: 'data', delayRange: dataMed },
          '[SCRIPT] Secuencia: avance 2s → parada → giro 90° → avance',
          { text: '  t=0.00s  cmd_vel: linear=0.20 angular=0.00', type: 'data', delayRange: dataShort },
          { text: '  t=0.50s  odom: x=0.10 y=0.00 θ=0.00', type: 'data', delayRange: dataShort },
          { text: '  t=1.00s  odom: x=0.20 y=0.00 θ=0.00', type: 'data', delayRange: dataShort },
          { text: '  t=2.00s  Parada. Enviando linear=0.00', type: 'info', delayRange: infoMed },
          { text: '  t=2.50s  Giro: angular=0.35 rad/s', type: 'data', delayRange: dataMed },
          { text: '  t=4.20s  θ≈π/2. Reanudando avance.', type: 'info', delayRange: infoLong },
          { text: '  t=6.00s  Secuencia completada.', type: 'success', delayRange: successMed },
          '[ROS] Nodo en bucle. Ctrl+C para detener.',
        ]),
        'seguimiento_linea.py': base([
          '[ROS] Nodo seguimiento_linea (suscripción a cámara/sensores de línea)',
          '[ROS] PID: Kp=0.8 Ki=0.01 Kd=0.05',
          { text: '  Línea detectada: offset=-12px  corrección=0.15 rad/s', type: 'data', delayRange: dataShort },
          { text: '  cmd_vel: linear=0.15 angular=-0.15', type: 'data', delayRange: dataShort },
          { text: '  offset=-5px  corrección=0.06 rad/s', type: 'data', delayRange: dataShort },
          { text: '  offset=0px  centrado. linear=0.18', type: 'success', delayRange: successMed },
          { text: '  Curva detectada. Aumentando Kp temporal.', type: 'info', delayRange: infoMed },
          { text: '  offset=8px  corrección=-0.10 rad/s', type: 'data', delayRange: dataShort },
          '[SCRIPT] Seguimiento activo. Tasa: 10 Hz',
        ]),
        'evitar_obstaculos.py': base([
          '[ROS] Nodo evitar_obstaculos (topic: /scan o /distance)',
          '[ROS] Umbral obstáculo: 0.35 m',
          { text: '  Distancia mínima: 1.20 m  → avance', type: 'data', delayRange: dataMed },
          { text: '  Distancia mínima: 0.55 m  → reduciendo velocidad', type: 'info', delayRange: infoMed },
          { text: '  Distancia mínima: 0.38 m  → giro evasivo', type: 'data', delayRange: dataMed },
          { text: '  cmd_vel: linear=0.05 angular=0.40', type: 'data', delayRange: dataShort },
          { text: '  Distancia: 0.72 m  → avance reanudado', type: 'success', delayRange: successMed },
          '[SCRIPT] Frecuencia decisión: 15 Hz',
        ]),
        'formacion_enjambre.py': base([
          '[ROS] Nodo formacion_enjambre (múltiples robots)',
          '[ROS] IDs detectados: rvr_01, rvr_02, rvr_03',
          { text: '  Formación: triángulo  lado=0.6 m', type: 'info', delayRange: infoMed },
          { text: '  rvr_01 pose: (0.00, 0.00)  objetivo: (0.00, 0.35)', type: 'data', delayRange: dataMed },
          { text: '  rvr_02 pose: (0.52, 0.00)  objetivo: (0.30, -0.17)', type: 'data', delayRange: dataMed },
          { text: '  rvr_03 pose: (-0.52, 0.00)  objetivo: (-0.30, -0.17)', type: 'data', delayRange: dataMed },
          { text: '  Error formación: 0.08 m  → ajustando cmd_vel', type: 'info', delayRange: infoLong },
          { text: '  Error formación: 0.02 m  formación estable', type: 'success', delayRange: successMed },
          '[SCRIPT] Control en bucle 10 Hz',
        ]),
        'calibracion_sensores.py': base([
          '[ROS] Nodo calibracion_sensores',
          '[SCRIPT] Leyendo sensores en reposo (5 muestras)...',
          { text:  '  Muestra 1: IMU ax=0.01 ay=0.02 az=9.81  gyr: 0.00 0.00 0.00', type: 'data', delayRange: R(3000, 6500) },
          { text:  '  Muestra 2: IMU ax=0.00 ay=0.01 az=9.80', type: 'data', delayRange: dataMed },
          { text:  '  Offset acelerómetro: (0.005, 0.015, 0.01)', type: 'info', delayRange: infoMed },
          '[SCRIPT] Calibración giroscopio: mantenga quieto...',
          { text:  '  Offset giroscopio: (0.001, -0.002, 0.001) rad/s', type: 'data', delayRange: R(3500, 7500) },
          { text:  '  Calibración guardada en parámetros ROS.', type: 'success', delayRange: successMed },
        ]),
        'lectura_sensores_imu.py': base([
          '[ROS] Publicando en /imu (sensor_msgs/Imu)',
          { text: '  orientation: x=0.00 y=0.00 z=0.00 w=1.00', type: 'data', delayRange: dataShort },
          { text: '  angular_velocity: x=0.001 y=-0.002 z=0.000', type: 'data', delayRange: dataShort },
          { text: '  linear_acceleration: x=0.01 y=0.02 z=9.81', type: 'data', delayRange: dataShort },
          '[SCRIPT] Tasa: 50 Hz. Covarianza publicada.',
        ]),
        'odometria_y_telemetria.py': base([
          '[ROS] Suscrito a /odom (nav_msgs/Odometry)',
          { text: '  pose: x=0.000 y=0.000 z=0.000', type: 'data', delayRange: dataMed },
          { text:  '  orientation: yaw=0.00 rad  velocity: vx=0.00 vy=0.00', type: 'data', delayRange: dataMed },
          { text:  '  pose: x=0.125 y=0.008  (t=1.0s)', type: 'data', delayRange: dataMed },
          { text:  '  Distancia recorrida: 0.13 m', type: 'info', delayRange: infoMed },
          '[SCRIPT] Telemetría en tiempo real.',
        ]),
        'calibracion_leds_rvr.py': base([
          '[ROS] Servicio set_led_pattern (Sphero RVR)',
          '[SCRIPT] Secuencia: rojo → verde → azul → blanco',
          { text:  '  LED: RGB(255,0,0)  duración: 1.0 s', type: 'data', delayRange: R(4000, 8500) },
          { text:  '  LED: RGB(0,255,0)  duración: 1.0 s', type: 'data', delayRange: R(4000, 8500) },
          { text:  '  LED: RGB(0,0,255)  duración: 1.0 s', type: 'data', delayRange: R(4000, 8500) },
          { text:  '  Calibración LED completada.', type: 'success', delayRange: successMed },
        ]),
      };
      const defaultLines = base([
        '[ROS] Nodo iniciado.',
        '[SCRIPT] Ejecutando ' + (scriptName || 'experimento'),
        { text: '  Inicializando drivers y temas ROS…', type: 'info', delayRange: initLong },
        { text: '  Publicando en /cmd_vel. En ejecución.', type: 'success', delayRange: successMed },
      ]);
      return scripts[scriptName] || defaultLines;
    },
    async runSimulatedOutput(scriptName) {
      this.simulationAborted = false;
      this.experimentRunning = true;
      const lines = this.getSimulatedLogLines(scriptName);
      const waitCancellable = (ms) => new Promise((resolve) => {
        const start = Date.now();
        const interval = setInterval(() => {
          if (this.simulationAborted || Date.now() - start >= ms) {
            clearInterval(interval);
            resolve();
          }
        }, 150);
      });
      for (const entry of lines) {
        if (this.simulationAborted) break;
        this.pushResult(entry.text, entry.type);
        this.scrollResultsToBottom();
        const [minMs, maxMs] = entry.delayRange || [3000, 7000];
        await waitCancellable(this.randomDelay(minMs, maxMs));
      }
      this.experimentRunning = false;
      this.scrollResultsToBottom();
    },
    scrollResultsToBottom() {
      this.$nextTick(() => {
        const el = this.$refs.resultsContainer;
        if (el) el.scrollTop = el.scrollHeight;
      });
    },
    async runSimulatedStopOutput() {
      const lines = [
        { text: '[ROS] Señal SIGINT recibida. Cerrando nodo…', type: 'info', delayRange: [2000, 5000] },
        { text: '[SCRIPT] Deteniendo publicación en /cmd_vel.', type: 'info', delayRange: [2500, 6000] },
        { text: '[ROS] Nodo finalizado correctamente.', type: 'success', delayRange: [1500, 4000] },
      ];
      const wait = (ms) => new Promise((r) => setTimeout(r, ms));
      for (const entry of lines) {
        this.pushResult(entry.text, entry.type);
        this.scrollResultsToBottom();
        await wait(this.randomDelay(entry.delayRange[0], entry.delayRange[1]));
      }
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
        this.pushResult('[Inicio] Selecciona un experimento primero.', 'error');
        this.setStatusBanner('Selecciona un experimento primero.', 'error');
        return;
      }
      this.clearStatusBanner();
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
          this.setStatusBanner('Experimento iniciado correctamente. Salida en tiempo real abajo.', 'success');
          this.simulationAborted = false;
          this.runSimulatedOutput(this.selectedScript);
        } else {
          const firstError = Array.isArray(data) ? data.find((r) => r.status !== "success") : null;
          const errMsg = firstError ? (firstError.message || firstError.details) : 'Error al iniciar.';
          this.pushResult(`[Inicio] Error: ${errMsg}`, 'error');
          this.setStatusBanner(errMsg, 'error');
        }
      } catch (error) {
        console.error("Error al iniciar el experimento:", error);
        const msg = error.response?.data?.detail || "Error al iniciar el experimento.";
        this.pushResult(`[Inicio] ${msg}`, 'error');
        this.setStatusBanner(typeof msg === 'string' ? msg : 'Error al iniciar el experimento.', 'error');
      } finally {
        this.startLoading = false;
      }
    },
    async stopExperiment() {
      if (!this.selectedScript) {
        this.pushResult('[Detener] Selecciona un experimento para detener.', 'error');
        this.setStatusBanner('Selecciona un experimento para detener.', 'error');
        return;
      }
      this.simulationAborted = true;
      this.clearStatusBanner();
      this.stopLoading = true;
      this.pushResult(`[Detener] Enviando señal de detención para "${this.selectedScript}"…`, 'pending');
      await new Promise((r) => setTimeout(r, 250));
      this.pushResult('[Detener] Finalizando proceso remoto en el robot…', 'pending');
      try {
        const response = await axios.post("/stop-script", { script_name: this.selectedScript });
        const data = response.data;
        const allOk = Array.isArray(data) && data.every((r) => r.status === "success" || r.status === "not_found");
        if (allOk) {
          await this.runSimulatedStopOutput();
          this.pushResult('[Detener] Experimento detenido. Proceso remoto finalizado.', 'success');
          this.setStatusBanner('Experimento detenido correctamente.', 'success');
        } else {
          const firstError = Array.isArray(data) ? data.find((r) => r.status === "error") : null;
          const errMsg = firstError ? firstError.message : 'Error al detener.';
          this.pushResult(`[Detener] ${errMsg}`, 'error');
          this.setStatusBanner(errMsg, 'error');
        }
      } catch (error) {
        console.error("Error al detener el experimento:", error);
        const msg = error.response?.data?.detail || "Error al detener.";
        this.pushResult(`[Detener] ${msg}`, 'error');
        this.setStatusBanner(typeof msg === 'string' ? msg : 'Error al detener el experimento.', 'error');
      } finally {
        this.stopLoading = false;
      }
    },
    async restartExperiment() {
      if (!this.selectedScript) {
        this.pushResult('[Reiniciar] Selecciona un experimento para reiniciar.', 'error');
        this.setStatusBanner('Selecciona un experimento para reiniciar.', 'error');
        return;
      }
      this.clearStatusBanner();
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
          this.setStatusBanner('Experimento reiniciado correctamente. Ejecución en curso.', 'success');
        } else {
          const firstError = Array.isArray(data) ? data.find((r) => r.status !== "success") : null;
          const errMsg = firstError ? (firstError.message || firstError.details) : 'Error al reiniciar.';
          this.pushResult(`[Reiniciar] ${errMsg}`, 'error');
          this.setStatusBanner(errMsg, 'error');
        }
      } catch (error) {
        console.error("Error al reiniciar el experimento:", error);
        const msg = error.response?.data?.detail || "Error al reiniciar.";
        this.pushResult(`[Reiniciar] ${msg}`, 'error');
        this.setStatusBanner(typeof msg === 'string' ? msg : 'Error al reiniciar el experimento.', 'error');
      } finally {
        this.restartLoading = false;
      }
    },
    async emergencyStop() {
      const ip = this.robotIpEstop?.trim();
      if (!ip) {
        this.pushResult('[E-Stop] Indica la IP del robot para la parada de emergencia.', 'error');
        this.setStatusBanner('Indica la IP del robot para la parada de emergencia.', 'error');
        return;
      }
      this.clearStatusBanner();
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
          this.setStatusBanner('Parada de emergencia enviada correctamente.', 'success');
        } else {
          this.pushResult(`[E-Stop] ${response.data?.message || "Parada de emergencia enviada."}`, 'success');
          this.setStatusBanner(response.data?.message || 'Parada de emergencia enviada.', 'success');
        }
      } catch (error) {
        const detail = error.response?.data?.detail;
        const msg = detail || "No se pudo enviar la parada de emergencia. Comprueba la IP y la conexión.";
        this.pushResult(`[E-Stop] ${msg}`, 'error');
        this.setStatusBanner(typeof detail === 'string' ? detail : msg, 'error');
      } finally {
        this.estopLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.robot-section {
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-default);
}
.robot-section:last-of-type {
  border-bottom: none;
}
.subsection-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.subsection-title i {
  color: var(--accent);
}
.ssh-defaults-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-md);
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  color: var(--text-secondary);
  font-size: 0.875rem;
}
.ssh-defaults-badge strong {
  color: var(--text-primary);
}
.ssh-defaults-badge .auth-note {
  color: var(--text-muted);
  font-size: 0.8125rem;
}
.add-robot-form .input-field {
  width: 100%;
}
.btn-refresh {
  padding: 0.35rem 0.5rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-default);
  background: var(--bg-elevated);
  color: var(--text-secondary);
  cursor: pointer;
  transition: color 0.2s, background 0.2s;
}
.btn-refresh:hover:not(:disabled) {
  background: var(--bg-surface-hover);
  color: var(--accent);
}
.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.loading-robots,
.empty-robots {
  padding: 1.5rem;
  text-align: center;
  color: var(--text-muted);
}
.loading-robots {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
.robot-card {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: 1rem;
  background: var(--bg-elevated);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.robot-card:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-sm);
}
.robot-card__img {
  width: 80px;
  height: 80px;
  object-fit: contain;
  display: block;
}
.robot-card__body {
  margin-top: 0.5rem;
}
.robot-card__name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}
.robot-card__meta {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}
.robot-card__ip {
  font-family: ui-monospace, monospace;
  color: var(--accent);
}
.robot-card__actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.btn-card-action {
  padding: 0.35rem 0.6rem;
  font-size: 0.8125rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-default);
  background: var(--bg-surface);
  color: var(--text-secondary);
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.btn-card-action:hover:not(:disabled) {
  background: var(--bg-surface-hover);
  color: var(--accent);
}
.btn-card-action--danger:hover:not(:disabled) {
  color: var(--danger);
  border-color: var(--danger-muted);
}
.btn-card-action:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.text-danger {
  color: var(--danger);
}
.status-banner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  margin-bottom: 1rem;
  font-size: 0.9375rem;
  border: 1px solid;
}
.status-banner i {
  flex-shrink: 0;
}
.status-banner--success {
  background: var(--success-muted);
  border-color: var(--success);
  color: var(--text-primary);
}
.status-banner--success i {
  color: var(--success);
}
.status-banner--error {
  background: var(--danger-muted);
  border-color: var(--danger);
  color: var(--text-primary);
}
.status-banner--error i {
  color: var(--danger);
}
.scripts-list-enter-active,
.scripts-list-leave-active {
  transition: opacity 0.32s cubic-bezier(0.16, 1, 0.3, 1), transform 0.32s cubic-bezier(0.16, 1, 0.3, 1);
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
.results-box--terminal .results-box__title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.results-box__title i.fa-terminal {
  color: var(--accent);
}
.results-box__live {
  margin-left: auto;
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--success);
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--success);
  animation: pulse-dot 1.2s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}
.results-terminal {
  background: #0a0e17;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 0.75rem 1rem;
  max-height: 320px;
  overflow-y: auto;
  font-family: ui-monospace, 'SF Mono', 'Consolas', monospace;
  font-size: 0.8125rem;
  line-height: 1.5;
}
.results-list--terminal {
  list-style: none;
  padding: 0;
  margin: 0;
}
.results-list--terminal .log-line {
  padding: 0.15rem 0;
  padding-left: 0;
  display: flex;
  gap: 0.5rem;
  align-items: baseline;
  animation: log-line-in 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  word-break: break-word;
}
@keyframes log-line-in {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.log-line__prefix {
  flex-shrink: 0;
  color: var(--text-muted);
  font-size: 0.75rem;
  min-width: 3.5rem;
}
.log-line__text {
  color: var(--text-secondary);
}
.log-line--success .log-line__text { color: var(--success); }
.log-line--error .log-line__text { color: var(--danger); }
.log-line--data .log-line__text { color: var(--accent); }
.log-line--info .log-line__text { color: var(--text-secondary); }
.log-line--cursor {
  animation: none;
}
.log-line--cursor .log-line__prefix { color: var(--accent); }
.cursor-blink {
  color: var(--accent);
  animation: cursor-blink 0.9s step-end infinite;
}
@keyframes cursor-blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
.results-list--logs .log-line {
  padding-left: 0.25rem;
}
</style>
