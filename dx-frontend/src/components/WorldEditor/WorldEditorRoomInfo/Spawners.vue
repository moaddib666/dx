<template>
  <div class="info-section">
    <h4>Spawners</h4>
    <div class="spawners-container">
      <!-- Spawners -->
      <div v-if="roomSpawners.length > 0" class="entity-group">
        <div class="entity-header">
          <i class="icon-spawn" style="color: #8800ff;"></i>
          <span>NPC Spawners ({{ roomSpawners.length }})</span>
        </div>
        <div class="entity-list">
          <div
              v-for="spawner in roomSpawners"
              :key="spawner.id"
              class="entity-item spawner-item"
              :class="{ 'inactive': !spawner.is_active }"
          >
            <div class="entity-avatar">
              <div class="spawner-icon" :class="{ 'active': spawner.is_active }">
                <i class="icon-spawn"></i>
              </div>
            </div>
            <div class="entity-info">
              <span class="entity-name">{{ getSpawnerName(spawner) }}</span>
              <div class="entity-details">
                <span class="spawner-status" :class="{ 'active': spawner.is_active }">
                  {{ spawner.is_active ? 'Active' : 'Inactive' }}
                </span>
                <span class="spawner-limit">Limit: {{ spawner.spawn_limit || 1 }}</span>
                <span class="spawner-cycles">Respawn: {{ spawner.respawn_cycles || 1 }} cycles</span>
              </div>
            </div>
            <div class="entity-actions">
              <!-- Toggle Active/Inactive -->
              <button
                  class="action-btn toggle-btn"
                  :class="{ 'active': spawner.is_active }"
                  :title="spawner.is_active ? 'Deactivate Spawner' : 'Activate Spawner'"
                  @click="toggleSpawnerStatus(spawner)"
              >
                <i :class="spawner.is_active ? 'icon-pause' : 'icon-play'"></i>
              </button>
              <!-- Edit/Setup Spawner -->
              <button
                  class="action-btn edit-btn"
                  title="Edit Spawner"
                  @click="editSpawner(spawner)"
              >
                <i class="icon-edit"></i>
              </button>
              <!-- Delete Spawner -->
              <button
                  class="action-btn delete-btn"
                  title="Delete Spawner"
                  @click="deleteSpawner(spawner)"
              >
                <i class="icon-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- No Spawners Message -->
      <div v-else class="no-entities">
        <div class="no-entities-content">
          <i class="icon-spawn no-entities-icon"></i>
          <p class="no-entities-text">No spawners in this room</p>
          <button
              v-if="editable"
              class="create-spawner-btn"
              @click="createSpawner"
          >
            <i class="icon-plus"></i>
            Create Spawner
          </button>
        </div>
      </div>

      <!-- Create Spawner Button (when spawners exist) -->
      <div v-if="editable && roomSpawners.length > 0" class="spawner-actions">
        <button
            class="create-spawner-btn"
            @click="createSpawner"
        >
          <i class="icon-plus"></i>
          Create New Spawner
        </button>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="spawnerToDelete" class="modal-overlay" @click="cancelDelete">
      <div class="modal-content" @click.stop>
        <h3>Confirm Delete</h3>
        <p>Are you sure you want to delete this spawner? This action cannot be undone.</p>
        <div class="modal-actions">
          <button class="modal-btn" @click="cancelDelete">Cancel</button>
          <button class="modal-btn danger" @click="confirmDelete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { GMWorldNPCSpawnersApi } from '@/api/backendService.js';

export default {
  name: 'Spawners',
  props: {
    room: {
      type: Object,
      required: true
    },
    spawners: {
      type: Array,
      default: () => []
    },
    editable: {
      type: Boolean,
      default: false
    }
  },
  emits: [
    'spawner-created',
    'spawner-updated',
    'spawner-deleted',
    'spawner-edit',
    'spawner-create'
  ],
  data() {
    return {
      spawnerToDelete: null,
      isUpdating: false
    };
  },
  computed: {
    roomSpawners() {
      return this.spawners.filter(spawner => spawner.position_id === this.room.id);
    }
  },
  methods: {
    getSpawnerName(spawner) {
      // Try to get character template name if available
      if (spawner.character_template_name) {
        return `${spawner.character_template_name} Spawner`;
      }
      return `Spawner #${spawner.id}`;
    },

    async toggleSpawnerStatus(spawner) {
      if (this.isUpdating) return;

      try {
        this.isUpdating = true;
        const newStatus = !spawner.is_active;

        // Update spawner status via API
        const updateData = {
          ...spawner,
          is_active: newStatus
        };

        await GMWorldNPCSpawnersApi.gamemasterSpawnersNpcPartialUpdate(spawner.id, updateData);

        // Update local spawner object
        spawner.is_active = newStatus;

        this.$emit('spawner-updated', spawner.id);
      } catch (error) {
        console.error('Failed to toggle spawner status:', error);
        // You might want to show a toast notification here
      } finally {
        this.isUpdating = false;
      }
    },

    editSpawner(spawner) {
      this.$emit('spawner-edit', spawner);
    },

    createSpawner() {
      this.$emit('spawner-create', { id: this.room.id });
    },

    deleteSpawner(spawner) {
      this.spawnerToDelete = spawner;
    },

    async confirmDelete() {
      if (!this.spawnerToDelete) return;

      try {
        await GMWorldNPCSpawnersApi.gamemasterSpawnersNpcDestroy(this.spawnerToDelete.id);
        this.$emit('spawner-deleted', this.spawnerToDelete.id);
        this.spawnerToDelete = null;
      } catch (error) {
        console.error('Failed to delete spawner:', error);
        // You might want to show a toast notification here
      }
    },

    cancelDelete() {
      this.spawnerToDelete = null;
    }
  }
};
</script>

<style scoped>
.info-section {
  margin-bottom: 1rem;
}

.info-section h4 {
  margin: 0 0 0.5rem 0;
  color: #1E90FF;
  font-size: 1rem;
  font-weight: 600;
}

.spawners-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.entity-group {
  background: #333;
  border-radius: 6px;
  overflow: hidden;
}

.entity-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #2a2a2a;
  border-bottom: 1px solid #444;
  font-weight: 500;
  color: #ccc;
}

.entity-list {
  display: flex;
  flex-direction: column;
}

.entity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-bottom: 1px solid #444;
  transition: background-color 0.2s ease;
}

.entity-item:last-child {
  border-bottom: none;
}

.entity-item:hover {
  background: #3a3a3a;
}

.spawner-item.inactive {
  opacity: 0.6;
}

.entity-avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.spawner-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #555;
  color: #8800ff;
  font-size: 16px;
  transition: all 0.2s ease;
}

.spawner-icon.active {
  background: #8800ff;
  color: white;
}

.entity-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.entity-name {
  font-weight: 500;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.entity-details {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.spawner-status {
  font-size: 0.8rem;
  padding: 0.125rem 0.375rem;
  border-radius: 3px;
  background: #555;
  color: #ccc;
}

.spawner-status.active {
  background: #28a745;
  color: white;
}

.spawner-limit,
.spawner-cycles {
  font-size: 0.8rem;
  color: #aaa;
}

.entity-actions {
  display: flex;
  gap: 0.25rem;
  flex-shrink: 0;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
}

.toggle-btn {
  background: #555;
  color: #ccc;
}

.toggle-btn:hover {
  background: #666;
}

.toggle-btn.active {
  background: #28a745;
  color: white;
}

.edit-btn {
  background: #007bff;
  color: white;
}

.edit-btn:hover {
  background: #0056b3;
}

.delete-btn {
  background: #dc3545;
  color: white;
}

.delete-btn:hover {
  background: #c82333;
}

.no-entities {
  padding: 2rem;
  text-align: center;
  color: #888;
}

.no-entities-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.no-entities-icon {
  font-size: 3rem;
  color: #555;
}

.no-entities-text {
  margin: 0;
  font-size: 1rem;
}

.create-spawner-btn {
  padding: 0.5rem 1rem;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  transition: background-color 0.2s ease;
}

.create-spawner-btn:hover {
  background: #218838;
}

.spawner-actions {
  display: flex;
  justify-content: center;
  padding-top: 0.5rem;
}

/* Modal Styles */
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
  border-radius: 8px;
  padding: 1.5rem;
  max-width: 400px;
  width: 90%;
  color: #fff;
}

.modal-content h3 {
  margin: 0 0 1rem 0;
  color: #1E90FF;
}

.modal-content p {
  margin: 0 0 1.5rem 0;
  color: #ccc;
}

.modal-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.modal-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s ease;
}

.modal-btn:not(.danger) {
  background: #555;
  color: #fff;
}

.modal-btn:not(.danger):hover {
  background: #666;
}

.modal-btn.danger {
  background: #dc3545;
  color: white;
}

.modal-btn.danger:hover {
  background: #c82333;
}
</style>