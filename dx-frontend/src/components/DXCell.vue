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
      <!-- Text overlay -->
      <div class="text-overlay">
        <div class="name">{{ title }}</div>
        <div class="subtitle">{{ subtitle }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Import the same fonts as in the original HTML */
@import url('https://fonts.googleapis.com/css2?family=Cinzel&family=Source+Code+Pro&display=swap');

.card {
  /* Base styling */
  width: 100%;
  height: 100%;
  text-align: center;

  /* Flex layout for better responsiveness */
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  /* Color */
  color: #d6b97b;
  font-family: 'Cinzel', serif;
  container-type: inline-size;
}

/* Image container to ensure consistent sizing */
.image-container {
  width: 100%;
  height: 100%; /* Take up full height of the card */
  overflow: hidden; /* Prevent image from overflowing container */
  position: relative; /* For absolute positioning of the text overlay */

  border: 0.3rem solid transparent;
  border-image-slice:
      60 60 60 60;
  border-image-width:
      10px 10px 10px 10px;
  border-image-outset:
      0px 0px 0px 0px;
  border-image-repeat:
      stretch stretch;
  border-image-source: url("@/assets/images/border/borderassets.png");
}

/* Image styling */
.card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block; /* Remove any default spacing */
}

/* Text overlay styling */
.text-overlay {
  position: absolute;
  bottom: 0; /* Position 10% from the bottom */
  left: 0;
  width: 100%;
  background-color: rgba(13, 15, 17, 0.7); /* Semi-transparent background */
  z-index: 1;
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
  font-size: 10cqw;
  opacity: 0.7;
}

.subtitle {
  font-family: 'Source Code Pro', monospace;
  opacity: 0.7; /* Increased opacity for better visibility on image */
  font-size: 7cqw;
  margin-top: 0.2em;
}

.name {
  font-weight: bold;
  font-size: 11cqw;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8); /* Add shadow for better readability */
}

</style>