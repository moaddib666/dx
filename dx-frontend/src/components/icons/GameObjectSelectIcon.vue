<script setup lang="ts">
import { defineProps, computed, ref, onMounted } from 'vue';
import gameObjectIcon from '@/assets/icons/gameobject.png';
import { worldEditorService } from '@/services/WorldEditorService.js';

// Define props for the component
const props = defineProps<{
  id?: string | number; // Optional ID of the game object
  alt?: string; // Optional alt text for the image
}>();

// State for the game object data
const gameObject = ref(null);
const loading = ref(false);
const error = ref(null);

// Compute the icon source based on whether an ID is provided
const iconSrc = computed(() => {
  if (!props.id || !gameObject.value) {
    return gameObjectIcon; // Use placeholder icon if no ID or game object not found
  }

  // If game object has an image, use it
  if (gameObject.value.image) {
    return gameObject.value.image;
  }

  // Fallback to placeholder icon
  return gameObjectIcon;
});

// Compute the alt text based on the alt prop or default to a descriptive text
const altText = computed(() => {
  if (props.alt) {
    return props.alt;
  }

  if (gameObject.value && gameObject.value.name) {
    return `Game Object: ${gameObject.value.name}`;
  }

  return 'Game Object';
});

// Fetch game object data when the component is mounted or when the ID changes
const fetchGameObject = async () => {
  if (!props.id) {
    gameObject.value = null;
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    // Find game object by ID in the gameObjects array
    const gameObjectData = worldEditorService.gameObjects.find(obj => obj.id === props.id);
    gameObject.value = gameObjectData;

    if (!gameObjectData) {
      console.warn(`Game object with ID ${props.id} not found`);
    }
  } catch (err) {
    console.error('Error fetching game object:', err);
    error.value = err;
    gameObject.value = null;
  } finally {
    loading.value = false;
  }
};

// Watch for changes to the ID prop
onMounted(() => {
  fetchGameObject();
});
</script>

<template>
  <div class="game-object-select-icon">
    <img :src="iconSrc" class="icon" :alt="altText" :class="{ 'is-loading': loading }"/>
    <div v-if="error" class="error-message">!</div>
  </div>
</template>

<style scoped>
.game-object-select-icon {
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