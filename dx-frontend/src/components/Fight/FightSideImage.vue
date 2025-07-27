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
    <img :src="getImageSrc()" :alt="`${props.side} character`" />
  </div>
</template>

<style scoped>
.fight-side-image {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}

.fight-side-image img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}

.flip-horizontal {
  transform: scaleX(-1);
}
</style>