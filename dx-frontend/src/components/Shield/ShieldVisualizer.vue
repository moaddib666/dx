<template>
  <div class="shield-visualizer" :title="description">
    <div class="shield-image" :style="{ backgroundImage: `url(${shield.icon})` }">
      <span class="shield-level">{{ level }}</span>
    </div>
    <div class="shield-cycles">{{ cyclesLeft }}</div>
  </div>
</template>

<script>
export default {
  name: "ShieldVisualizer",
  computed: {
    description() {
      return `Defend from the ${this.shield.id} attacks`;
    },
  },
  props: {
    shield: {
      type: Object,
      required: true,
    },
    level: {
      type: Number,
      required: true,
    },
    cyclesLeft: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style scoped>
.shield-visualizer {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  justify-content: center;
}

.shield-image {
  display: flex;
  width: 2rem;
  height: 2rem;
  background-size: cover;
  background-position: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  justify-content: center;
  align-items: center;
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}

.shield-level {
  cursor: pointer;
  font-size: 0.9rem;
  color: rgb(255, 251, 22);
  text-shadow: 0 0 0.1rem rgb(0, 0, 0);
  font-weight: bold;
  padding: 0.2rem 0.5rem;
  border-radius: 0.5rem;
}

.shield-cycles {
  margin-top: 0.3rem;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: bold;
}
</style>
