<script>
export default {
  name: "BarComponent",
  props: {
    type: {
      type: String,
      required: true
    },
    currentValue: {
      type: Number,
      required: true
    },
    maxValue: {
      type: Number,
      required: true
    }
  },
  computed: {
    barWidth() {
      return (this.currentValue / this.maxValue) * 100 + '%';
    },
    barClass() {
      switch (this.type) {
        case 'health':
          return 'health-bar';
        case 'energy':
          return 'energy-bar';
        case 'ap':
          return 'ap-bar';
        default:
          return "health-bar"
      }
    }
  }
}
</script>

<template>
  <div class="bar-component">
    <div class="bar-container">
      <div class="bar" :class="barClass" :style="{ width: barWidth }"></div>
      <div class="bar-labels">
        <span class="current-value">{{ currentValue }}</span>/<span class="max-value">{{ maxValue }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bar-component {
  font-family: 'Orbitron', sans-serif;
  width: 100%;
  margin: 0.1vh;
}

.bar-container {
  width: 100%;
  height: 2vh;
  background-color: rgba(46, 46, 46, 0.8);
  border-radius: 0.4rem;
  overflow: hidden;
  position: relative;
  box-shadow: 0 0 0.1rem rgba(0, 0, 0, 0.5);
}

.bar {
  height: 100%;
  transition: width 0.3s ease-in-out;
  border-radius: 0.4rem;
  color: #fff;
  font-family: 'Orbitron', sans-serif; /* Sci-fi themed font */
}

.health-bar {
  background: linear-gradient(135deg, rgba(255, 69, 0, 0.8) 0%, rgba(255, 140, 0, 0.3) 100%);
  box-shadow: 0 0 0.4rem rgba(255, 99, 71, 0.6), 0 0 20px rgba(255, 69, 0, 0.8) inset;
}

.energy-bar {
  background: linear-gradient(135deg, rgba(30, 144, 255, 0.8) 0%, rgba(135, 206, 250, 0.3) 100%);
  box-shadow: 0 0 0.4rem rgba(135, 206, 250, 0.6), 0 0 20px rgba(30, 144, 255, 0.8) inset;
}

.ap-bar {
  background: linear-gradient(135deg, rgba(0, 255, 0, 0.8) 0%, rgba(0, 128, 0, 0.3) 100%);
  box-shadow: 0 0 0.4rem rgba(0, 255, 0, 0.6), 0 0 20px rgba(0, 128, 0, 0.8) inset;

}

.bar-labels {
  position: absolute;
  width: 100%;
  text-align: center;
  top: 0;
  font-size: 0.8rem;
  font-weight: bold;
  line-height: 0.8rem; /* Ensures the text is vertically centered */
  pointer-events: none; /* Ensures the text doesn't interfere with any interactive elements */
}
</style>
