<template>
  <div
      v-if="isVisible"
      :style="glitchStyle"
      class="glitch-effect"
      @click="handleClick"
  >
    <div class="glitch-inner"></div>
  </div>
</template>

<script>
export default {
  name: "GlitchEffect",
  props: {
    containerSelector: {
      type: String,
      default: ".location-view" // Default to the main location view
    },
    minSize: {
      type: Number,
      default: 2 // Minimum size as percentage of screen
    },
    maxSize: {
      type: Number,
      default: 15 // Maximum size as percentage of screen
    },
    appearChance: {
      type: Number,
      default: 0.3 // 30% chance to appear when triggered
    },
    onGlitchClick: {
      type: Function,
      default: () => {
      }
    }
  },
  data() {
    return {
      isVisible: false,
      position: {x: 0, y: 0},
      size: {width: 0, height: 0},
      rotation: 0,
      clipPath: "",
      filter: ""
    };
  },
  computed: {
    glitchStyle() {
      return {
        left: `${this.position.x}%`,
        top: `${this.position.y}%`,
        width: `${this.size.width}%`,
        height: `${this.size.height}%`,
        transform: `rotate(${this.rotation}deg)`,
        clipPath: this.clipPath,
        filter: this.filter
      };
    }
  },
  mounted() {
    // Set up interval to randomly show the glitch
    setInterval(() => {
      this.tryToAppear();
    }, 30000); // Try to appear every 30 seconds

    // Initial attempt to appear
    setTimeout(() => {
      this.tryToAppear();
    }, 5000); // First attempt after 5 seconds
  },
  methods: {
    tryToAppear() {
      // Only appear based on chance
      if (Math.random() < this.appearChance) {
        this.generateRandomProperties();
        this.isVisible = true;

        // Auto-hide after a random time between 10-30 seconds
        setTimeout(() => {
          this.isVisible = false;
        }, 10000 + Math.random() * 20000);
      }
    },
    generateRandomProperties() {
      // Generate random size
      const width = this.minSize + Math.random() * (this.maxSize - this.minSize);
      const height = this.minSize + Math.random() * (this.maxSize - this.minSize);

      // Generate random position (ensuring it stays within container)
      const x = Math.random() * (100 - width);
      const y = Math.random() * (100 - height);

      // Generate random rotation
      const rotation = Math.random() * 360;

      // Generate random broken glass clip path
      this.clipPath = this.generateBrokenShape();

      // Generate random filter effects
      this.filter = this.generateRandomFilter();

      // Set the properties
      this.position = {x, y};
      this.size = {width, height};
      this.rotation = rotation;
    },
    generateBrokenShape() {
      // Create a jagged, broken-glass-like polygon
      const points = [];
      const numPoints = 8 + Math.floor(Math.random() * 8); // 8-15 points

      for (let i = 0; i < numPoints; i++) {
        const angle = (i / numPoints) * 2 * Math.PI;
        // Vary the radius to create jagged edges
        const radius = 45 + Math.random() * 10;
        const x = 50 + radius * Math.cos(angle);
        const y = 50 + radius * Math.sin(angle);
        points.push(`${x}% ${y}%`);
      }

      return `polygon(${points.join(', ')})`;
    },
    generateRandomFilter() {
      // Generate random visual effects using CSS filters
      const hueRotate = Math.floor(Math.random() * 360);
      const saturate = 100 + Math.floor(Math.random() * 200);
      const brightness = 80 + Math.floor(Math.random() * 50);
      const contrast = 100 + Math.floor(Math.random() * 50);

      return `hue-rotate(${hueRotate}deg) saturate(${saturate}%) brightness(${brightness}%) contrast(${contrast}%)`;
    },
    handleClick() {
      // Hide the glitch when clicked
      this.isVisible = false;

      // Call the provided callback
      this.onGlitchClick();
    }
  }
};
</script>

<style scoped>
.glitch-effect {
  position: absolute;
  pointer-events: auto;
  cursor: pointer;
  z-index: 100;
  overflow: hidden;
  opacity: 0.7;
  transition: opacity 0.3s;
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
}

.glitch-effect:hover {
  opacity: 0.9;
}

.glitch-inner {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, rgba(255, 255, 255, 0.2), rgba(0, 255, 255, 0.3), rgba(255, 0, 255, 0.3));
  animation: glitch-animation 5s infinite alternate;
  backdrop-filter: blur(2px);
}

@keyframes glitch-animation {
  0% {
    background-position: 0% 0%;
  }
  20% {
    background-position: 20% 20%;
  }
  40% {
    background-position: 40% 40%;
    transform: skewX(5deg);
  }
  60% {
    background-position: 60% 60%;
    transform: skewX(-5deg);
  }
  80% {
    background-position: 80% 80%;
  }
  100% {
    background-position: 100% 100%;
  }
}
</style>