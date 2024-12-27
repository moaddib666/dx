<template>
  <div class="position compact">
    <span class="grid">Grid: ({{ position.grid_x }}, {{ position.grid_y }}, {{ position.grid_z }})</span>
    <span class="sub-location">Sub-location: {{ position.sub_location }}</span>
  </div>
</template>

<script>
export default {
  name: 'PositionComponent',
  props: {
    position: Object,
  },
};
</script>

<style scoped>
.position.compact {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.5rem;
  border: 1px solid #444;
  border-radius: 4px;
  background: #1c1c1c;
  font-size: 0.8rem;
  color: #e0e0e0;
}

.grid {
  font-weight: bold;
  color: #ffcc00;
}

.sub-location {
  color: #aaa;
}
</style>
