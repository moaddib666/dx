<template>
  <div class="world-editor-room-info">
    <!-- Full Container Drop Zone -->
    <div
        ref="dropZone"
        class="room-drop-zone"
    >
      <div class="drop-zone-overlay"
           @dragover.prevent
           @dragenter.prevent="handleDragEnter"
           @dragleave.prevent="handleDragLeave"
           @drop.prevent="handleEntityDrop">
        <div class="drop-zone-message">
          <i class="drop-zone-icon">📦</i>
          <span class="drop-zone-text">Drop Item or NPC Here</span>
        </div>
      </div>
    </div>

    <div class="room-info-header">
      <h3>Room Information</h3>
      <button class="close-btn" title="Close" @click="closePanel">
        <i class="icon-times"></i>
      </button>
    </div>

    <div class="room-info-content">
      <!-- Basic Room Info -->
      <BasicInformation
          :room="room"
          :editable="editable"
          @update:room-type="updateRoomType"
      />

      <!-- Room Labels -->
      <Labels
          :labels="localRoom.labels"
          :editable="editable"
          @update:labels="updateLabels"
      />

      <!-- Room Entities -->
      <Entities
          :room="room"
          @player-click="onPlayerClick"
          @npc-click="onNpcClick"
      />

      <!-- Room Connections -->
      <Connections
          :room="room"
          :room-connections="roomConnections"
          :editable="editable"
          @open-connection-info="openConnectionInfo"
          @remove-connection="removeConnection"
      />

      <!-- Connection Information Modal -->
      <WorldEditorConnectionInfo
          v-if="selectedConnection"
          :connection="selectedConnection"
          :editable="editable"
          :editorState="editorState"
          @close="selectedConnection = null"
          @connection-updated="onConnectionUpdated"
          @connection-deleted="removeConnection"
          @view-room="viewRoom"
      />

      <!-- Room Actions -->
      <div v-if="editable" class="info-section">
        <h4>Actions</h4>
        <div class="action-buttons">
          <button class="action-btn" @click="duplicateRoom">
            <i class="icon-copy"></i> Duplicate Room
          </button>
          <button class="action-btn danger" @click="confirmDelete">
            <i class="icon-trash"></i> Delete Room
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click="cancelDelete">
      <div class="modal-content" @click.stop>
        <h3>Confirm Delete</h3>
        <p>Are you sure you want to delete this room? This action cannot be undone.</p>
        <div class="modal-actions">
          <button class="modal-btn" @click="cancelDelete">Cancel</button>
          <button class="modal-btn danger" @click="deleteRoom">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WorldEditorConnectionInfo from '@/components/WorldEditor/WorldEditorConnectionInfo.vue';
import EditInDjangoAdmin from '@/components/EditInDjangoAdmin.vue';
import {gameMasterItemSpawnerService} from '@/services/GameMasterItemSpawnerService.js';
import {dragDropService} from '@/services/DragDropService.js';
import {characterTemplatesService} from '@/services/CharacterTemplatesService.js';

// Import the new components
import BasicInformation from '@/components/WorldEditor/WorldEditorRoomInfo/BasicInformation.vue';
import Labels from '@/components/WorldEditor/WorldEditorRoomInfo/Labels.vue';
import Entities from '@/components/WorldEditor/WorldEditorRoomInfo/Entities.vue';
import Connections from '@/components/WorldEditor/WorldEditorRoomInfo/Connections.vue';

export default {
  name: 'WorldEditorRoomInfo',
  components: {
    WorldEditorConnectionInfo,
    EditInDjangoAdmin,
    BasicInformation,
    Labels,
    Entities,
    Connections
  },
  props: {
    room: {
      type: Object,
      required: true
    },
    editable: {
      type: Boolean,
      default: false
    },
    editorState: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      localRoom: null,
      showDeleteConfirm: false,
      selectedConnection: null,
      isDraggingItem: false // Flag to track if an item is being dragged
    };
  },
  computed: {
    roomConnections() {
      if (!this.room || !this.localRoom) {
        return [];
      }

      // Use the connections array from the localRoom
      return this.localRoom.connections || [];
    }
  },
  watch: {
    room: {
      handler(newRoom) {
        this.localRoom = JSON.parse(JSON.stringify(newRoom));
      },
      immediate: true,
      deep: true
    }
  },

  created() {
    // No initialization needed here anymore
  },
  mounted() {
    // Register the drop zone with the drag drop service
    if (this.$refs.dropZone) {
      dragDropService.registerDropTarget(this.$refs.dropZone);
    }
  },
  beforeUnmount() {
    // Unregister the drop zone
    if (this.$refs.dropZone) {
      dragDropService.unregisterDropTarget(this.$refs.dropZone);
    }
  },
  methods: {
    // Methods for handling events from child components
    updateRoomType(newType) {
      this.localRoom.type = newType;
      this.onRoomUpdated();
    },

    updateLabels(newLabels) {
      this.localRoom.labels = newLabels;
      this.onRoomUpdated();
    },

    closePanel() {
      this.$emit('close');
    },



    onPlayerClick(player) {
      // Emit an event to open the character card for this player
      if (player && player.id && player.object_type?.model === 'character') {
        this.$emit('character-selected', player.id);
      }
    },

    onNpcClick(npc) {
      // Emit an event to open the character card for this NPC
      if (npc && npc.id && npc.object_type?.model === 'character') {
        this.$emit('character-selected', npc.id);
      }
    },

    onRoomUpdated() {
      this.$emit('room-updated', this.room, {
        type: this.localRoom.type,
        labels: this.localRoom.labels.filter(label => label.trim() !== '')
      });
    },



    openConnectionInfo(connection) {
      if (!connection) {
        console.error('Cannot open connection info: connection is undefined');
        return;
      }
      this.selectedConnection = connection;
    },

    onConnectionUpdated(connectionId, updates) {
      if (!connectionId) {
        console.error('Cannot update connection: connectionId is undefined');
        return;
      }

      // Emit an event to update the connection in the parent component
      this.$emit('connection-updated', connectionId, updates);
    },

    removeConnection(connection) {
      if (!connection) {
        console.error('Cannot remove connection: connection is undefined');
        return;
      }

      // If connection is an object, extract the ID
      let connectionId;
      if (typeof connection === 'object') {
        if (!connection.id) {
          console.error('Cannot remove connection: connection.id is undefined');
          return;
        }
        connectionId = connection.id;
      } else {
        connectionId = connection;
      }

      this.$emit('connection-removed', connectionId);

      // If the selected connection is being removed, close the modal
      if (this.selectedConnection && this.selectedConnection.id === connectionId) {
        this.selectedConnection = null;
      }
    },

    viewRoom(roomId) {
      if (!roomId) {
        console.error('Cannot view room: roomId is undefined');
        return;
      }

      if (!this.editorState || !this.editorState.rooms) {
        console.error('Cannot view room: editorState or editorState.rooms is undefined');
        return;
      }

      // Find the room in the editor state
      const room = this.editorState.rooms.get(roomId);
      if (room) {
        // Emit an event to select the room in the parent component
        this.$emit('room-selected', room);
      } else {
        console.error(`Cannot view room: room with id ${roomId} not found`);
      }
    },

    duplicateRoom() {
      this.$emit('room-duplicated', this.room);
    },

    confirmDelete() {
      this.showDeleteConfirm = true;
    },

    cancelDelete() {
      this.showDeleteConfirm = false;
    },

    deleteRoom() {
      this.showDeleteConfirm = false;
      this.$emit('room-deleted', this.room);
    },

    // Handle drag enter event
    handleDragEnter(event) {
      console.log('Drag enter on room info');
      const dropZone = event.currentTarget.closest('.room-drop-zone');
      if (dropZone) {
        dropZone.classList.add('drag-active');
      }
    },

    // Handle drag leave event
    handleDragLeave(event) {
      console.log('Drag leave on room info');
      const dropZone = event.currentTarget.closest('.room-drop-zone');
      if (dropZone) {
        // Only remove if we're actually leaving the drop zone area
        // Check if the related target is outside the drop zone
        if (!dropZone.contains(event.relatedTarget)) {
          dropZone.classList.remove('drag-active');
        }
      }
    },

    // Handle entity (item or NPC) drop event
    async handleEntityDrop(event) {
      console.log('Drop event triggered on room info');
      const dropZone = event.currentTarget.closest('.room-drop-zone');

      try {
        // Prevent default to stop browser from opening the dragged item
        event.preventDefault();

        // Remove active state immediately
        if (dropZone) {
          dropZone.classList.remove('drag-active');
        }

        // Get the dropped data
        console.log('Event dataTransfer types:', event.dataTransfer.types);

        // Check if this is an NPC template
        const isNpcTemplate = event.dataTransfer.types.includes('application/npc-template');

        // Try to get the data from different MIME types
        let itemData;
        if (isNpcTemplate) {
          itemData = event.dataTransfer.getData('application/npc-template');
        } else {
          itemData = event.dataTransfer.getData('application/json');
          if (!itemData) {
            itemData = event.dataTransfer.getData('text/plain');
          }
        }

        console.log('Got data from drop event:', itemData);

        if (!itemData) {
          console.warn('No data received from drop event');
          return;
        }

        // Try to parse the data
        const droppedEntity = JSON.parse(itemData);
        console.log('Parsed data:', droppedEntity);

        if (!droppedEntity || !droppedEntity.id) {
          console.warn('Invalid data received:', itemData);
          return;
        }

        console.log('Entity dropped on room:', droppedEntity, this.room);

        // Show success feedback
        if (dropZone) {
          dropZone.classList.add('drop-success');

          // Remove the success feedback after a short delay
          setTimeout(() => {
            dropZone.classList.remove('drop-success');
          }, 1000);
        }

        // Handle based on entity type
        if (this.room && this.room.id) {
          let result;

          if (isNpcTemplate) {
            // Create position object for the NPC
            const position = {
              id: this.room.id,
              grid_x: this.room.position.grid_x,
              grid_y: this.room.position.grid_y,
              grid_z: this.room.position.grid_z
            };

            // Use CharacterTemplatesService to create an NPC from the template
            result = await characterTemplatesService.createNpcFromTemplate(droppedEntity.id, position);
            console.log('NPC created successfully:', result);

            // Update the room's NPC count without triggering a full map reload
            if (this.room.npcs && result) {
              // Add the new NPC to the room's npcs array
              this.room.npcs.push({
                id: result.id,
                name: droppedEntity.name,
                behavior: droppedEntity.behavior,
                object_type: {
                  app_label: 'world',
                  model: 'character'
                }
              });

              // Emit an event to notify parent components that the room has been updated
              this.$emit('room-npcs-updated', this.room);
            }
          } else {
            // Use the GameMasterItemSpawnerService to spawn the item at the room's position
            result = await gameMasterItemSpawnerService.spawnItemToPosition(droppedEntity.id, this.room.id);

            if (result) {
              console.log('Item spawned successfully:', result);

              // Update the room's object count without triggering a full map reload
              if (this.room.objects) {
                // Add the new object to the room's objects array
                this.room.objects.push({
                  id: result.id || result.world_item?.id,
                  name: droppedEntity.name,
                  type: droppedEntity.type,
                  object_type: {
                    app_label: 'world',
                    model: 'gameobject'
                  }
                });

                // Emit an event to notify parent components that the room has been updated
                this.$emit('room-objects-updated', this.room);
              }
            }
          }
        }

        // Notify the drag drop service that we've ended dragging
        dragDropService.endDrag();
      } catch (error) {
        console.error('Error handling dropped item:', error);

        // Remove any active states on error
        if (dropZone) {
          dropZone.classList.remove('drag-active', 'drop-success');
        }
      }
    },

    // Optional: Method to handle global drag state changes
    // Call this when drag starts globally to show light highlight
    onGlobalDragStart() {
      const dropZone = this.$refs.dropZone;
      if (dropZone) {
        dropZone.classList.add('drag-over-highlight');
      }
    },

    // Optional: Method to handle global drag end
    // Call this when drag ends globally to remove highlights
    onGlobalDragEnd() {
      const dropZone = this.$refs.dropZone;
      if (dropZone) {
        dropZone.classList.remove('drag-over-highlight', 'drag-active', 'drop-success');
      }
    },

  }
};
</script>

<style scoped>
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.world-editor-room-info {
  background: #2d2d2d;
  border: 1px solid #555;
  border-radius: 4px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* Full Container Drop Zone */
.room-drop-zone {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  border-radius: 4px;
  pointer-events: none;
}

/* Drop Zone Overlay - Hidden by default */
.drop-zone-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(30, 144, 255, 0.25);
  border: 3px solid rgba(30, 144, 255, 0.7);
  box-shadow: 0 0 15px rgba(30, 144, 255, 0.5);
  border-radius: 4px;
  display: none; /* Hidden by default */
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

/* Show overlay when dragging over */
.room-drop-zone.drag-active .drop-zone-overlay {
  display: flex; /* Show when active */
}

/* Optional: Show overlay when any dragging is happening (lighter version) */
.room-drop-zone.drag-over-highlight .drop-zone-overlay {
  display: flex;
  background-color: rgba(30, 144, 255, 0.15);
  border: 2px solid rgba(30, 144, 255, 0.5);
  box-shadow: 0 0 10px rgba(30, 144, 255, 0.3);
  pointer-events: all;
}

/* Drop Zone Message */
.drop-zone-message {
  background-color: rgba(0, 0, 0, 0.8);
  border-radius: 8px;
  padding: 15px 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  transform: scale(0.95);
  transition: transform 0.3s ease;
}

.room-drop-zone.drag-active .drop-zone-message {
  transform: scale(1);
}

.drop-zone-icon {
  font-size: 2.5rem;
  color: #1E90FF;
}

.drop-zone-text {
  color: white;
  font-weight: bold;
  font-size: 1.1rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.7);
}

/* Visual feedback for successful drop */
.room-drop-zone.drop-success .drop-zone-overlay {
  display: flex;
  background-color: rgba(76, 175, 80, 0.25);
  border: 3px solid rgba(76, 175, 80, 0.7);
  box-shadow: 0 0 15px rgba(76, 175, 80, 0.5);
}

.room-drop-zone.drop-success .drop-zone-message {
  background-color: rgba(76, 175, 80, 0.9);
}

.room-drop-zone.drop-success .drop-zone-text {
  color: white;
}

.room-drop-zone.drop-success .drop-zone-icon {
  color: white;
}

.room-info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #333;
  border-bottom: 1px solid #555;
}

.room-info-header h3 {
  margin: 0;
  color: #1E90FF;
  font-size: 1.1rem;
  font-weight: 600;
}

.close-btn {
  padding: 0.25rem;
  background: transparent;
  color: #ccc;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #555;
  color: #fff;
}

.room-info-content {
  flex: 1;
  padding: 0.1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

/* Info Sections */
.info-section {
  background: #333;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 1rem;
}

.info-section h4 {
  margin: 0 0 0.75rem 0;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Basic Info Grid */
.info-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-item label {
  color: #ccc;
  font-size: 0.9rem;
  font-weight: 500;
}

.info-item span {
  color: #fff;
  font-size: 0.9rem;
}

.info-item select {
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.25rem;
  font-size: 0.9rem;
}

.info-item select:focus {
  outline: none;
  border-color: #1E90FF;
}

.info-item select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Labels */
.labels-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.label-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.label-input {
  flex: 1;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  font-size: 0.9rem;
}

.label-input:focus {
  outline: none;
  border-color: #1E90FF;
}

.label-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.remove-label-btn {
  padding: 0.25rem;
  background: #d32f2f;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.remove-label-btn:hover {
  background: #f44336;
}

.add-label-btn {
  padding: 0.5rem;
  background: #1E90FF;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
}

.add-label-btn:hover {
  background: #4FC3F7;
}

/* Entities */
.entities-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.entity-group {
  background: #444;
  border-radius: 4px;
  padding: 0.75rem;
}

.entity-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #fff;
}

.entity-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.entity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.25rem 0.5rem;
  background: #555;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.entity-item:hover {
  background-color: #666;
}

.entity-item:hover .entity-name {
  color: #1E90FF;
}

.entity-avatar {
  margin-right: 0.5rem;
}

.avatar-image {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #777;
}

.entity-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-right: 0.5rem;
}

.entity-name {
  color: #fff;
  font-size: 0.9rem;
}

.entity-status,
.entity-type,
.entity-rarity,
.entity-danger,
.entity-charges {
  color: #ccc;
  font-size: 0.8rem;
  font-style: italic;
}

.entity-charges {
  color: #88ccff;
}

.empty-entities {
  text-align: center;
  color: #aaa;
  font-style: italic;
  padding: 2rem;
}

/* Connections */
.connections-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.connection-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.connection-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: #444;
  border-radius: 4px;
}

.connection-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.connection-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.connection-direction {
  color: #fff;
  font-size: 0.9rem;
  font-weight: 500;
}

.connection-id {
  color: #aaa;
  font-size: 0.8rem;
  font-family: monospace;
}

.connection-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.connection-type {
  color: #ccc;
  font-size: 0.8rem;
}

.connection-status {
  font-size: 0.8rem;
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  background: #4CAF50;
  color: #fff;
}

.connection-status.locked {
  background: #FFC107;
  color: #333;
}

.connection-actions {
  display: flex;
  gap: 0.25rem;
}

.view-connection-btn {
  padding: 0.25rem;
  background: #1E90FF;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-connection-btn:hover {
  background: #4FC3F7;
}

.remove-connection-btn {
  padding: 0.25rem;
  background: #d32f2f;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.remove-connection-btn:hover {
  background: #f44336;
}

.empty-connections {
  text-align: center;
  color: #aaa;
  font-style: italic;
  padding: 1rem;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  padding: 0.75rem;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.action-btn:hover {
  background: #555;
  border-color: #666;
}

.action-btn.danger {
  background: #d32f2f;
  border-color: #d32f2f;
}

.action-btn.danger:hover {
  background: #f44336;
  border-color: #f44336;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #2d2d2d;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 2rem;
  max-width: 400px;
  width: 90%;
}

.modal-content h3 {
  margin: 0 0 1rem 0;
  color: #fff;
}

.modal-content p {
  margin: 0 0 1.5rem 0;
  color: #ccc;
  line-height: 1.4;
}

.modal-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.modal-btn {
  padding: 0.5rem 1rem;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-btn:hover {
  background: #555;
}

.modal-btn.danger {
  background: #d32f2f;
  border-color: #d32f2f;
}

.modal-btn.danger:hover {
  background: #f44336;
}

/* Scrollbar Styling */
.room-info-content::-webkit-scrollbar {
  width: 6px;
}

.room-info-content::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.room-info-content::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}

.room-info-content::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* Responsive Design */
@media (max-width: 768px) {
  .room-info-header {
    padding: 0.75rem;
  }

  .room-info-content {
    padding: 0.75rem;
    gap: 1rem;
  }

  .info-section {
    padding: 0.75rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .modal-content {
    padding: 1.5rem;
  }
}

/* Icon placeholders */
.icon-times::before {
  content: '✕';
}

.icon-plus::before {
  content: '+';
}

.icon-users::before {
  content: '👥';
}

.icon-user-friends::before {
  content: '👫';
}

.icon-cube::before {
  content: '📦';
}

.icon-exclamation-triangle::before {
  content: '⚠️';
}

.icon-unlink::before {
  content: '⛓';
}

.icon-info-circle::before {
  content: 'ℹ️';
}

.icon-copy::before {
  content: '📋';
}

.icon-trash::before {
  content: '🗑';
}
</style>
