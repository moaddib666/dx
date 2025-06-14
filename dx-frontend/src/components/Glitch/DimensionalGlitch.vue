<template>
  <div
      v-if="!hidden"
      :class="{
      'force-visible': forceVisible,
      'shake': isShaking,
      'clicked-once': clickCount >= 1
    }"
      :style="glitchStyle"
      class="dimensional-glitch"
      @click="handleClick"
  >
    <svg
        :style="{ transform: `rotate(${shakeRotation}deg)` }"
        height="100%"
        width="100%"
    >
      <defs>
        <filter id="glass-effect">
          <feGaussianBlur stdDeviation="1"/>
          <feColorMatrix type="saturate" values="0.3"/>
        </filter>
      </defs>

      <polygon
          :points="polygonPoints"
          :stroke="strokeColor"
          :stroke-width="strokeWidth"
          fill="rgba(255, 255, 255, 0.05)"
          filter="url(#glass-effect)"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: "DimensionalGlitch",
  props: {
    forceVisible: {
      type: Boolean,
      required: false,
      default: false
    },
    glitchId: {
      type: String,
      required: false,
      default: () => `glitch_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    }
  },
  emits: ['glitch-found'],
  data() {
    return {
      hidden: false,
      clickCount: 0,
      isShaking: false,
      shakeRotation: 0,
      position: {x: 0, y: 0},
      size: {width: 0, height: 0},
      rotation: 0,
      polygonPoints: '',
      pulsePhase: 0,
      pulseInterval: null
    };
  },
  computed: {
    glitchStyle() {
      return {
        position: 'absolute',
        left: this.position.x + 'px',
        top: this.position.y + 'px',
        width: this.size.width + 'px',
        height: this.size.height + 'px',
        transform: `rotate(${this.rotation}deg)`,
        cursor: 'pointer',
        zIndex: 1000,
        backdropFilter: this.backdropEffect,
        WebkitBackdropFilter: this.backdropEffect,
        filter: 'drop-shadow(2px 2px 8px rgba(0, 0, 0, 0.3))',
        transition: this.isShaking ? 'none' : 'all 0.3s ease'
      };
    },
    backdropEffect() {
      const effects = [
        'saturate(0.4) blur(1px)',
        'hue-rotate(180deg) saturate(0.6)',
        'contrast(1.2) saturate(0.5)',
        'sepia(0.3) saturate(0.7)',
        'blur(0.5px) brightness(0.8)'
      ];
      return effects[Math.floor(Math.random() * effects.length)];
    },
    strokeColor() {
      if (this.forceVisible) {
        const opacity = (Math.sin(this.pulsePhase) + 1) / 2;
        return `rgba(255, 255, 255, ${0.3 + opacity * 0.7})`;
      }
      return 'transparent';
    },
    strokeWidth() {
      return this.forceVisible ? '2' : '0';
    }
  },
  mounted() {
    this.generateGlitch();
    if (this.forceVisible) {
      this.startPulse();
    }
  },
  beforeUnmount() {
    if (this.pulseInterval) {
      clearInterval(this.pulseInterval);
    }
  },
  watch: {
    forceVisible(newVal) {
      if (newVal) {
        this.startPulse();
      } else {
        this.stopPulse();
      }
    }
  },
  methods: {
    generateGlitch() {
      // Get container dimensions
      const container = this.$el?.parentElement;
      const containerWidth = container ? container.clientWidth : window.innerWidth;
      const containerHeight = container ? container.clientHeight : window.innerHeight;

      // Generate random size (10vh to 15vh)
      const vhSize = Math.random() * 5 + 10; // 10-15vh
      const baseSize = (vhSize / 100) * window.innerHeight;

      // Random proportions
      const aspectRatio = Math.random() * 1.5 + 0.5; // 0.5 to 2.0
      this.size.width = baseSize * aspectRatio;
      this.size.height = baseSize;

      // Generate random position
      this.position.x = Math.random() * (containerWidth - this.size.width);
      this.position.y = Math.random() * (containerHeight - this.size.height);

      // Random rotation
      this.rotation = Math.random() * 360;

      // Generate polygon points
      this.polygonPoints = this.generatePolygonPoints();
    },

    generatePolygonPoints() {
      const corners = Math.floor(Math.random() * 3) + 3; // 3-5 corners
      const centerX = this.size.width / 2;
      const centerY = this.size.height / 2;
      const points = [];

      for (let i = 0; i < corners; i++) {
        const angle = (i / corners) * Math.PI * 2;
        const radiusX = (this.size.width / 2) * (0.6 + Math.random() * 0.4);
        const radiusY = (this.size.height / 2) * (0.6 + Math.random() * 0.4);

        const x = centerX + Math.cos(angle) * radiusX;
        const y = centerY + Math.sin(angle) * radiusY;

        points.push(`${x},${y}`);
      }

      return points.join(' ');
    },

    handleClick() {
      this.clickCount++;

      if (this.clickCount === 1) {
        // First click: shake effect
        this.performShake();
      } else if (this.clickCount === 2) {
        // Second click: emit event and hide
        this.$emit('glitch-found', this.glitchId);
        this.hidden = true;
      }
    },

    performShake() {
      this.isShaking = true;
      let shakeCount = 0;
      const maxShakes = 8;

      const shakeInterval = setInterval(() => {
        this.shakeRotation = (Math.random() - 0.5) * 20; // ±10 degrees
        shakeCount++;

        if (shakeCount >= maxShakes) {
          clearInterval(shakeInterval);
          this.isShaking = false;
          this.shakeRotation = 0;
        }
      }, 80);
    },

    startPulse() {
      if (this.pulseInterval) return;

      this.pulseInterval = setInterval(() => {
        this.pulsePhase += 0.2;
      }, 50);
    },

    stopPulse() {
      if (this.pulseInterval) {
        clearInterval(this.pulseInterval);
        this.pulseInterval = null;
      }
    }
  }
};
</script>

<style scoped>
.dimensional-glitch {
  pointer-events: auto;
}

.dimensional-glitch:hover {
  filter: drop-shadow(2px 2px 12px rgba(255, 255, 255, 0.2)) !important;
}

.force-visible {
  filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.4)) !important;
}

.shake {
  animation: glitch-shake 0.1s ease-in-out infinite;
}

.clicked-once {
  filter: drop-shadow(0 0 6px rgba(0, 255, 255, 0.5)) !important;
}

@keyframes glitch-shake {
  0%, 100% {
    transform: translateX(0) translateY(0);
  }
  25% {
    transform: translateX(-2px) translateY(-1px);
  }
  50% {
    transform: translateX(2px) translateY(1px);
  }
  75% {
    transform: translateX(-1px) translateY(2px);
  }
}
</style>