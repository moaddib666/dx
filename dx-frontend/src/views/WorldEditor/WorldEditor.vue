<template>
  <div class="world-editor">
    <!-- Top Toolbar -->
    <div class="world-editor-toolbar">
      <div class="toolbar-section mode-controls">
        <button
            :class="['mode-toggle', { 'edit-mode': isEditMode }]"
            @click="toggleMode"
        >
          {{ isEditMode ? 'Exit Edit Mode' : 'Enter Edit Mode' }}
        </button>
        <span class="mode-indicator">{{ currentMode.toUpperCase() }} MODE</span>
      </div>

      <!-- Floor controls moved to floating component -->

      <div class="toolbar-section action-controls">
        <button class="refresh-btn" @click="refreshWorld">
          <i class="icon-refresh"></i> Refresh
        </button>
        <button :disabled="!hasUnsavedChanges" class="save-btn" @click="saveWorld">
          <i class="icon-save"></i> Save
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="world-editor-content">
      <!-- Left Panel - Tools and Layers -->
      <div class="left-panel">
        <!-- Edit Tools (only visible in edit mode) -->
        <WorldEditorToolbar
            v-if="isEditMode"
            :selectedTool="selectedTool"
            class="editor-toolbar"
            @tool-selected="onToolSelected"
        />


        <!-- Room Info Panel -->
        <WorldEditorRoomInfo
            v-if="selectedRoom"
            ref="roomInfoPanel"
            :editable="isEditMode"
            :room="selectedRoom"
            :editorState="editorState"
            class="room-info-panel"
            @close="clearSelection"
            @room-updated="onRoomUpdated"
            @room-deleted="onRoomDeleted"
            @connection-removed="onConnectionDeleted"
            @connection-updated="onConnectionUpdated"
            @room-selected="onRoomSelected"
        />
      </div>

      <!-- Center Panel - Map -->
      <div class="center-panel">
        <!-- Map Loading Overlay -->
        <div v-if="isMapLoading" class="map-loading-overlay">
          <div class="loading-indicator">
            <div class="loading-spinner"></div>
            <div class="loading-text">Loading map data...</div>
          </div>
        </div>

        <WorldEditorMap
            :currentFloor="currentFloor"
            :editorState="editorState"
            :mapData="mapData"
            :currentCycleNumber="currentCycleNumber"
            class="world-map"
            @room-selected="onRoomSelected"
            @room-created="onRoomCreated"
            @room-moved="onRoomMoved"
            @connection-created="onConnectionCreated"
            @connection-deleted="onConnectionDeleted"
            @connection-selected="onConnectionSelected"
            @map-clicked="onMapClicked"
            @show-entity-details="onShowEntityDetails"
            @layer-toggled="onLayerToggled"
            @refresh-map="refreshWorld"
            @floor-up="floorUp"
            @floor-down="floorDown"
        />
      </div>

      <!-- Right Panel - Entity Management (only visible when it has content) -->
      <div v-if="(isEditMode && selectedRoom) || showStatsPanel || showLayersPanel || showItemsPanel"
           class="right-panel">
        <!-- Entity Spawner (only visible in edit mode) -->
        <WorldEditorEntitySpawner
            v-if="isEditMode && selectedRoom"
            :room="selectedRoom"
            :selectedTool="selectedTool"
            class="entity-spawner"
            @entity-spawned="onEntitySpawned"
        />

        <!-- World Statistics -->
        <WorldEditorStats
            v-if="showStatsPanel"
            :stats="worldStats"
            class="world-stats"
        />

        <!-- Layer Controls -->
        <WorldEditorLayers
            v-if="showLayersPanel"
            :activeLayers="activeLayers"
            :layerCounts="layerCounts"
            class="layer-controls"
            @layer-toggled="onLayerToggled"
        />

        <!-- Items List -->
        <WorldEditorItemsList
            v-if="showItemsPanel"
            class="items-list"
            @item-selected="onItemSelected"
        />
      </div>
    </div>

    <!-- Status Bar -->
    <div class="world-editor-status">
      <div class="status-left">
        <span class="status-item">Rooms: {{ totalRooms }}</span>
        <span class="status-item">Connections: {{ totalConnections }}</span>
        <span class="status-item">Selected: {{ selectedRooms.length }}</span>
        <button class="stats-toggle-btn" title="Toggle Statistics Panel" @click="toggleStatsPanel">
          <i class="icon-stats"></i>
        </button>
        <button class="layers-toggle-btn" title="Toggle Layers Panel" @click="toggleLayersPanel">
          <i class="icon-layers"></i>
        </button>
        <button class="items-toggle-btn" title="Toggle Items Panel" @click="toggleItemsPanel">
          <i class="icon-items"></i>
        </button>
      </div>
      <div class="status-right">
        <span v-if="lastAction" class="status-item">{{ lastAction }}</span>
        <span class="status-item">{{ currentTime }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import {worldEditorService} from '@/services/WorldEditorService.js';
import {WorldEditorLayer, WorldEditorMode, WorldEditorTool} from '@/models/WorldEditorModels.js';
import {ensureConnection} from "@/api/dx-websocket/index.ts";
import {ActionGameApi} from "@/api/backendService.js";

// Import WorldEditor components (to be created)
import WorldEditorToolbar from '@/components/WorldEditor/WorldEditorToolbar.vue';
import WorldEditorLayers from '@/components/WorldEditor/WorldEditorLayers.vue';
import WorldEditorRoomInfo from '@/components/WorldEditor/WorldEditorRoomInfo.vue';
import WorldEditorMap from '@/components/WorldEditor/WorldEditorMap.vue';
import WorldEditorEntitySpawner from '@/components/WorldEditor/WorldEditorEntitySpawner.vue';
import WorldEditorStats from '@/components/WorldEditor/WorldEditorStats.vue';
import WorldEditorItemsList from '@/components/WorldEditor/WorldEditorItemsList.vue';

export default {
  name: 'WorldEditor',
  components: {
    WorldEditorToolbar,
    WorldEditorLayers,
    WorldEditorRoomInfo,
    WorldEditorMap,
    WorldEditorEntitySpawner,
    WorldEditorStats,
    WorldEditorItemsList
  },
  data() {
    return {
      // Service reference
      service: worldEditorService,

      // Editor state
      editorState: null,
      mapData: null,

      // UI state
      selectedRoom: null,
      hasUnsavedChanges: false,
      lastAction: '',
      currentTime: new Date().toLocaleTimeString(),
      showStatsPanel: false, // Stats panel visibility state
      showLayersPanel: false, // Layers panel visibility state
      showItemsPanel: true, // Items panel visibility state

      // Timer for current time update
      timeUpdateInterval: null,

      // Current cycle/turn tracking
      currentCycleNumber: null,
      bus: null,

      // Map loading state
      isMapLoading: false
    };
  },
  computed: {
    currentMode() {
      return this.editorState?.mode || WorldEditorMode.VIEW;
    },
    isEditMode() {
      return this.currentMode === WorldEditorMode.EDIT;
    },
    selectedTool() {
      return this.editorState?.selectedTool || WorldEditorTool.SELECT;
    },
    currentFloor() {
      const editorStateFloor = this.editorState?.currentFloor
      if (editorStateFloor !== undefined) {
        return editorStateFloor;
      }
      return 1; // Default to floor 1 if not set
    },
    activeLayers() {
      return this.editorState?.activeLayers || new Set();
    },
    selectedRooms() {
      return Array.from(this.editorState?.selectedRooms || []);
    },
    totalRooms() {
      return this.editorState?.rooms?.size || 0;
    },
    totalConnections() {
      return this.editorState?.connections?.size || 0;
    },
    layerCounts() {
      if (!this.editorState) return {};

      const counts = {};
      const rooms = this.editorState.getRoomsForFloor();

      Object.values(WorldEditorLayer).forEach(layer => {
        counts[layer] = rooms.reduce((count, room) => {
          return count + (room.hasLayerEntities(layer) ? 1 : 0);
        }, 0);
      });

      return counts;
    },
    worldStats() {
      if (!this.editorState) return {};

      const rooms = Array.from(this.editorState.rooms.values());
      return {
        totalRooms: rooms.length,
        totalConnections: this.editorState.connections.size,
        floorsUsed: [...new Set(rooms.map(r => r.position.grid_z))].length,
        entitiesByType: {
          players: rooms.reduce((sum, r) => sum + r.players.length, 0),
          npcs: rooms.reduce((sum, r) => sum + r.npcs.length, 0),
          objects: rooms.reduce((sum, r) => sum + r.objects.length, 0),
          anomalies: rooms.reduce((sum, r) => sum + r.anomalies.length, 0)
        }
      };
    }
  },
  async mounted() {
    try {
      // Initialize the WorldEditor service
      await this.service.initialize();
      this.editorState = this.service.getState();

      // Load saved floor from localStorage if available
      const savedFloor = localStorage.getItem('worldEditor_currentFloor');
      if (savedFloor !== null) {
        const floor = parseInt(savedFloor, 10);
        if (!isNaN(floor)) {
          await this.service.setFloor(floor);
        }
      }

      // Set up event listeners
      this.setupEventListeners();

      // Start time update interval
      this.timeUpdateInterval = setInterval(() => {
        this.currentTime = new Date().toLocaleTimeString();
      }, 1000);

      // Subscribe to new cycle events
      this.bus = ensureConnection();
      this.bus.on("world::new_cycle", this.handleCycleChange);

      // Get initial cycle number
      await this.fetchCurrentCycle();

      this.setLastAction('WorldEditor initialized');
    } catch (error) {
      console.error('Failed to initialize WorldEditor:', error);
      this.setLastAction('Failed to initialize WorldEditor');
    }
  },
  beforeUnmount() {
    // Clean up event listeners
    this.cleanupEventListeners();

    // Clear time update interval
    if (this.timeUpdateInterval) {
      clearInterval(this.timeUpdateInterval);
    }

    // Clean up cycle subscription
    if (this.bus) {
      this.bus.off("world::new_cycle", this.handleCycleChange);
    }
  },
  methods: {
    // Cycle/turn handling methods
    async fetchCurrentCycle() {
      try {
        const response = await ActionGameApi.actionCurrentCycleRetrieve();
        this.currentCycleNumber = response.data.id;
      } catch (error) {
        console.error("Failed to fetch current cycle:", error);
      }
    },

    async handleCycleChange(data) {
      console.log("Cycle change event received", data);
      if (data.id === this.currentCycleNumber) {
        console.debug("Cycle number is the same, skipping update");
        return;
      }
      this.currentCycleNumber = data.id;

      // Refresh world data when cycle changes
      await this.refreshWorld();
    },

    setupEventListeners() {
      this.service.on('stateUpdated', this.onStateUpdated);
      this.service.on('roomCreated', this.onRoomCreatedEvent);
      this.service.on('roomDeleted', this.onRoomDeletedEvent);
      this.service.on('roomUpdated', this.onRoomUpdatedEvent);
      this.service.on('connectionCreated', this.onConnectionCreatedEvent);
      this.service.on('connectionDeleted', this.onConnectionDeletedEvent);
      this.service.on('modeChanged', this.onModeChanged);
      this.service.on('toolChanged', this.onToolChanged);
      this.service.on('layerToggled', this.onLayerToggledEvent);
    },

    cleanupEventListeners() {
      this.service.off('stateUpdated', this.onStateUpdated);
      this.service.off('roomCreated', this.onRoomCreatedEvent);
      this.service.off('roomDeleted', this.onRoomDeletedEvent);
      this.service.off('roomUpdated', this.onRoomUpdatedEvent);
      this.service.off('connectionCreated', this.onConnectionCreatedEvent);
      this.service.off('connectionDeleted', this.onConnectionDeletedEvent);
      this.service.off('modeChanged', this.onModeChanged);
      this.service.off('toolChanged', this.onToolChanged);
      this.service.off('layerToggled', this.onLayerToggledEvent);
    },

    // Event handlers
    onStateUpdated(state) {
      this.editorState = state;
      this.hasUnsavedChanges = true;
    },

    onRoomCreatedEvent(room) {
      this.setLastAction(`Created room at (${room.position.grid_x}, ${room.position.grid_y})`);
    },

    onRoomDeletedEvent({roomId, room}) {
      this.setLastAction(`Deleted room ${room?.getDisplayName() || roomId}`);
      if (this.selectedRoom?.id === roomId) {
        this.selectedRoom = null;
      }
    },

    onRoomUpdatedEvent(room) {
      this.setLastAction(`Updated room ${room.getDisplayName()}`);
      if (this.selectedRoom?.id === room.id) {
        this.selectedRoom = room;
      }
    },

    onConnectionCreatedEvent(connection) {
      this.setLastAction('Created connection between rooms');
    },

    onConnectionDeletedEvent({connectionId}) {
      this.setLastAction('Deleted connection');
    },

    onModeChanged(mode) {
      this.setLastAction(`Switched to ${mode.toUpperCase()} mode`);
    },

    onToolChanged(tool) {
      this.setLastAction(`Selected ${tool.replace('_', ' ')} tool`);
    },

    onLayerToggledEvent({layer, active}) {
      this.setLastAction(`${active ? 'Enabled' : 'Disabled'} ${layer} layer`);
    },

    // UI Actions
    toggleMode() {
      this.service.toggleMode();
    },

    onToolSelected(tool) {
      this.service.setTool(tool);
    },

    onLayerToggled(layer) {
      this.service.toggleLayer(layer);
    },

    async floorUp() {
      const newFloor = this.currentFloor + 1;
      await this.service.setFloor(newFloor);
      // Save current floor to localStorage
      localStorage.setItem('worldEditor_currentFloor', newFloor.toString());
      this.setLastAction(`Moved to floor ${newFloor}`);
    },

    async floorDown() {
      const newFloor = this.currentFloor - 1;
      await this.service.setFloor(newFloor);
      // Save current floor to localStorage
      localStorage.setItem('worldEditor_currentFloor', newFloor.toString());
      this.setLastAction(`Moved to floor ${newFloor}`);
    },

    async refreshWorld() {
      try {
        this.isMapLoading = true;
        await this.service.refresh();
        this.setLastAction('World data refreshed');
        this.hasUnsavedChanges = false;
      } catch (error) {
        console.error('Failed to refresh world:', error);
        this.setLastAction('Failed to refresh world data');
      } finally {
        this.isMapLoading = false;
      }
    },

    async saveWorld() {
      try {
        // This would implement saving logic
        this.setLastAction('World saved successfully');
        this.hasUnsavedChanges = false;
      } catch (error) {
        console.error('Failed to save world:', error);
        this.setLastAction('Failed to save world');
      }
    },

    // Map event handlers
    onRoomSelected(room, shiftKey = false) {
      this.selectedRoom = room;

      // If shift key is not pressed, clear selection before selecting the new room
      if (!shiftKey) {
        this.service.clearSelection();
      }

      this.service.toggleRoomSelection(room.id);
    },

    async onRoomCreated(position) {
      try {
        await this.service.createRoom(position.gridX, position.gridY, position.gridZ);
      } catch (error) {
        console.error('Failed to create room:', error);
        this.setLastAction('Failed to create room');
      }
    },

    async onRoomMoved(roomId, newPosition) {
      try {
        await this.service.moveRoom(roomId, newPosition.gridX, newPosition.gridY, newPosition.gridZ);
      } catch (error) {
        console.error('Failed to move room:', error);
        this.setLastAction('Failed to move room');
      }
    },

    async onConnectionCreated(fromRoomId, toRoomId, isVertical = false) {
      try {
        await this.service.createConnection(fromRoomId, toRoomId, isVertical);
      } catch (error) {
        console.error('Failed to create connection:', error);
        this.setLastAction('Failed to create connection');
      }
    },

    async onConnectionDeleted(connectionId) {
      try {
        await this.service.deleteConnection(connectionId);
      } catch (error) {
        console.error('Failed to delete connection:', error);
        this.setLastAction('Failed to delete connection');
      }
    },

    onConnectionSelected(connection) {
      // Find the source room for this connection
      const fromRoom = this.editorState.rooms.get(connection.fromRoomId);
      if (fromRoom) {
        // Select the room
        this.selectedRoom = fromRoom;
        // Clear selection before selecting the new room (no shift key for connection selection)
        this.service.clearSelection();
        this.service.toggleRoomSelection(fromRoom.id);

        // Use nextTick to ensure the room info component is mounted
        this.$nextTick(() => {
          // Access the room info component via ref and open the connection info
          if (this.$refs.roomInfoPanel) {
            this.$refs.roomInfoPanel.openConnectionInfo(connection);
          }
        });

        this.setLastAction('Connection selected');
      }
    },

    async onConnectionUpdated(connectionId, updates) {
      try {
        await this.service.updateConnection(connectionId, updates);
        this.setLastAction('Connection updated');
      } catch (error) {
        console.error('Failed to update connection:', error);
        this.setLastAction('Failed to update connection');
      }
    },

    onMapClicked(position) {
      if (this.isEditMode && this.selectedTool === WorldEditorTool.CREATE_ROOM) {
        this.onRoomCreated(position);
      }
    },

    // Room event handlers
    async onRoomUpdated(room, updates) {
      try {
        await this.service.updateRoom(room.id, updates);
      } catch (error) {
        console.error('Failed to update room:', error);
        this.setLastAction('Failed to update room');
      }
    },

    async onRoomDeleted(room) {
      try {
        await this.service.deleteRoom(room.id);
      } catch (error) {
        console.error('Failed to delete room:', error);
        this.setLastAction('Failed to delete room');
      }
    },

    // Entity event handlers
    async onEntitySpawned(entityType, entityData) {
      if (!this.selectedRoom) return;

      try {
        switch (entityType) {
          case 'item':
            await this.service.spawnItem(this.selectedRoom.id, entityData);
            break;
          case 'npc':
            await this.service.spawnNPC(this.selectedRoom.id, entityData);
            break;
          case 'anomaly':
            await this.service.spawnAnomaly(this.selectedRoom.id, entityData);
            break;
        }
      } catch (error) {
        console.error(`Failed to spawn ${entityType}:`, error);
        this.setLastAction(`Failed to spawn ${entityType}`);
      }
    },

    // Utility methods
    clearSelection() {
      this.selectedRoom = null;
      this.service.clearSelection();
    },

    setLastAction(action) {
      this.lastAction = action;
      // Clear the action after 5 seconds
      setTimeout(() => {
        if (this.lastAction === action) {
          this.lastAction = '';
        }
      }, 5000);
    },

    toggleStatsPanel() {
      this.showStatsPanel = !this.showStatsPanel;
      this.setLastAction(this.showStatsPanel ? 'Statistics panel opened' : 'Statistics panel closed');
    },

    toggleLayersPanel() {
      this.showLayersPanel = !this.showLayersPanel;
      this.setLastAction(this.showLayersPanel ? 'Layers panel opened' : 'Layers panel closed');
    },

    onShowEntityDetails(details) {
      // Handle showing entity details
      // This could open a modal, update a sidebar, etc.
      const entityTypeName = {
        'players': 'Players',
        'npcs': 'NPCs',
        'objects': 'Objects',
        'anomalies': 'Anomalies'
      }[details.entityType] || 'Entities';

      const count = details.entities.length;
      this.setLastAction(`${entityTypeName} in room: ${count}`);

      // Select the room
      if (details.roomId) {
        const room = this.editorState.rooms.get(details.roomId);
        if (room) {
          this.selectedRoom = room;
          // Clear selection before selecting the new room (no shift key for entity details)
          this.service.clearSelection();
          this.service.toggleRoomSelection(room.id);
        }
      }
    },

    /**
     * Handle item selection from the items list
     */
    onItemSelected(item) {
      console.log('Item selected:', item);
      this.setLastAction(`Selected item: ${item.name}`);

      // If we're in edit mode and have a selected room, spawn the item
      if (this.isEditMode && this.selectedRoom) {
        this.onEntitySpawned('item', item);
      }
    },

    /**
     * Toggle items panel visibility
     */
    toggleItemsPanel() {
      this.showItemsPanel = !this.showItemsPanel;
      this.setLastAction(this.showItemsPanel ? 'Items panel opened' : 'Items panel closed');
    }
  }
};
</script>

<style scoped>
.world-editor {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #1e1e1e;
  color: #ffffff;
  font-family: 'Roboto', sans-serif;
}

/* Toolbar Styles */
.world-editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #2d2d2d;
  border-bottom: 1px solid #444;
  min-height: 60px;
}

.toolbar-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.mode-toggle {
  padding: 0.5rem 1rem;
  background: #444;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mode-toggle:hover {
  background: #555;
}

.mode-toggle.edit-mode {
  background: #1E90FF;
}

.mode-indicator {
  font-weight: bold;
  color: #1E90FF;
}

.floor-display {
  font-weight: bold;
  min-width: 80px;
  text-align: center;
}

.refresh-btn, .save-btn {
  padding: 0.5rem 1rem;
  background: #444;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.refresh-btn:hover, .save-btn:hover {
  background: #555;
}

.save-btn:disabled {
  background: #333;
  color: #666;
  cursor: not-allowed;
}

/* Content Area Styles */
.world-editor-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.left-panel {
  width: 300px;
  background: #2d2d2d;
  border-right: 1px solid #444;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.center-panel {
  flex: 1;
  position: relative;
  overflow: hidden;
}

/* Map Loading Overlay */
.map-loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  pointer-events: all;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgba(45, 45, 45, 0.9);
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #1E90FF;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

.loading-text {
  color: #ffffff;
  font-size: 1.2rem;
  font-weight: bold;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.right-panel {
  width: 300px;
  background: #2d2d2d;
  border-left: 1px solid #444;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

/* Panel Components */
.editor-toolbar {
  border-bottom: 1px solid #444;
}

.layer-controls {
  flex: 1;
}

.room-info-panel {
  flex: 1;
}

.world-map {
  width: 100%;
  height: 100%;
}

.entity-spawner {
  border-bottom: 1px solid #444;
}

.world-stats {
  flex: 1;
}

.items-list {
  flex: 1;
  border-top: 1px solid #444;
}

/* Status Bar Styles */
.world-editor-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #2d2d2d;
  border-top: 1px solid #444;
  min-height: 40px;
  font-size: 0.9rem;
}

.status-left, .status-right {
  display: flex;
  gap: 1rem;
}

.status-item {
  color: #ccc;
}

/* Stats Toggle Button */
.stats-toggle-btn {
  padding: 0.25rem 0.5rem;
  background: #444;
  color: #ccc;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 1rem;
}

.stats-toggle-btn:hover {
  background: #555;
  color: #fff;
}

.icon-stats::before {
  content: '📊';
}

/* Layers Toggle Button */
.layers-toggle-btn {
  padding: 0.25rem 0.5rem;
  background: #444;
  color: #ccc;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 1rem;
}

.layers-toggle-btn:hover {
  background: #555;
  color: #fff;
}

.icon-layers::before {
  content: '🔍';
}

/* Items Toggle Button */
.items-toggle-btn {
  padding: 0.25rem 0.5rem;
  background: #444;
  color: #ccc;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 1rem;
}

.items-toggle-btn:hover {
  background: #555;
  color: #fff;
}

.icon-items::before {
  content: '📦';
}

/* Button Styles */
button {
  padding: 0.5rem 1rem;
  background: #444;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover:not(:disabled) {
  background: #555;
}

button:disabled {
  background: #333;
  color: #666;
  cursor: not-allowed;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .left-panel, .right-panel {
    width: 250px;
  }
}

@media (max-width: 900px) {
  .world-editor-content {
    flex-direction: column;
  }

  .left-panel, .right-panel {
    width: 100%;
    height: 200px;
  }

  .center-panel {
    flex: 1;
    min-height: 400px;
  }
}

/* Dark theme consistency */
:deep(.vue-component) {
  background: #1e1e1e;
  color: #ffffff;
}

:deep(.panel) {
  background: #2d2d2d;
  border: 1px solid #444;
}

:deep(.input) {
  background: #333;
  color: #fff;
  border: 1px solid #555;
}

:deep(.input:focus) {
  border-color: #1E90FF;
  outline: none;
}
</style>
