<template>
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
      @click="onRoomClick"
  />
</template>

<script>
import {RoomType} from "@/utils/mapData.js";

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
  },
  data() {
    return {
      roomType: RoomType.DEFAULT.value,
      roomLabel: null,
    };
  },
  created() {
    this.extractLabels();
  },
  computed: {
    left() {
      return this.positionData.position.grid_x * this.cellSize + this.cellPadding / 2;
    },
    top() {
      return this.positionData.position.grid_y * this.cellSize + this.cellPadding / 2;
    },
    width() {
      return this.cellSize - this.cellPadding;
    },
    height() {
      return this.cellSize - this.cellPadding;
    },
  },
  methods: {
    extractLabels() {
      const labels = this.positionData.labels;
      if (!labels) {
        return
      }
      if (labels.length >= 1) {
        this.roomType = labels[0];
      }
      if (labels.length >= 2) {
        this.roomLabel = labels[1];
      }
    },
    onRoomClick() {
      this.$emit("room-click", this.positionData.position.id);
    },
  },
};
</script>
