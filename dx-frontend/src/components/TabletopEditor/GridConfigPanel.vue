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

      <!-- Perspective Morph (Legacy) -->
      <div class="config-section">
        <h4 class="section-title">Perspective Morph (Legacy)</h4>
        <p class="section-hint">Simple axis-based morphing (-1.0 to 1.0)</p>

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

      <!-- 4-Point Morphing -->
      <div class="config-section">
        <h4 class="section-title">4-Point Morphing</h4>
        <p class="section-hint">Adjust corner positions for perspective/rhomboid (-1.0 to 1.0)</p>

        <!-- Top Left Corner -->
        <div class="corner-group">
          <label class="corner-label">Top Left:</label>
          <div class="corner-inputs">
            <div class="config-row-compact">
              <label class="config-label-small">X:</label>
              <input
                type="number"
                class="config-input-small"
                :value="cornerOffsets.topLeft.x"
                @input="updateCornerOffset('topLeft', 'x', $event)"
                min="-1"
                max="1"
                step="0.05"
              />
            </div>
            <div class="config-row-compact">
              <label class="config-label-small">Y:</label>
              <input
                type="number"
                class="config-input-small"
                :value="cornerOffsets.topLeft.y"
                @input="updateCornerOffset('topLeft', 'y', $event)"
                min="-1"
                max="1"
                step="0.05"
              />
            </div>
          </div>
        </div>

        <!-- Top Right Corner -->
        <div class="corner-group">
          <label class="corner-label">Top Right:</label>
          <div class="corner-inputs">
            <div class="config-row-compact">
              <label class="config-label-small">X:</label>
              <input
                type="number"
                class="config-input-small"
                :value="cornerOffsets.topRight.x"
                @input="updateCornerOffset('topRight', 'x', $event)"
                min="-1"
                max="1"
                step="0.05"
              />
            </div>
            <div class="config-row-compact">
              <label class="config-label-small">Y:</label>
              <input
                type="number"
                class="config-input-small"
                :value="cornerOffsets.topRight.y"
                @input="updateCornerOffset('topRight', 'y', $event)"
                min="-1"
                max="1"
                step="0.05"
              />
            </div>
          </div>
        </div>

        <!-- Bottom Left Corner -->
        <div class="corner-group">
          <label class="corner-label">Bottom Left:</label>
          <div class="corner-inputs">
            <div class="config-row-compact">
              <label class="config-label-small">X:</label>
              <input
                type="number"
                class="config-input-small"
                :value="cornerOffsets.bottomLeft.x"
                @input="updateCornerOffset('bottomLeft', 'x', $event)"
                min="-1"
                max="1"
                step="0.05"
              />
            </div>
            <div class="config-row-compact">
              <label class="config-label-small">Y:</label>
              <input
                type="number"
                class="config-input-small"
                :value="cornerOffsets.bottomLeft.y"
                @input="updateCornerOffset('bottomLeft', 'y', $event)"
                min="-1"
                max="1"
                step="0.05"
              />
            </div>
          </div>
        </div>

        <!-- Bottom Right Corner -->
        <div class="corner-group">
          <label class="corner-label">Bottom Right:</label>
          <div class="corner-inputs">
            <div class="config-row-compact">
              <label class="config-label-small">X:</label>
              <input
                type="number"
                class="config-input-small"
                :value="cornerOffsets.bottomRight.x"
                @input="updateCornerOffset('bottomRight', 'x', $event)"
                min="-1"
                max="1"
                step="0.05"
              />
            </div>
            <div class="config-row-compact">
              <label class="config-label-small">Y:</label>
              <input
                type="number"
                class="config-input-small"
                :value="cornerOffsets.bottomRight.y"
                @input="updateCornerOffset('bottomRight', 'y', $event)"
                min="-1"
                max="1"
                step="0.05"
              />
            </div>
          </div>
        </div>

        <!-- Reset Button -->
        <button class="reset-button" @click="resetCornerOffsets">
          Reset to Default
        </button>
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
    },
    cornerOffsets() {
      if (!this.gridConfig || !this.gridConfig.cornerOffsets) {
        return {
          topLeft: { x: 0, y: 0 },
          topRight: { x: 0, y: 0 },
          bottomLeft: { x: 0, y: 0 },
          bottomRight: { x: 0, y: 0 }
        };
      }
      return this.gridConfig.cornerOffsets;
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
    },
    updateCornerOffset(corner, axis, event) {
      const value = parseFloat(event.target.value);
      if (!isNaN(value) && value >= -1 && value <= 1) {
        const newCornerOffsets = {
          ...this.cornerOffsets,
          [corner]: {
            ...this.cornerOffsets[corner],
            [axis]: value
          }
        };
        this.updateGridConfig({ cornerOffsets: newCornerOffsets });
      }
    },
    resetCornerOffsets() {
      const defaultOffsets = {
        topLeft: { x: 0, y: 0 },
        topRight: { x: 0, y: 0 },
        bottomLeft: { x: 0, y: 0 },
        bottomRight: { x: 0, y: 0 }
      };
      this.updateGridConfig({ cornerOffsets: defaultOffsets });
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

/* 4-Point Morphing Styles */
.corner-group {
  margin-bottom: 12px;
  padding: 8px;
  background: rgba(20, 20, 30, 0.5);
  border-radius: 4px;
}

.corner-label {
  display: block;
  font-size: 12px;
  color: #00d4ff;
  font-weight: 600;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.corner-inputs {
  display: flex;
  gap: 10px;
}

.config-row-compact {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
}

.config-label-small {
  font-size: 11px;
  color: #aaa;
  font-weight: 500;
  min-width: 15px;
}

.config-input-small {
  flex: 1;
  background: rgba(20, 20, 30, 0.8);
  border: 1px solid rgba(100, 100, 150, 0.4);
  border-radius: 4px;
  padding: 4px 6px;
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  text-align: right;
}

.config-input-small:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 5px rgba(0, 212, 255, 0.3);
}

.reset-button {
  width: 100%;
  margin-top: 10px;
  padding: 8px 12px;
  background: rgba(0, 212, 255, 0.15);
  border: 1px solid rgba(0, 212, 255, 0.4);
  border-radius: 4px;
  color: #00d4ff;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-button:hover {
  background: rgba(0, 212, 255, 0.25);
  border-color: #00d4ff;
  box-shadow: 0 0 8px rgba(0, 212, 255, 0.3);
}

.reset-button:active {
  transform: scale(0.98);
}
</style>
