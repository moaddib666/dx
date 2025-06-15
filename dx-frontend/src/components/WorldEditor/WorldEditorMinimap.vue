<template>
  <div class="world-editor-minimap">
    <!-- SVG for minimap rendering -->
    <svg
        class="minimap-svg"
        height="100%"
        width="100%"
        @click="onMinimapClick"
    >
      <!-- Background -->
      <rect
          fill="#1e1e1e"
          height="100%"
          stroke="#555"
          stroke-width="1"
          width="100%"
          x="0"
          y="0"
      />

      <!-- Rooms -->
      <g class="minimap-rooms">
        <rect
            v-for="room in floorRooms"
            :key="'minimap-room-' + room.id"
            :fill="getRoomColor(room)"
            :height="roomSize"
            :width="roomSize"
            :x="getRoomX(room)"
            :y="getRoomY(room)"
            rx="2"
            ry="2"
        />
      </g>

      <!-- View bounds indicator -->
      <rect
          v-if="viewBounds"
          :height="transformedViewBounds.height"
          :width="transformedViewBounds.width"
          :x="transformedViewBounds.x"
          :y="transformedViewBounds.y"
          class="view-bounds"
          fill="rgba(30, 144, 255, 0.1)"
          stroke="#1E90FF"
          stroke-dasharray="4,2"
          stroke-width="2"
      />
    </svg>

    <!-- Floor indicator -->
    <div class="floor-indicator">
      Floor {{ currentFloor }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'WorldEditorMinimap',
  props: {
    rooms: {
      type: Array,
      default: () => []
    },
    currentFloor: {
      type: Number,
      default: 1
    },
    viewBounds: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      // Minimap configuration
      padding: 10,
      roomSize: 4,
      scale: 0.1, // Scale factor for converting map coordinates to minimap
      lastUpdateTime: 0, // For debouncing updates
      debounceDelay: 50 // Milliseconds to wait before updating
    };
  },
  computed: {
    // Filter rooms for current floor
    floorRooms() {
      return this.rooms.filter(room => room.position.grid_z === this.currentFloor);
    },

    // Calculate bounds of all rooms
    mapBounds() {
      if (!this.floorRooms.length) {
        return {minX: 0, maxX: 0, minY: 0, maxY: 0};
      }

      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;

      this.floorRooms.forEach(room => {
        const {grid_x, grid_y} = room.position;
        if (grid_x < minX) minX = grid_x;
        if (grid_x > maxX) maxX = grid_x;
        if (grid_y < minY) minY = grid_y;
        if (grid_y > maxY) maxY = grid_y;
      });

      return {minX, maxX, minY, maxY};
    },

    // Transform view bounds from main map to minimap coordinates
    transformedViewBounds() {
      if (!this.viewBounds) return null;

      const {minX, minY} = this.mapBounds;
      const cellSize = 80; // Same as in WorldEditorMap

      // Convert main map coordinates to minimap coordinates
      // Ignore any properties starting with underscore (like _windowWidth, _windowHeight)
      return {
        x: (this.viewBounds.x / cellSize - minX) * cellSize * this.scale + this.padding,
        y: (this.viewBounds.y / cellSize - minY) * cellSize * this.scale + this.padding,
        width: this.viewBounds.width * this.scale,
        height: this.viewBounds.height * this.scale
      };
    }
  },
  mounted() {
    // Adjust scale based on map bounds and minimap size
    this.updateScale();

    // Add resize event listener
    window.addEventListener('resize', this.handleResize);
  },

  beforeUnmount() {
    // Clean up resize event listener
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    // Update scale factor based on map bounds and minimap size
    updateScale() {
      const {minX, maxX, minY, maxY} = this.mapBounds;
      const width = maxX - minX + 2; // Add margin
      const height = maxY - minY + 2;

      if (width === 0 || height === 0) return;

      const containerWidth = this.$el.clientWidth - this.padding * 2;
      const containerHeight = this.$el.clientHeight - this.padding * 2;

      // Calculate scale to fit map in minimap
      const scaleX = containerWidth / (width * 80); // 80 is cellSize from WorldEditorConfig
      const scaleY = containerHeight / (height * 80);

      this.scale = Math.min(scaleX, scaleY, 0.2); // Limit max scale
    },

    // Get room position on minimap
    getRoomX(room) {
      const {minX} = this.mapBounds;
      return (room.position.grid_x - minX) * 80 * this.scale + this.padding;
    },

    getRoomY(room) {
      const {minY} = this.mapBounds;
      return (room.position.grid_y - minY) * 80 * this.scale + this.padding;
    },

    // Get room color based on type
    getRoomColor(room) {
      if (room.type === 'special') return '#8A2BE2';
      if (room.type === 'secret') return '#9932CC';
      if (room.type === 'dangerous') return '#B22222';
      return '#444';
    },

    // Handle click on minimap
    onMinimapClick(event) {
      const {minX, minY} = this.mapBounds;
      const rect = event.target.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      // Convert click coordinates to map coordinates
      const mapX = (x - this.padding) / this.scale + minX * 80;
      const mapY = (y - this.padding) / this.scale + minY * 80;

      // Emit navigate event with map coordinates
      this.$emit('navigate', {x: mapX, y: mapY});
    },

    // Handle window resize with debouncing
    handleResize() {
      const now = Date.now();
      if (now - this.lastUpdateTime > this.debounceDelay) {
        this.lastUpdateTime = now;
        requestAnimationFrame(() => {
          this.updateScale();
        });
      }
    }
  },
  watch: {
    // Update scale when rooms or floor changes
    floorRooms() {
      this.$nextTick(() => {
        this.updateScale();
      });
    },

    // Debounce viewBounds updates for better performance
    viewBounds: {
      handler() {
        const now = Date.now();
        if (now - this.lastUpdateTime > this.debounceDelay) {
          this.lastUpdateTime = now;
          // Use requestAnimationFrame for smooth visual updates
          requestAnimationFrame(() => {
            // The actual update happens through the transformedViewBounds computed property
          });
        }
      },
      deep: true
    }
  }
};
</script>

<style scoped>
.world-editor-minimap {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.minimap-svg {
  cursor: pointer;
}

.view-bounds {
  pointer-events: none;
}

.floor-indicator {
  position: absolute;
  top: 5px;
  left: 5px;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  padding: 2px 5px;
  border-radius: 3px;
  font-size: 10px;
  pointer-events: none;
}

/* Hover effect for better UX */
.minimap-svg:hover .view-bounds {
  stroke: #4FC3F7;
}
</style>
