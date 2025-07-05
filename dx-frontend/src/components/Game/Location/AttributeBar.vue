<template>
  <div
    class="dx-attribute-bar"
    :class="{ 'dx-attribute-bar--compact': compact }"
    @click="toggleCompact"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <!-- Bar Container -->
    <div class="dx-attribute-bar__container" :aria-label="`${type} attribute: ${current} out of ${max}`">
      <!-- Background with energy pattern -->
      <div class="dx-attribute-bar__background"></div>

      <!-- Current Value Bar -->
      <div
        class="dx-attribute-bar__current"
        :class="{ 'dx-attribute-bar__current--changing': isChanging }"
        :style="{
          width: `${(current / max) * 100}%`,
          background: gradientColor
        }"
      >
        <!-- Energy flow effect -->
        <div class="dx-attribute-bar__energy-flow"></div>
      </div>

      <!-- Change Indicator (shows when value changes) -->
      <div
        v-if="showDeltas && deltaValue !== 0"
        class="dx-attribute-bar__delta"
        :class="{
          'dx-attribute-bar__delta--positive': deltaValue > 0,
          'dx-attribute-bar__delta--negative': deltaValue < 0
        }"
      >
        {{ deltaValue > 0 ? '+' : '' }}{{ deltaValue }}
      </div>

      <!-- Glow Effect -->
      <div class="dx-attribute-bar__glow"></div>

      <!-- Sharp Border -->
      <div class="dx-attribute-bar__border"></div>
    </div>

    <!-- Values Display -->
    <div class="dx-attribute-bar__values">
<!--      <span class="dx-attribute-bar__type" v-if="!compact || isHovered">{{ type }}</span>-->
      <span class="dx-attribute-bar__numbers">{{ current }} / {{ max }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';

// Props
const props = defineProps({
  current: {
    type: Number,
    required: true
  },
  max: {
    type: Number,
    required: true
  },
  type: {
    type: String,
    required: true // "Health", "Energy", "Action Points"
  },
  showDeltas: {
    type: Boolean,
    default: true
  },
  compact: {
    type: Boolean,
    default: false
  },
  theme: {
    type: String,
    default: 'default' // 'combat', 'exploration', 'default'
  }
});

// Reactive state
const previousValue = ref(props.current);
const deltaValue = ref(0);
const isChanging = ref(false);
const isHovered = ref(false);
const localCompact = ref(props.compact);

// Computed properties
const gradientColor = computed(() => {
  switch (props.type) {
    case "Health":
      return "linear-gradient(90deg, rgba(220,20,60,1) 0%, rgba(255,69,0,1) 100%)";
    case "Energy":
      return "linear-gradient(90deg, rgba(0,191,255,1) 0%, rgba(30,144,255,1) 100%)";
    case "Action Points":
      return "linear-gradient(90deg, rgba(50,205,50,1) 0%, rgba(0,255,0,1) 100%)";
    default:
      return "linear-gradient(90deg, rgba(192,192,192,1) 0%, rgba(255,215,0,1) 100%)";
  }
});

// Watch for changes in current value
watch(() => props.current, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    deltaValue.value = newValue - oldValue;
    previousValue.value = oldValue;
    isChanging.value = true;

    // Reset changing state after animation completes
    setTimeout(() => {
      isChanging.value = false;
    }, 1500);

    // Reset delta display after a delay
    setTimeout(() => {
      deltaValue.value = 0;
    }, 2000);
  }
});

// Methods
const toggleCompact = () => {
  localCompact.value = !localCompact.value;
};

// Lifecycle hooks
onMounted(() => {
  // Initialize with current value
  previousValue.value = props.current;
});
</script>

<style scoped>
/* CSS Variables for theming */
:root {
  --dx-primary-blue: #00BFFF;
  --dx-secondary-blue: #1E90FF;
  --dx-primary-green: #00FF00;
  --dx-secondary-green: #32CD32;
  --dx-primary-red: #FF0000;
  --dx-secondary-red: #DC143C;
  --dx-primary-gold: #FFD700;
  --dx-primary-silver: #C0C0C0;
  --dx-bg-dark: #1A1A1A;
  --dx-bg-darker: #000000;
  --dx-text-light: rgba(255, 255, 255, 0.9);
  --dx-border-light: rgba(255, 255, 255, 0.3);
  --dx-glow-intensity: 0.6;
  --dx-animation-speed: 0.3s;
}

/* Main Container */
.dx-attribute-bar {
  position: relative;
  width: 100%;
  height: 1rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: height var(--dx-animation-speed) ease;
  will-change: transform, opacity;
}

.dx-attribute-bar--compact {
  height: 0.6rem;
}

/* Bar Container */
.dx-attribute-bar__container {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 0.25rem;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

/* Background with pattern */
.dx-attribute-bar__background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--dx-bg-dark);
  background-image:
    linear-gradient(90deg,
      rgba(30, 30, 30, 0.5) 1px,
      transparent 1px),
    linear-gradient(0deg,
      rgba(30, 30, 30, 0.5) 1px,
      transparent 1px);
  background-size: 10px 10px;
  opacity: 0.3;
}

/* Current Value Bar */
.dx-attribute-bar__current {
  position: relative;
  height: 100%;
  transition: width 0.5s cubic-bezier(0.25, 1, 0.5, 1);
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
  clip-path: polygon(
    0 0,
    calc(100% - 5px) 0,
    100% 50%,
    calc(100% - 5px) 100%,
    0 100%
  );
}

/* Energy flow animation */
.dx-attribute-bar__energy-flow {
  position: absolute;
  top: 0;
  left: 0;
  width: 200%;
  height: 100%;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.2) 50%,
    transparent 100%);
  animation: flowAnimation 2s linear infinite;
}

@keyframes flowAnimation {
  0% {
    transform: translateX(-50%);
  }
  100% {
    transform: translateX(0%);
  }
}

/* Changing animation */
.dx-attribute-bar__current--changing {
  animation: pulseAnimation 0.5s ease-in-out;
}

@keyframes pulseAnimation {
  0%, 100% {
    filter: brightness(1);
  }
  50% {
    filter: brightness(1.5);
  }
}

/* Delta indicator */
.dx-attribute-bar__delta {
  position: absolute;
  top: -1.5rem;
  right: 0;
  font-size: 0.8rem;
  font-weight: bold;
  padding: 0.1rem 0.3rem;
  border-radius: 0.25rem;
  animation: fadeUpAndOut 2s forwards;
  z-index: 10;
}

.dx-attribute-bar__delta--positive {
  color: var(--dx-primary-green);
  text-shadow: 0 0 5px rgba(0, 255, 0, 0.7);
}

.dx-attribute-bar__delta--negative {
  color: var(--dx-primary-red);
  text-shadow: 0 0 5px rgba(255, 0, 0, 0.7);
}

@keyframes fadeUpAndOut {
  0% {
    opacity: 0;
    transform: translateY(0);
  }
  10% {
    opacity: 1;
  }
  80% {
    opacity: 1;
    transform: translateY(-10px);
  }
  100% {
    opacity: 0;
    transform: translateY(-20px);
  }
}

/* Glow effect */
.dx-attribute-bar__glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  box-shadow: inset 0 0 15px rgba(255, 255, 255, 0.3);
  pointer-events: none;
}

/* Sharp border */
.dx-attribute-bar__border {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 1px solid var(--dx-border-light);
  border-radius: 0.25rem;
  box-sizing: border-box;
  pointer-events: none;
}

/* Values display */
.dx-attribute-bar__values {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  transform: translateY(-50%);
  padding: 0 0.5rem;
  box-sizing: border-box;
  pointer-events: none;
  z-index: 5;
}

.dx-attribute-bar__type {
  font-size: 0.7rem;
  font-weight: bold;
  color: var(--dx-text-light);
  text-shadow: 0 0 3px rgba(0, 0, 0, 0.8);
  transition: opacity var(--dx-animation-speed) ease;
}

.dx-attribute-bar__numbers {
  font-size: 0.7rem;
  font-weight: bold;
  color: var(--dx-text-light);
  text-shadow: 0 0 3px rgba(0, 0, 0, 0.8);
  margin-left: auto;
}

/* Hover effects */
.dx-attribute-bar:hover {
  transform: translateY(-1px);
  filter: brightness(1.1);
}

/* Accessibility - reduced motion */
@media (prefers-reduced-motion: reduce) {
  .dx-attribute-bar__current,
  .dx-attribute-bar__energy-flow,
  .dx-attribute-bar__delta {
    animation: none;
    transition: none;
  }
}
</style>