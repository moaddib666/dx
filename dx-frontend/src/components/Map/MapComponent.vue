<template>
  <div ref="container" class="svg-map-container">
    <!-- Simple control bar to toggle modes and show current floor -->
    <div class="control-bar">
      <button @click="$emit('syncMap')"> Sync</button>
      <button @click="toggleMode">
        {{ dragMode ? "Switch to Interact" : "Switch to Drag" }}
      </button>
      <span>Floor: {{ currentFloor }}</span>
      <button @click="floorUp">Floor +</button>
      <button @click="floorDown">Floor -</button>
    </div>

    <!-- Main SVG, with panning/zoom when dragMode is true -->
    <svg
        height="100%"
        width="100%"
        @click="onSvgClick"
        @mousedown="onMouseDown"
        @mousemove="onMouseMove"
        @mouseup="onMouseUp"
        @wheel.prevent="onWheel"
    >
      <!-- A single group to apply pan+zoom transforms -->
      <g :transform="finalTransform">
        <!-- Grid lines, aligned to integer cell boundaries -->
        <g class="grid">
          <line
              v-for="(vl, i) in gridLines.vertical"
              :key="'vLine-' + i"
              :x1="vl.x"
              :x2="vl.x"
              :y1="vl.y1"
              :y2="vl.y2"
              stroke="#aaa"
              stroke-width="0.5"
          />
          <line
              v-for="(hl, i) in gridLines.horizontal"
              :key="'hLine-' + i"
              :x1="hl.x1"
              :x2="hl.x2"
              :y1="hl.y"
              :y2="hl.y"
              stroke="#aaa"
              stroke-width="0.5"
          />
        </g>

        <!-- Connections on this floor (non-vertical) -->
        <line
            v-for="(c, i) in flatConnections"
            :key="'conn-' + i"
            :x1="posCenterX(c.fromPos)"
            :x2="posCenterX(c.toPos)"
            :y1="posCenterY(c.fromPos)"
            :y2="posCenterY(c.toPos)"
            stroke="red"
            stroke-width="2"
        />

        <!-- Positions (rooms) for the current floor -->
        <g
            v-for="(posObj, i) in filteredPositions"
            :key="'pos-' + posObj.position.id"
            @click.stop="onPositionClick(posObj)"
        >
          <!-- Simple rect for demonstration -->
          <!--          <rect-->
          <!--              :fill="getPositionFill(posObj)"-->
          <!--              :height="cellSize - cellPadding"-->
          <!--              :stroke="isSelected(posObj.position.id) ? 'orange' : '#666'"-->
          <!--              :width="cellSize - cellPadding"-->
          <!--              :x="posLeft(posObj)"-->
          <!--              :y="posTop(posObj)"-->
          <!--              rx="8"-->
          <!--              ry="8"-->
          <!--              stroke-width="2"-->
          <!--          />-->
          <Room
              :cellPadding="cellPadding"
              :cellSize="cellSize"
              :positionData="posObj"
              :fill="getPositionFill(posObj)"
              :stroke="isSelected(posObj.position.id) ? 'orange' : '#666'"
              :stroke-width="2"
              :showLabel="true"
          />
          <!-- Position label -->
          <text
              :x="posLeft(posObj) + (cellSize / 2) - 15"
              :y="posTop(posObj) + cellSize - 15"
              fill="#fff"
              font-size="10"
              text-anchor="middle"
          >
            {{ getPositionLabel(posObj) }}
          </text>
        </g>
      </g>
    </svg>
  </div>
</template>

<script>
import {WorldGameApi} from "@/api/backendService.js";
import Room from "@/components/Map/MapRoomComponent.vue";

export default {
  name: "GridMap",
  components: {Room},
  props: {
    mapData: {
      type: Object,
      required: true,
    },
    // We read/write currentFloor to show positions with position.grid_z === currentFloor
    initialFloor: {
      type: Number,
      default: 1,
    },
    cellSize: {
      type: Number,
      default: 80,
    },
    cellPadding: {
      type: Number,
      default: 35,
    }
  },
  data() {
    return {
      // current floor in data so we can modify it
      currentFloor: this.initialFloor,

      // Pan & Zoom
      panX: 0,
      panY: 0,
      zoom: 1,
      isDragging: false,
      dragStart: {x: 0, y: 0},

      // When true => we handle panning/zoom on drag
      // When false => we treat clicks as "interact" (create new position)
      dragMode: true,

      // track selected positions:
      selectedPosIds: [],
    };
  },
  computed: {
    filteredPositions() {
      // Positions that match the currentFloor
      return (this.mapData.positions || []).filter(
          (p) => p.position.grid_z === this.currentFloor
      );
    },
    // Create a bounding box from filtered positions
    bounds() {
      if (!this.filteredPositions.length) {
        return {minX: 0, maxX: 0, minY: 0, maxY: 0};
      }
      let minX = Infinity,
          maxX = -Infinity,
          minY = Infinity,
          maxY = -Infinity;
      for (const p of this.filteredPositions) {
        const gx = p.position.grid_x;
        const gy = p.position.grid_y;
        if (gx < minX) minX = gx;
        if (gx > maxX) maxX = gx;
        if (gy < minY) minY = gy;
        if (gy > maxY) maxY = gy;
      }
      return {minX, maxX, minY, maxY};
    },
    // Basic set of connections that are NOT vertical and belong on this floor
    flatConnections() {
      const results = [];
      for (const c of this.mapData.connections || []) {
        if (c.is_vertical) continue; // skip vertical
        const fromPos = this.getPosObjById(c.position_from);
        const toPos = this.getPosObjById(c.position_to);
        if (!fromPos || !toPos) continue;
        // same floor as current
        if (
            fromPos.position.grid_z === this.currentFloor &&
            toPos.position.grid_z === this.currentFloor
        ) {
          results.push({fromPos, toPos});
        }
      }
      return results;
    },

    // Minimal set of grid lines around the bounding box
    gridLines() {
      // expand a bit
      const margin = 2;
      const {minX, maxX, minY, maxY} = this.bounds;
      const startX = Math.floor(minX) - margin;
      const endX = Math.ceil(maxX) + margin;
      const startY = Math.floor(minY) - margin;
      const endY = Math.ceil(maxY) + margin;

      const vertical = [];
      const horizontal = [];
      // Vertical lines at integer X
      for (let x = startX; x <= endX; x++) {
        const px = x * this.cellSize; // the actual SVG px
        vertical.push({
          x: px,
          y1: startY * this.cellSize,
          y2: endY * this.cellSize,
        });
      }
      // Horizontal lines
      for (let y = startY; y <= endY; y++) {
        const py = y * this.cellSize;
        horizontal.push({
          y: py,
          x1: startX * this.cellSize,
          x2: endX * this.cellSize,
        });
      }
      return {vertical, horizontal};
    },

    // The final SVG transform for pan+zoom
    finalTransform() {
      return `translate(${this.panX}, ${this.panY}) scale(${this.zoom})`;
    },
  },
  mounted() {
    // Center the map somewhat
    if (this.$refs.container) {
      this.panX = this.$refs.container.offsetWidth / 2;
      this.panY = this.$refs.container.offsetHeight / 2;
    }
  },
  methods: {
    roomSelected(room) {
      this.$emit("select-room", room);
    },
    romCreated(room) {
      this.$emit("create-room", room);
    },
    // Floor up/down
    floorUp() {
      this.currentFloor += 1;
    },
    floorDown() {
      this.currentFloor -= 1;
    },
    // Toggle between drag mode and interact mode
    toggleMode() {
      this.dragMode = !this.dragMode;
    },

    onMouseDown(e) {
      if (!this.dragMode) return; // no dragging if not in drag mode
      this.isDragging = true;
      this.dragStart.x = e.clientX - this.panX;
      this.dragStart.y = e.clientY - this.panY;
    },
    onMouseMove(e) {
      if (!this.isDragging) return;
      this.panX = e.clientX - this.dragStart.x;
      this.panY = e.clientY - this.dragStart.y;
    },
    onMouseUp() {
      this.isDragging = false;
    },
    onWheel(e) {
      if (!this.dragMode) return; // only zoom in drag mode
      const direction = e.deltaY < 0 ? 1 : -1;
      let newZoom = this.zoom + direction * 0.1;
      newZoom = Math.max(0.3, Math.min(4, newZoom));
      // Zoom around mouse
      const rect = this.$refs.container.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;
      const ratio = newZoom / this.zoom;
      this.panX = mx - (mx - this.panX) * ratio;
      this.panY = my - (my - this.panY) * ratio;
      this.zoom = newZoom;
    },

    // If user clicks on empty space (and not in drag mode), create a new position
    async onSvgClick(e) {
      if (this.dragMode) {
        // If in drag mode, do nothing special here
        return;
      }
      // Convert screen coords to map coords
      const [mapX, mapY] = this.screenToMap(e.clientX, e.clientY);
      // Snap to integer cell
      const gx = Math.floor(mapX / this.cellSize);
      const gy = Math.floor(mapY / this.cellSize);

      // Check if a position already exists here
      const existing = this.mapData.positions.find(
          (po) =>
              po.position.grid_x === gx &&
              po.position.grid_y === gy &&
              po.position.grid_z === this.currentFloor
      );
      if (!existing) {
        // create new position
        await this.createNewPosition(gx, gy);
      }
    },
    async createNewPosition(x, y) {
      try {
        const pos = (await WorldGameApi.worldMapsPositionAddCreate(
            {
              grid_x: x,
              grid_y: y,
              grid_z: this.currentFloor,
            }
        )).data;
        this.mapData.positions.push(pos);
        this.romCreated(pos);
      } catch (e) {
        console.error("Error creating position", e);
      }

    },
    screenToMap(clientX, clientY) {
      // Reverse finalTransform
      const rect = this.$refs.container.getBoundingClientRect();
      const sx = clientX - rect.left;
      const sy = clientY - rect.top;
      const unTranslateX = sx - this.panX;
      const unTranslateY = sy - this.panY;
      const factor = 1 / this.zoom;
      const mapPx = unTranslateX * factor;
      const mapPy = unTranslateY * factor;
      return [mapPx, mapPy];
    },

    // For a position ID, return the position object with shape { position: {...}, ... }
    getPosObjById(id) {
      return this.mapData.positions.find((p) => p.position.id === id);
    },

    // ========== Position Geometry ========== //
    posLeft(posObj) {
      // X cell + small offset
      return posObj.position.grid_x * this.cellSize + this.cellPadding / 2;
    },
    posTop(posObj) {
      return posObj.position.grid_y * this.cellSize + this.cellPadding / 2;
    },
    posCenterX(posObj) {
      return posObj.position.grid_x * this.cellSize + this.cellSize / 2;
    },
    posCenterY(posObj) {
      return posObj.position.grid_y * this.cellSize + this.cellSize / 2;
    },

    // ========== Position Click ========== //
    onPositionClick(posObj) {
      // Simple single-selection example
      this.roomSelected(posObj);
      const pid = posObj.position.id;
      if (this.selectedPosIds.includes(pid)) {
        this.selectedPosIds = this.selectedPosIds.filter((x) => x !== pid);
      } else {
        this.selectedPosIds = [pid];
      }
    },
    isSelected(pid) {
      return this.selectedPosIds.includes(pid);
    },

    // ========== Position Appearance ========== //
    getPositionFill(posObj) {
      // For demonstration, highlight the "current_position" in mapData
      if (posObj.position.id === this.mapData.current_position) {
        return "#1E90FF";
      }
      return "#444";
    },
    getPositionLabel(posObj) {
      // Show the last label or "grid coords"
      if (posObj.labels && posObj.labels.length) {
        return posObj.labels[posObj.labels.length - 1];
      }
      const {grid_x, grid_y} = posObj.position;
      return `(${grid_x}, ${grid_y})`;
    },
  },
};
</script>

<style scoped>
.svg-map-container {
  position: relative;
  width: 100%;
  height: 100%;
  background: #1e1e1e;
  user-select: none; /* prevent text selection on drag */
  overflow: hidden; /* no scrollbars */
  cursor: default; /* normal cursor */
}

.svg-map-container:active {
  /* if we are in drag mode, the JS sets the cursor to grabbing, etc.
     For simplicity, let's not do that here, or do:
     cursor: grabbing;
  */
}

.control-bar {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 99;
  display: flex;
  gap: 10px;
  align-items: center;
  background: #2c2c2c;
  padding: 5px 10px;
  border-radius: 4px;
  border: 1px solid #444;
}

.control-bar button {
  background: #444;
  color: #fff;
  border: 1px solid #666;
  cursor: pointer;
  padding: 5px 8px;
  border-radius: 3px;
}

.control-bar button:hover {
  background: #555;
}
</style>
