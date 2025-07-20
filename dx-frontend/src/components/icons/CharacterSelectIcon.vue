<script setup lang="ts">
import { defineProps, computed, ref, onMounted } from 'vue';
import characterIcon from '@/assets/icons/character.PNG';
import { characterTemplatesService } from '@/services/CharacterTemplatesService.js';

// Define props for the component
const props = defineProps<{
  id?: string | number; // Optional ID of the character
  alt?: string; // Optional alt text for the image
}>();

// State for the character data
const character = ref(null);
const loading = ref(false);
const error = ref(null);

// Compute the icon source based on whether an ID is provided
const iconSrc = computed(() => {
  if (!props.id || !character.value) {
    return characterIcon; // Use placeholder icon if no ID or character not found
  }

  // If character has an image, use it
  if (character.value.image) {
    return character.value.image;
  }

  // Fallback to placeholder icon
  return characterIcon;
});

// Compute the alt text based on the alt prop or default to a descriptive text
const altText = computed(() => {
  if (props.alt) {
    return props.alt;
  }

  if (character.value && character.value.name) {
    return `Character: ${character.value.name}`;
  }

  return 'Character';
});

// Fetch character data when the component is mounted or when the ID changes
const fetchCharacter = async () => {
  if (!props.id) {
    character.value = null;
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    // Get character template by ID
    const characterData = characterTemplatesService.getTemplateById(props.id);
    character.value = characterData;
  } catch (err) {
    console.error('Error fetching character:', err);
    error.value = err;
    character.value = null;
  } finally {
    loading.value = false;
  }
};

// Watch for changes to the ID prop
onMounted(() => {
  fetchCharacter();
});
</script>

<template>
  <div class="character-select-icon">
    <img :src="iconSrc" class="icon" :alt="altText" :class="{ 'is-loading': loading }"/>
    <div v-if="error" class="error-message">!</div>
  </div>
</template>

<style scoped>
.character-select-icon {
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