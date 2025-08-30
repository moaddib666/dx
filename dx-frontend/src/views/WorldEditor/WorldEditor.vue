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

      <!-- SubLocation Selector -->
      <div class="toolbar-section sublocation-controls">
        <label class="sublocation-label">SubLocation:</label>
        <button
          class="sublocation-selector-btn"
          :disabled="isSubLocationsLoading || subLocations.length === 0"
          @click="openSubLocationModal"
        >
          <div v-if="isSubLocationsLoading" class="loading-state">
            Loading...
          </div>
          <div v-else-if="subLocations.length === 0" class="empty-state">
            No SubLocations
          </div>
          <div v-else-if="currentSubLocation" class="selected-sublocation">
            <div
              class="sublocation-background"
              :style="{ backgroundImage: currentSubLocation.image ? `url(${currentSubLocation.image})` : 'none' }"
            >
              <div class="sublocation-overlay">
                <span class="sublocation-name">{{ currentSubLocation.name }}</span>
              </div>
            </div>
          </div>
          <div v-else class="no-selection">
            Select SubLocation
          </div>
        </button>
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
            @auto-connect-toggled="onAutoConnectToggled"
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
            @character-selected="openCharacterCard"
        />
      </div>

      <!-- Center Panel - Map -->
      <div class="center-panel">
        <!-- Map Loading Overlay -->
        <Loader
          v-if="isMapLoading"
          text="Loading map data..."
          message="Please wait while we fetch the map"
        />

        <WorldEditorMap
            ref="worldEditorMap"
            :currentFloor="currentFloor"
            :editorState="editorState"
            :mapData="mapData"
            :currentCycleNumber="currentCycleNumber"
            class="world-map"
            @room-selected="onRoomSelected"
            @room-created="onRoomCreated"
            @room-moved="onRoomMoved"
            @room-deleted="onRoomDeleted"
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

      <!-- Right Panel - Entity Management (only visible when it has content and not in edit mode) -->
      <div v-if="!isEditMode && (showItemsPanel || showNPCTemplatesPanel)"
           class="right-panel">

        <!-- Items List -->
        <WorldEditorItemsList
            v-if="showItemsPanel"
            class="items-list"
            @item-selected="onItemSelected"
        />

        <!-- NPC Templates List -->
        <NPCTemplatesList
            v-if="showNPCTemplatesPanel"
            class="npc-templates-list"
            @template-selected="onTemplateSelected"
        />
      </div>

      <!-- Character Cards Overlay -->
      <GameMasterCharacterCard
          v-for="characterId in openedCharacterIds"
          :key="characterId"
          :characterId="characterId"
          :style="getCharacterCardStyle(characterId)"
          @close="closeCharacterCard(characterId)"
          @item-selected="onCharacterItemSelected"
      />

      <!-- SubLocation Selector Modal -->
      <div v-if="showSubLocationModal" class="modal-overlay" @click="closeSubLocationModal">
        <div class="modal-content" @click.stop>
          <GMSubLocationSelector
            :subLocations="subLocations"
            :selectedSubLocationId="currentSubLocation?.id"
            @select="onSubLocationSelected"
            @close="closeSubLocationModal"
          />
        </div>
      </div>
    </div>

    <!-- Status Bar -->
    <div class="world-editor-status">
      <div class="status-left">
        <span class="status-item">Rooms: {{ totalRooms }}</span>
        <span class="status-item">Connections: {{ totalConnections }}</span>
        <span class="status-item">Selected: {{ selectedRooms.length }}</span>
        <button class="items-toggle-btn" title="Toggle Items Panel" @click="toggleItemsPanel">
          <i class="icon-items"></i>
        </button>
        <button class="npc-templates-toggle-btn" title="Toggle NPC Templates Panel" @click="toggleNPCTemplatesPanel">
          <i class="icon-npc-templates"></i>
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
import {worldEditorService} from '@/services/WorldEditorService.ts';
import {WorldEditorLayer, WorldEditorMode, WorldEditorTool} from '@/models/WorldEditorModels.ts';
import {ensureConnection} from "@/api/dx-websocket/index.ts";
import {ActionGameApi, GMWorldSubLocationsApi} from "@/api/backendService.js";

// Import WorldEditor components (to be created)
import WorldEditorToolbar from '@/components/WorldEditor/WorldEditorToolbar.vue';
import WorldEditorRoomInfo from '@/components/WorldEditor/WorldEditorRoomInfo.vue';
import WorldEditorMap from '@/components/WorldEditor/WorldEditorMap.vue';
import WorldEditorEntitySpawner from '@/components/WorldEditor/WorldEditorEntitySpawner.vue';
import WorldEditorItemsList from '@/components/WorldEditor/WorldEditorItemsList.vue';
import NPCTemplatesList from '@/components/shared/NPCTemplatesList.vue';
import GameMasterCharacterCard from '@/components/WorldEditor/GameMasterCharacterCard.vue';
import GMSubLocationSelector from '@/components/GameMaster/Character/GMSubLocationSelector.vue';
import Loader from '@/components/Loader.vue';

export default {
  name: 'WorldEditor',
  components: {
    WorldEditorToolbar,
    WorldEditorRoomInfo,
    WorldEditorMap,
    WorldEditorEntitySpawner,
    WorldEditorItemsList,
    NPCTemplatesList,
    GameMasterCharacterCard,
    GMSubLocationSelector,
    Loader
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
      showItemsPanel: true, // Items panel visibility state
      showNPCTemplatesPanel: false, // NPC Templates panel visibility state
      autoConnectEnabled: true, // Auto-connect toggle state (default enabled)

      // Timer for current time update
      timeUpdateInterval: null,

      // Current cycle/turn tracking
      currentCycleNumber: null,
      bus: null,

      // Map loading state
      isMapLoading: false,

      // Character cards
      openedCharacterIds: [],

      // SubLocation management
      subLocations: [],
      currentSubLocation: null,
      isSubLocationsLoading: false,
      showSubLocationModal: false
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

      // Fetch SubLocations and restore saved SubLocation
      await this.fetchSubLocations();
      const savedSubLocation = localStorage.getItem('worldEditor_currentSubLocation');
      if (savedSubLocation) {
        try {
          const parsedSubLocation = JSON.parse(savedSubLocation);
          // Verify the saved SubLocation still exists in the fetched list
          const existingSubLocation = this.subLocations.find(sl => sl.id === parsedSubLocation.id);
          if (existingSubLocation) {
            this.currentSubLocation = existingSubLocation;
          }
        } catch (error) {
          console.warn('Failed to parse saved SubLocation:', error);
        }
      }

      // Set up event listeners
      this.setupEventListeners();

      // Set up keyboard event listeners
      this.setupKeyboardListeners();

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

    // Clean up keyboard event listeners
    this.cleanupKeyboardListeners();

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

    // SubLocation management methods
    async fetchSubLocations() {
      try {
        this.isSubLocationsLoading = true;
        const response = await GMWorldSubLocationsApi.gamemasterWorldSubLocationsList(true); // Only active SubLocations
        this.subLocations = response.data.results || response.data || [];

        // Set the first active SubLocation as current if none is selected
        if (!this.currentSubLocation && this.subLocations.length > 0) {
          this.currentSubLocation = this.subLocations[0];
        }
      } catch (error) {
        console.error("Failed to fetch SubLocations:", error);
        this.subLocations = [];
      } finally {
        this.isSubLocationsLoading = false;
      }
    },

    selectSubLocation(subLocation) {
      this.currentSubLocation = subLocation;
      this.setLastAction(`Selected SubLocation: ${subLocation.name}`);
      // Save selected SubLocation to localStorage
      localStorage.setItem('worldEditor_currentSubLocation', JSON.stringify(subLocation));
    },

    // SubLocation modal methods
    openSubLocationModal() {
      this.showSubLocationModal = true;
    },

    closeSubLocationModal() {
      this.showSubLocationModal = false;
    },

    onSubLocationSelected(subLocation) {
      this.selectSubLocation(subLocation);
      this.closeSubLocationModal();
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

    // Keyboard event listeners
    setupKeyboardListeners() {
      document.addEventListener('keydown', this.handleKeyDown);
    },

    cleanupKeyboardListeners() {
      document.removeEventListener('keydown', this.handleKeyDown);
    },

    handleKeyDown(event) {
      // Handle Escape key to cancel in-progress actions
      if (event.key === 'Escape') {
        this.handleEscapeKey();
      }
    },

    handleEscapeKey() {
      // Cancel any in-progress actions in the map component
      if (this.$refs.worldEditorMap) {
        this.$refs.worldEditorMap.cancelInProgressActions();
      }

      // Provide user feedback
      this.setLastAction('Action canceled');
    },

    // Event handlers
    onStateUpdated(state) {
      this.editorState = state;
      this.hasUnsavedChanges = true;
      // Force Vue to detect changes in the state object
      this.$forceUpdate();
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

    onAutoConnectToggled(enabled) {
      this.autoConnectEnabled = enabled;
      this.setLastAction(`Auto-connect ${enabled ? 'enabled' : 'disabled'}`);
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
      // Handle spawner creation if CREATE_SPAWNER tool is active
      if (this.currentTool === WorldEditorTool.CREATE_SPAWNER) {
        this.onCreateSpawnerInRoom(room);
        return;
      }

      this.selectedRoom = room;

      // If shift key is not pressed, clear selection before selecting the new room
      if (!shiftKey) {
        this.service.clearSelection();
      }

      this.service.toggleRoomSelection(room.id);
    },

    async onRoomCreated(position) {
      try {
        const subLocationId = this.currentSubLocation ? this.currentSubLocation.id : null;
        const previouslySelectedRoom = this.selectedRoom;

        const newRoom = await this.service.createRoom(position.gridX, position.gridY, position.gridZ, subLocationId);

        // Automatically select the newly created room (Issue #2)
        if (newRoom) {
          this.selectedRoom = newRoom;
          this.service.clearSelection();
          this.service.toggleRoomSelection(newRoom.id);

          // Create automatic connection if auto-connect is enabled and there was a previously selected room
          if (this.autoConnectEnabled && previouslySelectedRoom && previouslySelectedRoom.id !== newRoom.id) {
            try {
              await this.service.createConnection(previouslySelectedRoom.id, newRoom.id, false);
              this.setLastAction(`Created room and auto-connected to ${previouslySelectedRoom.getDisplayName?.() || 'previous room'}`);
            } catch (connectionError) {
              console.error('Failed to create automatic connection:', connectionError);
              this.setLastAction('Created room but failed to create automatic connection');
            }
          } else {
            this.setLastAction('Created room');
          }
        }
      } catch (error) {
        console.error('Failed to create room:', error);
        this.setLastAction('Failed to create room');
      }
    },

    async onCreateSpawnerInRoom(room) {
      try {
        // For now, use a default character template ID
        // In a real implementation, this should open a dialog to select character template
        const defaultCharacterTemplateId = '0c772e55-920d-4e7f-918a-89fb01f32b76'; // From the example in issue description

        const newSpawner = await this.service.createSpawner(room.id, defaultCharacterTemplateId);

        if (newSpawner) {
          this.setLastAction(`Created spawner in ${room.getDisplayName?.() || 'room'}`);

          // Optionally switch back to select tool after creating spawner
          this.service.setTool(WorldEditorTool.SELECT);
        }
      } catch (error) {
        console.error('Failed to create spawner:', error);
        this.setLastAction('Failed to create spawner');
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
    },

    /**
     * Toggle NPC templates panel visibility
     */
    toggleNPCTemplatesPanel() {
      this.showNPCTemplatesPanel = !this.showNPCTemplatesPanel;
      this.setLastAction(this.showNPCTemplatesPanel ? 'NPC Templates panel opened' : 'NPC Templates panel closed');
    },

    /**
     * Open a character card for the given character ID
     * @param {string} characterId - The ID of the character to open
     */
    openCharacterCard(characterId) {
      if (!characterId) return;

      // Check if character is already opened
      if (this.openedCharacterIds.includes(characterId)) {
        // Move to front if already opened
        this.openedCharacterIds = this.openedCharacterIds.filter(id => id !== characterId);
        this.openedCharacterIds.unshift(characterId);
      } else {
        // Add to opened characters, maintaining max of 2
        this.openedCharacterIds.unshift(characterId);
        if (this.openedCharacterIds.length > 2) {
          this.openedCharacterIds.pop();
        }
      }

      this.setLastAction(`Character card opened: ${characterId}`);
    },

    /**
     * Close a character card
     * @param {string} characterId - The ID of the character to close
     */
    closeCharacterCard(characterId) {
      this.openedCharacterIds = this.openedCharacterIds.filter(id => id !== characterId);
      this.setLastAction(`Character card closed: ${characterId}`);
    },

    /**
     * Get the style for a character card based on its position in the openedCharacterIds array
     * @param {string} characterId - The ID of the character
     * @returns {Object} - The style object for the character card
     */
    getCharacterCardStyle(characterId) {
      const index = this.openedCharacterIds.indexOf(characterId);
      if (index === -1) return {};

      // Only set z-index to allow free movement in any direction
      return {
        zIndex: 1000 - index
      };
    },

    /**
     * Handle item selection from a character card
     * @param {Object} item - The selected item
     */
    onCharacterItemSelected(item) {
      console.log('Character item selected:', item);
      this.setLastAction(`Selected character item: ${item.name}`);

      // If we're in edit mode and have a selected room, spawn the item
      if (this.isEditMode && this.selectedRoom) {
        this.onEntitySpawned('item', item);
      }
    },

    /**
     * Handle template selection from the NPC templates list
     * @param {Object} template - The selected NPC template
     */
    onTemplateSelected(template) {
      console.log('NPC template selected:', template);
      this.setLastAction(`Selected NPC template: ${template.name}`);

      // If we're in edit mode and have a selected room, spawn the NPC from the template
      if (this.isEditMode && this.selectedRoom) {
        this.spawnNPCFromTemplate(template, this.selectedRoom);
      }
    },

    /**
     * Spawn an NPC from a template in the specified room
     * @param {Object} template - The NPC template
     * @param {Object} room - The room to spawn the NPC in
     */
    async spawnNPCFromTemplate(template, room) {
      try {
        console.log(`Spawning NPC from template ${template.id} in room ${room.id}`);

        // Create position object for the NPC
        const position = {
          id: room.id,
          grid_x: room.position.grid_x,
          grid_y: room.position.grid_y,
          grid_z: room.position.grid_z
        };

        // Use the character templates service to create the NPC
        const { characterTemplatesService } = await import('@/services/CharacterTemplatesService.ts');
        const npc = await characterTemplatesService.createNpcFromTemplate(template.id, position);

        this.setLastAction(`Created NPC from template: ${template.name}`);

        // Refresh the world to show the new NPC
        await this.refreshWorld();

        return npc;
      } catch (error) {
        console.error('Failed to spawn NPC from template:', error);
        this.setLastAction(`Failed to create NPC from template: ${error.message || 'Unknown error'}`);
        throw error;
      }
    },

    /**
     * Handle showing entity details, including opening character cards for characters
     */
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

          // If the entity type is players or npcs, open character cards for them
          if ((details.entityType === 'players' || details.entityType === 'npcs') && details.entities.length > 0) {
            // Open character cards for up to 2 characters
            const charactersToOpen = details.entities.slice(0, 2);
            charactersToOpen.forEach(character => {
              if (character.id) {
                this.openCharacterCard(character.id);
              }
            });
          }
        }
      }
    },

  }
};
</script>

<style scoped>
.world-editor {
  display: flex;
  flex: 1;
  width: 100%;
  flex-direction: column;
  max-height: 100vh;
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

.npc-templates-list {
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

/* NPC Templates Toggle Button */
.npc-templates-toggle-btn {
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

.npc-templates-toggle-btn:hover {
  background: #555;
  color: #fff;
}

.icon-npc-templates::before {
  content: '👤';
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

/* SubLocation Selector Button */
.sublocation-selector-btn {
  min-width: 200px;
  height: 60px;
  padding: 0;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid #444;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  position: relative;
}

.sublocation-selector-btn:hover:not(:disabled) {
  border-color: #7fff16;
  transform: translateY(-1px);
}

.sublocation-selector-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.loading-state,
.empty-state,
.no-selection {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #ccc;
  font-size: 0.9rem;
}

.selected-sublocation {
  height: 100%;
  width: 100%;
}

.sublocation-background {
  height: 100%;
  width: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-color: rgba(0, 0, 0, 0.2);
  position: relative;
}

.sublocation-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  padding: 8px 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sublocation-name {
  color: #fada95;
  font-weight: 600;
  font-size: 0.9rem;
  text-align: center;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  width: 90vw;
  max-width: 1200px;
  height: 80vh;
  max-height: 600px;
  background: transparent;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
}
</style>
