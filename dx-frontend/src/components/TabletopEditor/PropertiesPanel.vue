<template>
  <div class="properties-panel">
    <h3 class="properties-title">Cell Properties</h3>

    <div v-if="!selectedCell" class="no-selection">
      <p>No cell selected</p>
      <p class="hint">Use the Select tool to inspect cells</p>
    </div>

    <div v-else class="properties-content">
      <!-- Cell Info -->
      <div class="property-section">
        <h4 class="section-title">Cell Info</h4>
        <div class="property-row">
          <span class="property-label">Position:</span>
          <span class="property-value">{{ selectedCell.x }}, {{ selectedCell.y }}</span>
        </div>
        <div class="property-row">
          <span class="property-label">Layer:</span>
          <span class="property-value">{{ selectedCell.layer }} ({{ layerName }})</span>
        </div>
        <div class="property-row">
          <span class="property-label">Terrain:</span>
          <select
            v-model="cellTerrain"
            class="terrain-select"
            @change="updateCellTerrain"
          >
            <option value="grass">Grass (1.0x)</option>
            <option value="road">Road (0.75x)</option>
            <option value="dirt">Dirt (1.0x)</option>
            <option value="sand">Sand (1.25x)</option>
            <option value="swamp">Swamp (2.0x)</option>
            <option value="water">Water (∞)</option>
            <option value="lava">Lava (∞)</option>
            <option value="snow">Snow (1.5x)</option>
            <option value="rock">Rock (∞)</option>
            <option value="forest">Forest (1.5x)</option>
            <option value="mountain">Mountain (∞)</option>
            <option value="void">Void (∞)</option>
          </select>
        </div>
        <div class="property-row">
          <span class="property-label">Passable:</span>
          <span :class="['property-value', cellPassable ? 'status-yes' : 'status-no']">
            {{ cellPassable ? 'Yes' : 'No' }}
          </span>
        </div>
        <div class="property-row">
          <span class="property-label">Movement Cost:</span>
          <span class="property-value">{{ movementCost }}</span>
        </div>
      </div>

      <!-- Connections -->
      <div class="property-section">
        <h4 class="section-title">Connections (Movement)</h4>
        <div class="connections-grid">
          <!-- Top row: NW, N, NE -->
          <button
            class="connection-btn north-west"
            :class="{ blocked: isEdgeBlocked('northWest') }"
            :disabled="!isDirectionEditable('northWest')"
            @click="toggleConnection('northWest')"
          >
            ↖ NW
          </button>
          <button
            class="connection-btn north"
            :class="{ blocked: isEdgeBlocked('north') }"
            :disabled="!isDirectionEditable('north')"
            @click="toggleConnection('north')"
          >
            ↑ North
          </button>
          <button
            class="connection-btn north-east"
            :class="{ blocked: isEdgeBlocked('northEast') }"
            :disabled="!isDirectionEditable('northEast')"
            @click="toggleConnection('northEast')"
          >
            ↗ NE
          </button>

          <!-- Middle row: W, (center spacer), E -->
          <button
            class="connection-btn west"
            :class="{ blocked: isEdgeBlocked('west') }"
            :disabled="!isDirectionEditable('west')"
            @click="toggleConnection('west')"
          >
            ← West
          </button>
          <div class="connection-center">Cell</div>
          <button
            class="connection-btn east"
            :class="{ blocked: isEdgeBlocked('east') }"
            :disabled="!isDirectionEditable('east')"
            @click="toggleConnection('east')"
          >
            → East
          </button>

          <!-- Bottom row: SW, S, SE -->
          <button
            class="connection-btn south-west"
            :class="{ blocked: isEdgeBlocked('southWest') }"
            :disabled="!isDirectionEditable('southWest')"
            @click="toggleConnection('southWest')"
          >
            ↙ SW
          </button>
          <button
            class="connection-btn south"
            :class="{ blocked: isEdgeBlocked('south') }"
            :disabled="!isDirectionEditable('south')"
            @click="toggleConnection('south')"
          >
            ↓ South
          </button>
          <button
            class="connection-btn south-east"
            :class="{ blocked: isEdgeBlocked('southEast') }"
            :disabled="!isDirectionEditable('southEast')"
            @click="toggleConnection('southEast')"
          >
            ↘ SE
          </button>
        </div>
      </div>

      <!-- Spawner Info -->
      <div v-if="cellData?.spawner" class="property-section">
        <h4 class="section-title">Spawner</h4>
        <div class="property-row">
          <span class="property-label">Type:</span>
          <span class="property-value spawner-type">{{ cellData.spawner.type }}</span>
        </div>
        <div v-if="cellData.spawner.properties.name" class="property-row">
          <span class="property-label">Name:</span>
          <span class="property-value">{{ cellData.spawner.properties.name }}</span>
        </div>
        <button class="remove-btn" @click="removeSpawner">Remove Spawner</button>
      </div>

      <!-- Game Object Info -->
      <div v-if="cellData?.gameObject" class="property-section">
        <h4 class="section-title">Game Object</h4>
        <div class="property-row">
          <span class="property-label">Type:</span>
          <span class="property-value object-type">{{ cellData.gameObject.type }}</span>
        </div>
        <div v-if="cellData.gameObject.properties.name" class="property-row">
          <span class="property-label">Name:</span>
          <span class="property-value">{{ cellData.gameObject.properties.name }}</span>
        </div>
        <button class="remove-btn" @click="removeGameObject">Remove Object</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import { TERRAIN_CONFIGS, DIRECTION_DELTAS } from '@/types/tabletop';

export default {
  name: 'PropertiesPanel',
  computed: {
    ...mapGetters('tabletopEditor', [
      'selectedCell',
      'getCell',
      'getEdge',
      'currentMap',
      'gridConfig'
    ]),
    cellData() {
      if (!this.selectedCell) return null;
      return this.getCell(this.selectedCell.x, this.selectedCell.y, this.selectedCell.layer);
    },
    layerName() {
      if (!this.selectedCell || !this.currentMap) return '';
      const layer = this.currentMap.layers.find(l => l.id === this.selectedCell.layer);
      return layer ? layer.name : '';
    },
    cellTerrain: {
      get() {
        if (!this.cellData) return 'grass';
        return this.cellData.terrain || 'grass';
      },
      set(value) {
        // This will be handled by updateCellTerrain method
      }
    },
    cellPassable() {
      if (!this.cellData) return true;
      return this.cellData.passable !== false;
    },
    movementCost() {
      if (!this.cellData || !this.cellData.terrain) return '1.0';
      const terrainConfig = TERRAIN_CONFIGS[this.cellData.terrain];
      if (!terrainConfig) return '1.0';
      const cost = terrainConfig.movementCost;
      return cost === Infinity ? '∞' : cost.toFixed(2);
    }
  },
  methods: {
    ...mapActions('tabletopEditor', [
      'toggleCellConnection',
      'clearCellContent',
      'updateCell'
    ]),
    updateCellTerrain() {
      if (!this.selectedCell) return;

      const terrain = this.cellTerrain;
      const terrainConfig = TERRAIN_CONFIGS[terrain];
      const passable = terrainConfig.movementCost !== Infinity;

      this.updateCell({
        x: this.selectedCell.x,
        y: this.selectedCell.y,
        layer: this.selectedCell.layer,
        updates: {
          terrain,
          passable
        }
      });
    },
    isEdgeBlocked(direction) {
      if (!this.selectedCell || !this.currentMap) return false;

      const delta = DIRECTION_DELTAS[direction];
      if (!delta) return false;

      const toX = this.selectedCell.x + delta.dx;
      const toY = this.selectedCell.y + delta.dy;

      const edge = this.getEdge(
        this.selectedCell.x,
        this.selectedCell.y,
        toX,
        toY,
        this.selectedCell.layer
      );

      // If edge doesn't exist, it's not blocked (default open)
      if (!edge) return false;

      return edge.blocked === true;
    },
    isDirectionEditable(direction) {
      if (!this.selectedCell || !this.gridConfig || !this.currentMap) return false;

      const layer = this.selectedCell.layer;

      // Check layer is active
      const layerMeta = Array.isArray(this.currentMap.layers)
        ? this.currentMap.layers.find(l => l.id === layer)
        : null;
      if (!layerMeta || layerMeta.active === false) return false;

      const { columns, rows } = this.gridConfig;

      const delta = DIRECTION_DELTAS[direction];
      if (!delta) return false;

      const fromCell = this.getCell(this.selectedCell.x, this.selectedCell.y, layer);
      const fromPassable = !fromCell || fromCell.passable !== false;
      if (!fromPassable) return false;

      const nx = this.selectedCell.x + delta.dx;
      const ny = this.selectedCell.y + delta.dy;

      // Off-grid neighbors are not editable
      if (nx < 0 || ny < 0 || nx >= columns || ny >= rows) {
        return false;
      }

      const neighborCell = this.getCell(nx, ny, layer);
      const neighborPassable = !neighborCell || neighborCell.passable !== false;

      return neighborPassable;
    },
    toggleConnection(direction) {
      if (!this.selectedCell) return;
      this.toggleCellConnection({
        x: this.selectedCell.x,
        y: this.selectedCell.y,
        layer: this.selectedCell.layer,
        direction
      });
    },
    removeSpawner() {
      if (!this.selectedCell) return;
      this.clearCellContent({
        x: this.selectedCell.x,
        y: this.selectedCell.y,
        layer: this.selectedCell.layer
      });
    },
    removeGameObject() {
      if (!this.selectedCell) return;
      this.clearCellContent({
        x: this.selectedCell.x,
        y: this.selectedCell.y,
        layer: this.selectedCell.layer
      });
    }
  }
};
</script>

<style scoped>
.properties-panel {
  background: rgba(20, 20, 30, 0.95);
  border: 1px solid rgba(100, 100, 150, 0.3);
  border-radius: 8px;
  padding: 15px;
  color: #e0e0e0;
  max-height: 600px;
  overflow-y: auto;
}

.properties-title {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: bold;
  color: #00d4ff;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.no-selection {
  text-align: center;
  padding: 30px 20px;
  color: #888;
}

.no-selection p {
  margin: 5px 0;
}

.hint {
  font-size: 12px;
  font-style: italic;
}

.properties-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.property-section {
  background: rgba(40, 40, 60, 0.4);
  border: 1px solid rgba(100, 100, 150, 0.2);
  border-radius: 6px;
  padding: 12px;
}

.section-title {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: bold;
  color: #00d4ff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.property-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid rgba(100, 100, 150, 0.1);
}

.property-row:last-child {
  border-bottom: none;
}

.property-label {
  font-size: 13px;
  color: #aaa;
  font-weight: 500;
}

.property-value {
  font-size: 13px;
  color: #fff;
  font-weight: 600;
}

.terrain-select {
  background: rgba(40, 40, 60, 0.8);
  border: 1px solid rgba(100, 100, 150, 0.5);
  border-radius: 4px;
  padding: 4px 8px;
  color: #00d4ff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.terrain-select:hover {
  border-color: #00d4ff;
  background: rgba(0, 212, 255, 0.1);
}

.terrain-select:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 8px rgba(0, 212, 255, 0.3);
}

.status-yes {
  color: #00ff00;
}

.status-no {
  color: #ff6b6b;
}

.spawner-type {
  text-transform: capitalize;
  color: #ffaa00;
}

.object-type {
  text-transform: capitalize;
  color: #00aaff;
}

.connections-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.connection-btn {
  background: rgba(0, 212, 255, 0.2);
  border: 2px solid #00d4ff;
  border-radius: 4px;
  padding: 8px;
  color: #00d4ff;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
  font-weight: 600;
}

.connection-center {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: #aaa;
}

.connection-btn:hover {
  background: rgba(0, 212, 255, 0.3);
  transform: scale(1.05);
}

.connection-btn.blocked {
  background: rgba(255, 0, 0, 0.2);
  border-color: #ff6b6b;
  color: #ff6b6b;
}

.connection-btn.blocked:hover {
  background: rgba(255, 0, 0, 0.3);
}

.remove-btn {
  width: 100%;
  margin-top: 10px;
  background: rgba(255, 0, 0, 0.2);
  border: 2px solid #ff6b6b;
  border-radius: 4px;
  padding: 8px;
  color: #ff6b6b;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 13px;
  font-weight: 600;
}

.remove-btn:hover {
  background: rgba(255, 0, 0, 0.3);
  transform: scale(1.02);
}

/* Scrollbar styling */
.properties-panel::-webkit-scrollbar {
  width: 6px;
}

.properties-panel::-webkit-scrollbar-track {
  background: rgba(20, 20, 30, 0.5);
  border-radius: 3px;
}

.properties-panel::-webkit-scrollbar-thumb {
  background: rgba(0, 212, 255, 0.3);
  border-radius: 3px;
}

.properties-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 212, 255, 0.5);
}
</style>
