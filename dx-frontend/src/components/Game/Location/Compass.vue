<template>
  <div class="compass-container">
    <!-- Directional grid -->
    <div class="direction-grid">
      <div
          v-for="direction in computedCompassDirections"
          :key="direction.name"
          :class="['direction-cell', direction.position]"
      >
        <button
            :class="[
            'direction-btn',
            {
              'btn-active': isInteractive(direction),
              'btn-disabled': !isInteractive(direction) && !direction.locked,
              'btn-locked': direction.locked,
            }
          ]"
            @click="handleClick(direction)"
            :disabled="!isInteractive(direction)"
        >
          <span class="direction-arrow">{{ direction.label }}</span>
          <span class="direction-label">{{ direction.displayName }}</span>
        </button>
      </div>
    </div>

    <!-- Center control -->
    <div class="center-control">
      <div class="center-display">
        <div class="current-location">{{ currentDimension || 'DIM-1' }}</div>
      </div>

      <button
          v-if="centerConnection"
          :class="[
          'dimensional-btn',
          {
            'dim-active': isInteractive(centerConnection),
            'dim-locked': centerConnection.locked,
          }
        ]"
          @click="handleClick(centerConnection)"
          :disabled="!isInteractive(centerConnection)"
      >
        <span class="dim-arrow">
          {{ centerConnection.direction === 'Up' ? '▲' : '▼' }}
        </span>
        <span class="dim-label">{{ centerConnection.direction }}</span>
      </button>
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
    currentDimension: {
      type: [String, Number],
      default: 1
    }
  },
  computed: {
    computedCompassDirections() {
      const baseDirections = [
        {name: "North-West", displayName: "NW", label: "↖", position: "nw"},
        {name: "North", displayName: "N", label: "↑", position: "n"},
        {name: "North-East", displayName: "NE", label: "↗", position: "ne"},
        {name: "West", displayName: "W", label: "←", position: "w"},
        {name: "East", displayName: "E", label: "→", position: "e"},
        {name: "South-West", displayName: "SW", label: "↙", position: "sw"},
        {name: "South", displayName: "S", label: "↓", position: "s"},
        {name: "South-East", displayName: "SE", label: "↘", position: "se"},
      ];

      return baseDirections.map((direction) => {
        const connection = this.connections.find((conn) => conn.direction === direction.name);
        return {
          ...direction,
          locked: connection?.is_locked || false,
          is_active: connection?.is_active || false,
        };
      });
    },

    centerConnection() {
      return this.connections.find(
          (conn) => conn.direction === "Up" || conn.direction === "Down"
      );
    }
  },
  methods: {
    isInteractive(direction) {
      return direction.is_active && !direction.locked;
    },
    handleClick(direction) {
      if (this.isInteractive(direction)) {
        this.$emit("move", direction.name || direction.direction);
      }
    }
  },
};
</script>

<style scoped>
.compass-container {
  width: 280px;
  height: 280px;
  background: #0a0f1c;
  border: 1px solid #1e293b;
  border-radius: 8px;
  position: relative;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.direction-grid {
  position: absolute;
  top: 16px;
  left: 16px;
  right: 16px;
  bottom: 16px;
  display: grid;
  grid-template-areas:
    "nw  n  ne"
    "w   c  e"
    "sw  s  se";
  grid-template-columns: 72px 1fr 72px;
  grid-template-rows: 72px 1fr 72px;
  gap: 8px;
}

.direction-cell.nw { grid-area: nw; }
.direction-cell.n { grid-area: n; }
.direction-cell.ne { grid-area: ne; }
.direction-cell.w { grid-area: w; }
.direction-cell.e { grid-area: e; }
.direction-cell.sw { grid-area: sw; }
.direction-cell.s { grid-area: s; }
.direction-cell.se { grid-area: se; }

.direction-btn {
  width: 100%;
  height: 100%;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
  color: #94a3b8;
}

.direction-btn:hover:not(:disabled) {
  background: #2d3d52;
  border-color: #475569;
}

.direction-arrow {
  font-size: 20px;
  font-weight: 600;
  line-height: 1;
}

.direction-label {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.btn-active {
  background: #1e40af !important;
  border-color: #2563eb !important;
  color: #dbeafe !important;
}

.btn-active:hover {
  background: #1d4ed8 !important;
  border-color: #3b82f6 !important;
}

.btn-disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.btn-locked {
  background: #7f1d1d !important;
  border-color: #991b1b !important;
  color: #fecaca !important;
  cursor: not-allowed;
}

.center-control {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.center-display {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 4px;
  padding: 6px 12px;
}

.current-location {
  font-size: 12px;
  font-weight: 600;
  color: #fbbf24;
  letter-spacing: 1px;
}

.dimensional-btn {
  background: #059669;
  border: 1px solid #10b981;
  border-radius: 6px;
  padding: 8px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  cursor: pointer;
  transition: all 0.15s ease;
  color: #d1fae5;
  min-width: 60px;
}

.dimensional-btn:hover:not(:disabled) {
  background: #047857;
  border-color: #059669;
}

.dim-arrow {
  font-size: 16px;
  font-weight: bold;
}

.dim-label {
  font-size: 10px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dim-locked {
  background: #7f1d1d !important;
  border-color: #991b1b !important;
  color: #fecaca !important;
  cursor: not-allowed;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .compass-container {
    width: 240px;
    height: 240px;
  }

  .direction-grid {
    grid-template-columns: 60px 1fr 60px;
    grid-template-rows: 60px 1fr 60px;
  }

  .direction-arrow {
    font-size: 18px;
  }

  .direction-label {
    font-size: 10px;
  }
}
</style>