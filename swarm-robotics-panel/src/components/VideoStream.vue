<template>
  <div class="bg-gray-800 p-6 mt-6 rounded-lg">
    <h2 class="text-xl md:text-2xl mb-4">Live Video Stream</h2>
    <div class="video-container mx-auto" ref="videoContainer">
      <img id="videoStream" :src="videoStreamSrc" alt="ROS Video Stream" />
      <button @click="toggleFullscreen" class="fullscreen-btn">
        <i class="fas fa-expand"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "VideoStream",
  data() {
    return {
      videoStreamSrc: 'http://atriz-project.duckdns.org/video/stream?topic=/usb_cam/image_raw',
    };
  },
  methods: {
    toggleFullscreen() {
      if (!document.fullscreenElement) {
        this.$refs.videoContainer.requestFullscreen().catch(err => {
          console.error("Error al intentar entrar en pantalla completa:", err);
        });
      } else {
        document.exitFullscreen();
      }
    },
    adjustVideoContainerSize() {
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

      this.$refs.videoContainer.style.width = `${containerWidth}px`;
      this.$refs.videoContainer.style.height = `${containerHeight}px`;

      this.$refs.videoStream.style.width = '100%';
      this.$refs.videoStream.style.height = '100%';
    },
  },
  mounted() {
    this.adjustVideoContainerSize();
    window.addEventListener('resize', this.adjustVideoContainerSize);
  },
};
</script>
