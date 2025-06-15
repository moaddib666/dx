<template>
  <div
      :class="{ 'force-visible': forceVisible, 'discovered': discovered }"
      :style="glitchStyle"
      class="dimensional-glitch"
      @click="handleGlitchClick"
  >
    <svg
        :style="{ filter: currentFilter }"
        height="100%"
        width="100%"
    >
      <defs>
        <!-- Glitch pattern - more subtle glass-like effect -->
        <pattern
            :id="`glitch-pattern-${glitchId}`"
            height="8"
            patternUnits="userSpaceOnUse"
            width="8"
        >
          <rect fill="transparent" height="8" width="8"/>
          <rect fill="rgba(255,255,255,0.15)" height="1" width="1"/>
          <rect fill="rgba(255,255,255,0.12)" height="1" width="1" x="4" y="4"/>
          <rect fill="rgba(200,200,255,0.1)" height="1" width="1" x="2" y="6"/>
        </pattern>

        <!-- Noise filter for distortion - more subtle glass crack effect -->
        <filter :id="`noise-${glitchId}`">
          <feTurbulence
              baseFrequency="0.5"
              numOctaves="2"
              result="noise"
              type="fractalNoise"
          />
          <feDisplacementMap
              :scale="discovered ? '2' : '0.5'"
              in="SourceGraphic"
              in2="noise"
          />
        </filter>
      </defs>

      <!-- Main cracked shape - more realistic glass crack -->
      <path
          :d="crackedPath"
          :fill="`url(#glitch-pattern-${glitchId})`"
          :filter="`url(#noise-${glitchId})`"
          :stroke="discovered || forceVisible ? 'rgba(255,255,255,0.7)' : 'rgba(255,255,255,0.05)'"
          :stroke-width="discovered || forceVisible ? '1.2' : '0.3'"
      />

      <!-- Additional fractal lines - subtle crack extensions -->
      <line
          v-for="(line, i) in fractalLines"
          :key="i"
          :opacity="discovered || forceVisible ? 0.7 : 0.15"
          :stroke="discovered || forceVisible ? 'rgba(255,255,255,0.6)' : 'rgba(255,255,255,0.03)'"
          :stroke-width="discovered || forceVisible ? '0.8' : '0.2'"
          :x1="line.x1"
          :x2="line.x2"
          :y1="line.y1"
          :y2="line.y2"
      />
    </svg>

    <!-- Content slot for any text or elements -->
    <div v-if="$slots.default" class="glitch-content">
      <slot></slot>
    </div>

    <!-- Pulse effect when discovered or force visible -->
    <div
        v-if="discovered || forceVisible"
        :class="{ 'force-visible-pulse': forceVisible && !discovered }"
        class="dimensional-pulse"
    />
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
  emits: ['glitch-clicked'],
  data() {
    return {
      discovered: false,
      position: {x: 0, y: 0},
      size: {width: 100, height: 105},
      rotation: 0,
      opacity: 0.1,
      glitchType: 0,
      crackedPath: '',
      fractalLines: []
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
        opacity: this.discovered || this.forceVisible ? 0.9 : this.opacity, // Increased opacity for better visibility
        pointerEvents: 'auto',
        cursor: 'pointer',
        transition: this.discovered ? 'all 0.5s ease-out' : 'none',
        zIndex: 100, // Lower z-index so it doesn't appear above important UI
        mixBlendMode: 'screen', // Blend with background
        backdropFilter: 'blur(0.3px)' // Subtle blur effect behind cracks
      };
    },
    currentFilter() {
      if (this.discovered || this.forceVisible) {
        // Enhanced highlight effect for better visibility
        return 'brightness(150%) contrast(120%) drop-shadow(0 0 4px rgba(255,255,255,0.5))';
      }

      // More subtle effects for undiscovered state
      switch (this.glitchType) {
        case 0:
          return 'brightness(105%) contrast(102%) drop-shadow(0 0 1px rgba(255,255,255,0.1))';
        case 1:
          return 'brightness(103%) contrast(101%) drop-shadow(0 0 0.5px rgba(255,255,255,0.08))';
        case 2:
          return 'brightness(102%) contrast(100%) drop-shadow(0 0 0.3px rgba(255,255,255,0.05))';
        default:
          return 'none';
      }
    }
  },
  mounted() {
    // Use nextTick to ensure the component is fully rendered before calculating dimensions
    this.$nextTick(() => {
      // Add a small random delay to stagger the appearance of multiple glitches
      setTimeout(() => {
        this.generateGlitch();
      }, Math.random() * 500); // Random delay up to 500ms
    });
  },
  methods: {
    generateGlitch() {
      // Get container dimensions
      const container = this.$el.parentElement;
      const containerWidth = container ? container.clientWidth : window.innerWidth;
      const containerHeight = container ? container.clientHeight : window.innerHeight;

      // Generate random size (5%-25% of screen) - increased range for more variety
      const minSize = Math.min(containerWidth, containerHeight) * 0.05;
      const maxSize = Math.min(containerWidth, containerHeight) * 0.25;

      // Randomly decide if width and height should be similar or different
      const sameSize = Math.random() > 0.5;

      if (sameSize) {
        const size = Math.random() * (maxSize - minSize) + minSize;
        this.size.width = size;
        this.size.height = size;
      } else {
        this.size.width = Math.random() * (maxSize - minSize) + minSize;
        this.size.height = Math.random() * (maxSize - minSize) + minSize;
      }

      // Generate random position - ensure it's fully visible within container
      const margin = Math.min(containerWidth, containerHeight) * 0.05; // 5% margin
      this.position.x = margin + Math.random() * (containerWidth - this.size.width - (2 * margin));
      this.position.y = margin + Math.random() * (containerHeight - this.size.height - (2 * margin));

      // Generate random properties with more variation
      this.rotation = Math.random() * 360;
      this.opacity = Math.random() * 0.5 + 0.2; // Increased opacity range (0.2-0.7)
      this.glitchType = Math.floor(Math.random() * 3);

      // Generate cracked glass path
      this.crackedPath = this.generateCrackedPath();

      // Generate fractal lines
      this.fractalLines = this.generateFractalLines();
    },

    generateCrackedPath() {
      // Create a more realistic glass crack pattern
      const centerX = this.size.width / 2;
      const centerY = this.size.height / 2;

      // Randomize the impact point slightly off-center
      const impactX = centerX + (Math.random() - 0.5) * this.size.width * 0.3;
      const impactY = centerY + (Math.random() - 0.5) * this.size.height * 0.3;

      // Determine number of primary cracks (3-7)
      const numPrimaryCracks = Math.floor(Math.random() * 5) + 3;

      let path = `M ${impactX} ${impactY}`;

      // Create primary cracks radiating from impact point
      for (let i = 0; i < numPrimaryCracks; i++) {
        // Randomize angle with some clustering
        const baseAngle = (i / numPrimaryCracks) * Math.PI * 2;
        const angleVariation = (Math.random() - 0.5) * 0.5; // Small variation
        const angle = baseAngle + angleVariation;

        // Randomize length of crack
        const maxDimension = Math.max(this.size.width, this.size.height);
        const crackLength = Math.random() * maxDimension * 0.4 + maxDimension * 0.1;

        // Add some waviness to the crack
        const segments = Math.floor(Math.random() * 3) + 2;
        let currentX = impactX;
        let currentY = impactY;

        for (let j = 0; j < segments; j++) {
          const segmentLength = crackLength / segments;
          const segmentAngle = angle + (Math.random() - 0.5) * 0.3; // Slight angle variation

          const endX = currentX + Math.cos(segmentAngle) * segmentLength;
          const endY = currentY + Math.sin(segmentAngle) * segmentLength;

          // First segment starts from impact point
          if (j === 0 && i === 0) {
            path += ` L ${endX} ${endY}`;
          } else {
            // Use quadratic curves for more natural cracks
            const controlX = currentX + Math.cos(segmentAngle) * segmentLength * 0.5 + (Math.random() - 0.5) * 5;
            const controlY = currentY + Math.sin(segmentAngle) * segmentLength * 0.5 + (Math.random() - 0.5) * 5;
            path += ` M ${currentX} ${currentY} Q ${controlX} ${controlY} ${endX} ${endY}`;
          }

          currentX = endX;
          currentY = endY;
        }
      }

      return path; // No 'Z' to keep cracks open-ended
    },

    generateFractalLines() {
      // Generate more realistic secondary cracks
      const numLines = Math.floor(Math.random() * 5) + 5; // 5-10 lines
      const lines = [];

      // Get dimensions for constraining lines
      const centerX = this.size.width / 2;
      const centerY = this.size.height / 2;

      for (let i = 0; i < numLines; i++) {
        // Start points more likely to be near center
        const startDistanceFromCenter = Math.random() * this.size.width * 0.3;
        const startAngle = Math.random() * Math.PI * 2;
        const x1 = centerX + Math.cos(startAngle) * startDistanceFromCenter;
        const y1 = centerY + Math.sin(startAngle) * startDistanceFromCenter;

        // End points more likely to be toward edges
        const length = Math.random() * this.size.width * 0.2 + this.size.width * 0.05;
        const endAngle = startAngle + (Math.random() - 0.5) * 0.8; // Slight deviation
        const x2 = x1 + Math.cos(endAngle) * length;
        const y2 = y1 + Math.sin(endAngle) * length;

        lines.push({x1, y1, x2, y2});
      }

      return lines;
    },

    generateGlitchId() {
      return `glitch_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    },

    handleGlitchClick() {
      if (this.discovered) return;

      this.discovered = true;
      this.$emit('glitch-clicked', this.glitchId);

      // Auto-hide after animation
      setTimeout(() => {
        if (this.$el) {
          this.$el.style.display = 'none';
        }
      }, 2000);
    }
  }
};
</script>

<style scoped>
.dimensional-glitch {
  pointer-events: auto;
  position: relative;
  cursor: pointer;
  /* Add subtle glass-like reflection */
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.01) 0%, rgba(255, 255, 255, 0) 50%, rgba(255, 255, 255, 0.02) 100%);
}

.dimensional-glitch:hover:not(.discovered):not(.force-visible) svg {
  /* More subtle hover effect */
  filter: brightness(110%) contrast(105%) drop-shadow(0 0 1px rgba(255, 255, 255, 0.2)) !important;
}

.force-visible {
  opacity: 0.9 !important; /* Increased for better visibility */
  animation: forceVisiblePulse 2s infinite alternate; /* Add pulsing animation to draw attention */
}

.force-visible svg path {
  stroke: rgba(255, 255, 255, 0.8) !important; /* Increased opacity for better visibility */
  stroke-width: 1.5 !important; /* Increased for better visibility */
}

.force-visible svg line {
  stroke: rgba(255, 255, 255, 0.7) !important; /* Increased opacity for better visibility */
  opacity: 0.8 !important; /* Increased for better visibility */
}

.discovered {
  animation: dimensionalFlicker 0.3s ease-out; /* Reduced duration */
}

/* Style for content inside the glitch - more subtle */
.glitch-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: rgba(255, 255, 255, 0.5); /* Changed from cyan to white with lower opacity */
  font-family: monospace;
  font-size: 0.8rem; /* Smaller font */
  text-shadow: 0 0 2px rgba(255, 255, 255, 0.3); /* Reduced glow */
  z-index: 101; /* Lower z-index */
  pointer-events: none;
  text-align: center;
  width: 100%;
  padding: 5px;
  mix-blend-mode: overlay; /* Changed from screen for better blending */
  animation: glitchText 3s infinite alternate; /* Slower animation */
  opacity: 0.7; /* Base opacity reduced */
}

.force-visible .glitch-content {
  opacity: 0.8; /* Reduced from 1 */
  color: rgba(255, 255, 255, 0.7); /* Changed from cyan to white with lower opacity */
  text-shadow: 0 0 3px rgba(255, 255, 255, 0.4); /* Reduced glow */
}

.dimensional-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 150%; /* Reduced from 200% */
  height: 150%; /* Reduced from 200% */
  transform: translate(-50%, -50%);
  background: radial-gradient(circle, rgba(255, 255, 255, 0.05) 0%, transparent 70%); /* Changed from cyan to white with lower opacity */
  border-radius: 50%;
  animation: dimensionalPulse 0.8s ease-out; /* Reduced duration */
  pointer-events: none;
  opacity: 0.7; /* Added base opacity */
}

.force-visible-pulse {
  animation: forceVisiblePulseEffect 3s infinite ease-in-out !important;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  width: 180%;
  height: 180%;
}

@keyframes dimensionalPulse {
  0% {
    transform: translate(-50%, -50%) scale(0.1);
    opacity: 0.5; /* Reduced from 1 */
  }
  100% {
    transform: translate(-50%, -50%) scale(1.5); /* Reduced from 2 */
    opacity: 0;
  }
}

@keyframes dimensionalFlicker {
  0%, 100% {
    opacity: 0.7;
  }
  /* Reduced from 1 */
  20% {
    opacity: 0.2;
    transform: scale(1.05) rotate(2deg);
  }
  /* Reduced scale and rotation */
  40% {
    opacity: 0.5;
    transform: scale(0.98) rotate(-1deg);
  }
  /* Reduced scale and rotation */
  60% {
    opacity: 0.3;
    transform: scale(1.02) rotate(1deg);
  }
  /* Reduced scale and rotation */
  80% {
    opacity: 0.6;
    transform: scale(0.99) rotate(-0.5deg);
  }
  /* Reduced scale and rotation */
}

@keyframes glitchText {
  0%, 100% {
    opacity: 0.6;
    transform: translate(-50%, -50%) scale(1);
  }
  /* Reduced opacity */
  25% {
    opacity: 0.4;
    transform: translate(-50.5%, -49.5%) scale(1.01);
  }
  /* Reduced movement and scale */
  50% {
    opacity: 0.7;
    transform: translate(-49.5%, -50.5%) scale(0.99);
  }
  /* Reduced movement and scale */
  75% {
    opacity: 0.5;
    transform: translate(-50.2%, -49.8%) scale(1.005);
  }
  /* Reduced movement and scale */
}

@keyframes forceVisiblePulse {
  0% {
    opacity: 0.7;
    filter: drop-shadow(0 0 2px rgba(255, 255, 255, 0.3));
  }
  50% {
    opacity: 1;
    filter: drop-shadow(0 0 6px rgba(255, 255, 255, 0.7));
  }
  100% {
    opacity: 0.8;
    filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.5));
  }
}

@keyframes forceVisiblePulseEffect {
  0% {
    transform: translate(-50%, -50%) scale(0.9);
    opacity: 0.3;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.1);
    opacity: 0.7;
  }
  100% {
    transform: translate(-50%, -50%) scale(0.9);
    opacity: 0.3;
  }
}
</style>
