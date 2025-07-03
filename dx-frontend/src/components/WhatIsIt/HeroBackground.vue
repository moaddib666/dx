<template>
  <div class="hero-background" @click="$emit('toggle-zoom', $event)"></div>
</template>

<script>
export default {
  name: 'HeroBackground',
  emits: ['toggle-zoom']
}
</script>

<style scoped>
.hero-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/images/backgrounds/generic-background.png');
  background-size: cover;
  background-position: center 10%;
  background-attachment: fixed;
  z-index: -1;
}

.hero-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7));
}

@media (max-width: 768px) {
  .hero-background {
    background-attachment: scroll; /* Fixed attachment can cause issues on mobile */
  }
}
</style>