<template>
  <div
      v-if="!hidden && isVisible"
      :class="{
      'force-visible': forceVisible,
      'shake': isShaking,
      'clicked-once': clickCount >= 1,
      'glitch-active': glitchActive
    }"
      :style="glitchStyle"
      class="dimensional-glitch"
      @click="handleClick"
  >
    <!-- Scan lines overlay -->
    <div :style="scanLinesStyle" class="scan-lines"></div>

    <!-- Static noise overlay -->
    <div :style="staticStyle" class="static-noise"></div>

    <!-- RGB displacement layers -->
    <div :style="redLayerStyle" class="rgb-layer red-layer">
      <svg height="100%" width="100%">
        <polygon
            :filter="redFilterUrl"
            :points="polygonPoints"
            fill="rgba(255, 0, 0, 0.4)"
        />
      </svg>
    </div>

    <div :style="greenLayerStyle" class="rgb-layer green-layer">
      <svg height="100%" width="100%">
        <polygon
            :filter="greenFilterUrl"
            :points="polygonPoints"
            fill="rgba(0, 255, 0, 0.4)"
        />
      </svg>
    </div>

    <div :style="blueLayerStyle" class="rgb-layer blue-layer">
      <svg height="100%" width="100%">
        <polygon
            :filter="blueFilterUrl"
            :points="polygonPoints"
            fill="rgba(0, 0, 255, 0.4)"
        />
      </svg>
    </div>

    <!-- Main glitch shape -->
    <svg
        :style="{ transform: `rotate(${shakeRotation}deg)` }"
        height="100%"
        width="100%"
        class="main-glitch"
    >
      <defs>
        <!-- Enhanced glitch effects -->
        <filter :id="`glitch-effect-1-${glitchId}`">
          <feGaussianBlur stdDeviation="0.8"/>
          <feColorMatrix type="saturate" values="2.5"/>
          <feOffset dx="2" dy="1"/>
          <feComposite in2="SourceGraphic" operator="multiply"/>
        </filter>

        <filter :id="`glitch-effect-2-${glitchId}`">
          <feColorMatrix :values="hueRotateValue" type="hueRotate"/>
          <feColorMatrix type="saturate" values="3"/>
          <feOffset :dx="offsetX" :dy="offsetY"/>
          <feComposite in2="SourceGraphic" operator="screen"/>
        </filter>

        <filter :id="`glitch-effect-3-${glitchId}`">
          <feComponentTransfer>
            <feFuncR intercept="0.2" slope="1.8" type="linear"/>
            <feFuncG intercept="-0.2" slope="1.4" type="linear"/>
            <feFuncB intercept="0.1" slope="2.0" type="linear"/>
          </feComponentTransfer>
          <feColorMatrix type="saturate" values="2.8"/>
          <feOffset dx="-1" dy="-2"/>
        </filter>

        <filter :id="`glitch-effect-4-${glitchId}`">
          <feTurbulence baseFrequency="0.9" numOctaves="4" result="noise"/>
          <feDisplacementMap in="SourceGraphic" in2="noise" scale="3"/>
          <feColorMatrix type="saturate" values="0.3"/>
        </filter>

        <filter :id="`glitch-effect-5-${glitchId}`">
          <feGaussianBlur stdDeviation="0.3"/>
          <feColorMatrix type="matrix"
                         values="1.2 -0.2 0.8 0 0.1
                                 0.3 1.5 -0.1 0 -0.05
                                 -0.1 0.4 1.8 0 0.02
                                 0 0 0 1 0"/>
          <feOffset :dx="digitalOffset" dy="0"/>
        </filter>

        <!-- RGB channel filters -->
        <filter :id="`red-filter-${glitchId}`">
          <feColorMatrix type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.6 0"/>
          <feOffset dx="2" dy="0"/>
        </filter>

        <filter :id="`green-filter-${glitchId}`">
          <feColorMatrix type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 0.4 0"/>
          <feOffset dx="-1" dy="1"/>
        </filter>

        <filter :id="`blue-filter-${glitchId}`">
          <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 0.5 0"/>
          <feOffset dx="1" dy="-1"/>
        </filter>
      </defs>

      <polygon
          :points="polygonPoints"
          :stroke="strokeColor"
          :stroke-width="strokeWidth"
          :fill="mainFillColor"
          :filter="glitchFilterUrl"
      />

      <!-- Additional corrupted fragments -->
      <polygon
          v-for="(fragment, index) in corruptedFragments"
          :key="index"
          :fill="fragment.color"
          :filter="fragment.filter"
          :opacity="fragment.opacity"
          :points="fragment.points"
      />
    </svg>

    <!-- Digital artifacts -->
    <div class="digital-artifacts">
      <div
          v-for="(artifact, index) in digitalArtifacts"
          :key="index"
          :style="artifact.style"
          class="artifact"
      ></div>
    </div>
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
      isVisible: false,
      clickCount: 0,
      isShaking: false,
      shakeRotation: 0,
      position: {x: 0, y: 0},
      size: {width: 0, height: 0},
      rotation: 0,
      polygonPoints: '',
      pulsePhase: 0,
      pulseInterval: null,
      glitchInterval: null,
      selectedEffectIndex: Math.floor(Math.random() * 5) + 1,
      glitchActive: false,

      // Enhanced glitch properties
      hueRotateValue: 0,
      offsetX: 0,
      offsetY: 0,
      digitalOffset: 0,
      scanLinePosition: 0,
      staticOpacity: 0,
      corruptedFragments: [],
      digitalArtifacts: [],

      // RGB displacement
      rgbDisplacement: {
        red: {x: 0, y: 0},
        green: {x: 0, y: 0},
        blue: {x: 0, y: 0}
      }
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
        filter: this.forceVisible
            ? 'drop-shadow(0 0 8px rgba(255, 255, 255, 0.6)) saturate(1.5)'
            : 'drop-shadow(2px 2px 8px rgba(0, 0, 0, 0.3))',
        transition: this.isShaking ? 'none' : 'all 0.3s ease',
        mixBlendMode: 'screen'
      };
    },

    scanLinesStyle() {
      return {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: `repeating-linear-gradient(
          0deg,
          transparent,
          transparent 1px,
          rgba(0, 255, 255, 0.1) 1px,
          rgba(0, 255, 255, 0.1) 2px
        )`,
        transform: `translateY(${this.scanLinePosition}px)`,
        opacity: this.glitchActive ? 0.6 : 0.2,
        pointerEvents: 'none'
      };
    },

    staticStyle() {
      return {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: `
          radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px),
          radial-gradient(circle, rgba(0,255,255,0.05) 1px, transparent 1px)
        `,
        backgroundSize: '4px 4px, 6px 6px',
        backgroundPosition: '0 0, 2px 2px',
        opacity: this.staticOpacity,
        pointerEvents: 'none',
        animation: 'static-flicker 0.1s infinite linear'
      };
    },

    redLayerStyle() {
      return {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        transform: `translate(${this.rgbDisplacement.red.x}px, ${this.rgbDisplacement.red.y}px)`,
        mixBlendMode: 'screen',
        pointerEvents: 'none'
      };
    },

    greenLayerStyle() {
      return {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        transform: `translate(${this.rgbDisplacement.green.x}px, ${this.rgbDisplacement.green.y}px)`,
        mixBlendMode: 'screen',
        pointerEvents: 'none'
      };
    },

    blueLayerStyle() {
      return {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        transform: `translate(${this.rgbDisplacement.blue.x}px, ${this.rgbDisplacement.blue.y}px)`,
        mixBlendMode: 'screen',
        pointerEvents: 'none'
      };
    },

    effectIndex() {
      return this.selectedEffectIndex;
    },

    glitchFilterUrl() {
      return `url(#glitch-effect-${this.effectIndex}-${this.glitchId})`;
    },

    redFilterUrl() {
      return `url(#red-filter-${this.glitchId})`;
    },

    greenFilterUrl() {
      return `url(#green-filter-${this.glitchId})`;
    },

    blueFilterUrl() {
      return `url(#blue-filter-${this.glitchId})`;
    },

    strokeColor() {
      if (this.forceVisible) {
        const opacity = (Math.sin(this.pulsePhase) + 1) / 2;
        return `rgba(0, 255, 255, ${0.4 + opacity * 0.6})`;
      }
      return this.glitchActive ? 'rgba(255, 0, 255, 0.8)' : 'rgba(255, 255, 255, 0.3)';
    },

    strokeWidth() {
      return this.forceVisible ? '3' : (this.glitchActive ? '2' : '1');
    },

    mainFillColor() {
      if (this.forceVisible) {
        const pulse = (Math.sin(this.pulsePhase * 2) + 1) / 2;
        return `rgba(255, 255, 255, ${0.2 + pulse * 0.3})`;
      }
      return this.glitchActive ? 'rgba(0, 255, 255, 0.3)' : 'rgba(255, 255, 255, 0.1)';
    }
  },

  mounted() {
    this.generateGlitch();
    this.scheduleAppearance();
    if (this.forceVisible) {
      this.isVisible = true;
      this.startEffects();
    }
  },

  beforeUnmount() {
    this.stopAllEffects();
  },

  watch: {
    forceVisible(newVal) {
      if (newVal) {
        this.isVisible = true;
        this.startEffects();
      } else {
        this.stopEffects();
      }
    }
  },

  methods: {
    scheduleAppearance() {
      if (!this.forceVisible) {
        // Random delay between 1-5 seconds
        const delay = (Math.random() * 4 + 1) * 1000;
        setTimeout(() => {
          this.isVisible = true;
          this.startEffects();
        }, delay);
      }
    },

    generateGlitch() {
      const container = this.$el?.parentElement;
      const containerWidth = container ? container.clientWidth : window.innerWidth;
      const containerHeight = container ? container.clientHeight : window.innerHeight;

      const vhSize = Math.random() * 5 + 10;
      const baseSize = (vhSize / 100) * window.innerHeight;

      const aspectRatio = Math.random() * 1.5 + 0.5;
      this.size.width = baseSize * aspectRatio;
      this.size.height = baseSize;

      this.position.x = Math.random() * (containerWidth - this.size.width);
      this.position.y = Math.random() * (containerHeight - this.size.height);

      this.rotation = Math.random() * 360;
      this.polygonPoints = this.generatePolygonPoints();
      this.generateCorruptedFragments();
      this.generateDigitalArtifacts();
    },

    generatePolygonPoints() {
      const corners = Math.floor(Math.random() * 3) + 3;
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

    generateCorruptedFragments() {
      const fragmentCount = Math.floor(Math.random() * 3) + 2;
      this.corruptedFragments = [];

      for (let i = 0; i < fragmentCount; i++) {
        const fragment = {
          points: this.generateFragmentPoints(),
          color: this.getRandomGlitchColor(),
          filter: `url(#glitch-effect-${Math.floor(Math.random() * 5) + 1}-${this.glitchId})`,
          opacity: Math.random() * 0.4 + 0.2
        };
        this.corruptedFragments.push(fragment);
      }
    },

    generateFragmentPoints() {
      const corners = 3;
      const centerX = this.size.width / 2;
      const centerY = this.size.height / 2;
      const points = [];

      for (let i = 0; i < corners; i++) {
        const angle = (i / corners) * Math.PI * 2 + Math.random();
        const radius = (Math.min(this.size.width, this.size.height) / 4) * Math.random();

        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;

        points.push(`${x},${y}`);
      }

      return points.join(' ');
    },

    generateDigitalArtifacts() {
      const artifactCount = Math.floor(Math.random() * 5) + 3;
      this.digitalArtifacts = [];

      for (let i = 0; i < artifactCount; i++) {
        const artifact = {
          style: {
            position: 'absolute',
            left: Math.random() * this.size.width + 'px',
            top: Math.random() * this.size.height + 'px',
            width: (Math.random() * 10 + 2) + 'px',
            height: (Math.random() * 3 + 1) + 'px',
            backgroundColor: this.getRandomGlitchColor(),
            opacity: Math.random() * 0.8 + 0.2,
            transform: `rotate(${Math.random() * 360}deg)`,
            pointerEvents: 'none'
          }
        };
        this.digitalArtifacts.push(artifact);
      }
    },

    getRandomGlitchColor() {
      const colors = [
        'rgba(255, 0, 255, 0.8)',
        'rgba(0, 255, 255, 0.8)',
        'rgba(255, 255, 0, 0.6)',
        'rgba(255, 0, 0, 0.7)',
        'rgba(0, 255, 0, 0.7)',
        'rgba(0, 0, 255, 0.7)'
      ];
      return colors[Math.floor(Math.random() * colors.length)];
    },

    handleClick() {
      this.clickCount++;

      if (this.clickCount === 1) {
        this.performShake();
        this.intensifyGlitch();
      } else if (this.clickCount === 2) {
        this.$emit('glitch-found', this.glitchId);
        this.hidden = true;
        this.stopAllEffects();
      }
    },

    performShake() {
      this.isShaking = true;
      let shakeCount = 0;
      const maxShakes = 12;

      const shakeInterval = setInterval(() => {
        this.shakeRotation = (Math.random() - 0.5) * 30;
        shakeCount++;

        if (shakeCount >= maxShakes) {
          clearInterval(shakeInterval);
          this.isShaking = false;
          this.shakeRotation = 0;
        }
      }, 60);
    },

    intensifyGlitch() {
      this.glitchActive = true;
      setTimeout(() => {
        this.glitchActive = false;
      }, 2000);
    },

    startEffects() {
      this.startPulse();
      this.startGlitchAnimation();
    },

    stopEffects() {
      this.stopPulse();
      this.stopGlitchAnimation();
    },

    stopAllEffects() {
      this.stopPulse();
      this.stopGlitchAnimation();
    },

    startPulse() {
      if (this.pulseInterval) return;

      this.pulseInterval = setInterval(() => {
        this.pulsePhase += 0.15;
      }, 50);
    },

    stopPulse() {
      if (this.pulseInterval) {
        clearInterval(this.pulseInterval);
        this.pulseInterval = null;
      }
    },

    startGlitchAnimation() {
      if (this.glitchInterval) return;

      this.glitchInterval = setInterval(() => {
        // Animate glitch properties
        this.hueRotateValue = Math.random() * 360;
        this.offsetX = (Math.random() - 0.5) * 6;
        this.offsetY = (Math.random() - 0.5) * 6;
        this.digitalOffset = (Math.random() - 0.5) * 4;
        this.scanLinePosition = (Math.random() - 0.5) * 10;
        this.staticOpacity = Math.random() * 0.3;

        // RGB displacement
        this.rgbDisplacement.red.x = (Math.random() - 0.5) * 4;
        this.rgbDisplacement.red.y = (Math.random() - 0.5) * 2;
        this.rgbDisplacement.green.x = (Math.random() - 0.5) * 3;
        this.rgbDisplacement.green.y = (Math.random() - 0.5) * 3;
        this.rgbDisplacement.blue.x = (Math.random() - 0.5) * 5;
        this.rgbDisplacement.blue.y = (Math.random() - 0.5) * 2;

        // Occasionally regenerate fragments for more chaos
        if (Math.random() < 0.1) {
          this.generateCorruptedFragments();
        }

        if (Math.random() < 0.05) {
          this.generateDigitalArtifacts();
        }
      }, 100);
    },

    stopGlitchAnimation() {
      if (this.glitchInterval) {
        clearInterval(this.glitchInterval);
        this.glitchInterval = null;
      }
    }
  }
};
</script>

<style scoped>
.dimensional-glitch {
  pointer-events: auto;
  will-change: transform, filter;
}

.dimensional-glitch:hover {
  filter: drop-shadow(0 0 12px rgba(0, 255, 255, 0.4)) saturate(2) !important;
}

.force-visible {
  filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.6)) saturate(1.8) !important;
}

.glitch-active {
  filter: drop-shadow(0 0 20px rgba(255, 0, 255, 0.8)) saturate(3) !important;
  animation: glitch-pulse 0.2s ease-in-out infinite alternate;
}

.shake {
  animation: enhanced-glitch-shake 0.06s ease-in-out infinite;
}

.clicked-once {
  filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.7)) saturate(2.5) !important;
}

.rgb-layer {
  will-change: transform;
}

.main-glitch {
  position: relative;
  z-index: 10;
}

.scan-lines {
  will-change: transform, opacity;
}

.static-noise {
  will-change: opacity;
}

.digital-artifacts {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.artifact {
  will-change: transform;
}

@keyframes enhanced-glitch-shake {
  0%, 100% {
    transform: translateX(0) translateY(0) rotate(0deg);
  }
  10% {
    transform: translateX(-3px) translateY(-2px) rotate(-1deg);
  }
  20% {
    transform: translateX(4px) translateY(1px) rotate(1deg);
  }
  30% {
    transform: translateX(-2px) translateY(3px) rotate(-2deg);
  }
  40% {
    transform: translateX(3px) translateY(-1px) rotate(1deg);
  }
  50% {
    transform: translateX(-1px) translateY(2px) rotate(-1deg);
  }
  60% {
    transform: translateX(2px) translateY(-3px) rotate(2deg);
  }
  70% {
    transform: translateX(-4px) translateY(1px) rotate(-1deg);
  }
  80% {
    transform: translateX(1px) translateY(-2px) rotate(1deg);
  }
  90% {
    transform: translateX(-2px) translateY(4px) rotate(-2deg);
  }
}

@keyframes glitch-pulse {
  0% {
    transform: scale(1) skew(0deg);
  }
  100% {
    transform: scale(1.02) skew(0.5deg);
  }
}

@keyframes static-flicker {
  0%, 100% {
    background-position: 0 0, 2px 2px;
  }
  25% {
    background-position: 1px 1px, 3px 1px;
  }
  50% {
    background-position: -1px 0, 1px 3px;
  }
  75% {
    background-position: 2px -1px, 0 1px;
  }
}
</style>