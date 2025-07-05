<template>
  <div class="auth-background" @click="$emit('toggle-zoom', $event)"></div>
</template>

<script>
export default {
  name: 'AuthBackground',
  emits: ['toggle-zoom']
}
</script>

<style scoped>
.auth-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-image: url('@/assets/images/backgrounds/login_v1.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  z-index: -1;
}

.auth-background::after {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100vh;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7));
}

@media (max-width: 768px) {
  .auth-background {
    background-attachment: scroll; /* Fixed attachment can cause issues on mobile */
  }

  .auth-background::after {
    position: absolute; /* Use absolute instead of fixed on mobile for better performance */
    height: 100%; /* Use 100% instead of 100vh on mobile for better compatibility */
  }
}
</style>