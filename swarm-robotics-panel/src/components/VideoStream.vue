<template>
  <div class="card-panel card-panel--relative">
    <h2 class="section-title">Transmisión de vídeo en vivo</h2>

    <!-- Overlay de carga: cámara local o conexión MJPEG -->
    <div v-if="loading || streamConnecting" class="loading-overlay loading-overlay--video">
      <div class="loading-overlay__content">
        <div class="loading-overlay__spinner" aria-hidden="true"></div>
        <p class="loading-overlay__text">{{ loadingMessage }}</p>
      </div>
    </div>

    <!-- Origen: cámara local o stream MJPEG del robot -->
    <div class="video-source-select mb-4">
      <label class="block mb-2 text-sm font-medium label-muted">Origen del vídeo</label>
      <div class="flex flex-wrap gap-4 items-center">
        <label class="inline-flex items-center gap-2 cursor-pointer">
          <input type="radio" v-model="source" value="local" @change="onSourceChange" />
          <span>Cámara local</span>
        </label>
        <label class="inline-flex items-center gap-2 cursor-pointer">
          <input type="radio" v-model="source" value="robot" @change="onSourceChange" />
          <span>Stream del robot (MJPEG)</span>
        </label>
      </div>
      <div v-if="source === 'robot'" class="robot-stream-params mt-3 flex flex-wrap gap-3 items-end">
        <div>
          <label for="robot-ip-video" class="block mb-1 text-sm label-muted">IP del robot</label>
          <input id="robot-ip-video" v-model="robotIp" type="text" class="input-field w-40" placeholder="10.20.50.231" />
        </div>
        <div>
          <label for="stream-quality" class="block mb-1 text-sm label-muted">Calidad (1–100)</label>
          <input id="stream-quality" v-model.number="streamQuality" type="number" min="1" max="100" class="input-field w-20" />
        </div>
        <div>
          <label for="stream-width" class="block mb-1 text-sm label-muted">Ancho</label>
          <input id="stream-width" v-model.number="streamWidth" type="number" min="160" max="1920" class="input-field w-24" />
        </div>
        <div>
          <label for="stream-height" class="block mb-1 text-sm label-muted">Alto</label>
          <input id="stream-height" v-model.number="streamHeight" type="number" min="120" max="1080" class="input-field w-24" />
        </div>
      </div>
    </div>

    <div class="video-container video-container--rounded mx-auto" ref="videoContainer">
      <!-- Cámara local: <video> con getUserMedia -->
      <video v-show="source === 'local'" ref="videoStream" autoplay playsinline muted class="video-feed"></video>
      <!-- Stream robot: MJPEG por URL según desarrollo.tex -->
      <img
        v-show="source === 'robot' && mjpegUrl"
        :src="mjpegUrl"
        alt="Stream del robot"
        class="video-feed video-feed--img"
        ref="mjpegImg"
        @load="onMjpegLoad"
        @error="onMjpegError"
      />
      <p v-if="error" class="video-message video-message--error">{{ error }}</p>
      <p v-else-if="source === 'local' && !streamActive && !loading" class="video-message">Tu cámara se mostrará aquí.</p>
      <p v-else-if="source === 'robot' && !mjpegUrl" class="video-message">Indica la IP del robot para ver el stream MJPEG.</p>
      <p v-else-if="source === 'robot' && streamConnecting" class="video-message video-message--connecting">
        <span class="spinner-inline"></span>
        Conectando al stream MJPEG (web_video_server)…
      </p>
      <p v-else-if="source === 'robot' && mjpegUrl" class="video-message video-message--hint">Stream del robot (web_video_server).</p>
      <p v-else-if="loading" class="video-message">Solicitando acceso a la cámara…</p>
      <button @click="toggleFullscreen" class="fullscreen-btn">
        <i class="fas fa-expand"></i>
      </button>
    </div>

    <!-- Logs de estado (según desarrollo.tex: usb_cam, web_video_server, MJPEG) -->
    <div class="results-box mt-4">
      <h3 class="results-box__title">Estado del stream</h3>
      <div v-if="streamLogs.length">
        <ul class="results-list list-disc pl-5 space-y-0 results-list--logs">
          <li v-for="(log, index) in streamLogs" :key="index" :class="logClass(log)" class="sim-step log-line">
            {{ log.text }}
          </li>
        </ul>
      </div>
      <p v-else class="results-box__empty">Selecciona origen (cámara local o stream del robot) para ver el estado de conexión.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "VideoStream",
  data() {
    return {
      source: "local", // "local" | "robot"
      robotIp: "",
      streamQuality: 50,
      streamWidth: 640,
      streamHeight: 480,
      streamTopic: "/usb_cam/image_raw",
      stream: null,
      streamActive: false,
      loading: false,
      error: null,
      streamConnecting: false,
      streamConnectTimeout: null,
      streamLogs: [],
    };
  },
  watch: {
    mjpegUrl(url) {
      if (this.source === 'robot' && url) {
        this.streamConnecting = true;
        this.error = null;
        if (!this.streamLogs.some(l => l.text.startsWith('[1/2]'))) this.pushLog('[1/2] Conectando a web_video_server (MJPEG)…', 'pending');
        clearTimeout(this.streamConnectTimeout);
        this.streamConnectTimeout = setTimeout(() => {
          if (this.streamConnecting) this.streamConnecting = false;
        }, 4000);
      }
    },
  },
  computed: {
    loadingMessage() {
      if (this.loading) return "Solicitando acceso a la cámara (getUserMedia)…";
      if (this.streamConnecting) return "Conectando al stream MJPEG (web_video_server)…";
      return "Cargando…";
    },
    mjpegUrl() {
      if (this.source !== "robot" || !this.robotIp?.trim()) return "";
      const ip = this.robotIp.trim();
      const q = Math.min(100, Math.max(1, this.streamQuality || 50));
      const w = Math.min(1920, Math.max(160, this.streamWidth || 640));
      const h = Math.min(1080, Math.max(120, this.streamHeight || 480));
      return `http://${ip}:8080/stream?topic=${encodeURIComponent(this.streamTopic)}&type=mjpeg&quality=${q}&width=${w}&height=${h}`;
    },
  },
  methods: {
    pushLog(text, type = 'pending') {
      this.streamLogs.push({ text, type });
    },
    logClass(log) {
      if (log.type === 'success') return 'text-green-600 dark:text-green-400';
      if (log.type === 'error') return 'text-red-600 dark:text-red-400';
      return 'text-gray-600 dark:text-gray-400';
    },
    onSourceChange() {
      this.streamLogs = [];
      if (this.source === "local") {
        this.streamConnecting = false;
        clearTimeout(this.streamConnectTimeout);
        this.error = null;
        this.startCamera();
      } else {
        this.stopCamera();
        this.error = null;
        if (this.mjpegUrl) {
          this.streamConnecting = true;
          this.pushLog('[1/2] Conectando a web_video_server (MJPEG)…', 'pending');
        }
      }
    },
    onMjpegLoad() {
      this.streamConnecting = false;
      clearTimeout(this.streamConnectTimeout);
      if (this.streamLogs.length) this.pushLog('[2/2] Stream MJPEG activo (usb_cam → web_video_server).', 'success');
      else this.pushLog('Stream MJPEG activo.', 'success');
    },
    onMjpegError() {
      this.streamConnecting = false;
      clearTimeout(this.streamConnectTimeout);
      this.pushLog('Error al cargar el stream MJPEG. Comprueba la IP y que web_video_server esté en ejecución.', 'error');
    },
    async startCamera() {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        this.error = 'Tu navegador no soporta acceso a la cámara.';
        return;
      }
      this.loading = true;
      this.error = null;
      this.pushLog('[1/2] Solicitando acceso a la cámara (getUserMedia)…', 'pending');
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        const video = this.$refs.videoStream;
        if (video) {
          video.srcObject = this.stream;
          this.streamActive = true;
          this.$nextTick(() => this.adjustVideoContainerSize());
        }
        this.pushLog('[2/2] Cámara local activa.', 'success');
      } catch (err) {
        console.error('Error al acceder a la cámara:', err);
        this.pushLog('Error: ' + (err.name === 'NotAllowedError' ? 'Acceso denegado.' : err.name === 'NotFoundError' ? 'No se encontró cámara.' : (err.message || 'error desconocido')), 'error');
        if (err.name === 'NotAllowedError') {
          this.error = 'Se ha denegado el acceso a la cámara. Permítelo en el navegador.';
        } else if (err.name === 'NotFoundError') {
          this.error = 'No se encontró ninguna cámara.';
        } else {
          this.error = 'No se pudo usar la cámara: ' + (err.message || 'error desconocido');
        }
      } finally {
        this.loading = false;
      }
    },
    stopCamera() {
      if (this.stream) {
        this.stream.getTracks().forEach((track) => track.stop());
        this.stream = null;
      }
      this.streamActive = false;
      const video = this.$refs.videoStream;
      if (video && video.srcObject) {
        video.srcObject = null;
      }
    },
    toggleFullscreen() {
      const container = this.$refs.videoContainer;
      if (!container) return;
      if (!document.fullscreenElement) {
        container.requestFullscreen().catch(err => {
          console.error("Error al intentar entrar en pantalla completa:", err);
        });
      } else {
        document.exitFullscreen();
      }
    },
    adjustVideoContainerSize() {
      const container = this.$refs.videoContainer;
      const streamEl = this.$refs.videoStream;
      if (!container || !streamEl) return;

      const width = window.innerWidth;
      const height = window.innerHeight;

      let containerWidth, containerHeight;

      if (width <= 768) {
        containerWidth = width * 0.9;
      } else if (width <= 1024) {
        containerWidth = width * 0.8;
      } else {
        containerWidth = width * 0.6;
      }

      containerHeight = (containerWidth * 9) / 16;

      if (containerHeight > height * 0.6) {
        containerHeight = height * 0.6;
        containerWidth = (containerHeight * 16) / 9;
      }

      container.style.width = `${containerWidth}px`;
      container.style.height = `${containerHeight}px`;
      streamEl.style.width = '100%';
      streamEl.style.height = '100%';
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.adjustVideoContainerSize();
      if (this.source === "local") this.startCamera();
    });
    window.addEventListener("resize", this.adjustVideoContainerSize);
  },
  beforeUnmount() {
    this.stopCamera();
    window.removeEventListener("resize", this.adjustVideoContainerSize);
  },
};
</script>

<style scoped>
.card-panel--relative {
  position: relative;
}
.loading-overlay--video {
  min-height: 120px;
}
.video-container--rounded {
  border-radius: 1rem;
  overflow: hidden;
}
.video-feed {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: #1a202c;
  border-radius: 1rem;
}
.video-feed--img {
  display: block;
}
.video-message--hint {
  font-size: 0.75rem;
  color: var(--text-muted);
}
</style>
