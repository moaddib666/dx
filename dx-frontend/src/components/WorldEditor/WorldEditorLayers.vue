<template>
  <div class="world-editor-layers">
    <div class="layers-header">
      <h3>Layers</h3>
      <div class="layer-actions">
        <button :title="allLayersActive ? 'Hide All' : 'Show All'" class="action-btn" @click="toggleAllLayers">
          {{ allLayersActive ? 'Hide All' : 'Show All' }}
        </button>
      </div>
    </div>

    <div class="layers-content">
      <div
          v-for="layer in layerDefinitions"
          :key="layer.id"
          class="layer-item"
      >
        <div class="layer-control">
          <label class="layer-toggle">
            <input
                :checked="isLayerActive(layer.id)"
                type="checkbox"
                @change="toggleLayer(layer.id)"
            />
            <span class="layer-checkbox"></span>
          </label>

          <div class="layer-info">
            <div class="layer-name">
              <i :class="layer.icon" :style="{ color: layer.color }"></i>
              <span>{{ layer.name }}</span>
            </div>
            <div v-if="layerCounts[layer.id] !== undefined" class="layer-count">
              {{ layerCounts[layer.id] }} {{ layer.countLabel }}
            </div>
          </div>

          <div class="layer-opacity">
            <input
                :disabled="!isLayerActive(layer.id)"
                :value="layerOpacity[layer.id] || 1"
                class="opacity-slider"
                max="1"
                min="0.1"
                step="0.1"
                type="range"
                @input="updateLayerOpacity(layer.id, $event.target.value)"
            />
            <span class="opacity-value">{{ Math.round((layerOpacity[layer.id] || 1) * 100) }}%</span>
          </div>
        </div>

        <!-- Layer Options -->
        <div v-if="isLayerActive(layer.id) && layer.options" class="layer-options">
          <div
              v-for="option in layer.options"
              :key="option.id"
              class="layer-option"
          >
            <label v-if="option.type === 'checkbox'">
              <input
                  :checked="layerSettings[layer.id]?.[option.id] || false"
                  type="checkbox"
                  @change="updateLayerSetting(layer.id, option.id, $event.target.checked)"
              />
              {{ option.label }}
            </label>

            <div v-else-if="option.type === 'select'" class="select-option">
              <label>{{ option.label }}:</label>
              <select
                  :value="layerSettings[layer.id]?.[option.id] || option.default"
                  @change="updateLayerSetting(layer.id, option.id, $event.target.value)"
              >
                <option
                    v-for="choice in option.choices"
                    :key="choice.value"
                    :value="choice.value"
                >
                  {{ choice.label }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Layer Presets -->
      <div class="layer-presets">
        <h4>Presets</h4>
        <div class="preset-buttons">
          <button
              v-for="preset in layerPresets"
              :key="preset.id"
              :title="preset.description"
              class="preset-btn"
              @click="applyPreset(preset)"
          >
            {{ preset.name }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {WorldEditorLayer} from '@/models/WorldEditorModels.js';

export default {
  name: 'WorldEditorLayers',
  props: {
    activeLayers: {
      type: Set,
      default: () => new Set()
    },
    layerCounts: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      layerOpacity: {
        [WorldEditorLayer.PLAYERS]: 1,
        [WorldEditorLayer.NPCS]: 1,
        [WorldEditorLayer.OBJECTS]: 1,
        [WorldEditorLayer.ANOMALIES]: 1,
        [WorldEditorLayer.TBD]: 1
      },

      layerSettings: {
        [WorldEditorLayer.PLAYERS]: {},
        [WorldEditorLayer.NPCS]: {},
        [WorldEditorLayer.OBJECTS]: {},
        [WorldEditorLayer.ANOMALIES]: {},
        [WorldEditorLayer.TBD]: {}
      },

      layerDefinitions: [
        {
          id: WorldEditorLayer.PLAYERS,
          name: 'Players',
          icon: 'icon-users',
          color: '#00ff00',
          countLabel: 'rooms with players',
          options: [
            {
              id: 'showNames',
              type: 'checkbox',
              label: 'Show player names',
              default: true
            },
            {
              id: 'showStatus',
              type: 'checkbox',
              label: 'Show player status',
              default: false
            },
            {
              id: 'displayMode',
              type: 'select',
              label: 'Display Mode',
              default: 'icons',
              choices: [
                {value: 'icons', label: 'Icons Only'},
                {value: 'names', label: 'Names Only'},
                {value: 'both', label: 'Icons & Names'}
              ]
            }
          ]
        },
        {
          id: WorldEditorLayer.NPCS,
          name: 'NPCs',
          icon: 'icon-user-friends',
          color: '#ffff00',
          countLabel: 'rooms with NPCs',
          options: [
            {
              id: 'showNames',
              type: 'checkbox',
              label: 'Show NPC names',
              default: true
            },
            {
              id: 'showTypes',
              type: 'checkbox',
              label: 'Show NPC types',
              default: false
            },
            {
              id: 'filterByType',
              type: 'select',
              label: 'Filter by Type',
              default: 'all',
              choices: [
                {value: 'all', label: 'All NPCs'},
                {value: 'friendly', label: 'Friendly Only'},
                {value: 'hostile', label: 'Hostile Only'},
                {value: 'neutral', label: 'Neutral Only'}
              ]
            }
          ]
        },
        {
          id: WorldEditorLayer.OBJECTS,
          name: 'Objects',
          icon: 'icon-cube',
          color: '#ff8800',
          countLabel: 'rooms with objects',
          options: [
            {
              id: 'showNames',
              type: 'checkbox',
              label: 'Show object names',
              default: false
            },
            {
              id: 'showRarity',
              type: 'checkbox',
              label: 'Show rarity indicators',
              default: true
            },
            {
              id: 'filterByType',
              type: 'select',
              label: 'Filter by Type',
              default: 'all',
              choices: [
                {value: 'all', label: 'All Objects'},
                {value: 'weapons', label: 'Weapons'},
                {value: 'armor', label: 'Armor'},
                {value: 'consumables', label: 'Consumables'},
                {value: 'misc', label: 'Miscellaneous'}
              ]
            }
          ]
        },
        {
          id: WorldEditorLayer.ANOMALIES,
          name: 'Anomalies',
          icon: 'icon-exclamation-triangle',
          color: '#ff0088',
          countLabel: 'rooms with anomalies',
          options: [
            {
              id: 'showNames',
              type: 'checkbox',
              label: 'Show anomaly names',
              default: true
            },
            {
              id: 'showDanger',
              type: 'checkbox',
              label: 'Show danger levels',
              default: true
            },
            {
              id: 'filterByDanger',
              type: 'select',
              label: 'Filter by Danger',
              default: 'all',
              choices: [
                {value: 'all', label: 'All Anomalies'},
                {value: 'low', label: 'Low Danger'},
                {value: 'medium', label: 'Medium Danger'},
                {value: 'high', label: 'High Danger'},
                {value: 'extreme', label: 'Extreme Danger'}
              ]
            }
          ]
        },
        {
          id: WorldEditorLayer.TBD,
          name: 'Special',
          icon: 'icon-star',
          color: '#888888',
          countLabel: 'special rooms',
          options: [
            {
              id: 'showLabels',
              type: 'checkbox',
              label: 'Show special labels',
              default: true
            }
          ]
        }
      ],

      layerPresets: [
        {
          id: 'all',
          name: 'All',
          description: 'Show all layers',
          layers: [
            WorldEditorLayer.PLAYERS,
            WorldEditorLayer.NPCS,
            WorldEditorLayer.OBJECTS,
            WorldEditorLayer.ANOMALIES,
            WorldEditorLayer.TBD
          ]
        },
        {
          id: 'entities',
          name: 'Entities',
          description: 'Show only players and NPCs',
          layers: [
            WorldEditorLayer.PLAYERS,
            WorldEditorLayer.NPCS
          ]
        },
        {
          id: 'items',
          name: 'Items',
          description: 'Show only objects and anomalies',
          layers: [
            WorldEditorLayer.OBJECTS,
            WorldEditorLayer.ANOMALIES
          ]
        },
        {
          id: 'minimal',
          name: 'Minimal',
          description: 'Show only players',
          layers: [
            WorldEditorLayer.PLAYERS
          ]
        },
        {
          id: 'none',
          name: 'None',
          description: 'Hide all layers',
          layers: []
        }
      ]
    };
  },
  computed: {
    allLayersActive() {
      return this.layerDefinitions.every(layer => this.isLayerActive(layer.id));
    }
  },
  methods: {
    isLayerActive(layerId) {
      return this.activeLayers.has(layerId);
    },

    toggleLayer(layerId) {
      this.$emit('layer-toggled', layerId);
    },

    toggleAllLayers() {
      if (this.allLayersActive) {
        // Hide all layers
        this.layerDefinitions.forEach(layer => {
          if (this.isLayerActive(layer.id)) {
            this.toggleLayer(layer.id);
          }
        });
      } else {
        // Show all layers
        this.layerDefinitions.forEach(layer => {
          if (!this.isLayerActive(layer.id)) {
            this.toggleLayer(layer.id);
          }
        });
      }
    },

    updateLayerOpacity(layerId, opacity) {
      this.layerOpacity[layerId] = parseFloat(opacity);
      this.$emit('layer-opacity-changed', {
        layer: layerId,
        opacity: this.layerOpacity[layerId]
      });
    },

    updateLayerSetting(layerId, settingId, value) {
      if (!this.layerSettings[layerId]) {
        this.layerSettings[layerId] = {};
      }
      this.layerSettings[layerId][settingId] = value;

      this.$emit('layer-setting-changed', {
        layer: layerId,
        setting: settingId,
        value
      });
    },

    applyPreset(preset) {
      // First, hide all layers
      this.layerDefinitions.forEach(layer => {
        if (this.isLayerActive(layer.id) && !preset.layers.includes(layer.id)) {
          this.toggleLayer(layer.id);
        }
      });

      // Then, show preset layers
      preset.layers.forEach(layerId => {
        if (!this.isLayerActive(layerId)) {
          this.toggleLayer(layerId);
        }
      });
    }
  }
};
</script>

<style scoped>
.world-editor-layers {
  background: #2d2d2d;
  border-bottom: 1px solid #444;
  padding: 1rem;
  max-height: 500px;
  overflow-y: auto;
}

.layers-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.layers-header h3 {
  margin: 0;
  color: #1E90FF;
  font-size: 1.1rem;
  font-weight: 600;
}

.layer-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.25rem 0.5rem;
  background: #444;
  color: #ccc;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: #555;
  color: #fff;
}

.layers-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Layer Items */
.layer-item {
  background: #333;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.75rem;
  transition: all 0.3s ease;
}

.layer-item:hover {
  border-color: #666;
}

.layer-control {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Layer Toggle */
.layer-toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.layer-toggle input[type="checkbox"] {
  display: none;
}

.layer-checkbox {
  width: 18px;
  height: 18px;
  border: 2px solid #555;
  border-radius: 3px;
  background: #2d2d2d;
  position: relative;
  transition: all 0.3s ease;
}

.layer-toggle input[type="checkbox"]:checked + .layer-checkbox {
  background: #1E90FF;
  border-color: #1E90FF;
}

.layer-toggle input[type="checkbox"]:checked + .layer-checkbox::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 12px;
  font-weight: bold;
}

/* Layer Info */
.layer-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.layer-name {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #fff;
}

.layer-name i {
  font-size: 16px;
}

.layer-count {
  font-size: 0.8rem;
  color: #aaa;
}

/* Layer Opacity */
.layer-opacity {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 100px;
}

.opacity-slider {
  flex: 1;
  height: 4px;
  background: #555;
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}

.opacity-slider::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  background: #1E90FF;
  border-radius: 50%;
  cursor: pointer;
}

.opacity-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  background: #1E90FF;
  border-radius: 50%;
  border: none;
  cursor: pointer;
}

.opacity-slider:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.opacity-value {
  font-size: 0.8rem;
  color: #ccc;
  min-width: 35px;
  text-align: right;
}

/* Layer Options */
.layer-options {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #555;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.layer-option {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.layer-option label {
  color: #ccc;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.layer-option input[type="checkbox"] {
  accent-color: #1E90FF;
}

.select-option {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.select-option label {
  color: #ccc;
  font-size: 0.9rem;
}

.select-option select {
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.25rem;
  font-size: 0.9rem;
}

.select-option select:focus {
  outline: none;
  border-color: #1E90FF;
}

/* Layer Presets */
.layer-presets {
  background: #333;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 1rem;
}

.layer-presets h4 {
  margin: 0 0 0.75rem 0;
  color: #1E90FF;
  font-size: 0.9rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.preset-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.preset-btn {
  padding: 0.4rem 0.8rem;
  background: #444;
  color: #ccc;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s ease;
}

.preset-btn:hover {
  background: #555;
  color: #fff;
  border-color: #666;
}

.preset-btn:active {
  background: #1E90FF;
  border-color: #1E90FF;
}

/* Scrollbar Styling */
.world-editor-layers::-webkit-scrollbar {
  width: 6px;
}

.world-editor-layers::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.world-editor-layers::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}

.world-editor-layers::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* Responsive Design */
@media (max-width: 768px) {
  .world-editor-layers {
    padding: 0.5rem;
    max-height: 400px;
  }

  .layer-control {
    gap: 0.5rem;
  }

  .layer-opacity {
    min-width: 80px;
  }

  .preset-buttons {
    gap: 0.25rem;
  }

  .preset-btn {
    padding: 0.3rem 0.6rem;
    font-size: 0.75rem;
  }
}

/* Icon placeholders */
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

.icon-star::before {
  content: '⭐';
}
</style>
