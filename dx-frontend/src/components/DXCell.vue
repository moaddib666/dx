<script setup lang="ts">
import { computed, ref } from 'vue';

interface Props {
  image: string;
  title: string;
  subtitle: string;
}

const props = defineProps<Props>();

// Track if image failed to load
const imageError = ref(false);

// Computed property to handle image source
const imageSource = computed(() => props.image);

// Handle image load error
const handleImageError = () => {
  imageError.value = true;
};
</script>

<template>
  <div class="card">
    <div class="image-container">
      <!-- Show image if no error -->
      <img
        v-if="!imageError"
        :src="imageSource"
        alt="Card Image"
        @error="handleImageError"
      />
      <!-- Show placeholder if image failed to load -->
      <div v-else class="image-placeholder">
        <div class="placeholder-icon">?</div>
        <div class="placeholder-text">Image not found</div>
      </div>
    </div>
    <div class="name">{{ title }}</div>
    <div class="subtitle">{{ subtitle }}</div>
  </div>
</template>

<style scoped>
/* Import the same fonts as in the original HTML */
@import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Source+Code+Pro&display=swap');

.card {
  /* Base styling */
  width: 100%;
  height: 100%;
  background-color: #0d0f11;
  border: 0.0625em solid #2a2d31;
  padding: 0.75em;
  box-shadow: 0 0 0.625em #000;
  border-radius: 0.25em;
  text-align: center;

  /* Flex layout for better responsiveness */
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  /* Make the component adapt to its container */
  box-sizing: border-box;

  /* Color */
  color: #d6b97b;
  font-family: 'Cinzel', serif;
  container-type: inline-size;
}

/* Image container to ensure consistent sizing */
.image-container {
  width: 100%;
  aspect-ratio: 1 / 1.12; /* Approximates the original ratio */
  margin-bottom: 0.5em;
  border: 0.0625em solid #2a2d31;
  overflow: hidden; /* Prevent image from overflowing container */
  box-sizing: border-box;
}

/* Image styling */
.card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block; /* Remove any default spacing */
  aspect-ratio: 1
}

/* Placeholder styling */
.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #1a1c1f;
  color: #d6b97b;
}

.placeholder-icon {
  font-size: 2em;
  font-weight: bold;
  margin-bottom: 0.25em;
}

.placeholder-text {
  font-size: 0.75em;
  opacity: 0.7;
}

.subtitle {
  font-family: 'Source Code Pro', monospace;
  opacity: 0.4;
  font-size: 7cqw;
}

.name {
  font-weight: bold;
  font-size: 11cqw;
}

</style>