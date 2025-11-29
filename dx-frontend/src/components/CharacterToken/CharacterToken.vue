<script setup lang="ts">
import { computed } from 'vue';

// Define props interface
interface Props {
  image?: string;
}

const props = withDefaults(defineProps<Props>(), {
  image: undefined
});

// Placeholder image - a simple data URI for a gray circle
const placeholderImage = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Ccircle cx="50" cy="50" r="40" fill="%23cccccc"/%3E%3Ctext x="50" y="55" font-size="14" text-anchor="middle" fill="%23666666"%3ENo Image%3C/text%3E%3C/svg%3E';

// Use provided image or fallback to placeholder
const characterImage = computed(() => props.image || placeholderImage);
</script>

<template>
  <div class="character-token">
    <!-- Background layer -->
    <div class="token-layer token-background"></div>

    <!-- Character image layer with mask and overlay -->
    <div class="token-layer token-character">
      <div class="character-image-container" :style="{ backgroundImage: `url(${characterImage})` }"></div>
      <div class="token-overlay"></div>
    </div>

    <!-- Border layer -->
    <div class="token-layer token-border"></div>
  </div>
</template>

<style scoped>
.character-token {
  position: relative;
  width: 100%;
  height: 100%;
  aspect-ratio: 1 / 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.token-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Background layer */
.token-background {
  z-index: 1;
  background-image: url('@/assets/rpg_token/Tokenfill.png');
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}

/* Character layer */
.token-character {
  z-index: 2;
}

.character-image-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70%;
  height: 70%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 50%;
  mask-image: radial-gradient(circle, rgba(0, 0, 0, 0.9) 5%, rgba(0, 0, 0, 0) 85%);
}

.token-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  background-size: 100% 100%, contain;
  background: url('@/assets/rpg_token/Tokenfill.png') no-repeat, no-repeat center, center;
  mask-image: url('@/assets/rpg_token/Tokenbg.png');
  mask-size: contain;
  mask-position: center;
  mask-repeat: no-repeat;
  -webkit-mask-image: url('@/assets/rpg_token/Tokenbg.png');
  -webkit-mask-size: contain;
  -webkit-mask-position: center;
  -webkit-mask-repeat: no-repeat;
  mix-blend-mode: lighten;
}

/* Border layer */
.token-border {
  z-index: 3;
  pointer-events: none;
  background-image: url('@/assets/rpg_token/Token border.png');
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}
</style>