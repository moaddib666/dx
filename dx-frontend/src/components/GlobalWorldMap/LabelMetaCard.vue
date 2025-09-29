<template>
  <div
    v-if="visible"
    class="label-meta-card"
    @click.stop
  >
    <!-- Top section: Image and Name -->
    <div class="card-header">
      <div class="card-image">
        <img
          v-if="metadata?.image"
          :src="metadata.image"
          :alt="metadata.name"
          @error="onImageError"
        />
        <div v-else class="image-placeholder">
          <i class="fas fa-map-marker-alt"></i>
        </div>
      </div>
      <div class="card-title">
        <h3>{{ metadata?.name || 'Unknown Place' }}</h3>
      </div>
    </div>

    <!-- Bottom section: Blurred background with description and tags -->
    <div class="card-content">
      <div class="content-blur-overlay"></div>
      <div class="content-text">
        <div class="description">
          <p v-if="metadata?.description">{{ metadata.description }}</p>
          <p v-else class="no-description">No description available</p>
        </div>
        <div class="tags" v-if="metadata?.tags && metadata.tags.length > 0">
          <span
            v-for="tag in metadata.tags"
            :key="tag"
            class="tag"
          >
            {{ tag }}
          </span>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="fas fa-spinner fa-spin"></i>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { PlaceMetadata } from '@/services/metadata/MetadataResolver'

interface Props {
  visible: boolean
  metadata: PlaceMetadata | null
  position: { x: number; y: number }
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const emit = defineEmits<{
  close: []
}>()

const imageError = ref(false)

const onImageError = () => {
  imageError.value = true
}

// Reset image error when metadata changes
watch(() => props.metadata?.image, () => {
  imageError.value = false
})
</script>

<style scoped>
.label-meta-card {
  position: fixed;
  bottom: -0.5rem; /* 20px padding from bottom edge */
  left: 5rem; /* 20px padding from left edge */
  width: 20rem;
  height: 40rem; /* 2:3 ratio (300x450) */
  background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
  border: 1px solid #fada95;
  border-radius: 12px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.8),
    0 0 20px rgba(250, 218, 149, 0.3);
  z-index: 1000;
  overflow: hidden;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  backdrop-filter: blur(10px);
  animation: fadeInScale 0.3s ease-out;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.card-header {
  height: 60%; /* Top 60% for image and title */
  position: relative;
  display: flex;
  flex-direction: column;
}

.card-image {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
  object-position: center top;
}

.card-image:hover img {
  transform: scale(1.05);
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(45deg, #2a2a2a, #3a3a3a);
  color: #fada95;
  font-size: 3rem;
}

.card-title {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  padding: 2rem 1rem 1rem;
  color: #fada95;
}

.card-title h3 {
  margin: 0;
  font-size: 1.4rem;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  line-height: 1.2;
}

.card-content {
  height: 40%; /* Bottom 40% for description and tags */
  position: relative;
  display: flex;
  flex-direction: column;
}

.content-blur-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  z-index: 1;
}

.content-text {
  position: relative;
  z-index: 2;
  padding: 1rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: #ffffff;
}

.description {
  flex: 1;
  overflow-y: auto;
}

.description p {
  margin: 0;
  font-size: 0.76rem;
  line-height: 1.4;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
}

.no-description {
  color: #888;
  font-style: italic;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.tag {
  background: rgba(250, 218, 149, 0.2);
  border: 1px solid #fada95;
  color: #fada95;
  padding: 0.2rem 0.5rem;
  border-radius: 0.2rem;
  font-size: 0.5rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  backdrop-filter: blur(4px);
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20;
  backdrop-filter: blur(4px);
}

.loading-spinner {
  color: #fada95;
  font-size: 2rem;
}

</style>