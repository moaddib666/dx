<template>
  <div class="image-gallery">
    <div v-for="(item, index) in items" :key="index" class="gallery-item">
      <img
        :src="item.src"
        :alt="item.alt"
        class="gallery-image zoomable-image"
        @click="$emit('toggle-zoom', $event)"
      />
      <p class="image-caption">{{ item.caption }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface ImageData {
  src: string
  alt: string
  caption: string
}

defineProps<{
  items: ImageData[]
}>()

defineEmits<{
  (e: 'toggle-zoom', event: Event): void
}>()
</script>

<style scoped>
.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.gallery-item {
  text-align: center;
}

.gallery-image {
  width: 100%;
  max-width: 450px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  position: relative;
}

.zoomable-image {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 3px solid transparent;
  position: relative;
}

.zoomable-image::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.5), inset 0 0 15px rgba(255, 215, 0, 0.3);
  z-index: 1;
  pointer-events: none;
  animation: borderPulse 3s infinite alternate;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.zoomable-image:hover {
  transform: scale(1.03);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
}

.zoomable-image:hover::before {
  opacity: 1;
}

.image-caption {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--light-steel-blue, #b0c4de);
  font-style: italic;
}

@keyframes borderPulse {
  0% {
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.3), inset 0 0 15px rgba(255, 215, 0, 0.2);
  }
  100% {
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.6), inset 0 0 20px rgba(255, 215, 0, 0.4);
  }
}

@media (max-width: 768px) {
  .image-gallery {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .gallery-image {
    max-width: 100%;
  }

  .zoomable-image::before {
    border-width: 1px;
  }
}

@media (max-width: 480px) {
  .zoomable-image:hover {
    transform: scale(1.02);
  }
}
</style>