<script setup lang="ts">
import {SubLocation} from "@/api/dx-backend";
import {computed} from "vue";

interface Props {
  subLocation: SubLocation
  selected: boolean
}

const props = defineProps<Props>();
const emit = defineEmits<{
  'copy-id': [subLocationId: string];
  'filter-by-location': [subLocation: SubLocation];
}>();

const imageUrl = computed(() => {
  return props.subLocation?.image || '/src/assets/images/default-location.png';
});

// Fast action handlers
const handleCopyId = (event: Event) => {
  event.stopPropagation();
  emit('copy-id', props.subLocation.id);
};

const handleFilterByLocation = (event: Event) => {
  event.stopPropagation();
  emit('filter-by-location', props.subLocation);
};
</script>

<template>
  <div class="selector-card" :class="{selected: props.selected}">
    <div class="image-container">
      <img :src="imageUrl" :alt="props.subLocation.name" class="location-image"/>

      <!-- Fast Actions Overlay -->
      <div class="fast-actions">
        <button
          class="action-btn copy-btn"
          title="Copy SubLocation ID"
          @click="handleCopyId"
        >
          📋
        </button>
        <button
          class="action-btn location-btn"
          title="Filter by Location"
          @click="handleFilterByLocation"
          v-if="props.subLocation.location"
        >
          🗺️
        </button>
      </div>
    </div>
    <div class="sublocation-info">
      <h3 class="sublocation-name">{{ props.subLocation.name }}</h3>
      <p class="location-name">{{ props.subLocation.location || 'Unknown Location' }}</p>
      <p class="sublocation-description" v-if="props.subLocation.description">
        {{ props.subLocation.description.length > 60 ? props.subLocation.description.substring(0, 60) + '...' : props.subLocation.description }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.selector-card {
  aspect-ratio: 4 / 5;
  display: flex;
  flex-direction: column;
  padding: 0.525rem;
  border: 2px solid transparent;
  border-radius: 0.35rem;
  cursor: pointer;
  transition: border-color 0.3s, background-color 0.3s, transform 0.2s ease;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(4px);
  height: 100%;
}

.selector-card:hover {
  background: rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}

.selector-card.selected {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
}

.image-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.35rem;
  overflow: hidden;
  border-radius: 0.263rem;
  position: relative;
  background: rgba(0, 0, 0, 0.1);
}

.location-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.263rem;
}

.fast-actions {
  position: absolute;
  top: 0.35rem;
  right: 0.35rem;
  display: flex;
  flex-direction: column;
  gap: 0.175rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.selector-card:hover .fast-actions {
  opacity: 1;
}

.action-btn {
  width: 1.75rem;
  height: 1.75rem;
  border: none;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.action-btn:hover {
  background: rgba(0, 0, 0, 0.9);
  transform: scale(1.1);
}

.copy-btn:hover {
  background: rgba(34, 139, 34, 0.8);
}

.location-btn:hover {
  background: rgba(30, 144, 255, 0.8);
}

.sublocation-info {
  flex-shrink: 0;
  text-align: center;
}

.sublocation-name {
  margin: 0 0 0.175rem 0;
  font-size: 0.7rem;
  font-weight: 600;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.location-name {
  margin: 0 0 0.175rem 0;
  font-size: 0.6rem;
  color: #b8860b;
  font-weight: 500;
  line-height: 1.1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sublocation-description {
  margin: 0;
  font-size: 0.55rem;
  color: #cccccc;
  line-height: 1.1;
  opacity: 0.8;
}
</style>