<template>
  <div class="hero-background" @click="$emit('toggle-zoom', $event)"></div>
</template>

<script setup lang="ts">
defineEmits<{
  (e: 'toggle-zoom', event: Event): void
}>()
</script>

<style scoped>
.hero-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh; /* Explicitly set to 100vh instead of 100% */
  background-image: url('@/assets/images/backgrounds/generic-background.png');
  background-size: cover;
  background-position: center 10%;
  background-attachment: fixed;
  z-index: -1;
}

.hero-background::after {
  content: '';
  position: fixed; /* Changed from absolute to fixed to match the parent */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100vh; /* Explicitly set to 100vh to match the parent */
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7));
}

@media (max-width: 768px) {
  .hero-background {
    background-attachment: scroll; /* Fixed attachment can cause issues on mobile */
  }

  .hero-background::after {
    position: absolute; /* Use absolute instead of fixed on mobile for better performance */
    height: 100%; /* Use 100% instead of 100vh on mobile for better compatibility */
  }
}
</style>