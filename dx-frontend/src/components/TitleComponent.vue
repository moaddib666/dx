<template>
  <div>
    <div class="title">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      font: 'Orbitron',
      color: '#FFFFFF',
      glow: true
    };
  },
  computed: {
    titleStyle() {
      return {
        fontFamily: this.font,
        color: this.color,
        textShadow: this.glow ? '0 0 10px rgba(0, 255, 255, 0.8), 0 0 20px rgba(0, 255, 255, 0.6)' : 'none',
        textAlign: 'center',
        marginTop: '2vw',
      };
    }
  }
};
</script>

<style scoped>
@font-face {
  font-family: 'Orbitron';
  src: url('@/assets/fonts/Orbitron-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

.title {
  font-family: 'Orbitron', sans-serif;
  color: #FFFFFF;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.6), 0 0 20px rgba(0, 255, 255, 0.4);
  margin-top: 2vw;
  transition: all 0.3s ease;
  position: relative;
}

@media (max-width: 600px) {
  .title {
    font-size: 6vw;
  }
}

@media (min-width: 601px) and (max-width: 1200px) {
  .title {
    font-size: 4vw;
  }
}

@media (min-width: 1201px) {
  .title {
    font-size: 3vw;
  }
}
</style>
