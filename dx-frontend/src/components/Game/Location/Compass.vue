<template>
  <div class="compass-container">
    <div
        v-for="direction in computedCompassDirections"
        :key="direction.name"
        :class="['compass-block', direction.position]"
    >
      <div
          class="compass-arrow"
          :class="{
          active: isInteractive(direction),
          disabled: !isInteractive(direction) && !direction.locked,
          locked: direction.locked,
          center: direction.name === 'Up' || direction.name === 'Down',
        }"
          @click="handleClick(direction)"
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
      type: Array, // Array of objects with {direction, is_active, locked}
      required: true,
    },
  },
  computed: {
    computedCompassDirections() {
      // Define base directions
      const baseDirections = [
        {name: "North-West", label: "↖", position: "top-left", locked: false},
        {name: "North", label: "↑", position: "top-center", locked: false},
        {name: "North-East", label: "↗", position: "top-right", locked: false},
        {name: "West", label: "←", position: "middle-left", locked: false},
        {name: "East", label: "→", position: "middle-right", locked: false},
        {name: "South-West", label: "↙", position: "bottom-left", locked: false},
        {name: "South", label: "↓", position: "bottom-center", locked: false},
        {name: "South-East", label: "↘", position: "bottom-right", locked: false},
      ];

      // Find connections and add locking/active states
      const directionsWithStates = baseDirections.map((direction) => {
        const connection = this.connections.find((conn) => conn.direction === direction.name);
        return {
          ...direction,
          locked: connection?.is_locked || false,
          is_active: connection?.is_active || false,
        };
      });

      // Handle center connection (Up/Down)
      const centerConnection = this.connections.find(
          (conn) => conn.direction === "Up" || conn.direction === "Down"
      );
      const center = {
        name: centerConnection?.direction || "Center",
        label: centerConnection?.direction === "Up" ? "↑" : centerConnection?.direction === "Down" ? "↓" : "",
        position: "middle-center",
        locked: centerConnection?.is_locked || false,
        is_active: centerConnection?.is_active || false,
      };

      return [...directionsWithStates, center];
    },
  },
  methods: {
    isInteractive(direction) {
      return direction.is_active && !direction.locked;
    },
    handleClick(direction) {
      if (this.isInteractive(direction)) {
        this.$emit("move", direction.name);
      }
    },
  },
};
</script>

<style scoped>
/* Compass Container */
.compass-container {
  display: grid;
  grid-template-areas:
    "NW N NE"
    "W  C  E"
    "SW S SE";
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  width: 180px;
  height: 180px;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  box-sizing: border-box;
}

/* Compass Blocks */
.compass-block {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  position: relative;
}

.compass-block.top-left {
  grid-area: NW;
}

.compass-block.top-center {
  grid-area: N;
}

.compass-block.top-right {
  grid-area: NE;
}

.compass-block.middle-left {
  grid-area: W;
}

.compass-block.middle-center {
  grid-area: C;
}

.compass-block.middle-right {
  grid-area: E;
}

.compass-block.bottom-left {
  grid-area: SW;
}

.compass-block.bottom-center {
  grid-area: S;
}

.compass-block.bottom-right {
  grid-area: SE;
}

/* Arrow Styles */
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
  background-color: rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease-in-out;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Active Arrow */
.compass-arrow.active {
  background-color: rgba(10, 168, 184, 0.9);
  color: white;
  cursor: pointer;
  transform: scale(1.1);
  box-shadow: 0 4px 6px rgba(10, 168, 184, 0.4);
}

.compass-arrow.active:hover {
  transform: scale(1.3);
  background-color: rgba(10, 168, 184, 1);
}

/* Disabled Arrow */
.compass-arrow.disabled {
  background-color: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.4);
  cursor: not-allowed;
  opacity: 0.5;
}

/* Locked Arrow */
.compass-arrow.locked {
  background-color: rgba(255, 69, 58, 0.2);
  color: rgba(255, 69, 58, 0.9);
  cursor: not-allowed;
}

/* Center Arrow */
.compass-arrow.center {
  background-color: rgba(255, 195, 0, 0.9);
  color: white;
  font-size: 20px;
  font-weight: bold;
  border: 2px solid rgba(255, 255, 255, 0.7);
  box-shadow: 0 4px 8px rgba(255, 195, 0, 0.4);
  transform: scale(1.2);
}

.compass-arrow.center.locked {
  background-color: rgba(255, 69, 58, 0.2);
  color: rgba(255, 69, 58, 0.9);
}

.compass-arrow.center.locked:hover {
  cursor: not-allowed;
  transform: scale(1.2);
  background-color: rgba(255, 69, 58, 0.2);
}


.compass-arrow.center:hover {
  transform: scale(1.4);
  background-color: rgba(255, 195, 0, 1);
}
</style>
