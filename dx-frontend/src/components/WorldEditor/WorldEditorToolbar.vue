<template>
  <div class="world-editor-toolbar">
    <div class="toolbar-header">
      <h3>Edit Tools</h3>
    </div>

    <div class="toolbar-content">
      <!-- Basic Tools -->
      <div class="tool-group">
        <h4>Basic Tools</h4>
        <div class="tool-grid">
          <button
              v-for="tool in basicTools"
              :key="tool.id"
              :class="['tool-btn', { 'active': selectedTool === tool.id }]"
              :title="tool.description"
              @click="selectTool(tool.id)"
          >
            <i :class="tool.icon"></i>
            <span>{{ tool.name }}</span>
          </button>
        </div>
      </div>

      <!-- Room Tools -->
      <div class="tool-group">
        <h4>Room Tools</h4>
        <div class="tool-grid">
          <button
              v-for="tool in roomTools"
              :key="tool.id"
              :class="['tool-btn', { 'active': selectedTool === tool.id }]"
              :title="tool.description"
              @click="selectTool(tool.id)"
          >
            <i :class="tool.icon"></i>
            <span>{{ tool.name }}</span>
          </button>
        </div>
      </div>

      <!-- Entity Tools -->
      <div class="tool-group">
        <h4>Entity Tools</h4>
        <div class="tool-grid">
          <button
              v-for="tool in entityTools"
              :key="tool.id"
              :class="['tool-btn', { 'active': selectedTool === tool.id }]"
              :title="tool.description"
              @click="selectTool(tool.id)"
          >
            <i :class="tool.icon"></i>
            <span>{{ tool.name }}</span>
          </button>
        </div>
      </div>

      <!-- Tool Options -->
      <div v-if="selectedToolConfig" class="tool-options">
        <h4>Tool Options</h4>
        <div class="options-content">
          <!-- Connection Type Options -->
          <div v-if="isConnectionTool" class="option-group">
            <label>
              <input
                  v-model="connectionOptions.vertical"
                  type="checkbox"
                  @change="updateToolOptions"
              />
              Vertical Connection
            </label>
          </div>

          <!-- Room Creation Options -->
          <div v-if="isRoomCreationTool" class="option-group">
            <label>Room Type:</label>
            <select v-model="roomOptions.type" @change="updateToolOptions">
              <option value="default">Default</option>
              <option value="special">Special</option>
              <option value="secret">Secret</option>
              <option value="dangerous">Dangerous</option>
            </select>
          </div>

          <!-- Entity Spawn Options -->
          <div v-if="isEntityTool" class="option-group">
            <label>Spawn Mode:</label>
            <select v-model="entityOptions.mode" @change="updateToolOptions">
              <option value="single">Single</option>
              <option value="multiple">Multiple</option>
              <option value="random">Random</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Tool Instructions -->
      <div v-if="selectedToolConfig" class="tool-instructions">
        <h4>Instructions</h4>
        <p>{{ selectedToolConfig.instructions }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import {WorldEditorTool} from '@/models/WorldEditorModels.js';

export default {
  name: 'WorldEditorToolbar',
  props: {
    selectedTool: {
      type: String,
      default: WorldEditorTool.SELECT
    }
  },
  data() {
    return {
      // Tool options
      connectionOptions: {
        vertical: false
      },
      roomOptions: {
        type: 'default'
      },
      entityOptions: {
        mode: 'single'
      },

      // Tool definitions
      basicTools: [
        {
          id: WorldEditorTool.SELECT,
          name: 'Select',
          icon: 'icon-cursor',
          description: 'Select and inspect rooms',
          instructions: 'Click on rooms to select them. Hold Ctrl to select multiple rooms.'
        }
      ],

      roomTools: [
        {
          id: WorldEditorTool.CREATE_ROOM,
          name: 'Create Room',
          icon: 'icon-plus-square',
          description: 'Create new rooms',
          instructions: 'Click on empty grid cells to create new rooms.'
        },
        {
          id: WorldEditorTool.DELETE_ROOM,
          name: 'Delete Room',
          icon: 'icon-trash',
          description: 'Delete existing rooms',
          instructions: 'Click on rooms to delete them. This will also remove all connections to the room.'
        },
        {
          id: WorldEditorTool.MOVE_ROOM,
          name: 'Move Room',
          icon: 'icon-move',
          description: 'Move rooms to new positions',
          instructions: 'Click and drag rooms to move them to new grid positions.'
        },
        {
          id: WorldEditorTool.CONNECT_ROOMS,
          name: 'Connect Rooms',
          icon: 'icon-link',
          description: 'Create connections between rooms',
          instructions: 'Click on the first room, then click on the second room to create a connection.'
        },
        {
          id: WorldEditorTool.DISCONNECT_ROOMS,
          name: 'Disconnect Rooms',
          icon: 'icon-unlink',
          description: 'Remove connections between rooms',
          instructions: 'Click on connection lines to remove them.'
        }
      ],

      entityTools: [
        {
          id: WorldEditorTool.SPAWN_ITEM,
          name: 'Spawn Item',
          icon: 'icon-package',
          description: 'Add items to rooms',
          instructions: 'Select a room first, then use the entity spawner panel to add items.'
        },
        {
          id: WorldEditorTool.EDIT_ITEM,
          name: 'Edit Item',
          icon: 'icon-edit',
          description: 'Edit existing items',
          instructions: 'Click on items in rooms to edit their properties.'
        },
        {
          id: WorldEditorTool.SPAWN_NPC,
          name: 'Spawn NPC',
          icon: 'icon-user',
          description: 'Add NPCs to rooms',
          instructions: 'Select a room first, then use the entity spawner panel to add NPCs.'
        },
        {
          id: WorldEditorTool.EDIT_NPC,
          name: 'Edit NPC',
          icon: 'icon-user-edit',
          description: 'Edit existing NPCs',
          instructions: 'Click on NPCs in rooms to edit their properties.'
        },
        {
          id: WorldEditorTool.SPAWN_ANOMALY,
          name: 'Spawn Anomaly',
          icon: 'icon-zap',
          description: 'Add anomalies to rooms',
          instructions: 'Select a room first, then use the entity spawner panel to add anomalies.'
        },
        {
          id: WorldEditorTool.EDIT_ANOMALY,
          name: 'Edit Anomaly',
          icon: 'icon-zap-edit',
          description: 'Edit existing anomalies',
          instructions: 'Click on anomalies in rooms to edit their properties.'
        }
      ]
    };
  },
  computed: {
    allTools() {
      return [...this.basicTools, ...this.roomTools, ...this.entityTools];
    },

    selectedToolConfig() {
      return this.allTools.find(tool => tool.id === this.selectedTool);
    },

    isConnectionTool() {
      return this.selectedTool === WorldEditorTool.CONNECT_ROOMS;
    },

    isRoomCreationTool() {
      return this.selectedTool === WorldEditorTool.CREATE_ROOM;
    },

    isEntityTool() {
      return [
        WorldEditorTool.SPAWN_ITEM,
        WorldEditorTool.SPAWN_NPC,
        WorldEditorTool.SPAWN_ANOMALY
      ].includes(this.selectedTool);
    }
  },
  methods: {
    selectTool(toolId) {
      this.$emit('tool-selected', toolId);
    },

    updateToolOptions() {
      // Emit tool options when they change
      const options = {
        connection: this.connectionOptions,
        room: this.roomOptions,
        entity: this.entityOptions
      };

      this.$emit('tool-options-changed', {
        tool: this.selectedTool,
        options
      });
    }
  }
};
</script>

<style scoped>
.world-editor-toolbar {
  background: #2d2d2d;
  border-bottom: 1px solid #444;
  padding: 1rem;
  max-height: 400px;
  overflow-y: auto;
}

.toolbar-header {
  margin-bottom: 1rem;
}

.toolbar-header h3 {
  margin: 0;
  color: #1E90FF;
  font-size: 1.1rem;
  font-weight: 600;
}

.toolbar-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Tool Groups */
.tool-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.tool-group h4 {
  margin: 0;
  color: #ccc;
  font-size: 0.9rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tool-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.25rem;
}

/* Tool Buttons */
.tool-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #333;
  color: #ccc;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  font-size: 0.9rem;
}

.tool-btn:hover {
  background: #444;
  color: #fff;
  border-color: #666;
}

.tool-btn.active {
  background: #1E90FF;
  color: #fff;
  border-color: #1E90FF;
}

.tool-btn i {
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

.tool-btn span {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Tool Options */
.tool-options {
  background: #333;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 1rem;
}

.tool-options h4 {
  margin: 0 0 0.5rem 0;
  color: #1E90FF;
  font-size: 0.9rem;
}

.options-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.option-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.option-group label {
  color: #ccc;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.option-group input[type="checkbox"] {
  accent-color: #1E90FF;
}

.option-group select {
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.25rem;
  font-size: 0.9rem;
}

.option-group select:focus {
  outline: none;
  border-color: #1E90FF;
}

/* Tool Instructions */
.tool-instructions {
  background: #333;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 1rem;
}

.tool-instructions h4 {
  margin: 0 0 0.5rem 0;
  color: #1E90FF;
  font-size: 0.9rem;
}

.tool-instructions p {
  margin: 0;
  color: #ccc;
  font-size: 0.85rem;
  line-height: 1.4;
}

/* Scrollbar Styling */
.world-editor-toolbar::-webkit-scrollbar {
  width: 6px;
}

.world-editor-toolbar::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.world-editor-toolbar::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}

.world-editor-toolbar::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* Responsive Design */
@media (max-width: 768px) {
  .world-editor-toolbar {
    padding: 0.5rem;
    max-height: 300px;
  }

  .toolbar-content {
    gap: 1rem;
  }

  .tool-btn {
    padding: 0.4rem;
    font-size: 0.8rem;
  }

  .tool-btn span {
    font-size: 0.8rem;
  }
}

/* Icon placeholders - these would be replaced with actual icon font */
.icon-cursor::before {
  content: '↖';
}

.icon-plus-square::before {
  content: '⊞';
}

.icon-trash::before {
  content: '🗑';
}

.icon-move::before {
  content: '↔';
}

.icon-link::before {
  content: '🔗';
}

.icon-unlink::before {
  content: '⛓';
}

.icon-package::before {
  content: '📦';
}

.icon-edit::before {
  content: '✏';
}

.icon-user::before {
  content: '👤';
}

.icon-user-edit::before {
  content: '👥';
}

.icon-zap::before {
  content: '⚡';
}

.icon-zap-edit::before {
  content: '🌟';
}
</style>
