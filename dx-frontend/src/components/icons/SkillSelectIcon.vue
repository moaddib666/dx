<script setup lang="ts">
import { defineProps, computed, ref, onMounted } from 'vue';
import skillIcon from '@/assets/icons/skill.PNG';
import skillService from '@/services/skillService.js';

// Define props for the component
const props = defineProps<{
  id?: string | number; // Optional ID of the skill
  alt?: string; // Optional alt text for the image
}>();

// State for the skill data
const skill = ref(null);
const loading = ref(false);
const error = ref(null);

// Compute the icon source based on whether an ID is provided
const iconSrc = computed(() => {
  if (!props.id || !skill.value) {
    return skillIcon; // Use placeholder icon if no ID or skill not found
  }

  // If skill has an image, use it
  if (skill.value.image) {
    return skill.value.image;
  }

  // Fallback to placeholder icon
  return skillIcon;
});

// Compute the alt text based on the alt prop or default to a descriptive text
const altText = computed(() => {
  if (props.alt) {
    return props.alt;
  }

  if (skill.value && skill.value.name) {
    return `Skill: ${skill.value.name}`;
  }

  return 'Skill';
});

// Fetch skill data when the component is mounted or when the ID changes
const fetchSkill = async () => {
  if (!props.id) {
    skill.value = null;
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    // Get skill by ID
    const skillData = skillService.getSkill(props.id);
    skill.value = skillData;

    if (!skillData) {
      console.warn(`Skill with ID ${props.id} not found`);
    }
  } catch (err) {
    console.error('Error fetching skill:', err);
    error.value = err;
    skill.value = null;
  } finally {
    loading.value = false;
  }
};

// Watch for changes to the ID prop
onMounted(() => {
  fetchSkill();
});
</script>

<template>
  <div class="skill-select-icon">
    <img :src="iconSrc" class="icon" :alt="altText" :class="{ 'is-loading': loading }"/>
    <div v-if="error" class="error-message">!</div>
  </div>
</template>

<style scoped>
.skill-select-icon {
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