<template>
  <div class="coordinates-display">
    <span v-for="(value, key) in coordinates" :key="key" class="coordinate">
      <span class="axis">{{ key.toUpperCase() }}:</span>
      <span class="value">{{ value }}</span>
    </span>
  </div>
</template>

<script>
export default {
  name: "CoordinatesDisplay",
  props: {
    coordinates: {
      type: Object,
      required: false,
      default: () => ({ x: 0, y: 0, z: 0 }), // Default coordinates
    },
  },
};
</script>

<style scoped>
.coordinates-display {
  display: flex;
  gap: 1rem; /* Space between coordinate groups */
  font-family: "Roboto Mono", monospace; /* A clean monospace font */
  font-size: 1rem;
  background: rgba(0, 0, 0, 0.6); /* Semi-transparent background */
  padding: 0.5rem 1rem;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.9); /* Bright text for visibility */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.coordinate {
  display: flex;
  gap: 0.25rem; /* Space between axis and value */
  align-items: center;
}

.axis {
  font-weight: bold;
  color: rgba(50, 205, 50, 1); /* Green color for axis labels */
}

.value {
  color: rgba(255, 255, 255, 0.9); /* White color for values */
}
</style>
