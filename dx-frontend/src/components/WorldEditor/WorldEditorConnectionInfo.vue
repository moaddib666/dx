<template>
  <div class="connection-info-modal">
    <div class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Connection Information</h3>
          <button class="close-btn" @click="closeModal">×</button>
        </div>

        <div class="modal-body">
          <!-- Status -->
          <div class="section">
            <div class="status-row">
              <div class="status-item" :class="{ active: isActive }">
                {{ isActive ? 'Active' : 'Inactive' }}
              </div>
              <div class="status-item" :class="{ active: isPublic }">
                {{ isPublic ? 'Public' : 'Private' }}
              </div>
              <div class="status-item" :class="{ active: isLocked }">
                {{ isLocked ? 'Locked' : 'Unlocked' }}
              </div>
            </div>
          </div>

          <!-- Details -->
          <div class="section">
            <h4>Details</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <label>ID</label>
                <span>{{ connection.id }}</span>
              </div>
              <div class="detail-item">
                <label>Type</label>
                <select v-model="localConnection.type" @change="onConnectionUpdated" :disabled="isLoading">
                  <option value="normal">Normal</option>
                  <option value="locked">Locked</option>
                  <option value="hidden">Hidden</option>
                  <option value="special">Special</option>
                </select>
              </div>
              <div class="detail-item">
                <label>Direction</label>
                <span>{{ connectionDirection }}</span>
              </div>
              <div class="detail-item">
                <label>Orientation</label>
                <span>{{ connection.isVertical ? 'Vertical' : 'Horizontal' }}</span>
              </div>
            </div>
            <div class="admin-link">
              <EditInDjangoAdmin
                  :id="connection.id"
                  app="world"
                  model="positionconnection"
              />
            </div>
          </div>

          <!-- Rooms -->
          <div class="section">
            <h4>Connected Rooms</h4>
            <div class="rooms-grid">
              <div class="room">
                <div class="room-header">
                  <span class="room-label">Source</span>
                </div>
                <div v-if="sourceRoom" class="room-info">
                  <div class="room-field">
                    <label>ID:</label>
                    <span>{{ sourceRoom.id }}</span>
                  </div>
                  <div class="room-field">
                    <label>Position:</label>
                    <span>({{ sourceRoom.position.grid_x }}, {{ sourceRoom.position.grid_y }}, {{ sourceRoom.position.grid_z }})</span>
                  </div>
                  <div class="room-field">
                    <label>Name:</label>
                    <span>{{ sourceRoom.getDisplayName() }}</span>
                  </div>
                  <button class="view-btn" @click="viewRoom(sourceRoom.id)">View</button>
                </div>
                <div v-else class="room-error">Room not found</div>
              </div>

              <div class="room">
                <div class="room-header">
                  <span class="room-label">Target</span>
                </div>
                <div v-if="targetRoom" class="room-info">
                  <div class="room-field">
                    <label>ID:</label>
                    <span>{{ targetRoom.id }}</span>
                  </div>
                  <div class="room-field">
                    <label>Position:</label>
                    <span>({{ targetRoom.position.grid_x }}, {{ targetRoom.position.grid_y }}, {{ targetRoom.position.grid_z }})</span>
                  </div>
                  <div class="room-field">
                    <label>Name:</label>
                    <span>{{ targetRoom.getDisplayName() }}</span>
                  </div>
                  <button class="view-btn" @click="viewRoom(targetRoom.id)">View</button>
                </div>
                <div v-else class="room-error">Room not found</div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="section">
            <h4>Actions</h4>
            <div class="actions-grid">
              <button class="action-btn" :class="{ active: isActive }" @click="toggleActive" :disabled="isLoading">
                {{ isActive ? 'Deactivate' : 'Activate' }}
              </button>
              <button class="action-btn" :class="{ active: isPublic }" @click="togglePublic" :disabled="isLoading">
                {{ isPublic ? 'Make Private' : 'Make Public' }}
              </button>
              <button class="action-btn" :class="{ active: isLocked }" @click="toggleLock" :disabled="isLoading">
                {{ isLocked ? 'Unlock' : 'Lock' }}
              </button>
              <button class="action-btn secondary" @click="configureConnection" :disabled="isLoading">
                Configure
              </button>
              <button class="action-btn danger" @click="confirmDelete" :disabled="isLoading">
                Delete
              </button>
            </div>
          </div>

          <!-- Error -->
          <div v-if="errorMessage" class="error">
            {{ errorMessage }}
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click="cancelDelete">
      <div class="modal-content small" @click.stop>
        <div class="modal-header">
          <h3>Confirm Delete</h3>
        </div>
        <div class="modal-body">
          <p>Delete this connection? This cannot be undone.</p>
          <div class="button-row">
            <button class="btn" @click="cancelDelete">Cancel</button>
            <button class="btn danger" @click="deleteConnection" :disabled="isLoading">
              {{ isLoading ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Configuration -->
    <div v-if="showConfigModal" class="modal-overlay" @click="cancelConfiguration">
      <div class="modal-content medium" @click.stop>
        <div class="modal-header">
          <h3>Configure Requirements</h3>
          <button class="close-btn" @click="cancelConfiguration">×</button>
        </div>
        <div class="modal-body">
          <div class="requirements">
            <div v-for="(requirement, index) in configData.requirements" :key="index" class="requirement">
              <div class="requirement-header">
                <span>Requirement {{ index + 1 }}</span>
                <button class="remove-btn" @click="removeRequirement(index)">×</button>
              </div>

              <div class="requirement-fields">
                <div class="field">
                  <label>Item</label>
                  <input type="text" v-model="itemSearchText" placeholder="Search items..." @input="searchItems" />
                  <select v-model="requirement.item_id">
                    <option value="">None</option>
                    <option v-for="item in filteredItems" :key="item.id" :value="item.id">
                      {{ item.name || item.id }}
                    </option>
                  </select>
                </div>

                <div class="field">
                  <label>Character</label>
                  <input type="text" v-model="characterSearchText" placeholder="Search characters..." @input="searchCharacters" />
                  <select v-model="requirement.character_id">
                    <option value="">None</option>
                    <option v-for="character in filteredCharacters" :key="character.id" :value="character.id">
                      {{ character.name || character.id }}
                    </option>
                  </select>
                </div>

                <div class="field">
                  <label>Skill</label>
                  <input type="text" v-model="skillSearchText" placeholder="Search skills..." @input="searchSkills" />
                  <select v-model="requirement.skill_id">
                    <option value="">None</option>
                    <option v-for="skill in filteredSkills" :key="skill.id" :value="skill.id">
                      {{ skill.name || skill.id }}
                    </option>
                  </select>
                </div>
              </div>
            </div>

            <button class="add-btn" @click="addRequirement">+ Add Requirement</button>
          </div>

          <div v-if="errorMessage" class="error">
            {{ errorMessage }}
          </div>

          <div class="button-row">
            <button class="btn" @click="cancelConfiguration">Cancel</button>
            <button class="btn primary" @click="saveConfiguration" :disabled="isLoading">
              {{ isLoading ? 'Saving...' : 'Save' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="isLoading && !showConfigModal && !showDeleteConfirm" class="loading">
      <div class="spinner"></div>
    </div>
  </div>
</template>

<script>
import EditInDjangoAdmin from '@/components/EditInDjangoAdmin.vue';
import { worldMapEditorService } from '@/services/WorldMapEditorService.js';
import WorldItemsGameMasterService from '@/services/worldItemsService.js';
import { gameMasterCharacterService } from '@/services/GameMasterCharacterService.js';
import defaultSkillServiceInstance from '@/services/skillService';

export default {
  name: 'WorldEditorConnectionInfo',
  components: {
    EditInDjangoAdmin
  },
  props: {
    connection: {
      type: Object,
      required: true
    },
    editorState: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localConnection: null,
      showDeleteConfirm: false,
      showConfigModal: false,
      configData: {
        requirements: []
      },
      itemSearchText: '',
      characterSearchText: '',
      skillSearchText: '',
      items: [],
      characters: [],
      skills: [],
      filteredItems: [],
      filteredCharacters: [],
      filteredSkills: [],
      isLoading: false,
      errorMessage: ''
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

      if (this.connection.isVertical) {
        const sourceZ = this.sourceRoom.position.grid_z;
        const targetZ = this.targetRoom.position.grid_z;
        return sourceZ < targetZ ? 'Up' : 'Down';
      }

      const sourceX = this.sourceRoom.position.grid_x;
      const sourceY = this.sourceRoom.position.grid_y;
      const targetX = this.targetRoom.position.grid_x;
      const targetY = this.targetRoom.position.grid_y;

      if (sourceX < targetX) return 'East';
      if (sourceX > targetX) return 'West';
      if (sourceY < targetY) return 'South';
      if (sourceY > targetY) return 'North';

      return 'Unknown';
    },
    isLocked() {
      return this.localConnection?.type === 'locked';
    },
    isActive() {
      return this.localConnection?.is_active === true;
    },
    isPublic() {
      return this.localConnection?.is_public === true;
    }
  },
  mounted() {
    this.initializeSearchData();
  },
  watch: {
    connection: {
      handler(newConnection) {
        if (!newConnection) {
          this.localConnection = { metadata: {} };
          return;
        }
        try {
          this.localConnection = JSON.parse(JSON.stringify(newConnection));
          if (!this.localConnection.metadata) {
            this.localConnection.metadata = {};
          }
        } catch (error) {
          console.error('Error initializing localConnection:', error);
          this.localConnection = { metadata: {} };
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

    async initializeSearchData() {
      await Promise.all([
        this.searchItems(),
        this.searchCharacters(),
        this.searchSkills()
      ]);
    },

    addRequirement() {
      this.configData.requirements.push({
        item_id: null,
        character_id: null,
        skill_id: null
      });
    },

    removeRequirement(index) {
      this.configData.requirements.splice(index, 1);
    },

    async searchItems() {
      if (!this.items.length) {
        try {
          this.items = [
            { id: 'item1', name: 'Sword' },
            { id: 'item2', name: 'Shield' },
            { id: 'item3', name: 'Potion' }
          ];
        } catch (error) {
          console.error('Error fetching items:', error);
        }
      }

      this.filteredItems = this.itemSearchText
          ? this.items.filter(item =>
              item.name.toLowerCase().includes(this.itemSearchText.toLowerCase()) ||
              item.id.toLowerCase().includes(this.itemSearchText.toLowerCase())
          )
          : this.items;
    },

    async searchCharacters() {
      if (!this.characters.length) {
        try {
          this.characters = [
            { id: 'char1', name: 'Warrior' },
            { id: 'char2', name: 'Mage' },
            { id: 'char3', name: 'Rogue' }
          ];
        } catch (error) {
          console.error('Error fetching characters:', error);
        }
      }

      this.filteredCharacters = this.characterSearchText
          ? this.characters.filter(character =>
              character.name.toLowerCase().includes(this.characterSearchText.toLowerCase()) ||
              character.id.toLowerCase().includes(this.characterSearchText.toLowerCase())
          )
          : this.characters;
    },

    async searchSkills() {
      if (!this.skills.length) {
        try {
          await defaultSkillServiceInstance.updateCache();
          this.skills = [
            { id: 'skill1', name: 'Fireball' },
            { id: 'skill2', name: 'Healing' },
            { id: 'skill3', name: 'Stealth' }
          ];
        } catch (error) {
          console.error('Error fetching skills:', error);
        }
      }

      this.filteredSkills = this.skillSearchText
          ? this.skills.filter(skill =>
              skill.name.toLowerCase().includes(this.skillSearchText.toLowerCase()) ||
              skill.id.toLowerCase().includes(this.skillSearchText.toLowerCase())
          )
          : this.skills;
    },

    async onConnectionUpdated() {
      if (!this.connection?.id) {
        console.error('Cannot update connection: connection or connection.id is undefined');
        return;
      }

      try {
        this.isLoading = true;
        this.errorMessage = '';

        const updatedData = {
          type: this.localConnection.type,
          metadata: this.localConnection.metadata
        };

        await worldMapEditorService.updatePositionConnection(this.connection.id, updatedData);
        this.$emit('connection-updated', this.connection.id, updatedData);
      } catch (error) {
        console.error('Error updating connection:', error);
        this.errorMessage = 'Failed to update connection. Please try again.';
      } finally {
        this.isLoading = false;
      }
    },

    async toggleLock() {
      try {
        this.isLoading = true;
        this.errorMessage = '';

        if (this.isLocked) {
          await worldMapEditorService.unlockPositionConnection(this.connection.id);
          this.localConnection.type = 'normal';
        } else {
          await worldMapEditorService.lockPositionConnection(this.connection.id);
          this.localConnection.type = 'locked';
        }

        this.$emit('connection-updated', this.connection.id, {
          type: this.localConnection.type
        });
      } catch (error) {
        console.error('Error toggling lock state:', error);
        this.errorMessage = 'Failed to change lock state. Please try again.';
      } finally {
        this.isLoading = false;
      }
    },

    async toggleActive() {
      try {
        this.isLoading = true;
        this.errorMessage = '';

        if (this.isActive) {
          await worldMapEditorService.deactivatePositionConnection(this.connection.id);
          this.localConnection.is_active = false;
        } else {
          await worldMapEditorService.activatePositionConnection(this.connection.id);
          this.localConnection.is_active = true;
        }

        this.$emit('connection-updated', this.connection.id, {
          is_active: this.localConnection.is_active
        });
      } catch (error) {
        console.error('Error toggling active state:', error);
        this.errorMessage = 'Failed to change active state. Please try again.';
      } finally {
        this.isLoading = false;
      }
    },

    async togglePublic() {
      try {
        this.isLoading = true;
        this.errorMessage = '';

        if (this.isPublic) {
          await worldMapEditorService.setPositionConnectionPrivate(this.connection.id);
          this.localConnection.is_public = false;
        } else {
          await worldMapEditorService.setPositionConnectionPublic(this.connection.id);
          this.localConnection.is_public = true;
        }

        this.$emit('connection-updated', this.connection.id, {
          is_public: this.localConnection.is_public
        });
      } catch (error) {
        console.error('Error toggling public state:', error);
        this.errorMessage = 'Failed to change public state. Please try again.';
      } finally {
        this.isLoading = false;
      }
    },

    configureConnection() {
      this.configData = {
        requirements: this.localConnection.requirements || []
      };

      if (!this.configData.requirements.length) {
        this.addRequirement();
      }

      this.initializeSearchData();
      this.showConfigModal = true;
    },

    async saveConfiguration() {
      try {
        this.isLoading = true;
        this.errorMessage = '';

        const validRequirements = this.configData.requirements.filter(req =>
            req.item_id || req.character_id || req.skill_id
        );

        if (validRequirements.length === 0) {
          this.errorMessage = 'At least one requirement must have an item, character, or skill selected.';
          this.isLoading = false;
          return;
        }

        this.configData.requirements = validRequirements;

        await worldMapEditorService.configurePositionConnection(this.connection.id, this.configData);

        this.localConnection = {
          ...this.localConnection,
          requirements: [...this.configData.requirements]
        };

        this.$emit('connection-updated', this.connection.id, this.configData);
        this.showConfigModal = false;
      } catch (error) {
        console.error('Error configuring connection:', error);
        this.errorMessage = 'Failed to configure connection. Please try again.';
      } finally {
        this.isLoading = false;
      }
    },

    cancelConfiguration() {
      this.showConfigModal = false;
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

    async deleteConnection() {
      this.showDeleteConfirm = false;
      if (!this.connection?.id) {
        console.error('Cannot delete connection: connection or connection.id is undefined');
        this.closeModal();
        return;
      }

      try {
        this.isLoading = true;
        this.errorMessage = '';

        await worldMapEditorService.deletePositionConnection(this.connection.id);
        this.$emit('connection-deleted', this.connection.id);
        this.closeModal();
      } catch (error) {
        console.error('Error deleting connection:', error);
        this.errorMessage = 'Failed to delete connection. Please try again.';
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Base */
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
  background: rgba(0, 0, 0, 0.5);
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
}

.modal-content.small {
  max-width: 400px;
}

.modal-content.medium {
  max-width: 600px;
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
  color: #fff;
  font-size: 1rem;
  font-weight: 500;
}

.close-btn {
  background: none;
  border: none;
  color: #ccc;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #fff;
}

.modal-body {
  padding: 1rem;
}

/* Sections */
.section {
  margin-bottom: 1.5rem;
}

.section:last-child {
  margin-bottom: 0;
}

.section h4 {
  margin: 0 0 0.75rem 0;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 500;
  border-bottom: 1px solid #555;
  padding-bottom: 0.5rem;
}

/* Status */
.status-row {
  display: flex;
  gap: 1rem;
}

.status-item {
  flex: 1;
  padding: 0.5rem;
  background: #444;
  border: 1px solid #555;
  border-radius: 4px;
  text-align: center;
  color: #ccc;
  font-size: 0.85rem;
}

.status-item.active {
  background: #1E90FF;
  border-color: #1E90FF;
  color: #fff;
}

/* Details */
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item label {
  color: #aaa;
  font-size: 0.8rem;
  font-weight: 500;
}

.detail-item span {
  color: #fff;
  font-size: 0.9rem;
}

.detail-item select {
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.5rem;
  font-size: 0.9rem;
}

.detail-item select:focus {
  outline: none;
  border-color: #1E90FF;
}

.admin-link {
  padding-top: 0.5rem;
  border-top: 1px solid #444;
}

/* Rooms */
.rooms-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.room {
  background: #444;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 1rem;
}

.room-header {
  margin-bottom: 0.75rem;
}

.room-label {
  color: #1E90FF;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
}

.room-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.room-field {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
}

.room-field label {
  color: #aaa;
  font-size: 0.8rem;
  min-width: 60px;
}

.room-field span {
  color: #fff;
  font-size: 0.8rem;
  text-align: right;
  word-break: break-all;
}

.view-btn {
  margin-top: 0.5rem;
  padding: 0.4rem 0.8rem;
  background: #1E90FF;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.view-btn:hover {
  background: #4FC3F7;
}

.room-error {
  color: #f44336;
  font-size: 0.8rem;
  font-style: italic;
}

/* Actions */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.5rem;
}

.action-btn {
  padding: 0.6rem;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}

.action-btn:hover {
  background: #555;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.active {
  background: #1E90FF;
  border-color: #1E90FF;
}

.action-btn.secondary {
  background: #666;
  border-color: #777;
}

.action-btn.danger {
  background: #d32f2f;
  border-color: #d32f2f;
}

.action-btn.danger:hover {
  background: #f44336;
}

/* Error */
.error {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid #f44336;
  border-radius: 4px;
  padding: 0.75rem;
  color: #f44336;
  font-size: 0.85rem;
}

/* Buttons */
.button-row {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn {
  padding: 0.6rem 1rem;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}

.btn:hover {
  background: #555;
}

.btn.primary {
  background: #1E90FF;
  border-color: #1E90FF;
}

.btn.primary:hover {
  background: #4FC3F7;
}

.btn.danger {
  background: #d32f2f;
  border-color: #d32f2f;
}

.btn.danger:hover {
  background: #f44336;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Requirements */
.requirements {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.requirement {
  background: #444;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 1rem;
}

.requirement-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.requirement-header span {
  color: #fff;
  font-size: 0.85rem;
  font-weight: 500;
}

.remove-btn {
  background: none;
  border: none;
  color: #f44336;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-btn:hover {
  color: #ff6b6b;
}

.requirement-fields {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.field label {
  color: #aaa;
  font-size: 0.8rem;
  font-weight: 500;
}

.field input,
.field select {
  background: #555;
  color: #fff;
  border: 1px solid #666;
  border-radius: 4px;
  padding: 0.4rem;
  font-size: 0.85rem;
}

.field input:focus,
.field select:focus {
  outline: none;
  border-color: #1E90FF;
}

.add-btn {
  padding: 0.75rem;
  background: #1E90FF;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}

.add-btn:hover {
  background: #4FC3F7;
}

/* Loading */
.loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1002;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
  }

  .status-row {
    flex-direction: column;
    gap: 0.5rem;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }

  .rooms-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .requirement-fields {
    gap: 0.5rem;
  }

  .button-row {
    flex-direction: column;
  }
}
</style>