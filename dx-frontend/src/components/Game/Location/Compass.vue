<template>
  <div class="compass-container">
    <div
        v-for="direction in compassDirections"
        :key="direction.name"
        :class="['compass-block', direction.position]"
    >
      <div
          :class="{ active: isInteractive(direction.name), disabled: !isInteractive(direction.name) }"
          class="compass-arrow"
          @click="isInteractive(direction.name) && handleMove(direction.name)"
      >
        {{ direction.label }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CompassComponent",
  props: {
    connections: {
      type: Array,
      required: true,
    },
    centerLabel: {
      type: String,
      default: "", // Center can now be dynamic, e.g., "Up", "Down", or empty
    },
    centerAction: {
      type: Boolean,
      default: false, // Allows interaction if center is enabled
    },
  },
  data() {
    return {
      compassDirections: [
        {name: "North-West", label: "↖", position: "top-left"},
        {name: "North", label: "↑", position: "top-center"},
        {name: "North-East", label: "↗", position: "top-right"},
        {name: "West", label: "←", position: "middle-left"},
        {name: "Center", label: this.centerLabel, position: "middle-center"}, // Dynamically set label
        {name: "East", label: "→", position: "middle-right"},
        {name: "South-West", label: "↙", position: "bottom-left"},
        {name: "South", label: "↓", position: "bottom-center"},
        {name: "South-East", label: "↘", position: "bottom-right"},
      ],
    };
  },
  methods: {
    isInteractive(direction) {
      if (direction === "Center") {
        return this.centerAction; // Center is interactive if centerAction is true
      }
      return this.connections.some((conn) => conn.direction === direction && conn.is_active);
    },
    handleMove(direction) {
      this.$emit("move", direction);
    },
  },
};
</script>

<style scoped>
/* Fullscreen Centering */
.screen-center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background-color: rgba(0, 0, 0, 0.8); /* Dark semi-transparent background */
  box-sizing: border-box;
}

/* Outer Container */
.compass-container {
  display: flex;
  flex-wrap: wrap;
  width: 180px;
  height: 180px;
  border: 2px solid rgba(255, 255, 255, 0.5); /* Semi-transparent border */
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1); /* Light semi-transparent background */
  backdrop-filter: blur(8px); /* Add subtle blur for modern look */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Slight shadow */
  box-sizing: border-box;
}

/* Blocks for the 3x3 Grid */
.compass-block {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 33.33%;
  height: 33.33%;
  box-sizing: border-box;
  position: relative;
}

/* Styling for Arrows */
.compass-arrow {
  width: 45px;
  height: 45px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  font-size: 18px;
  font-weight: bold;
  user-select: none;
  background-color: rgba(255, 255, 255, 0.2); /* Semi-transparent arrow background */
  color: rgba(255, 255, 255, 0.7); /* Light text color */
  transition: all 0.3s ease-in-out; /* Smooth transition for hover and active states */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Subtle shadow for depth */
}

/* Active Arrow Styling */
.compass-arrow.active {
  background-color: rgba(10, 168, 184, 0.9); /* Modern teal color */
  color: white;
  cursor: pointer;
  transform: scale(1.1); /* Slight scale to make it pop */
  box-shadow: 0 4px 6px rgba(10, 168, 184, 0.4); /* Glow effect */
}

.compass-arrow.active:hover {
  transform: scale(1.3); /* Larger scale on hover */
  background-color: rgba(10, 168, 184, 1); /* Full teal on hover */
}

/* Disabled Arrow Styling */
.compass-arrow.disabled {
  background-color: rgba(255, 255, 255, 0.1); /* Faint background */
  color: rgba(255, 255, 255, 0.4); /* Faded text color */
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
