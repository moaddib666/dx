<script setup lang="ts">
import { defineProps, computed, ref, onMounted } from 'vue';
import locationIcon from '@/assets/icons/location-icon.png';
import { worldMapEditorService } from '@/services/WorldMapEditorService.js';

// Define props for the component
const props = defineProps<{
  id?: string | number; // Optional ID of the location
  alt?: string; // Optional alt text for the image
}>();

// State for the location data
const location = ref(null);
const loading = ref(false);
const error = ref(null);

// Compute the icon source based on whether an ID is provided
const iconSrc = computed(() => {
  if (!props.id || !location.value) {
    return locationIcon; // Use placeholder icon if no ID or location not found
  }

  // If location has an image, use it
  if (location.value.image) {
    return location.value.image;
  }

  // Fallback to placeholder icon
  return locationIcon;
});

// Compute the alt text based on the alt prop or default to a descriptive text
const altText = computed(() => {
  if (props.alt) {
    return props.alt;
  }

  if (location.value && location.value.name) {
    return `Location: ${location.value.name}`;
  }

  return 'Location';
});

// Fetch location data when the component is mounted or when the ID changes
const fetchLocation = async () => {
  if (!props.id) {
    location.value = null;
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    // Find location by ID in the locations array
    // Assuming worldMapEditorService has a locations array or a method to get locations
    if (worldMapEditorService.locations) {
      const locationData = worldMapEditorService.locations.find(loc => loc.id === props.id);
      location.value = locationData;

      if (!locationData) {
        console.warn(`Location with ID ${props.id} not found`);
      }
    } else {
      console.warn('worldMapEditorService.locations is not available');
    }
  } catch (err) {
    console.error('Error fetching location:', err);
    error.value = err;
    location.value = null;
  } finally {
    loading.value = false;
  }
};

// Watch for changes to the ID prop
onMounted(() => {
  fetchLocation();
});
</script>

<template>
  <div class="location-selector-icon">
    <img :src="iconSrc" class="icon" :alt="altText" :class="{ 'is-loading': loading }"/>
    <div v-if="error" class="error-message">!</div>
  </div>
</template>

<style scoped>
.location-selector-icon {
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