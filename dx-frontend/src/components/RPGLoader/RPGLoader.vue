<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Props {
  loadingText?: string
  visible?: boolean
}

interface Emits {
  (e: 'mounted'): void
  (e: 'unmounted'): void
  (e: 'shadowEffect'): void
}

const props = withDefaults(defineProps<Props>(), {
  loadingText: 'Loading',
  visible: true
})

const emit = defineEmits<Emits>()

const shadowEffect = ref<HTMLElement | null>(null)
let particleInterval: number | null = null
let shadowInterval: number | null = null

const createParticle = () => {
  const container = document.querySelector('.campfire-container')
  if (!container) return

  const particle = document.createElement('div')
  particle.className = 'fire-particle'

  // Random horizontal position
  particle.style.left = (Math.random() * 30 + 35) + '%'

  // Random vertical position - spawn from both top and bottom areas
  const spawnFromTop = Math.random() > 0.5
  if (spawnFromTop) {
    particle.style.top = '10%'
    particle.style.bottom = 'auto'
  } else {
    particle.style.bottom = '20%'
    particle.style.top = 'auto'
  }

  // Random animation duration
  particle.style.animationDuration = (Math.random() * 2 + 2) + 's'

  container.appendChild(particle)

  // Remove particle after animation
  setTimeout(() => {
    if (particle.parentNode) {
      particle.parentNode.removeChild(particle)
    }
  }, 4000)
}

const triggerShadowEffect = () => {
  if (shadowEffect.value) {
    shadowEffect.value.classList.add('active')
    emit('shadowEffect')

    // Remove the active class after animation completes
    setTimeout(() => {
      if (shadowEffect.value) {
        shadowEffect.value.classList.remove('active')
      }
    }, 3000)
  }
}

const scheduleShadowEffect = () => {
  const randomDelay = Math.random() * 10000 + 20000 // 20-30 seconds in milliseconds
  shadowInterval = window.setTimeout(() => {
    triggerShadowEffect()
    scheduleShadowEffect() // Schedule the next shadow effect
  }, randomDelay)
}

onMounted(() => {
  // Create particles periodically
  particleInterval = window.setInterval(createParticle, 800)

  // Start the shadow effect scheduling
  scheduleShadowEffect()

  emit('mounted')
})

onUnmounted(() => {
  if (particleInterval) {
    clearInterval(particleInterval)
  }
  if (shadowInterval) {
    clearTimeout(shadowInterval)
  }

  emit('unmounted')
})
</script>

<template>
  <div v-if="visible" class="loading-container">
    <div class="campfire-container">
      <!-- Replace this src with your actual campfire image -->
      <img
        src="/src/assets/images/loader/flame2.png"
        alt="Campfire"
        class="campfire-image"
      >

      <!-- Shadow effect -->
      <div ref="shadowEffect" class="shadow-effect"></div>

      <!-- Fire particles -->
      <div class="fire-particle"></div>
      <div class="fire-particle"></div>
      <div class="fire-particle"></div>
      <div class="fire-particle"></div>
      <div class="fire-particle"></div>
    </div>

    <div class="loading-text">
      {{ loadingText }}<span class="loading-dots"></span>
    </div>
  </div>
</template>

<style scoped>
.loading-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: #000;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  overflow: hidden;
  font-family: Arial, sans-serif;
}

.campfire-container {
  position: relative;
  width: 200px;
  height: 200px;
  margin-bottom: 30px;
}

.campfire-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  position: relative;
  z-index: 2;
  filter: brightness(1.2) contrast(1.3) saturate(1.1);
  mix-blend-mode: screen;
  opacity: 0.95;
  user-select: none;
  pointer-events: none;
  -webkit-user-drag: none;
  -khtml-user-drag: none;
  -moz-user-drag: none;
  -o-user-drag: none;
  user-drag: none;
}

/* Shadow effect that passes between character and fire */
.shadow-effect {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(0, 0, 0, 0.7) 20%,
    rgba(0, 0, 0, 0.9) 50%,
    rgba(0, 0, 0, 0.7) 80%,
    transparent 100%
  );
  z-index: 3;
  opacity: 0;
  pointer-events: none;
}

.shadow-effect.active {
  animation: shadowPass 3s ease-in-out;
}

@keyframes shadowPass {
  0% {
    left: -100%;
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    left: 100%;
    opacity: 0;
  }
}

/* Fire particles - cyan theme */
.fire-particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background: #00ffff;
  border-radius: 50%;
  pointer-events: none;
  animation: floatUp 3s linear infinite;
  opacity: 0;
}

.fire-particle:nth-child(3) { left: 45%; animation-delay: 0s; }
.fire-particle:nth-child(4) { left: 55%; animation-delay: 0.5s; }
.fire-particle:nth-child(5) { left: 50%; animation-delay: 1s; }
.fire-particle:nth-child(6) { left: 40%; animation-delay: 1.5s; }
.fire-particle:nth-child(7) { left: 60%; animation-delay: 2s; }

/* Loading text */
.loading-text {
  color: #fada95;
  font-size: 2rem;
  font-weight: 600;
  font-family: 'Cinzel', serif;
  text-align: center;
  margin-top: 20px;
  user-select: none;
  pointer-events: none;
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  /* Enhanced shadow effects - less 3D, more shadows */
  text-shadow:
    2px 2px 4px rgba(0, 0, 0, 0.5),
    4px 4px 8px rgba(0, 0, 0, 0.3),
    0px 0px 10px rgba(250, 218, 149, 0.6),
    0px 0px 20px rgba(250, 218, 149, 0.3);
}

.loading-dots {
  display: inline-block;
  animation: dots 1.5s steps(4, end) infinite;
}

/* Animations */
@keyframes floatUp {
  0% {
    opacity: 1;
    transform: translateY(0px) scale(1);
    background: #00ffff;
  }
  50% {
    opacity: 0.7;
    background: #80ffff;
  }
  100% {
    opacity: 0;
    transform: translateY(-80px) scale(0.5);
    background: #ffff00;
  }
}

@keyframes textPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@keyframes dots {
  0%, 20% { content: ''; }
  40% { content: '.'; }
  60% { content: '..'; }
  80%, 100% { content: '...'; }
}

/* Responsive design */
@media (max-width: 768px) {
  .campfire-container {
    width: 150px;
    height: 150px;
  }

  .loading-text {
    font-size: 1.5rem;
  }
}
</style>