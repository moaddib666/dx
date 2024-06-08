<template>
  <div class="background-container" @mousemove="handleMouseMove">
    <slot></slot>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const hue = ref(100);
const saturation = ref(100);
const opacity = ref(1);

const handleMouseMove = (event) => {
  const { clientX, clientY, currentTarget } = event;
  const { offsetWidth, offsetHeight } = currentTarget;

  const xPercentage = clientX / offsetWidth;
  const yPercentage = clientY / offsetHeight;

  hue.value = 100 - yPercentage * 90; // From 100% to 10%
  saturation.value = 100 - yPercentage * 90; // From 100% to 10%
  opacity.value = 1 - xPercentage * 0.9; // From 100% to 10%
};
</script>

<style scoped>
.background-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background-image: url('@/assets/images/dx-1.webp'),
  url('@/assets/images/dx-2.webp'),
  url('@/assets/images/dx-3.webp'),
  url('@/assets/images/dx-4.webp');
  background-size: cover;
  background-position: center;
  transition: background 1s ease-in-out;
}

.background-container::before,
.background-container::after,
.background-container div:nth-child(2),
.background-container div:nth-child(3) {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  transition: opacity 1s ease-in-out, filter 1s ease-in-out;
}

.background-container::before {
  background-image: url('@/assets/images/dx-1.webp');
  opacity: 1;
  filter: hue-rotate(0deg) saturate(1);
}

.background-container div:nth-child(2) {
  background-image: url('@/assets/images/dx-2.webp');
  opacity: 0;
  filter: hue-rotate(0deg) saturate(1);
}

.background-container div:nth-child(3) {
  background-image: url('@/assets/images/dx-3.webp');
  opacity: 0;
  filter: hue-rotate(0deg) saturate(1);
}

.background-container::after {
  background-image: url('@/assets/images/dx-4.webp');
  opacity: 0;
  filter: hue-rotate(0deg) saturate(1);
}
</style>
