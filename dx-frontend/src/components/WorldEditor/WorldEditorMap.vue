<template>
  <div class="world-editor-map">
    <!-- Map Controls -->
    <div class="map-controls">
      <button :class="['control-btn', { active: dragMode }]" @click="toggleDragMode">
        {{ dragMode ? 'Drag Mode' : 'Interact Mode' }}
      </button>
      <button class="control-btn" @click="centerMap">
        <i class="icon-center"></i> Center
      </button>
      <button class="control-btn" @click="fitToContent">
        <i class="icon-fit"></i> Fit All
      </button>
    </div>

    <!-- Main SVG Map -->
    <svg
        ref="mapSvg"
        class="world-map-svg"
        @click="onSvgClick"
        @mousedown="onMouseDown"
        @mousemove="onMouseMove"
        @mouseup="onMouseUp"
        @wheel.prevent="onWheel"
    >
      <!-- Pattern definitions -->
      <defs>
        <pattern id="worldEditorTexture" patternUnits="userSpaceOnUse" width="1050" height="1050">
          <image href="@/assets/images/backgrounds/world-editor-texture.png" width="1050" height="1050"/>
        </pattern>
      </defs>

      <!-- Transform group for pan/zoom -->
      <g :transform="finalTransform">
        <!-- Background texture -->
        <rect x="-5000" y="-5000" width="10000" height="10000" fill="url(#worldEditorTexture)" opacity="0.35"/>
        <!-- Grid -->
        <g v-if="showGrid" class="grid-layer">
          <line
              v-for="(line, i) in gridLines.vertical"
              :key="'v-' + i"
              :stroke="gridColor"
              :x1="line.x"
              :x2="line.x"
              :y1="line.y1"
              :y2="line.y2"
              stroke-width="0.5"
          />
          <line
              v-for="(line, i) in gridLines.horizontal"
              :key="'h-' + i"
              :stroke="gridColor"
              :x1="line.x1"
              :x2="line.x2"
              :y1="line.y"
              :y2="line.y"
              stroke-width="0.5"
          />
        </g>

        <!-- Connections -->
        <g class="connections-layer">
          <line
              v-for="connection in visibleConnections"
              :key="'conn-' + connection.id"
              :class="['connection', { 'connection-vertical': connection.isVertical }]"
              :stroke="getConnectionColor(connection)"
              :stroke-width="getConnectionWidth(connection)"
              :x1="getConnectionStartX(connection)"
              :x2="getConnectionEndX(connection)"
              :y1="getConnectionStartY(connection)"
              :y2="getConnectionEndY(connection)"
              @click.stop="onConnectionClick(connection)"
          />
        </g>

        <g class="rooms-layer">
          <g
              v-for="room in visibleRooms"
              :key="'room-' + room.id"
              :class="['room-group', { 'room-selected': isRoomSelected(room.id) }]"
              @click.stop="onRoomClick(room, $event)"
              @mousedown.stop="onRoomMouseDown(room, $event)"
          >
            <!-- Room base -->
            <WorldEditorRoom
                :activeLayers="activeLayers"
                :cellPadding="cellPadding"
                :cellSize="cellSize"
                :editorState="editorState"
                :room="room"
                :selected="isRoomSelected(room.id)"
                @show-entity-details="onShowEntityDetails"
            />

            <!-- Room label -->
            <text
                :x="getRoomCenterX(room)"
                :y="getRoomBottom(room) - 5"
                class="room-label"
                fill="#fff"
                font-size="7.5"
                text-anchor="middle"
            >
              {{ getRoomLabel(room) }}
            </text>
          </g>
        </g>

        <!-- Tool overlays -->
        <g v-if="isEditMode" class="tool-overlay">
          <!-- Connection preview -->
          <line
              v-if="connectionPreview"
              :x1="connectionPreview.startX"
              :x2="connectionPreview.endX"
              :y1="connectionPreview.startY"
              :y2="connectionPreview.endY"
              class="connection-preview"
              stroke="#1E90FF"
              stroke-dasharray="5,5"
              stroke-width="2"
          />

          <!-- Room creation preview -->
          <rect
              v-if="roomCreationPreview"
              :height="cellSize - cellPadding"
              :width="cellSize - cellPadding"
              :x="roomCreationPreview.x"
              :y="roomCreationPreview.y"
              class="room-creation-preview"
              fill="rgba(30, 144, 255, 0.3)"
              stroke="#1E90FF"
              stroke-dasharray="5,5"
              stroke-width="2"
          />
        </g>
      </g>
    </svg>

    <!-- Minimap -->
    <div v-if="showMinimap" class="minimap">
      <WorldEditorMinimap
          :currentFloor="currentFloor"
          :rooms="allRooms"
          :viewBounds="viewBounds"
          @navigate="onMinimapNavigate"
      />
    </div>

    <!-- Entity Legend -->
    <div v-if="showLegend" ref="entityLegend" class="entity-legend">
      <div class="legend-header">
        <h4>Entity Legend</h4>
        <button class="legend-toggle-btn" @click="toggleLegend">
          <i class="icon-times"></i>
        </button>
      </div>
      <div class="legend-content">
        <div :class="{ 'inactive': !isLayerActive(WorldEditorLayer.PLAYERS) }" class="legend-item"
             @click="toggleLayer(WorldEditorLayer.PLAYERS, $event)">
          <div class="legend-icon">
            <svg height="20" viewBox="0 0 20 20" width="20">
              <circle class="entity-circle" cx="10" cy="10" fill="#00ff00" r="6" stroke="#000" stroke-width="1"/>
              <text fill="#000" font-size="8" font-weight="bold" text-anchor="middle" x="10" y="13">3</text>
            </svg>
          </div>
          <div class="legend-label">Players (Top-Left)</div>
        </div>
        <div :class="{ 'inactive': !isLayerActive(WorldEditorLayer.NPCS) }" class="legend-item"
             @click="toggleLayer(WorldEditorLayer.NPCS, $event)">
          <div class="legend-icon">
            <svg height="20" viewBox="0 0 20 20" width="20">
              <rect class="entity-square" fill="#ffff00" height="12" rx="2" ry="2" stroke="#000" stroke-width="1"
                    width="12" x="4"
                    y="4"/>
              <text fill="#000" font-size="8" font-weight="bold" text-anchor="middle" x="10" y="13">2</text>
            </svg>
          </div>
          <div class="legend-label">NPCs (Top-Right)</div>
        </div>
        <div :class="{ 'inactive': !isLayerActive(WorldEditorLayer.ANOMALIES) }" class="legend-item"
             @click="toggleLayer(WorldEditorLayer.ANOMALIES, $event)">
          <div class="legend-icon">
            <svg height="20" viewBox="0 0 20 20" width="20">
              <circle class="entity-circle" cx="10" cy="10" fill="#ff0000" r="6" stroke="#000" stroke-width="1"/>
              <text fill="#000" font-size="8" font-weight="bold" text-anchor="middle" x="10" y="13">1</text>
            </svg>
          </div>
          <div class="legend-label">Anomalies (Top-Middle)</div>
        </div>
        <div :class="{ 'inactive': !isLayerActive(WorldEditorLayer.OBJECTS) }" class="legend-item"
             @click="toggleLayer(WorldEditorLayer.OBJECTS, $event)">
          <div class="legend-icon">
            <svg height="20" viewBox="0 0 20 20" width="20">
              <rect class="entity-square" fill="#0088ff" height="12" rx="2" ry="2" stroke="#000" stroke-width="1"
                    width="12" x="4"
                    y="4"/>
              <text fill="#000" font-size="8" font-weight="bold" text-anchor="middle" x="10" y="13">5</text>
            </svg>
          </div>
          <div class="legend-label">Items (Left-Middle)</div>
        </div>
      </div>
    </div>

    <!-- Legend Toggle Button -->
    <button v-if="!showLegend" class="legend-btn" title="Show Legend" @click="toggleLegend">
      <i class="icon-info"></i>
    </button>

    <!-- Current Turn Component -->
    <div class="current-turn-container">
      <CurrentTurnComponent :currentTurn="currentCycleNumber"/>
    </div>

    <!-- Floor Switcher -->
    <WorldEditorFloorSwitcher
        :currentFloor="currentFloor"
        @floor-up="onFloorUp"
        @floor-down="onFloorDown"
    />
  </div>
</template>

<script>
import {WorldEditorConfig, WorldEditorLayer, WorldEditorTool} from '@/models/WorldEditorModels.ts';
import WorldEditorRoom from './WorldEditorRoom.vue';
import WorldEditorMinimap from './WorldEditorMinimap.vue';
import CurrentTurnComponent from '@/components/Game/CurrentTurnComponent.vue';
import WorldEditorFloorSwitcher from './WorldEditorFloorSwitcher.vue';

export default {
  name: 'WorldEditorMap',
  components: {
    WorldEditorRoom,
    WorldEditorMinimap,
    CurrentTurnComponent,
    WorldEditorFloorSwitcher
  },
  props: {
    mapData: {
      type: Object,
      default: () => ({})
    },
    editorState: {
      type: Object,
      required: true
    },
    currentFloor: {
      type: Number,
      default: 1
    },
    currentCycleNumber: {
      type: Number,
      default: null
    }
  },
  emits: [
    'room-selected',
    'room-created',
    'room-moved',
    'room-deleted',
    'connection-created',
    'connection-deleted',
    'connection-selected',
    'map-clicked',
    'show-entity-details',
    'layer-toggled',
    'refresh-map',
    'floor-up',
    'floor-down',
  ],
  data() {
    return {
      // Pan & Zoom
      panX: 0,
      panY: 0,
      zoom: 1,
      isDragging: false,
      dragStart: {x: 0, y: 0},

      // Debouncing for performance
      lastUpdateTime: 0,
      debounceDelay: 50,

      // SVG readiness and viewBounds caching
      svgReady: false,
      cachedViewBounds: null,

      // For triggering viewBounds recalculation on resize
      windowSize: {
        width: window.innerWidth,
        height: window.innerHeight
      },

      // Interaction state
      dragMode: true,
      selectedRoomForConnection: null,
      connectionPreview: null,
      roomCreationPreview: null,

      // UI settings
      showGrid: true,
      showMinimap: true,
      showLayerIndicators: true,
      showLegend: false,

      // Make WorldEditorLayer available in template
      WorldEditorLayer,

      // Configuration
      cellSize: WorldEditorConfig.cellSize,
      cellPadding: WorldEditorConfig.cellPadding,
      gridColor: WorldEditorConfig.gridColor
    };
  },
  computed: {
    isEditMode() {
      return this.editorState?.mode === 'edit';
    },

    selectedTool() {
      return this.editorState?.selectedTool || WorldEditorTool.SELECT;
    },

    activeLayers() {
      return this.editorState?.activeLayers || new Set();
    },

    allRooms() {
      return Array.from(this.editorState?.rooms?.values() || []);
    },

    visibleRooms() {
      return this.allRooms.filter(room => room.position.grid_z === this.currentFloor);
    },

    visibleConnections() {
      return Array.from(this.editorState?.connections?.values() || [])
          .filter(connection => {
            const fromRoom = this.editorState.rooms.get(connection.fromRoomId);
            const toRoom = this.editorState.rooms.get(connection.toRoomId);
            return fromRoom && toRoom &&
                fromRoom.position.grid_z === this.currentFloor &&
                toRoom.position.grid_z === this.currentFloor &&
                !connection.isVertical;
          });
    },

    bounds() {
      if (!this.visibleRooms.length) {
        return {minX: 0, maxX: 0, minY: 0, maxY: 0};
      }

      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;

      this.visibleRooms.forEach(room => {
        const {grid_x, grid_y} = room.position;
        if (grid_x < minX) minX = grid_x;
        if (grid_x > maxX) maxX = grid_x;
        if (grid_y < minY) minY = grid_y;
        if (grid_y > maxY) maxY = grid_y;
      });

      return {minX, maxX, minY, maxY};
    },

    gridLines() {
      const margin = 3;
      const {minX, maxX, minY, maxY} = this.bounds;
      const startX = Math.floor(minX) - margin;
      const endX = Math.ceil(maxX) + margin;
      const startY = Math.floor(minY) - margin;
      const endY = Math.ceil(maxY) + margin;

      const vertical = [];
      const horizontal = [];

      for (let x = startX; x <= endX; x++) {
        vertical.push({
          x: x * this.cellSize,
          y1: startY * this.cellSize,
          y2: endY * this.cellSize
        });
      }

      for (let y = startY; y <= endY; y++) {
        horizontal.push({
          y: y * this.cellSize,
          x1: startX * this.cellSize,
          x2: endX * this.cellSize
        });
      }

      return {vertical, horizontal};
    },

    finalTransform() {
      return `translate(${this.panX}, ${this.panY}) scale(${this.zoom})`;
    },

    viewBounds() {
      // Return cached bounds if SVG isn't ready yet
      if (!this.svgReady || !this.$refs.mapSvg) {
        return this.cachedViewBounds;
      }

      try {
        const rect = this.$refs.mapSvg.getBoundingClientRect();

        // Ensure we have valid dimensions
        if (!rect || rect.width === 0 || rect.height === 0) {
          return this.cachedViewBounds;
        }

        const factor = 1 / this.zoom;
        const bounds = {
          x: (-this.panX) * factor,
          y: (-this.panY) * factor,
          width: rect.width * factor,
          height: rect.height * factor,
          // Include dependencies to trigger reactivity
          _windowWidth: this.windowSize.width,
          _windowHeight: this.windowSize.height,
          _zoom: this.zoom,
          _panX: this.panX,
          _panY: this.panY
        };

        // Cache the valid bounds
        this.cachedViewBounds = bounds;
        return bounds;

      } catch (error) {
        console.warn('Error calculating viewBounds:', error);
        return this.cachedViewBounds;
      }
    }
  },
  mounted() {
    // Wait for next tick to ensure DOM is ready
    this.$nextTick(() => {
      // Set initial view bounds
      this.initializeViewBounds();

      // Mark SVG as ready
      this.svgReady = true;

      // Load saved map state from localStorage if available
      const savedMapState = localStorage.getItem('worldEditor_mapState');
      if (savedMapState) {
        try {
          const mapState = JSON.parse(savedMapState);
          this.panX = mapState.panX;
          this.panY = mapState.panY;
          this.zoom = mapState.zoom;
          console.log('Loaded map state from localStorage:', mapState);
        } catch (error) {
          console.error('Failed to parse saved map state:', error);
          // Center the map if loading saved state fails
          this.centerMap();
        }
      } else {
        // Center the map if no saved state
        this.centerMap();
      }
    });

    // If the legend is shown by default, add click-outside listener
    if (this.showLegend) {
      document.addEventListener('mousedown', this.handleClickOutside);
    }

    // Add resize event listener to update viewBounds
    window.addEventListener('resize', this.handleResize);
  },

  beforeUnmount() {
    // Clean up event listeners
    document.removeEventListener('mousedown', this.handleClickOutside);
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    // Save map state to localStorage
    saveMapState() {
      const mapState = {
        panX: this.panX,
        panY: this.panY,
        zoom: this.zoom
      };
      localStorage.setItem('worldEditor_mapState', JSON.stringify(mapState));
    },

    // Initialize view bounds safely
    initializeViewBounds() {
      try {
        const rect = this.$refs.mapSvg?.getBoundingClientRect();
        if (rect && rect.width > 0 && rect.height > 0) {
          const factor = 1 / this.zoom;
          this.cachedViewBounds = {
            x: (-this.panX) * factor,
            y: (-this.panY) * factor,
            width: rect.width * factor,
            height: rect.height * factor
          };
        }
      } catch (error) {
        console.warn('Error initializing viewBounds:', error);
      }
    },

    // Handle window resize with debouncing
    handleResize() {
      const now = Date.now();
      if (now - this.lastUpdateTime > this.debounceDelay) {
        this.lastUpdateTime = now;
        requestAnimationFrame(() => {
          // Update windowSize to trigger viewBounds recalculation
          this.windowSize = {
            width: window.innerWidth,
            height: window.innerHeight
          };

          // Recalculate view bounds
          if (this.svgReady) {
            this.initializeViewBounds();
          }
        });
      }
    },

    // Room positioning
    getRoomLeft(room) {
      return room.position.grid_x * this.cellSize + this.cellPadding / 2;
    },

    getRoomTop(room) {
      return room.position.grid_y * this.cellSize + this.cellPadding / 2;
    },

    getRoomCenterX(room) {
      return room.position.grid_x * this.cellSize + this.cellSize / 2;
    },

    getRoomCenterY(room) {
      return room.position.grid_y * this.cellSize + this.cellSize / 2;
    },

    getRoomBottom(room) {
      return this.getRoomTop(room) + this.cellSize - this.cellPadding;
    },

    getRoomLabel(room) {
      return room.getDisplayName();
    },

    // Connection positioning
    getConnectionStartX(connection) {
      const room = this.editorState.rooms.get(connection.fromRoomId);
      return room ? this.getRoomCenterX(room) : 0;
    },

    getConnectionStartY(connection) {
      const room = this.editorState.rooms.get(connection.fromRoomId);
      return room ? this.getRoomCenterY(room) : 0;
    },

    getConnectionEndX(connection) {
      const room = this.editorState.rooms.get(connection.toRoomId);
      return room ? this.getRoomCenterX(room) : 0;
    },

    getConnectionEndY(connection) {
      const room = this.editorState.rooms.get(connection.toRoomId);
      return room ? this.getRoomCenterY(room) : 0;
    },

    getConnectionColor(connection) {
      return connection.isVertical ?
          WorldEditorConfig.connectionColors.vertical :
          WorldEditorConfig.connectionColors.normal;
    },

    getConnectionWidth(connection) {
      return connection.isVertical ? 3 : 2;
    },

    // Layer management
    getActiveRoomLayers(room) {
      const layers = [];
      Object.values(WorldEditorLayer).forEach(layer => {
        if (this.activeLayers.has(layer) && room.hasLayerEntities(layer)) {
          layers.push(layer);
        }
      });
      return layers;
    },

    getLayerColor(layer) {
      return WorldEditorConfig.layerColors[layer] || '#888';
    },

    // Selection
    isRoomSelected(roomId) {
      return this.editorState?.selectedRooms?.has(roomId) || false;
    },

    // Mouse events
    onMouseDown(e) {
      if (!this.dragMode) return;

      this.isDragging = true;
      this.dragStart.x = e.clientX - this.panX;
      this.dragStart.y = e.clientY - this.panY;
    },

    onMouseMove(e) {
      if (this.isDragging && this.dragMode) {
        this.panX = e.clientX - this.dragStart.x;
        this.panY = e.clientY - this.dragStart.y;

        // Update view bounds during pan
        if (this.svgReady) {
          this.initializeViewBounds();
        }

        // Save map state to localStorage
        this.saveMapState();
      }

      // Update tool previews
      this.updateToolPreviews(e);
    },

    onMouseUp() {
      this.isDragging = false;
    },

    onWheel(e) {
      if (!this.dragMode) return;

      const direction = e.deltaY < 0 ? 1 : -1;
      let newZoom = this.zoom + direction * 0.1;
      newZoom = Math.max(0.2, Math.min(5, newZoom));

      // Zoom around mouse position
      const rect = this.$refs.mapSvg.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;
      const ratio = newZoom / this.zoom;

      this.panX = mx - (mx - this.panX) * ratio;
      this.panY = my - (my - this.panY) * ratio;
      this.zoom = newZoom;

      // Update view bounds after zoom
      if (this.svgReady) {
        this.initializeViewBounds();
      }

      // Save map state to localStorage
      this.saveMapState();
    },

    // Click events
    onSvgClick(e) {
      if (this.isDragging) return;

      const [mapX, mapY] = this.screenToMap(e.clientX, e.clientY);
      const gridX = Math.floor(mapX / this.cellSize);
      const gridY = Math.floor(mapY / this.cellSize);

      this.$emit('map-clicked', {
        gridX,
        gridY,
        gridZ: this.currentFloor,
        screenX: e.clientX,
        screenY: e.clientY
      });
    },

    onRoomClick(room, event) {
      this.handleRoomInteraction(room, event);
    },

    onRoomMouseDown(room, e) {
      if (this.selectedTool === WorldEditorTool.MOVE_ROOM) {
        // Start room dragging
        this.startRoomDrag(room, e);
      }
    },

    onConnectionClick(connection) {
      if (this.selectedTool === WorldEditorTool.DISCONNECT_ROOMS) {
        this.$emit('connection-deleted', connection.id);
      } else {
        // Emit connection-selected event for interactive connections
        this.$emit('connection-selected', connection);
      }
    },

    // Tool-specific interactions
    handleRoomInteraction(room, event) {
      switch (this.selectedTool) {
        case WorldEditorTool.SELECT:
          this.$emit('room-selected', room, event?.shiftKey || false);
          break;

        case WorldEditorTool.DELETE_ROOM:
          this.$emit('room-deleted', room);
          break;

        case WorldEditorTool.CONNECT_ROOMS:
          this.handleRoomConnection(room);
          break;

        default:
          this.$emit('room-selected', room, event?.shiftKey || false);
      }
    },

    handleRoomConnection(room) {
      if (!this.selectedRoomForConnection) {
        // First room selected for connection
        this.selectedRoomForConnection = room;
        this.updateConnectionPreview();
      } else if (this.selectedRoomForConnection.id !== room.id) {
        // Second room selected, create connection
        this.$emit('connection-created', this.selectedRoomForConnection.id, room.id);
        this.selectedRoomForConnection = null;
        this.connectionPreview = null;
      }
    },

    startRoomDrag(room, e) {
      // Implementation for room dragging would go here
      // This is a placeholder for the room moving functionality
    },

    // Tool previews
    updateToolPreviews(e) {
      if (!this.isEditMode) return;

      const [mapX, mapY] = this.screenToMap(e.clientX, e.clientY);

      switch (this.selectedTool) {
        case WorldEditorTool.CREATE_ROOM:
          this.updateRoomCreationPreview(mapX, mapY);
          break;

        case WorldEditorTool.CONNECT_ROOMS:
          this.updateConnectionPreview(mapX, mapY);
          break;

        default:
          this.clearPreviews();
      }
    },

    updateRoomCreationPreview(mapX, mapY) {
      const gridX = Math.floor(mapX / this.cellSize);
      const gridY = Math.floor(mapY / this.cellSize);

      // Check if room already exists at this position
      const existingRoom = this.visibleRooms.find(room =>
          room.position.grid_x === gridX && room.position.grid_y === gridY
      );

      if (!existingRoom) {
        this.roomCreationPreview = {
          x: gridX * this.cellSize + this.cellPadding / 2,
          y: gridY * this.cellSize + this.cellPadding / 2
        };
      } else {
        this.roomCreationPreview = null;
      }
    },

    updateConnectionPreview(mapX, mapY) {
      if (this.selectedRoomForConnection) {
        this.connectionPreview = {
          startX: this.getRoomCenterX(this.selectedRoomForConnection),
          startY: this.getRoomCenterY(this.selectedRoomForConnection),
          endX: mapX,
          endY: mapY
        };
      }
    },

    clearPreviews() {
      this.roomCreationPreview = null;
      this.connectionPreview = null;
    },

    // Cancel all in-progress actions (called when Escape key is pressed)
    cancelInProgressActions() {
      // Clear connection creation state
      this.selectedRoomForConnection = null;

      // Clear all previews
      this.clearPreviews();

      // Reset drag mode if needed
      this.dragMode = true;
    },

    // Coordinate conversion
    screenToMap(clientX, clientY) {
      const rect = this.$refs.mapSvg.getBoundingClientRect();
      const sx = clientX - rect.left;
      const sy = clientY - rect.top;
      const unTranslateX = sx - this.panX;
      const unTranslateY = sy - this.panY;
      const factor = 1 / this.zoom;
      return [unTranslateX * factor, unTranslateY * factor];
    },

    // Map navigation
    toggleDragMode() {
      this.dragMode = !this.dragMode;
      this.clearPreviews();
      this.selectedRoomForConnection = null;
    },

    centerMap() {
      if (this.visibleRooms.length === 0) {
        this.panX = 0;
        this.panY = 0;
        // Save map state to localStorage
        this.saveMapState();
        return;
      }

      const {minX, maxX, minY, maxY} = this.bounds;
      const centerX = (minX + maxX) / 2 * this.cellSize;
      const centerY = (minY + maxY) / 2 * this.cellSize;

      const rect = this.$refs.mapSvg?.getBoundingClientRect();
      if (rect && rect.width > 0 && rect.height > 0) {
        this.panX = rect.width / 2 - centerX * this.zoom;
        this.panY = rect.height / 2 - centerY * this.zoom;

        // Update view bounds after centering
        if (this.svgReady) {
          this.initializeViewBounds();
        }

        // Save map state to localStorage
        this.saveMapState();
      }
    },

    fitToContent() {
      if (this.visibleRooms.length === 0) return;

      const {minX, maxX, minY, maxY} = this.bounds;
      const contentWidth = (maxX - minX + 2) * this.cellSize;
      const contentHeight = (maxY - minY + 2) * this.cellSize;

      const rect = this.$refs.mapSvg?.getBoundingClientRect();
      if (rect && rect.width > 0 && rect.height > 0) {
        const scaleX = rect.width / contentWidth;
        const scaleY = rect.height / contentHeight;
        this.zoom = Math.min(scaleX, scaleY, 2); // Max zoom of 2x

        // Save map state to localStorage before centerMap
        this.saveMapState();

        this.centerMap();

        // Update view bounds after fitting
        if (this.svgReady) {
          this.initializeViewBounds();
        }
      }
    },

    onMinimapNavigate(position) {
      // Navigate to position from minimap
      const rect = this.$refs.mapSvg?.getBoundingClientRect();
      if (rect) {
        this.panX = rect.width / 2 - position.x * this.zoom;
        this.panY = rect.height / 2 - position.y * this.zoom;

        // Update view bounds after navigation
        if (this.svgReady) {
          this.initializeViewBounds();
        }
      }
    },

    toggleLegend() {
      this.showLegend = !this.showLegend;

      if (this.showLegend) {
        // Add click-outside event listener when legend is shown
        this.$nextTick(() => {
          // Use setTimeout to avoid immediate triggering of the event
          setTimeout(() => {
            document.addEventListener('mousedown', this.handleClickOutside);
          }, 100);
        });
      } else {
        // Remove click-outside event listener when legend is hidden
        document.removeEventListener('mousedown', this.handleClickOutside);
      }
    },

    handleClickOutside(event) {
      // Close legend when clicking outside of it
      if (this.$refs.entityLegend &&
          !this.$refs.entityLegend.contains(event.target) &&
          !event.target.closest('.legend-btn')) {
        this.showLegend = false;
        document.removeEventListener('mousedown', this.handleClickOutside);
      }
    },

    isLayerActive(layer) {
      return this.activeLayers.has(layer);
    },

    toggleLayer(layer, event) {
      // Stop event propagation to prevent click-outside from triggering
      if (event) {
        event.stopPropagation();
      }

      // Emit event to parent component to toggle the layer
      this.$emit('layer-toggled', layer);
    },

    onShowEntityDetails(details) {
      // Emit the event up to the parent component to handle
      this.$emit('show-entity-details', details);

      // Optionally, select the room that contains these entities
      if (details.roomId) {
        const room = this.visibleRooms.find(r => r.id === details.roomId);
        if (room) {
          this.onRoomClick(room);
        }
      }
    },

    // Floor switcher methods
    onFloorUp() {
      this.$emit('floor-up');
    },

    onFloorDown() {
      this.$emit('floor-down');
    }
  }
};
</script>

<style scoped>
.world-editor-map {
  position: relative;
  width: 100%;
  height: 100%;
  background: #000000;
  overflow: hidden;
}

/* Map Controls */
.map-controls {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
  display: flex;
  gap: 0.5rem;
}

.control-btn {
  padding: 0.5rem 1rem;
  background: rgba(45, 45, 45, 0.9);
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.control-btn:hover {
  background: rgba(85, 85, 85, 0.9);
}

.control-btn.active {
  background: rgba(30, 144, 255, 0.9);
  border-color: #1E90FF;
}

/* SVG Map */
.world-map-svg {
  width: 100%;
  height: 100%;
  cursor: default;
}

.world-map-svg.dragging {
  cursor: grabbing;
}

/* Grid */
.grid-layer line {
  pointer-events: none;
}

/* Connections */
.connection {
  cursor: pointer;
  transition: stroke-width 0.2s ease;
}

.connection:hover {
  stroke-width: 4 !important;
}

.connection-vertical {
  stroke-dasharray: 3, 3;
}

.connection-preview {
  pointer-events: none;
}

/* Rooms */
.room-group {
  cursor: pointer;
  transition: all 0.2s ease;
}

.room-group:hover {
  filter: brightness(1.2);
}

.room-selected {
  filter: brightness(1.4);
}

.room-label {
  pointer-events: none;
  font-family: 'Roboto', sans-serif;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
}

/* Layer Indicators */
.layer-indicators {
  pointer-events: none;
}

.layer-indicator {
  stroke: rgba(255, 255, 255, 0.3);
  stroke-width: 1;
}

/* Tool Overlays */
.tool-overlay {
  pointer-events: none;
}

.room-creation-preview {
  pointer-events: none;
}

/* Minimap */
.minimap {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 200px;
  height: 150px;
  background: rgba(45, 45, 45, 0.9);
  border: 1px solid #555;
  border-radius: 4px;
  z-index: 10;
}

/* Entity Legend */
.entity-legend {
  position: absolute;
  bottom: 10px;
  left: 10px;
  width: 220px;
  background: rgba(45, 45, 45, 0.9);
  border: 1px solid #555;
  border-radius: 4px;
  z-index: 10;
  color: #fff;
  font-size: 0.9rem;
}

.legend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid #555;
}

.legend-header h4 {
  margin: 0;
  font-size: 1rem;
  color: #1E90FF;
}

.legend-toggle-btn {
  background: transparent;
  border: none;
  color: #ccc;
  cursor: pointer;
  padding: 2px;
  border-radius: 3px;
}

.legend-toggle-btn:hover {
  background: #555;
  color: #fff;
}

.legend-content {
  padding: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.legend-icon {
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.legend-label {
  font-size: 0.85rem;
}

.legend-item {
  cursor: pointer;
  transition: all 0.2s ease;
}

.legend-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.legend-item.inactive {
  opacity: 0.5;
  filter: grayscale(0.8);
}

.legend-section {
  margin-bottom: 15px;
}

.legend-section h5 {
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  color: #1E90FF;
  border-bottom: 1px solid #555;
  padding-bottom: 5px;
}

.layer-toggles {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.layer-toggle-item {
  display: flex;
  align-items: center;
}

.layer-toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.layer-toggle input[type="checkbox"] {
  margin-right: 8px;
  accent-color: #1E90FF;
}

.toggle-label {
  font-size: 0.85rem;
}

.legend-btn {
  position: absolute;
  bottom: 10px;
  left: 10px;
  width: 36px;
  height: 36px;
  background: rgba(45, 45, 45, 0.9);
  border: 1px solid #555;
  border-radius: 4px;
  color: #1E90FF;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
}

.legend-btn:hover {
  background: rgba(65, 65, 65, 0.9);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .map-controls {
    flex-direction: column;
    gap: 0.25rem;
  }

  .control-btn {
    padding: 0.25rem 0.5rem;
    font-size: 0.8rem;
  }

  .minimap {
    width: 150px;
    height: 100px;
  }

  .entity-legend {
    width: 180px;
    font-size: 0.8rem;
  }

  .legend-header h4 {
    font-size: 0.9rem;
  }

  .legend-label {
    font-size: 0.75rem;
  }
}

/* Current Turn Component */
.current-turn-container {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 10;
}

/* Dark theme consistency */
:deep(.world-editor-room) {
  transition: all 0.2s ease;
}

:deep(.world-editor-room:hover) {
  filter: brightness(1.1);
}
</style>
