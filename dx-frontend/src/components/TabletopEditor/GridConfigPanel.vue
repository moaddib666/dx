<template>
  <div class="grid-config-panel">
    <h3 class="config-title">Grid Configuration</h3>

    <div v-if="!gridConfig" class="no-config">
      <p>No map loaded</p>
    </div>

    <div v-else class="config-content">
      <!-- Grid Dimensions -->
      <div class="config-section">
        <h4 class="section-title">Grid Dimensions</h4>

        <div class="config-row">
          <label class="config-label">Columns:</label>
          <input
            type="number"
            class="config-input"
            :value="gridConfig.columns"
            @input="updateColumns"
            min="5"
            max="100"
          />
        </div>

        <div class="config-row">
          <label class="config-label">Rows:</label>
          <input
            type="number"
            class="config-input"
            :value="gridConfig.rows"
            @input="updateRows"
            min="5"
            max="100"
          />
        </div>
      </div>

      <!-- Cell Size -->
      <div class="config-section">
        <h4 class="section-title">Cell Size (pixels)</h4>

        <div class="config-row">
          <label class="config-label">Width:</label>
          <input
            type="number"
            class="config-input"
            :value="gridConfig.cellWidth"
            @input="updateCellWidth"
            min="16"
            max="256"
          />
        </div>

        <div class="config-row">
          <label class="config-label">Height:</label>
          <input
            type="number"
            class="config-input"
            :value="gridConfig.cellHeight"
            @input="updateCellHeight"
            min="16"
            max="256"
          />
        </div>
      </div>

      <!-- Perspective Morph -->
      <div class="config-section">
        <h4 class="section-title">Perspective Morph</h4>
        <p class="section-hint">Adjust for isometric/angled views (-1.0 to 1.0)</p>

        <div class="config-row">
          <label class="config-label">X Morph:</label>
          <input
            type="number"
            class="config-input"
            :value="gridConfig.xMorph"
            @input="updateXMorph"
            min="-1"
            max="1"
            step="0.1"
          />
        </div>

        <div class="config-row">
          <label class="config-label">Y Morph:</label>
          <input
            type="number"
            class="config-input"
            :value="gridConfig.yMorph"
            @input="updateYMorph"
            min="-1"
            max="1"
            step="0.1"
          />
        </div>
      </div>

      <!-- Grid Info -->
      <div class="config-section info-section">
        <h4 class="section-title">Grid Info</h4>
        <div class="info-row">
          <span class="info-label">Total Cells:</span>
          <span class="info-value">{{ totalCells }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Grid Size:</span>
          <span class="info-value">{{ gridWidth }} × {{ gridHeight }} px</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'GridConfigPanel',
  computed: {
    ...mapGetters('tabletopEditor', [
      'gridConfig'
    ]),
    totalCells() {
      if (!this.gridConfig) return 0;
      return this.gridConfig.columns * this.gridConfig.rows;
    },
    gridWidth() {
      if (!this.gridConfig) return 0;
      return this.gridConfig.columns * this.gridConfig.cellWidth;
    },
    gridHeight() {
      if (!this.gridConfig) return 0;
      return this.gridConfig.rows * this.gridConfig.cellHeight;
    }
  },
  methods: {
    ...mapActions('tabletopEditor', [
      'updateGridConfig'
    ]),
    updateColumns(event) {
      const value = parseInt(event.target.value);
      if (!isNaN(value) && value >= 5 && value <= 100) {
        this.updateGridConfig({ columns: value });
      }
    },
    updateRows(event) {
      const value = parseInt(event.target.value);
      if (!isNaN(value) && value >= 5 && value <= 100) {
        this.updateGridConfig({ rows: value });
      }
    },
    updateCellWidth(event) {
      const value = parseInt(event.target.value);
      if (!isNaN(value) && value >= 16 && value <= 256) {
        this.updateGridConfig({ cellWidth: value });
      }
    },
    updateCellHeight(event) {
      const value = parseInt(event.target.value);
      if (!isNaN(value) && value >= 16 && value <= 256) {
        this.updateGridConfig({ cellHeight: value });
      }
    },
    updateXMorph(event) {
      const value = parseFloat(event.target.value);
      if (!isNaN(value) && value >= -1 && value <= 1) {
        this.updateGridConfig({ xMorph: value });
      }
    },
    updateYMorph(event) {
      const value = parseFloat(event.target.value);
      if (!isNaN(value) && value >= -1 && value <= 1) {
        this.updateGridConfig({ yMorph: value });
      }
    }
  }
};
</script>

<style scoped>
.grid-config-panel {
  background: rgba(20, 20, 30, 0.95);
  border: 1px solid rgba(100, 100, 150, 0.3);
  border-radius: 8px;
  padding: 15px;
  color: #e0e0e0;
  max-height: 600px;
  overflow-y: auto;
}

.config-title {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: bold;
  color: #00d4ff;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.no-config {
  text-align: center;
  padding: 30px 20px;
  color: #888;
}

.config-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.config-section {
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

.section-hint {
  margin: 0 0 10px 0;
  font-size: 11px;
  color: #888;
  font-style: italic;
}

.config-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  gap: 10px;
}

.config-label {
  font-size: 13px;
  color: #aaa;
  font-weight: 500;
  flex: 1;
}

.config-input {
  width: 80px;
  background: rgba(20, 20, 30, 0.8);
  border: 1px solid rgba(100, 100, 150, 0.4);
  border-radius: 4px;
  padding: 6px 8px;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  text-align: right;
}

.config-input:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 5px rgba(0, 212, 255, 0.3);
}

.info-section {
  background: rgba(0, 212, 255, 0.1);
  border-color: rgba(0, 212, 255, 0.3);
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
}

.info-label {
  font-size: 13px;
  color: #aaa;
  font-weight: 500;
}

.info-value {
  font-size: 13px;
  color: #00d4ff;
  font-weight: 700;
}

/* Scrollbar styling */
.grid-config-panel::-webkit-scrollbar {
  width: 6px;
}

.grid-config-panel::-webkit-scrollbar-track {
  background: rgba(20, 20, 30, 0.5);
  border-radius: 3px;
}

.grid-config-panel::-webkit-scrollbar-thumb {
  background: rgba(0, 212, 255, 0.3);
  border-radius: 3px;
}

.grid-config-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 212, 255, 0.5);
}
</style>
