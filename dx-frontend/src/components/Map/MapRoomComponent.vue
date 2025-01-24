<template>
  <g>
    <!-- Background rectangle -->
    <rect
        :fill="backgroundFill"
        :width="width"
        :x="left"
        :height="height"
        :y="top"
        :stroke="stroke"
        :stroke-width="strokeWidth"
        rx="8"
        ry="8"
    />

    <!-- Clipped circular image -->
    <clipPath :id="clipId">
      <circle
          :cx="left + width / 2"
          :cy="top + height / 2"
          :r="Math.min(width, height) / 2 - padding"
      />
    </clipPath>
    <image
        v-if="backgroundImage"
        :clip-path="`url(#${clipId})`"
        :height="height"
        :href="backgroundImageSrc"
        :width="width"
        :x="left"
        :y="top"
        preserveAspectRatio="xMidYMid slice"
    />
  </g>
</template>

<script>
import {RoomLabel, RoomType} from "@/utils/mapData.js";

export default {
  name: "Room",
  props: {
    positionData: {type: Object, required: true},
    cellSize: {type: Number, required: true},
    cellPadding: {type: Number, default: 10},
    fill: {type: String, default: "#444"},
    stroke: {type: String, default: "#666"},
    strokeWidth: {type: Number, default: 2},
    padding: {type: Number, default: 8}, // Padding for the circle
  },
  data() {
    return {
      roomType: null,
      roomLabel: null,
      backgroundImage: null,
    };
  },
  created() {
    this.extractLabels();
    this.loadIcon();
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
    backgroundFill() {
      if (this.roomType && RoomType[this.roomType.toUpperCase()]) {
        return RoomType[this.roomType.toUpperCase()].color;
      }
      return this.fill;
    },
    backgroundImageSrc() {
      return this.backgroundImage ? this.backgroundImage.src : null;
    },
    clipId() {
      // Unique ID for the clipPath to avoid conflicts
      return `clip-${this.positionData.position.id}`;
    },
  },
  watch: {
    positionData: {
      immediate: true,
      handler() {
        this.extractLabels();
        this.loadIcon();
      },
    },
  },
  methods: {
    extractLabels() {
      const labels = this.positionData.labels || [];
      this.roomType = labels[0] || null;
      this.roomLabel = labels[1] || null;
    },
    loadIcon() {
      const icon = RoomLabel.getIcon(this.roomLabel);
      if (icon instanceof HTMLImageElement) {
        this.backgroundImage = icon;
      } else {
        this.backgroundImage = null;
      }
    },
  },
};
</script>
