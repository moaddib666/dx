<template>
  <div v-if="isVisible" class="zoom-modal" @click="$emit('close')">
    <div class="zoomed-image" :style="zoomedImageStyle"></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  isVisible: boolean
  imageUrl: string
}>()

defineEmits<{
  (e: 'close'): void
}>()

const zoomedImageStyle = computed(() => ({
  backgroundImage: `url(${props.imageUrl})`
}))
</script>

<style scoped>
.zoom-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.9);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: zoom-out;
}

.zoomed-image {
  width: 90%;
  height: 90%;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(34, 211, 238, 0.3);
  animation: zoomIn 0.3s ease;
  border: 1px solid rgba(99, 247, 255, 0.4);
}

@keyframes zoomIn {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .zoomed-image {
    width: 95%;
    height: 80%;
  }
}

@media (max-width: 480px) {
  .zoomed-image {
    width: 98%;
    height: 70%;
  }
}
</style>