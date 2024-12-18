<template>
  <line
      :x1="start.grid_x * cellSize + cellSize / 2"
      :x2="end.grid_x * cellSize + cellSize / 2"
      :y1="start.grid_y * cellSize + cellSize / 2"
      :y2="end.grid_y * cellSize + cellSize / 2"
      stroke="black"
  />
</template>

<script>
export default {
  props: {
    start: Object,
    end: Object,
    cellSize: {
      type: Number,
      default: 50,
    },
  },
};
</script>
