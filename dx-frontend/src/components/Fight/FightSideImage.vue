<script setup lang="ts">
import techSideImage from '@/assets/fight/sides/tech-side.png';
import mageSideImage from '@/assets/fight/sides/mage-side.png';

const props = defineProps<{
  direction: 'left' | 'right';
  side: "mage" | "tech"
}>();

// Determine which image to use based on the side prop
const getImageSrc = () => {
  return props.side === 'tech' ? techSideImage : mageSideImage;
};
</script>

<template>
  <div class="fight-side-image" :class="{ 'flip-horizontal': props.direction === 'right' }">
    <!-- Blurred background image -->
    <div class="blurred-background">
      <img :src="getImageSrc()" :alt="`${props.side} character background`" />
    </div>
    <!-- Foreground image -->
    <img class="foreground-image" :src="getImageSrc()" :alt="`${props.side} character`" />
  </div>
</template>

<style scoped>
.fight-side-image {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  position: relative;
  overflow: hidden;
}

.blurred-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1;
}

.blurred-background img {
  max-height: 110%;
  max-width: 110%;
  object-fit: contain;
  filter: blur(15px);
  opacity: 0.7;
}

.foreground-image {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
  position: relative;
  z-index: 2;
}

.flip-horizontal {
  transform: scaleX(-1);
}
</style>