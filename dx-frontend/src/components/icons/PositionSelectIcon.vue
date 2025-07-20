<script setup lang="ts">
import { defineProps, computed, ref, onMounted } from 'vue';
import mapIcon from '@/assets/icons/position-selection-icon.png';
import { worldMapEditorService } from '@/services/WorldMapEditorService.js';

// Define props for the component
const props = defineProps<{
  id?: string | number; // Optional ID of the position
  alt?: string; // Optional alt text for the image
}>();

// State for the position data
const position = ref(null);
const loading = ref(false);
const error = ref(null);

// Compute the icon source based on whether an ID is provided
const iconSrc = computed(() => {
  if (!props.id || !position.value) {
    return mapIcon; // Use placeholder icon if no ID or position not found
  }

  // If position has an image, use it
  if (position.value.image) {
    return position.value.image;
  }

  // Fallback to placeholder icon
  return mapIcon;
});

// Compute the alt text based on the alt prop or default to a descriptive text
const altText = computed(() => {
  if (props.alt) {
    return props.alt;
  }

  if (position.value && position.value.name) {
    return `Position: ${position.value.name}`;
  }

  return 'Position';
});

// Fetch position data when the component is mounted or when the ID changes
const fetchPosition = async () => {
  if (!props.id) {
    position.value = null;
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    // Find position by ID in the positions array
    // Assuming worldMapEditorService has a positions array or a method to get positions
    if (worldMapEditorService.positions) {
      const positionData = worldMapEditorService.positions.find(pos => pos.id === props.id);
      position.value = positionData;

      if (!positionData) {
        console.warn(`Position with ID ${props.id} not found`);
      }
    } else {
      console.warn('worldMapEditorService.positions is not available');
    }
  } catch (err) {
    console.error('Error fetching position:', err);
    error.value = err;
    position.value = null;
  } finally {
    loading.value = false;
  }
};

// Watch for changes to the ID prop
onMounted(() => {
  fetchPosition();
});
</script>

<template>
  <div class="position-select-icon">
    <img :src="iconSrc" class="icon" :alt="altText" :class="{ 'is-loading': loading }"/>
    <div v-if="error" class="error-message">!</div>
  </div>
</template>

<style scoped>
.position-select-icon {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.icon {
  width: 90%;
  height: 90%;
  padding: 0;
  margin: 0;
  object-fit: contain;
}

.is-loading {
  opacity: 0.7;
}

.error-message {
  position: absolute;
  bottom: 5px;
  right: 5px;
  background-color: red;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
}
</style>