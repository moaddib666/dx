<script setup lang="ts">

import {defineProps} from 'vue';
import {Name535Enum} from "@/api/dx-backend";

interface Props {
  side: Name535Enum
}

const props = defineProps<Props>();

</script>

<template>
  <div class="overlay" :class="{ 'mage': side === Name535Enum.PathOfJSon, 'tech': side === Name535Enum.PathOfJohn }">
    <!-- The mage overlay is applied here -->
  </div>
</template>

<style scoped>

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  transition: all 0.3s ease-in-out;
}

.mage {
  background: url('@/assets/fight/ongoing/mage-overlay.png') no-repeat center center;
  background-size: cover;
  mask: linear-gradient(to bottom, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.9));
  backdrop-filter: blur(2rem); /* Optional: adds a blur effect to the background */
  mix-blend-mode: hard-light;
}

.tech {
  background: url('@/assets/fight/ongoing/tech-overlay.png') no-repeat center center;
  background-size: cover;
  mask: linear-gradient(to bottom, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.9));
  backdrop-filter: blur(2rem); /* Optional: adds a blur effect to the background */
  mix-blend-mode: hard-light;
}

</style>