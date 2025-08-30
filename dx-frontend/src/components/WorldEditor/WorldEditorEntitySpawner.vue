<template>
  <div class="world-editor-entity-spawner">
    <div class="spawner-header">
      <h3>Entity Spawner</h3>
      <div class="spawner-mode">
        <span class="current-tool">{{ formatToolName(selectedTool) }}</span>
      </div>
    </div>

    <div class="spawner-content">
      <!-- Entity Type GmCharSelector -->
      <div class="spawner-section">
        <h4>Entity Type</h4>
        <div class="entity-type-buttons">
          <button
              v-for="entityType in entityTypes"
              :key="entityType.id"
              :class="['entity-type-btn', { 'active': selectedEntityType === entityType.id }]"
              :disabled="!isSpawnTool"
              @click="selectEntityType(entityType.id)"
          >
            <i :class="entityType.icon" :style="{ color: entityType.color }"></i>
            <span>{{ entityType.name }}</span>
          </button>
        </div>
      </div>

      <!-- Entity Configuration -->
      <div v-if="selectedEntityType && isSpawnTool" class="spawner-section">
        <h4>{{ getEntityTypeName(selectedEntityType) }} Configuration</h4>

        <!-- Item Configuration -->
        <div v-if="selectedEntityType === 'item'" class="entity-config">
          <div class="config-group">
            <label>Item Type:</label>
            <select v-model="itemConfig.type">
              <option value="weapon">Weapon</option>
              <option value="armor">Armor</option>
              <option value="consumable">Consumable</option>
              <option value="misc">Miscellaneous</option>
            </select>
          </div>
          <div class="config-group">
            <label>Item Name:</label>
            <input v-model="itemConfig.name" placeholder="Enter item name" type="text"/>
          </div>
          <div class="config-group">
            <label>Rarity:</label>
            <select v-model="itemConfig.rarity">
              <option value="common">Common</option>
              <option value="uncommon">Uncommon</option>
              <option value="rare">Rare</option>
              <option value="epic">Epic</option>
              <option value="legendary">Legendary</option>
            </select>
          </div>
          <div class="config-group">
            <label>Quantity:</label>
            <input v-model.number="itemConfig.quantity" max="99" min="1" type="number"/>
          </div>
          <div class="config-group">
            <label>Description:</label>
            <textarea v-model="itemConfig.description" placeholder="Item description..."></textarea>
          </div>
        </div>

        <!-- NPC Configuration -->
        <div v-if="selectedEntityType === 'npc'" class="entity-config">
          <div class="config-group">
            <label>NPC Name:</label>
            <input v-model="npcConfig.name" placeholder="Enter NPC name" type="text"/>
          </div>
          <div class="config-group">
            <label>NPC Type:</label>
            <select v-model="npcConfig.type">
              <option value="friendly">Friendly</option>
              <option value="neutral">Neutral</option>
              <option value="hostile">Hostile</option>
              <option value="merchant">Merchant</option>
              <option value="quest_giver">Quest Giver</option>
            </select>
          </div>
          <div class="config-group">
            <label>Level:</label>
            <input v-model.number="npcConfig.level" max="100" min="1" type="number"/>
          </div>
          <div class="config-group">
            <label>Health:</label>
            <input v-model.number="npcConfig.health" max="9999" min="1" type="number"/>
          </div>
          <div class="config-group">
            <label>Behavior:</label>
            <select v-model="npcConfig.behavior">
              <option value="stationary">Stationary</option>
              <option value="patrol">Patrol</option>
              <option value="wander">Wander</option>
              <option value="guard">Guard</option>
            </select>
          </div>
          <div class="config-group">
            <label>Dialogue:</label>
            <textarea v-model="npcConfig.dialogue" placeholder="NPC dialogue..."></textarea>
          </div>
        </div>

        <!-- Anomaly Configuration -->
        <div v-if="selectedEntityType === 'anomaly'" class="entity-config">
          <div class="config-group">
            <label>Anomaly Name:</label>
            <input v-model="anomalyConfig.name" placeholder="Enter anomaly name" type="text"/>
          </div>
          <div class="config-group">
            <label>Anomaly Type:</label>
            <select v-model="anomalyConfig.type">
              <option value="temporal">Temporal</option>
              <option value="spatial">Spatial</option>
              <option value="energy">Energy</option>
              <option value="gravitational">Gravitational</option>
              <option value="dimensional">Dimensional</option>
            </select>
          </div>
          <div class="config-group">
            <label>Danger Level:</label>
            <select v-model="anomalyConfig.danger">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="extreme">Extreme</option>
            </select>
          </div>
          <div class="config-group">
            <label>Effect Radius:</label>
            <input v-model.number="anomalyConfig.radius" max="10" min="1" type="number"/>
          </div>
          <div class="config-group">
            <label>Duration (minutes):</label>
            <input v-model.number="anomalyConfig.duration" max="1440" min="1" type="number"/>
          </div>
          <div class="config-group">
            <label>Effects:</label>
            <textarea v-model="anomalyConfig.effects" placeholder="Describe the anomaly's effects..."></textarea>
          </div>
        </div>
      </div>

      <!-- Spawn Options -->
      <div v-if="selectedEntityType && isSpawnTool" class="spawner-section">
        <h4>Spawn Options</h4>
        <div class="spawn-options">
          <div class="option-group">
            <label>
              <input v-model="spawnOptions.randomPosition" type="checkbox"/>
              Random Position in Room
            </label>
          </div>
          <div class="option-group">
            <label>
              <input v-model="spawnOptions.autoGenerate" type="checkbox"/>
              Auto-generate Properties
            </label>
          </div>
          <div class="option-group">
            <label>Spawn Count:</label>
            <input v-model.number="spawnOptions.count" max="10" min="1" type="number"/>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div v-if="selectedEntityType && isSpawnTool" class="spawner-section">
        <div class="spawner-actions">
          <button class="action-btn preview" @click="previewEntity">
            <i class="icon-eye"></i> Preview
          </button>
          <button :disabled="!canSpawn" class="action-btn spawn" @click="spawnEntity">
            <i class="icon-plus"></i> Spawn {{ getEntityTypeName(selectedEntityType) }}
          </button>
          <button class="action-btn reset" @click="resetConfig">
            <i class="icon-refresh"></i> Reset
          </button>
        </div>
      </div>

      <!-- Entity Templates -->
      <div class="spawner-section">
        <h4>Quick Templates</h4>
        <div class="template-grid">
          <button
              v-for="template in availableTemplates"
              :key="template.id"
              :title="template.description"
              class="template-btn"
              @click="applyTemplate(template)"
          >
            <i :class="template.icon"></i>
            <span>{{ template.name }}</span>
          </button>
        </div>
      </div>

      <!-- Recent Spawns -->
      <div v-if="recentSpawns.length > 0" class="spawner-section">
        <h4>Recent Spawns</h4>
        <div class="recent-spawns">
          <div
              v-for="spawn in recentSpawns"
              :key="spawn.id"
              class="recent-spawn-item"
              @click="respawnEntity(spawn)"
          >
            <div class="spawn-info">
              <i :class="getEntityIcon(spawn.type)" :style="{ color: getEntityColor(spawn.type) }"></i>
              <span class="spawn-name">{{ spawn.name }}</span>
            </div>
            <span class="spawn-time">{{ formatTime(spawn.timestamp) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Preview Modal -->
    <div v-if="showPreview" class="modal-overlay" @click="closePreview">
      <div class="modal-content preview-modal" @click.stop>
        <div class="preview-header">
          <h3>Entity Preview</h3>
          <button class="close-btn" @click="closePreview">
            <i class="icon-times"></i>
          </button>
        </div>
        <div class="preview-content">
          <div class="preview-entity">
            <div class="entity-preview-icon">
              <i :class="getEntityIcon(selectedEntityType)" :style="{ color: getEntityColor(selectedEntityType) }"></i>
            </div>
            <div class="entity-preview-details">
              <h4>{{ getCurrentConfig().name || 'Unnamed ' + getEntityTypeName(selectedEntityType) }}</h4>
              <div class="preview-properties">
                <div v-for="(value, key) in getPreviewProperties()" :key="key" class="preview-property">
                  <span class="property-key">{{ formatPropertyName(key) }}:</span>
                  <span class="property-value">{{ value }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="preview-actions">
          <button class="modal-btn" @click="closePreview">Close</button>
          <button class="modal-btn primary" @click="spawnFromPreview">Spawn</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {WorldEditorTool} from '@/models/WorldEditorModels.ts';

export default {
  name: 'WorldEditorEntitySpawner',
  props: {
    room: {
      type: Object,
      default: null
    },
    selectedTool: {
      type: String,
      default: WorldEditorTool.SELECT
    }
  },
  data() {
    return {
      selectedEntityType: null,
      showPreview: false,

      // Entity configurations
      itemConfig: {
        type: 'misc',
        name: '',
        rarity: 'common',
        quantity: 1,
        description: ''
      },
      npcConfig: {
        name: '',
        type: 'neutral',
        level: 1,
        health: 100,
        behavior: 'stationary',
        dialogue: ''
      },
      anomalyConfig: {
        name: '',
        type: 'temporal',
        danger: 'low',
        radius: 1,
        duration: 60,
        effects: ''
      },

      // Spawn options
      spawnOptions: {
        randomPosition: false,
        autoGenerate: false,
        count: 1
      },

      // Entity types
      entityTypes: [
        {
          id: 'item',
          name: 'Item',
          icon: 'icon-cube',
          color: '#ff8800'
        },
        {
          id: 'npc',
          name: 'NPC',
          icon: 'icon-user-friends',
          color: '#ffff00'
        },
        {
          id: 'anomaly',
          name: 'Anomaly',
          icon: 'icon-exclamation-triangle',
          color: '#ff0088'
        }
      ],

      // Recent spawns
      recentSpawns: [
        {
          id: 1,
          type: 'item',
          name: 'Health Potion',
          timestamp: Date.now() - 300000
        },
        {
          id: 2,
          type: 'npc',
          name: 'Guard Captain',
          timestamp: Date.now() - 600000
        }
      ]
    };
  },
  computed: {
    isSpawnTool() {
      return [
        WorldEditorTool.SPAWN_ITEM,
        WorldEditorTool.SPAWN_NPC,
        WorldEditorTool.SPAWN_ANOMALY
      ].includes(this.selectedTool);
    },

    canSpawn() {
      if (!this.selectedEntityType || !this.room) return false;

      const config = this.getCurrentConfig();
      return config.name && config.name.trim() !== '';
    },

    availableTemplates() {
      const templates = {
        item: [
          {id: 'health_potion', name: 'Health Potion', icon: 'icon-heart', description: 'Basic healing item'},
          {id: 'sword', name: 'Iron Sword', icon: 'icon-sword', description: 'Basic weapon'},
          {id: 'armor', name: 'Leather Armor', icon: 'icon-shield', description: 'Basic protection'}
        ],
        npc: [
          {id: 'guard', name: 'Guard', icon: 'icon-shield', description: 'Basic guard NPC'},
          {id: 'merchant', name: 'Merchant', icon: 'icon-coins', description: 'Trading NPC'},
          {id: 'quest_giver', name: 'Quest Giver', icon: 'icon-scroll', description: 'Mission provider'}
        ],
        anomaly: [
          {id: 'time_rift', name: 'Time Rift', icon: 'icon-clock', description: 'Temporal distortion'},
          {id: 'gravity_well', name: 'Gravity Well', icon: 'icon-circle', description: 'Gravitational anomaly'},
          {id: 'energy_storm', name: 'Energy Storm', icon: 'icon-lightning', description: 'Energy discharge'}
        ]
      };

      return templates[this.selectedEntityType] || [];
    }
  },
  methods: {
    formatToolName(tool) {
      return tool.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    },

    selectEntityType(type) {
      this.selectedEntityType = type;
    },

    getEntityTypeName(type) {
      const typeMap = {
        item: 'Item',
        npc: 'NPC',
        anomaly: 'Anomaly'
      };
      return typeMap[type] || type;
    },

    getCurrentConfig() {
      switch (this.selectedEntityType) {
        case 'item':
          return this.itemConfig;
        case 'npc':
          return this.npcConfig;
        case 'anomaly':
          return this.anomalyConfig;
        default:
          return {};
      }
    },

    getEntityIcon(type) {
      const iconMap = {
        item: 'icon-cube',
        npc: 'icon-user-friends',
        anomaly: 'icon-exclamation-triangle'
      };
      return iconMap[type] || 'icon-question';
    },

    getEntityColor(type) {
      const colorMap = {
        item: '#ff8800',
        npc: '#ffff00',
        anomaly: '#ff0088'
      };
      return colorMap[type] || '#888888';
    },

    previewEntity() {
      this.showPreview = true;
    },

    closePreview() {
      this.showPreview = false;
    },

    spawnEntity() {
      const config = this.getCurrentConfig();
      const entityData = {
        ...config,
        id: Date.now() + Math.random(),
        timestamp: Date.now()
      };

      // Add to recent spawns
      this.recentSpawns.unshift({
        id: entityData.id,
        type: this.selectedEntityType,
        name: config.name,
        timestamp: entityData.timestamp
      });

      // Keep only last 10 spawns
      if (this.recentSpawns.length > 10) {
        this.recentSpawns = this.recentSpawns.slice(0, 10);
      }

      this.$emit('entity-spawned', this.selectedEntityType, entityData);
    },

    spawnFromPreview() {
      this.closePreview();
      this.spawnEntity();
    },

    resetConfig() {
      switch (this.selectedEntityType) {
        case 'item':
          this.itemConfig = {
            type: 'misc',
            name: '',
            rarity: 'common',
            quantity: 1,
            description: ''
          };
          break;
        case 'npc':
          this.npcConfig = {
            name: '',
            type: 'neutral',
            level: 1,
            health: 100,
            behavior: 'stationary',
            dialogue: ''
          };
          break;
        case 'anomaly':
          this.anomalyConfig = {
            name: '',
            type: 'temporal',
            danger: 'low',
            radius: 1,
            duration: 60,
            effects: ''
          };
          break;
      }
    },

    applyTemplate(template) {
      // Apply template based on type
      switch (template.id) {
        case 'health_potion':
          this.itemConfig = {
            type: 'consumable',
            name: 'Health Potion',
            rarity: 'common',
            quantity: 1,
            description: 'Restores 50 HP when consumed'
          };
          break;
        case 'sword':
          this.itemConfig = {
            type: 'weapon',
            name: 'Iron Sword',
            rarity: 'common',
            quantity: 1,
            description: 'A sturdy iron blade. +10 Attack'
          };
          break;
        case 'armor':
          this.itemConfig = {
            type: 'armor',
            name: 'Leather Armor',
            rarity: 'common',
            quantity: 1,
            description: 'Basic leather protection. +5 Defense'
          };
          break;
        case 'guard':
          this.npcConfig = {
            name: 'Guard',
            type: 'neutral',
            level: 5,
            health: 150,
            behavior: 'guard',
            dialogue: 'Halt! State your business.'
          };
          break;
        case 'merchant':
          this.npcConfig = {
            name: 'Merchant',
            type: 'friendly',
            level: 1,
            health: 50,
            behavior: 'stationary',
            dialogue: 'Welcome! Take a look at my wares.'
          };
          break;
        case 'quest_giver':
          this.npcConfig = {
            name: 'Quest Giver',
            type: 'friendly',
            level: 10,
            health: 100,
            behavior: 'stationary',
            dialogue: 'I have a task that needs doing...'
          };
          break;
        case 'time_rift':
          this.anomalyConfig = {
            name: 'Time Rift',
            type: 'temporal',
            danger: 'medium',
            radius: 3,
            duration: 120,
            effects: 'Slows time for all entities within radius'
          };
          break;
        case 'gravity_well':
          this.anomalyConfig = {
            name: 'Gravity Well',
            type: 'gravitational',
            danger: 'high',
            radius: 2,
            duration: 180,
            effects: 'Pulls entities toward center, deals damage'
          };
          break;
        case 'energy_storm':
          this.anomalyConfig = {
            name: 'Energy Storm',
            type: 'energy',
            danger: 'extreme',
            radius: 5,
            duration: 60,
            effects: 'Random energy discharges, high damage'
          };
          break;
      }
    },

    respawnEntity(spawn) {
      // This would respawn a previously created entity
      this.$emit('entity-spawned', spawn.type, spawn);
    },

    getPreviewProperties() {
      const config = this.getCurrentConfig();
      const properties = {};

      Object.keys(config).forEach(key => {
        if (config[key] !== '' && config[key] !== null && config[key] !== undefined) {
          properties[key] = config[key];
        }
      });

      return properties;
    },

    formatPropertyName(key) {
      return key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
    },

    formatTime(timestamp) {
      const now = Date.now();
      const diff = now - timestamp;
      const minutes = Math.floor(diff / 60000);
      const hours = Math.floor(minutes / 60);

      if (hours > 0) return `${hours}h ago`;
      if (minutes > 0) return `${minutes}m ago`;
      return 'Just now';
    }
  }
};
</script>

<style scoped>
.world-editor-entity-spawner {
  background: #2d2d2d;
  border: 1px solid #555;
  border-radius: 4px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.spawner-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #333;
  border-bottom: 1px solid #555;
}

.spawner-header h3 {
  margin: 0;
  color: #1E90FF;
  font-size: 1.1rem;
  font-weight: 600;
}

.spawner-mode {
  display: flex;
  align-items: center;
}

.current-tool {
  color: #ccc;
  font-size: 0.9rem;
  font-style: italic;
}

.spawner-content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Spawner Sections */
.spawner-section {
  background: #333;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 1rem;
}

.spawner-section h4 {
  margin: 0 0 0.75rem 0;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Entity Type Buttons */
.entity-type-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.entity-type-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #444;
  color: #ccc;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.entity-type-btn:hover:not(:disabled) {
  background: #555;
  color: #fff;
  border-color: #666;
}

.entity-type-btn.active {
  background: #1E90FF;
  color: #fff;
  border-color: #1E90FF;
}

.entity-type-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.entity-type-btn i {
  font-size: 1.2rem;
}

/* Entity Configuration */
.entity-config {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.config-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.config-group label {
  color: #ccc;
  font-size: 0.9rem;
  font-weight: 500;
}

.config-group input,
.config-group select,
.config-group textarea {
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.5rem;
  font-size: 0.9rem;
}

.config-group input:focus,
.config-group select:focus,
.config-group textarea:focus {
  outline: none;
  border-color: #1E90FF;
}

.config-group textarea {
  min-height: 60px;
  resize: vertical;
}

/* Spawn Options */
.spawn-options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.option-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.option-group label {
  color: #ccc;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.option-group input[type="checkbox"] {
  accent-color: #1E90FF;
}

.option-group input[type="number"] {
  width: 80px;
}

/* Action Buttons */
.spawner-actions {
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
  font-size: 0.9rem;
}

.action-btn:hover:not(:disabled) {
  background: #555;
  border-color: #666;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.preview {
  background: #666;
}

.action-btn.spawn {
  background: #1E90FF;
  border-color: #1E90FF;
}

.action-btn.spawn:hover:not(:disabled) {
  background: #4FC3F7;
}

.action-btn.reset {
  background: #d32f2f;
  border-color: #d32f2f;
}

.action-btn.reset:hover {
  background: #f44336;
}

/* Template Grid */
.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.5rem;
}

.template-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #444;
  color: #ccc;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.template-btn:hover {
  background: #555;
  color: #fff;
  border-color: #666;
}

.template-btn i {
  font-size: 1.5rem;
  color: #1E90FF;
}

.template-btn span {
  font-size: 0.8rem;
  font-weight: 500;
}

/* Recent Spawns */
.recent-spawns {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  max-height: 200px;
  overflow-y: auto;
}

.recent-spawn-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: #444;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.recent-spawn-item:hover {
  background: #555;
}

.spawn-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spawn-name {
  color: #fff;
  font-size: 0.9rem;
}

.spawn-time {
  color: #aaa;
  font-size: 0.8rem;
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
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.preview-modal {
  max-width: 600px;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #333;
  border-bottom: 1px solid #555;
}

.preview-header h3 {
  margin: 0;
  color: #fff;
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

.preview-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}

.preview-entity {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.entity-preview-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #444;
  border-radius: 8px;
  flex-shrink: 0;
}

.entity-preview-icon i {
  font-size: 2rem;
}

.entity-preview-details {
  flex: 1;
}

.entity-preview-details h4 {
  margin: 0 0 1rem 0;
  color: #fff;
  font-size: 1.2rem;
}

.preview-properties {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.preview-property {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: #333;
  border-radius: 4px;
}

.property-key {
  color: #ccc;
  font-size: 0.9rem;
  font-weight: 500;
}

.property-value {
  color: #fff;
  font-size: 0.9rem;
}

.preview-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  padding: 1rem;
  background: #333;
  border-top: 1px solid #555;
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

.modal-btn.primary {
  background: #1E90FF;
  border-color: #1E90FF;
}

.modal-btn.primary:hover {
  background: #4FC3F7;
}

/* Scrollbar Styling */
.spawner-content::-webkit-scrollbar,
.recent-spawns::-webkit-scrollbar,
.preview-content::-webkit-scrollbar {
  width: 6px;
}

.spawner-content::-webkit-scrollbar-track,
.recent-spawns::-webkit-scrollbar-track,
.preview-content::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.spawner-content::-webkit-scrollbar-thumb,
.recent-spawns::-webkit-scrollbar-thumb,
.preview-content::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}

.spawner-content::-webkit-scrollbar-thumb:hover,
.recent-spawns::-webkit-scrollbar-thumb:hover,
.preview-content::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* Responsive Design */
@media (max-width: 768px) {
  .spawner-header {
    padding: 0.75rem;
  }

  .spawner-content {
    padding: 0.75rem;
    gap: 1rem;
  }

  .spawner-section {
    padding: 0.75rem;
  }

  .spawner-actions {
    flex-direction: column;
  }

  .template-grid {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  }

  .template-btn {
    padding: 0.5rem;
  }

  .template-btn i {
    font-size: 1.2rem;
  }

  .template-btn span {
    font-size: 0.75rem;
  }

  .modal-content {
    width: 95%;
    max-height: 90vh;
  }

  .preview-entity {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .preview-actions {
    flex-direction: column;
  }
}

/* Icon placeholders */
.icon-cube::before {
  content: '📦';
}

.icon-user-friends::before {
  content: '👫';
}

.icon-exclamation-triangle::before {
  content: '⚠️';
}

.icon-eye::before {
  content: '👁';
}

.icon-plus::before {
  content: '+';
}

.icon-refresh::before {
  content: '🔄';
}

.icon-times::before {
  content: '✕';
}

.icon-question::before {
  content: '❓';
}

.icon-heart::before {
  content: '❤️';
}

.icon-sword::before {
  content: '⚔️';
}

.icon-shield::before {
  content: '🛡';
}

.icon-coins::before {
  content: '🪙';
}

.icon-scroll::before {
  content: '📜';
}

.icon-clock::before {
  content: '🕐';
}

.icon-circle::before {
  content: '⭕';
}

.icon-lightning::before {
  content: '⚡';
}
</style>
