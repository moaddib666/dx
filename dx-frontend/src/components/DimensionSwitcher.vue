<template>
  <div class="dimension-switcher container">
    <button
        v-for="dimension in dimensions"
        :key="dimension.id"
        @click="switchDimension(dimension.id)"
        :class="{ active: activeDimension === dimension.id }"
    >
      {{ dimension.name }}
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeDimension: 1,
      dimensions: [
        { id: 1, name: 'Dimension 1' },
        { id: 2, name: 'Dimension 2' },
        { id: 3, name: 'Dimension 3' },
        { id: 4, name: 'Dimension 4' }
      ]
    };
  },
  methods: {
    switchDimension(id) {
      this.activeDimension = id;
    }
  }
};
</script>

<style scoped>
.dimension-switcher {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.dimension-switcher button {
  margin: 0 10px;
  padding: 10px 20px;
  background-color: var(--deep-purple);
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
}

.dimension-switcher button:hover {
  background-color: var(--cyber-yellow);
  color: #000000;
}

.dimension-switcher .active {
  border: 2px solid var(--cyber-yellow);
  box-shadow: 0 0 10px var(--cyber-yellow);
}
</style>
