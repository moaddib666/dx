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
          <span class="property-label">Available:</span>
          <span :class="['property-value', cellData?.available ? 'status-yes' : 'status-no']">
            {{ cellData?.available ? 'Yes' : 'No' }}
          </span>
        </div>
      </div>

      <!-- Connections -->
      <div class="property-section">
        <h4 class="section-title">Connections (Movement)</h4>
        <div class="connections-grid">
          <button
            class="connection-btn north"
            :class="{ blocked: cellData && !cellData.connections.north }"
            @click="toggleConnection('north')"
          >
            ↑ North
          </button>
          <button
            class="connection-btn west"
            :class="{ blocked: cellData && !cellData.connections.west }"
            @click="toggleConnection('west')"
          >
            ← West
          </button>
          <button
            class="connection-btn east"
            :class="{ blocked: cellData && !cellData.connections.east }"
            @click="toggleConnection('east')"
          >
            → East
          </button>
          <button
            class="connection-btn south"
            :class="{ blocked: cellData && !cellData.connections.south }"
            @click="toggleConnection('south')"
          >
            ↓ South
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

export default {
  name: 'PropertiesPanel',
  computed: {
    ...mapGetters('tabletopEditor', [
      'selectedCell',
      'getCell',
      'currentMap'
    ]),
    cellData() {
      if (!this.selectedCell) return null;
      return this.getCell(this.selectedCell.x, this.selectedCell.y, this.selectedCell.layer);
    },
    layerName() {
      if (!this.selectedCell || !this.currentMap) return '';
      const layer = this.currentMap.layers.find(l => l.id === this.selectedCell.layer);
      return layer ? layer.name : '';
    }
  },
  methods: {
    ...mapActions('tabletopEditor', [
      'toggleCellConnection',
      'clearCellContent'
    ]),
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
  grid-template-columns: 1fr 1fr;
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
