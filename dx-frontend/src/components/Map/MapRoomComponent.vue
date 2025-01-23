<template>
  <g @click="onRoomClick">
    <!-- Room Background Rectangle -->
    <rect
        :fill="fill"
        :height="height"
        :stroke="stroke"
        :stroke-width="strokeWidth"
        :width="width"
        :x="left"
        :y="top"
        rx="8"
        ry="8"
    />

    <!-- Optional Label/Text -->
    <text
        v-if="showLabel"
        :fill="labelColor"
        :x="left + width / 2"
        :y="top + height / 2"
        dominant-baseline="middle"
        font-size="12"
        text-anchor="middle"
    >
      {{ label }}
    </text>
  </g>
</template>

<script>
export default {
  name: "Room",
  props: {
    positionData: {
      type: Object,
      required: true,
    },
    cellSize: {
      type: Number,
      required: true,
    },
    cellPadding: {
      type: Number,
      default: 10,
    },
    fill: {
      type: String,
      default: "#444",
    },
    stroke: {
      type: String,
      default: "#666",
    },
    strokeWidth: {
      type: Number,
      default: 2,
    },
    showLabel: {
      type: Boolean,
      default: true,
    },
    labelColor: {
      type: String,
      default: "#fff",
    },
  },
  computed: {
    // Calculate left position based on grid_x and cell size
    left() {
      return this.positionData.position.grid_x * this.cellSize + this.cellPadding / 2;
    },
    // Calculate top position based on grid_y and cell size
    top() {
      return this.positionData.position.grid_y * this.cellSize + this.cellPadding / 2;
    },
    // Adjusted width based on padding
    width() {
      return this.cellSize - this.cellPadding;
    },
    // Adjusted height based on padding
    height() {
      return this.cellSize - this.cellPadding;
    },
    // Use the last label as the room's label, or fallback to coordinates
    label() {
      const labels = this.positionData.labels || [];
      return labels.length > 0 ? labels[labels.length - 1] : `${this.positionData.position.grid_x}x${this.positionData.position.grid_y}`;
    },
  },
  methods: {
    onRoomClick() {
      this.$emit("room-click", this.positionData.position.id);
    },
  },
};
</script>

<style scoped>
/* Add optional styling here if needed */
</style>
