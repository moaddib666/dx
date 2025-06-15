<template>
  <div class="connection-info-modal">
    <div class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Connection Information</h3>
          <button class="close-btn" title="Close" @click="closeModal">
            <i class="icon-times"></i>
          </button>
        </div>

        <div class="modal-body">
          <!-- Basic Connection Info -->
          <div class="info-section">
            <h4>Basic Information</h4>
            <div class="info-grid">
              <div class="info-item">
                <label>Connection ID:</label>
                <span>{{ connection.id }}</span>
              </div>
              <div class="info-item">
                <label>Type:</label>
                <select v-model="localConnection.type" :disabled="!editable" @change="onConnectionUpdated">
                  <option value="normal">Normal</option>
                  <option value="locked">Locked</option>
                  <option value="hidden">Hidden</option>
                  <option value="special">Special</option>
                </select>
              </div>
              <div class="info-item">
                <label>Direction:</label>
                <span>{{ connectionDirection }}</span>
              </div>
              <div class="info-item">
                <label>Orientation:</label>
                <span>{{ connection.isVertical ? 'Vertical' : 'Horizontal' }}</span>
              </div>
            </div>
          </div>

          <!-- Connected Rooms -->
          <div class="info-section">
            <h4>Connected Rooms</h4>
            <div class="rooms-container">
              <div class="room-info">
                <h5>Source Room</h5>
                <div v-if="sourceRoom" class="room-details">
                  <div class="room-id">ID: {{ sourceRoom.id }}</div>
                  <div class="room-position">
                    Position: ({{ sourceRoom.position.grid_x }}, {{ sourceRoom.position.grid_y }},
                    {{ sourceRoom.position.grid_z }})
                  </div>
                  <div class="room-name">
                    Name: {{ sourceRoom.getDisplayName() }}
                  </div>
                  <button class="view-room-btn" @click="viewRoom(sourceRoom.id)">
                    View Room
                  </button>
                </div>
                <div v-else class="room-not-found">
                  Source room not found
                </div>
              </div>

              <div class="connection-arrow">
                <i class="icon-arrow-right"></i>
              </div>

              <div class="room-info">
                <h5>Target Room</h5>
                <div v-if="targetRoom" class="room-details">
                  <div class="room-id">ID: {{ targetRoom.id }}</div>
                  <div class="room-position">
                    Position: ({{ targetRoom.position.grid_x }}, {{ targetRoom.position.grid_y }},
                    {{ targetRoom.position.grid_z }})
                  </div>
                  <div class="room-name">
                    Name: {{ targetRoom.getDisplayName() }}
                  </div>
                  <button class="view-room-btn" @click="viewRoom(targetRoom.id)">
                    View Room
                  </button>
                </div>
                <div v-else class="room-not-found">
                  Target room not found
                </div>
              </div>
            </div>
          </div>

          <!-- Connection Parameters -->
          <div class="info-section">
            <h4>Parameters</h4>
            <div class="parameters-container">
              <div class="parameter-list">
                <div v-for="(value, key) in localConnection.metadata" :key="key" class="parameter-item">
                  <div class="parameter-name">
                    <input
                        v-model="parameterKeys[key]"
                        :disabled="!editable"
                        placeholder="Parameter name"
                        @blur="updateParameterKey(key)"
                    />
                  </div>
                  <div class="parameter-value">
                    <input
                        v-model="localConnection.metadata[key]"
                        :disabled="!editable"
                        placeholder="Parameter value"
                        @blur="onConnectionUpdated"
                    />
                  </div>
                  <button
                      v-if="editable"
                      class="remove-parameter-btn"
                      title="Remove parameter"
                      @click="removeParameter(key)"
                  >
                    <i class="icon-times"></i>
                  </button>
                </div>
              </div>
              <button
                  v-if="editable"
                  class="add-parameter-btn"
                  @click="addParameter"
              >
                <i class="icon-plus"></i> Add Parameter
              </button>
            </div>
          </div>

          <!-- Connection Actions -->
          <div v-if="editable" class="info-section">
            <h4>Actions</h4>
            <div class="action-buttons">
              <button
                  class="action-btn"
                  @click="toggleLock"
              >
                <i :class="isLocked ? 'icon-unlock' : 'icon-lock'"></i>
                {{ isLocked ? 'Unlock Connection' : 'Lock Connection' }}
              </button>
              <button
                  class="action-btn danger"
                  @click="confirmDelete"
              >
                <i class="icon-trash"></i> Delete Connection
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="modal-overlay confirmation-modal" @click="cancelDelete">
      <div class="modal-content" @click.stop>
        <h3>Confirm Delete</h3>
        <p>Are you sure you want to delete this connection? This action cannot be undone.</p>
        <div class="modal-actions">
          <button class="modal-btn" @click="cancelDelete">Cancel</button>
          <button class="modal-btn danger" @click="deleteConnection">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WorldEditorConnectionInfo',
  props: {
    connection: {
      type: Object,
      required: true
    },
    editorState: {
      type: Object,
      required: true
    },
    editable: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      localConnection: null,
      parameterKeys: {},
      showDeleteConfirm: false
    };
  },
  computed: {
    sourceRoom() {
      return this.editorState.rooms.get(this.connection.fromRoomId || this.connection.sourceRoomId);
    },
    targetRoom() {
      return this.editorState.rooms.get(this.connection.toRoomId || this.connection.targetRoomId);
    },
    connectionDirection() {
      if (!this.sourceRoom || !this.targetRoom) {
        return 'Unknown';
      }

      // If it's a vertical connection
      if (this.connection.isVertical) {
        // Compare z positions to determine if it's up or down
        const sourceZ = this.sourceRoom.position.grid_z;
        const targetZ = this.targetRoom.position.grid_z;

        // In the connection info modal, we always show the direction from source to target
        // If source room is on a lower floor than target room, the direction is Up
        // If source room is on a higher floor than target room, the direction is Down
        return sourceZ < targetZ ? 'Up' : 'Down';
      }

      // For horizontal connections, compare x and y positions
      const sourceX = this.sourceRoom.position.grid_x;
      const sourceY = this.sourceRoom.position.grid_y;
      const targetX = this.targetRoom.position.grid_x;
      const targetY = this.targetRoom.position.grid_y;

      // Determine the direction
      if (sourceX < targetX) return 'East';
      if (sourceX > targetX) return 'West';
      if (sourceY < targetY) return 'South';
      if (sourceY > targetY) return 'North';

      return 'Unknown';
    },
    isLocked() {
      return this.localConnection?.type === 'locked';
    }
  },
  watch: {
    connection: {
      handler(newConnection) {
        if (!newConnection) {
          console.error('Connection is undefined or null');
          this.localConnection = {metadata: {}};
          this.parameterKeys = {};
          return;
        }
        try {
          this.localConnection = JSON.parse(JSON.stringify(newConnection));
          // Ensure metadata is always an object
          if (!this.localConnection.metadata) {
            this.localConnection.metadata = {};
          }
          // Initialize parameter keys
          this.parameterKeys = {};
          Object.keys(this.localConnection.metadata).forEach(key => {
            this.parameterKeys[key] = key;
          });
        } catch (error) {
          console.error('Error initializing localConnection:', error);
          this.localConnection = {metadata: {}};
          this.parameterKeys = {};
        }
      },
      immediate: true,
      deep: true
    }
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },

    onConnectionUpdated() {
      if (!this.connection || !this.connection.id) {
        console.error('Cannot update connection: connection or connection.id is undefined');
        return;
      }
      this.$emit('connection-updated', this.connection.id, {
        type: this.localConnection.type,
        metadata: this.localConnection.metadata
      });
    },

    addParameter() {
      const newKey = `param_${Date.now()}`;
      this.$set(this.localConnection.metadata, newKey, '');
      this.$set(this.parameterKeys, newKey, '');
    },

    updateParameterKey(oldKey) {
      const newKey = this.parameterKeys[oldKey];
      if (newKey !== oldKey && newKey.trim() !== '') {
        const value = this.localConnection.metadata[oldKey];
        this.$delete(this.localConnection.metadata, oldKey);
        this.$set(this.localConnection.metadata, newKey, value);
        this.$delete(this.parameterKeys, oldKey);
        this.$set(this.parameterKeys, newKey, newKey);
        this.onConnectionUpdated();
      }
    },

    removeParameter(key) {
      this.$delete(this.localConnection.metadata, key);
      this.$delete(this.parameterKeys, key);
      this.onConnectionUpdated();
    },

    toggleLock() {
      this.localConnection.type = this.isLocked ? 'normal' : 'locked';
      this.onConnectionUpdated();
    },

    viewRoom(roomId) {
      this.$emit('view-room', roomId);
    },

    confirmDelete() {
      this.showDeleteConfirm = true;
    },

    cancelDelete() {
      this.showDeleteConfirm = false;
    },

    deleteConnection() {
      this.showDeleteConfirm = false;
      if (!this.connection || !this.connection.id) {
        console.error('Cannot delete connection: connection or connection.id is undefined');
        this.closeModal();
        return;
      }
      this.$emit('connection-deleted', this.connection.id);
      this.closeModal();
    }
  }
};
</script>

<style scoped>
.connection-info-modal {
  position: relative;
  z-index: 1000;
}

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
  width: 90%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #333;
  border-bottom: 1px solid #555;
}

.modal-header h3 {
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

.modal-body {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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

/* Connected Rooms */
.rooms-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.room-info {
  flex: 1;
  background: #444;
  border-radius: 4px;
  padding: 0.75rem;
}

.room-info h5 {
  margin: 0 0 0.5rem 0;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 500;
}

.room-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.room-id, .room-position, .room-name {
  color: #ccc;
  font-size: 0.85rem;
}

.view-room-btn {
  margin-top: 0.5rem;
  padding: 0.25rem 0.5rem;
  background: #1E90FF;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.85rem;
}

.view-room-btn:hover {
  background: #4FC3F7;
}

.room-not-found {
  color: #f44336;
  font-style: italic;
  font-size: 0.85rem;
}

.connection-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
  font-size: 1.5rem;
}

/* Parameters */
.parameters-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.parameter-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.parameter-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.parameter-name, .parameter-value {
  flex: 1;
}

.parameter-name input, .parameter-value input {
  width: 100%;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  font-size: 0.9rem;
}

.parameter-name input:focus, .parameter-value input:focus {
  outline: none;
  border-color: #1E90FF;
}

.parameter-name input:disabled, .parameter-value input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.remove-parameter-btn {
  padding: 0.25rem;
  background: #d32f2f;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.remove-parameter-btn:hover {
  background: #f44336;
}

.add-parameter-btn {
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

.add-parameter-btn:hover {
  background: #4FC3F7;
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

/* Delete Confirmation Modal */
.confirmation-modal {
  z-index: 1001;
}

.modal-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 1rem;
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

/* Icon placeholders */
.icon-times::before {
  content: '✕';
}

.icon-plus::before {
  content: '+';
}

.icon-arrow-right::before {
  content: '→';
}

.icon-lock::before {
  content: '🔒';
}

.icon-unlock::before {
  content: '🔓';
}

.icon-trash::before {
  content: '🗑';
}

/* Responsive Design */
@media (max-width: 768px) {
  .rooms-container {
    flex-direction: column;
  }

  .connection-arrow {
    transform: rotate(90deg);
    margin: 0.5rem 0;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>
