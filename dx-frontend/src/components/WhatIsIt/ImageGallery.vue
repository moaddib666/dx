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
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.gallery-item {
  text-align: center;
  max-width: 100%;
}

.gallery-image {
  width: 100%;
  max-width: 500px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  position: relative;
}

.zoomable-image {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(99, 247, 255, 0.3);
  position: relative;
}

.zoomable-image:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.3);
  border-color: rgba(99, 247, 255, 0.5);
}

.image-caption {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #9feaff;
  font-style: italic;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .image-gallery {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .gallery-image {
    max-width: 100%;
  }
}
</style>