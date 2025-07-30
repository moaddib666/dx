<template>
  <div class="character-stats">
    <!-- Normal Mode (≥30em) -->
    <div v-if="!isCompact" class="normal-stats">
      <div
          v-for="(attr, key) in details.attributes"
          :key="key"
          :class="['stat-row', `stat-${key}`]"
      >
        <div class="stat-info">
          <span class="stat-value">{{ attr.current }}/{{ attr.max }}</span>
        </div>
        <div class="stat-bar">
          <div
              class="stat-fill"
              :style="getStatBarStyle(attr, key)"
          ></div>
        </div>
      </div>
    </div>

    <!-- Compact Mode (<30em) -->
    <div v-else class="compact-stats">
      <div
          v-for="(attr, key, index) in getDisplayAttributes()"
          :key="key"
          :class="['stat-dot', `stat-${key}`]"
          :title="`${getStatLabel(key)}: ${attr.current}/${attr.max}`"
      >
        <div
            class="stat-circle"
            :style="getCircleStyle(attr, key)"
        >
          <span class="stat-number">{{ attr.current }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, defineProps } from 'vue'

const props = defineProps({
  details: {
    type: Object,
    required: true
  }
})

const windowWidth = ref(window.innerWidth)
const isCompact = computed(() => windowWidth.value < 480) // 30em * 16px

const statConfig = {
  health: {
    label: 'HP',
    color: '#e74c3c',
    glowColor: 'rgba(231, 76, 60, 0.3)'
  },
  energy: {
    label: 'EN',
    color: '#3498db',
    glowColor: 'rgba(52, 152, 219, 0.3)'
  },
  action: {
    label: 'AP',
    color: '#9b59b6',
    glowColor: 'rgba(155, 89, 182, 0.3)'
  }
}

const updateWindowWidth = () => {
  windowWidth.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', updateWindowWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateWindowWidth)
})

const getStatLabel = (key) => {
  return statConfig[key]?.label || key.toUpperCase()
}

const getStatBarStyle = (attr, key) => {
  const percentage = Math.max(0, Math.min(100, (attr.current / attr.max) * 100))
  const config = statConfig[key] || { color: '#95a5a6' }

  return {
    width: `${percentage}%`,
    backgroundColor: config.color,
    boxShadow: `0 0 0.5rem ${config.glowColor || 'rgba(149, 165, 166, 0.3)'}`
  }
}

const getCircleStyle = (attr, key) => {
  const percentage = Math.max(0, Math.min(100, (attr.current / attr.max) * 100))
  const config = statConfig[key] || { color: '#95a5a6', glowColor: 'rgba(149, 165, 166, 0.3)' }

  return {
    background: `conic-gradient(
      ${config.color} ${percentage}%,
      rgba(255, 255, 255, 0.1) ${percentage}%
    )`,
    boxShadow: `0 0 0.375rem ${config.glowColor}`
  }
}

const getDisplayAttributes = () => {
  if (!props.details.attributes) return {}
  return props.details.attributes
}
</script>

<style scoped>
.character-stats {
  width: 100%;
}

/* Normal Mode Styles */
.normal-stats {
  display: flex;
  flex-direction: column;
  gap: clamp(0.15rem, 0.5vw, 0.25rem);
}

.stat-row {
  display: flex;
  flex-direction: column;
  gap: 0.0625rem;
}

.stat-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  font-size: clamp(0.4rem, 0.8vw, 0.5rem);
  font-weight: 600;
  color: #ffffff;
  text-shadow: 0 0.0625rem 0.125rem rgba(0, 0, 0, 0.8);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.stat-value {
  font-size: clamp(0.4rem, 0.8vw, 0.5rem);
  font-weight: 700;
  color: #ffffff;
  text-shadow: 0 0.0625rem 0.125rem rgba(0, 0, 0, 0.8);
}

.stat-bar {
  height: clamp(0.125rem, 0.3vw, 0.1875rem);
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.0625rem;
  overflow: hidden;
  backdrop-filter: blur(0.125rem);
}

.stat-fill {
  height: 100%;
  border-radius: 0.0625rem;
  transition: width 0.3s ease;
  position: relative;
}

.stat-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg,
  transparent 0%,
  rgba(255, 255, 255, 0.3) 50%,
  transparent 100%
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* Compact Mode Styles */
.compact-stats {
  display: flex;
  justify-content: center;
  gap: clamp(0.2rem, 0.5vw, 0.3rem);
  flex-wrap: wrap;
}

.stat-dot {
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-circle {
  width: clamp(0.8rem, 2vw, 1rem);
  height: clamp(0.8rem, 2vw, 1rem);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 0.0625rem solid rgba(255, 255, 255, 0.3);
  transition: transform 0.2s ease;
  position: relative;
}

.stat-circle:hover {
  transform: scale(1.1);
}

.stat-number {
  font-size: clamp(0.35rem, 0.7vw, 0.45rem);
  font-weight: bold;
  color: #ffffff;
  text-shadow: 0 0.0625rem 0.125rem rgba(0, 0, 0, 0.9);
  z-index: 1;
}

/* Specific stat styling */
.stat-health .stat-label,
.stat-health .stat-value {
  color: #e74c3c;
  text-shadow: 0 0.0625rem 0.125rem rgba(231, 76, 60, 0.8);
}

.stat-energy .stat-label,
.stat-energy .stat-value {
  color: #3498db;
  text-shadow: 0 0.0625rem 0.125rem rgba(52, 152, 219, 0.8);
}

.stat-action .stat-label,
.stat-action .stat-value {
  color: #9b59b6;
  text-shadow: 0 0.0625rem 0.125rem rgba(155, 89, 182, 0.8);
}

/* Enhanced visual effects */
.stat-row {
  transition: transform 0.2s ease;
}

.character-stats:hover .stat-row {
  transform: translateX(0.125rem);
}

/* Responsive adjustments */
@media (max-width: 75em) { /* 1200px */
  .normal-stats {
    gap: clamp(0.125rem, 0.4vw, 0.2rem);
  }

  .stat-label,
  .stat-value {
    font-size: clamp(0.35rem, 0.7vw, 0.45rem);
  }

  .stat-bar {
    height: clamp(0.1rem, 0.25vw, 0.15rem);
  }
}

@media (max-width: 48em) { /* 768px */
  .normal-stats {
    gap: clamp(0.1rem, 0.3vw, 0.15rem);
  }

  .stat-label,
  .stat-value {
    font-size: clamp(0.3rem, 0.6vw, 0.4rem);
  }

  .stat-bar {
    height: clamp(0.08rem, 0.2vw, 0.125rem);
  }

  .stat-circle {
    width: clamp(0.7rem, 1.8vw, 0.9rem);
    height: clamp(0.7rem, 1.8vw, 0.9rem);
  }

  .stat-number {
    font-size: clamp(0.3rem, 0.6vw, 0.4rem);
  }
}

@media (max-width: 30em) { /* 480px - Compact Mode */
  .compact-stats {
    gap: clamp(0.15rem, 0.4vw, 0.25rem);
  }

  .stat-circle {
    width: clamp(0.6rem, 1.5vw, 0.8rem);
    height: clamp(0.6rem, 1.5vw, 0.8rem);
  }

  .stat-number {
    font-size: clamp(0.25rem, 0.5vw, 0.35rem);
  }
}

/* Very small screens */
@media (max-width: 20em) { /* 320px */
  .stat-circle {
    width: 0.6rem;
    height: 0.6rem;
  }

  .stat-number {
    font-size: 0.25rem;
  }

  .compact-stats {
    gap: 0.1rem;
  }
}

.stat-info {
  background: rgba(0, 0, 0, 0.5);
  border-radius: 0.25rem;
  flex: 1;
  padding: clamp(0.1rem, 0.3vw, 0.15rem);
  flex-direction: column;
  align-items: center;
  letter-spacing: 0.03em;
}
</style>