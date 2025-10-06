<template>
  <div
    v-if="visible && item"
    class="timeline-detail-card"
    @click.stop
  >
    <!-- Card container with timeline styling -->
    <div class="card-container">
      <!-- Background with gradient and cosmic effects -->
      <div class="card-background">
        <div class="gradient-overlay" :style="{ background: gradientStyle }"></div>

        <!-- Circular light effects -->
        <div class="light-effect"></div>

        <!-- Starfield effect -->
        <div class="starfield">
          <svg viewBox="0 0 200 200" class="stars-svg">
            <circle cx="30" cy="20" r="1" fill="#fada95" />
            <circle cx="170" cy="40" r="1.5" fill="#fada95" />
            <circle cx="50" cy="60" r="0.8" fill="#fada95" />
            <circle cx="150" cy="30" r="1" fill="#fada95" />
            <circle cx="90" cy="80" r="1.2" fill="#fada95" />
            <circle cx="120" cy="120" r="0.9" fill="#fada95" />
            <circle cx="60" cy="140" r="1.1" fill="#fada95" />
            <circle cx="180" cy="160" r="0.7" fill="#fada95" />
          </svg>
        </div>

        <!-- Dark gradient overlay for content readability -->
        <div class="content-gradient"></div>
      </div>

      <!-- Content -->
      <div class="card-content">
        <!-- Header with title and time -->
        <div class="content-header">
          <h3 class="card-title">{{ item.title }}</h3>
          <div class="time-badge">
            <i class="fas fa-clock"></i>
            <span>{{ item.time }}</span>
          </div>
        </div>

        <!-- Category and metadata -->
        <div class="metadata-section">
          <div class="category-badge">
            <i class="fas fa-folder"></i>
            <span>{{ getCategoryLabel(item.category) }}</span>
          </div>

          <div class="metadata-items">
            <div v-if="item.location" class="metadata-item">
              <i class="fas fa-map-marker-alt"></i>
              <span>{{ item.location }}</span>
            </div>
            <div v-if="item.participants" class="metadata-item">
              <i class="fas fa-users"></i>
              <span>{{ item.participants }}</span>
            </div>
          </div>
        </div>

        <!-- Description -->
        <div class="description-section">
          <div class="section-label">Description</div>
          <div class="description">
            <p v-if="item.description">{{ item.description }}</p>
            <p v-else class="no-description">No description available</p>
          </div>
        </div>

        <!-- Tags -->
        <div v-if="item.tags && item.tags.length > 0" class="tags-section">
          <div class="section-label">Tags</div>
          <div class="tags">
            <span
              v-for="tag in item.tags"
              :key="tag.label"
              class="tag"
            >
              {{ tag.label }}
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { TimelineItem, TimelineCategory } from '@/models/TimelineModels'

interface Props {
  visible: boolean
  item: TimelineItem | null
  categories: TimelineCategory[]
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const emit = defineEmits<{
  close: []
}>()

const imageError = ref(false)

const gradientStyle = computed(() => {
  return props.item?.gradient || 'linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%)'
})

const onImageError = () => {
  imageError.value = true
}

const getCategoryLabel = (categoryId: string): string => {
  const category = props.categories.find(c => c.id === categoryId)
  return category?.label || categoryId
}

const handleClose = () => {
  emit('close')
}
</script>

<style scoped>
.timeline-detail-card {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  z-index: 1000;
  font-family: 'Cinzel', 'Times New Roman', serif;
  animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.card-container {
  position: relative;
  width: 22rem;
  height: 32rem;
  border-radius: 0.75rem;
  overflow: hidden;
  border: 1px solid rgba(250, 218, 149, 0.6);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.9),
    0 0 24px rgba(250, 218, 149, 0.4);
  transition: all 0.3s ease;
}

/* Background effects */
.card-background {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.gradient-overlay {
  position: absolute;
  inset: 0;
}

.light-effect {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.3;
}

.light-effect::before {
  content: '';
  width: 16rem;
  height: 16rem;
  border-radius: 50%;
  background: rgba(250, 218, 149, 0.25);
  filter: blur(4rem);
}

.starfield {
  position: absolute;
  inset: 0;
  opacity: 0.3;
}

.stars-svg {
  width: 100%;
  height: 100%;
}

.content-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom,
    rgba(0, 0, 0, 0.3) 0%,
    rgba(0, 0, 0, 0.7) 50%,
    rgba(0, 0, 0, 0.9) 100%);
}

/* Close button */
.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(250, 218, 149, 0.6);
  color: #fada95;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
  backdrop-filter: blur(4px);
}

.close-button:hover {
  background: rgba(250, 218, 149, 0.2);
  border-color: #fada95;
  transform: scale(1.1);
  box-shadow: 0 0 16px rgba(250, 218, 149, 0.6);
}

.close-button i {
  font-size: 0.875rem;
}

/* Content */
.card-content {
  position: relative;
  z-index: 2;
  height: 100%;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow-y: auto;
}

/* Custom scrollbar */
.card-content::-webkit-scrollbar {
  width: 6px;
}

.card-content::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
}

.card-content::-webkit-scrollbar-thumb {
  background: rgba(250, 218, 149, 0.3);
  border-radius: 3px;
}

.card-content::-webkit-scrollbar-thumb:hover {
  background: rgba(250, 218, 149, 0.5);
}

/* Header */
.content-header {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(250, 218, 149, 0.2);
}

.card-title {
  color: #fada95;
  font-size: 1.25rem;
  font-weight: bold;
  margin: 0;
  line-height: 1.3;
  text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.9);
  letter-spacing: 0.02em;
}

.time-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.75rem;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  border-radius: 0.3rem;
  border: 1px solid rgba(250, 218, 149, 0.5);
  width: fit-content;
}

.time-badge i {
  color: #fada95;
  font-size: 0.75rem;
}

.time-badge span {
  color: #fada95;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* Metadata section */
.metadata-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.category-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.75rem;
  background: rgba(250, 218, 149, 0.15);
  border: 1px solid rgba(250, 218, 149, 0.4);
  border-radius: 0.3rem;
  width: fit-content;
  backdrop-filter: blur(4px);
}

.category-badge i {
  color: #fada95;
  font-size: 0.75rem;
}

.category-badge span {
  color: #fada95;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.metadata-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.metadata-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(250, 218, 149, 0.85);
  font-size: 0.875rem;
}

.metadata-item i {
  font-size: 0.875rem;
  width: 1.25rem;
  text-align: center;
  color: rgba(250, 218, 149, 0.7);
}

/* Description section */
.description-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.section-label {
  color: rgba(250, 218, 149, 0.6);
  font-size: 0.625rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.15em;
}

.description {
  flex: 1;
  overflow-y: auto;
}

.description p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.6;
  color: rgba(250, 218, 149, 0.9);
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.9);
}

.no-description {
  color: rgba(250, 218, 149, 0.4);
  font-style: italic;
}

/* Tags section */
.tags-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  border: 1px solid rgba(250, 218, 149, 0.5);
  background: rgba(0, 0, 0, 0.5);
  color: #fada95;
  font-size: 0.625rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: bold;
  backdrop-filter: blur(4px);
  transition: all 0.2s ease;
}

.tag:hover {
  background: rgba(250, 218, 149, 0.15);
  border-color: #fada95;
}

/* Loading overlay */
.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20;
  backdrop-filter: blur(6px);
}

.loading-spinner {
  color: #fada95;
  font-size: 2.5rem;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
