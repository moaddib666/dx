<script setup lang="ts">
// FightFooter component
</script>

<template>
  <div class="fight-footer">
    <div class="background-container">
      <div class="png-background-effect"></div>
      <div class="png-background"></div>
    </div>
  </div>
</template>

<style scoped>
.fight-footer {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  width: 100%;
  position: relative;
  overflow: hidden;
}

.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.png-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/fight/crowd.png') repeat-x center center;
  background-size: contain;
}

.png-background-effect {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    rgb(22, 234, 255),
    rgb(253, 167, 53)
  );
  background-size: contain;
  opacity: 0.5; /* Adjust opacity for the effect */
  mask: url('@/assets/fight/crowd.png') repeat-x center center;
  mask-size: contain;
  transform: scale(1.005);
  filter: blur(3rem) drop-shadow(0 0.2rem rgba(0, 0, 0, 0.6)) drop-shadow(0 0.1rem rgba(0, 0, 0, 0.4));
  backdrop-filter: blur(3rem);
  animation: gradientAnimation 5s linear infinite;
  transition: all 0.3s ease;
}

@keyframes gradientAnimation {
  0% {
    background: linear-gradient(rgb(22, 234, 255), rgb(253, 167, 53));
  }
  50% {
    background: linear-gradient(rgb(253, 167, 53), rgb(22, 234, 255));
  }
  100% {
    background: linear-gradient(rgb(22, 234, 255), rgb(253, 167, 53));
  }
}
</style>