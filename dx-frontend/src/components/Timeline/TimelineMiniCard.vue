<template>
  <div
    class="timeline-mini-card"
    :class="{ 'selected': isSelected }"
    @click="handleClick"
  >
    <!-- Selection glow -->
    <div v-if="isSelected" class="selection-glow"></div>

    <!-- Card container -->
    <div class="card-container">
      <!-- Background with gradient and effects -->
      <div class="card-background">
        <div class="gradient-overlay" :style="{ background: gradientStyle }"></div>
        <div class="light-effect"></div>
        <div class="starfield">
          <svg viewBox="0 0 200 200" class="stars-svg">
            <circle cx="30" cy="20" r="1" fill="#fada95" />
            <circle cx="170" cy="40" r="1.5" fill="#fada95" />
            <circle cx="50" cy="60" r="0.8" fill="#fada95" />
            <circle cx="150" cy="30" r="1" fill="#fada95" />
          </svg>
        </div>
        <div class="bottom-gradient"></div>
      </div>

      <!-- Time badge -->
      <div class="time-badge">
        <span>{{ item.time }}</span>
      </div>

      <!-- Content -->
      <div class="card-content">
        <h3 class="card-title">{{ item.title }}</h3>

        <div class="card-info">
          <div v-if="item.location" class="info-item">
            <i class="fas fa-map-marker-alt"></i>
            <span>{{ item.location }}</span>
          </div>
          <div v-if="item.participants" class="info-item">
            <i class="fas fa-users"></i>
            <span>{{ item.participants }}</span>
          </div>
        </div>

        <div class="card-tags">
          <span
            v-for="tag in item.tags"
            :key="tag.label"
            class="tag"
          >
            {{ tag.label }}
          </span>
        </div>
      </div>

      <!-- Loading overlay -->
      <div v-if="loading" class="loading-overlay">
        <i class="fas fa-spinner fa-spin"></i>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { TimelineItem } from '@/models/TimelineModels'

interface Props {
  item: TimelineItem
  isSelected?: boolean
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isSelected: false,
  loading: false
})

const emit = defineEmits<{
  click: [item: TimelineItem]
}>()

const gradientStyle = computed(() => {
  return props.item.gradient || 'linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%)'
})

const handleClick = () => {
  emit('click', props.item)
}
</script>

<style scoped>
.timeline-mini-card {
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
}

.timeline-mini-card.selected {
  transform: scale(1.05);
}

.timeline-mini-card:not(.selected):hover {
  transform: scale(1.02);
}

.selection-glow {
  position: absolute;
  inset: 0;
  background: rgba(250, 218, 149, 0.3);
  border-radius: 0.75rem;
  filter: blur(1rem);
  z-index: 0;
}

.card-container {
  position: relative;
  width: 14rem;
  height: 6rem;
  border-radius: 0.5rem;
  overflow: hidden;
  border: 1px solid rgba(250, 218, 149, 0.4);
  transition: all 0.3s ease;
  font-family: 'Cinzel', 'Times New Roman', serif;
}

.timeline-mini-card.selected .card-container {
  border-color: rgba(250, 218, 149, 0.8);
  box-shadow: 0 8px 32px rgba(250, 218, 149, 0.3);
}

.timeline-mini-card:not(.selected):hover .card-container {
  border-color: rgba(250, 218, 149, 0.6);
}

.card-background {
  position: absolute;
  inset: 0;
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
  opacity: 0.4;
}

.light-effect::before {
  content: '';
  width: 8rem;
  height: 8rem;
  border-radius: 50%;
  background: rgba(250, 218, 149, 0.3);
  filter: blur(2rem);
}

.starfield {
  position: absolute;
  inset: 0;
  opacity: 0.2;
}

.stars-svg {
  width: 100%;
  height: 100%;
}

.bottom-gradient {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3.5rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.9), transparent);
}

.time-badge {
  position: absolute;
  top: 0.4rem;
  right: 0.4rem;
  padding: 0.15rem 0.35rem;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  border-radius: 0.2rem;
  border: 1px solid rgba(250, 218, 149, 0.5);
  z-index: 2;
}

.time-badge span {
  color: #fada95;
  font-size: 0.5rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.card-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.6rem;
  z-index: 2;
}

.card-title {
  color: #fada95;
  font-size: 0.7rem;
  font-weight: bold;
  margin: 0 0 0.3rem 0;
  line-height: 1.1;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.card-info {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.3rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  color: rgba(250, 218, 149, 0.8);
  font-size: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.info-item i {
  font-size: 0.5rem;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.tag {
  padding: 0.1rem 0.3rem;
  border-radius: 0.2rem;
  border: 1px solid rgba(250, 218, 149, 0.6);
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-size: 0.45rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: bold;
  backdrop-filter: blur(4px);
}

.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  backdrop-filter: blur(4px);
}

.loading-overlay i {
  color: #fada95;
  font-size: 1.5rem;
}
</style>
