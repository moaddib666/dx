<template>
  <div class="tabletop-map-editor">
    <!-- Top Toolbar -->
    <div class="editor-toolbar">
      <div class="toolbar-section">
        <h1 class="editor-title">Tabletop Map Editor</h1>
        <span v-if="currentMap?.metadata?.name" class="map-name">{{ currentMap.metadata.name }}</span>
      </div>

      <div class="toolbar-section toolbar-actions">
        <button class="toolbar-btn" @click="showNewMapDialog = true">
          <span class="btn-icon">📄</span>
          New Map
        </button>
        <button class="toolbar-btn" @click="importMap">
          <span class="btn-icon">📂</span>
          Import
        </button>
        <button class="toolbar-btn" @click="exportMap" :disabled="!currentMap">
          <span class="btn-icon">💾</span>
          Export
        </button>
        <button class="toolbar-btn" @click="importBackground" :disabled="!currentMap">
          <span class="btn-icon">🖼️</span>
          Background
        </button>
        <button class="toolbar-btn automap-btn" @click="handleAutoMap" :disabled="!currentMap">
          <span class="btn-icon">🗺️</span>
          Auto-map
        </button>
        <button
          class="toolbar-btn save-btn"
          @click="handleSaveMap"
          :disabled="!isDirty"
        >
          <span class="btn-icon">✅</span>
          {{ isDirty ? 'Save*' : 'Saved' }}
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="editor-content">
      <!-- Left Panel -->
      <div class="left-panel">
        <ToolPanel />
        <LayerSelector />
      </div>

      <!-- Center Panel - Canvas -->
      <div class="center-panel">
        <div v-if="!currentMap" class="no-map-message">
          <h2>No Map Loaded</h2>
          <p>Create a new map or import an existing one to get started</p>
          <button class="create-map-btn" @click="showNewMapDialog = true">
            Create New Map
          </button>
        </div>
        <MapCanvas v-else :key="currentMap?.metadata?.created || 'default'" ref="mapCanvas" />
      </div>

      <!-- Right Panel -->
      <div class="right-panel">
        <!-- In normal editing modes, show cell Properties; in Map Config mode, show Grid Configuration -->
        <PropertiesPanel v-if="editorMode !== 'config'" />
        <GridConfigPanel v-else />
      </div>
    </div>

    <!-- New Map Dialog -->
    <div v-if="showNewMapDialog" class="modal-overlay" @click.self="showNewMapDialog = false">
      <div class="modal-dialog">
        <h2 class="modal-title">Create New Map</h2>
        <div class="modal-content">
          <div class="form-group">
            <label>Map Name:</label>
            <input
              v-model="newMapName"
              type="text"
              class="form-input"
              placeholder="Enter map name"
              @keyup.enter="handleCreateNewMap"
            />
          </div>
          <div class="form-group">
            <label>Author:</label>
            <input
              v-model="newMapAuthor"
              type="text"
              class="form-input"
              placeholder="Your name"
              @keyup.enter="handleCreateNewMap"
            />
          </div>
        </div>
        <div class="modal-actions">
          <button class="modal-btn cancel-btn" @click="showNewMapDialog = false">
            Cancel
          </button>
          <button class="modal-btn create-btn" @click="handleCreateNewMap">
            Create
          </button>
        </div>
      </div>
    </div>

    <!-- Hidden file inputs -->
    <input
      ref="importInput"
      type="file"
      accept=".png,.json,image/png,application/json"
      style="display: none"
      @change="handleImportFile"
    />
    <input
      ref="backgroundInput"
      type="file"
      accept="image/*"
      style="display: none"
      @change="handleBackgroundFile"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import MapCanvas from '@/components/TabletopEditor/MapCanvas.vue';
import LayerSelector from '@/components/TabletopEditor/LayerSelector.vue';
import ToolPanel from '@/components/TabletopEditor/ToolPanel.vue';
import PropertiesPanel from '@/components/TabletopEditor/PropertiesPanel.vue';
import GridConfigPanel from '@/components/TabletopEditor/GridConfigPanel.vue';
import { embedMetadataInPNG, extractMetadataFromPNG } from '@/utils/pngMetadata.js';

// ----- Movement edge map helpers -----
const CARDINAL_DELTAS = {
  north: { dx: 0, dy: -1 },
  south: { dx: 0, dy: 1 },
  east: { dx: 1, dy: 0 },
  west: { dx: -1, dy: 0 }
};

const OPPOSITE_DIRECTION = {
  north: 'south',
  south: 'north',
  east: 'west',
  west: 'east'
};

const DIAGONAL_DELTAS = {
  northEast: { dx: 1, dy: -1 },
  northWest: { dx: -1, dy: -1 },
  southEast: { dx: 1, dy: 1 },
  southWest: { dx: -1, dy: 1 }
};

const OPPOSITE_DIAGONAL_DIRECTION = {
  northEast: 'southWest',
  southWest: 'northEast',
  northWest: 'southEast',
  southEast: 'northWest'
};

function buildCellLookup(cells) {
  const lookup = new Map();
  if (Array.isArray(cells)) {
    cells.forEach(cell => {
      lookup.set(`${cell.x},${cell.y},${cell.layer}`, cell);
    });
  }
  return lookup;
}

function getCellState(mapData, lookup, x, y, layerId) {
  if (!mapData || !mapData.grid) {
    return {
      available: false,
      connections: {
        north: false,
        south: false,
        east: false,
        west: false,
        northEast: false,
        northWest: false,
        southEast: false,
        southWest: false
      }
    };
  }

  const { columns, rows } = mapData.grid;

  // Out of bounds -> treated as unavailable
  if (x < 0 || y < 0 || x >= columns || y >= rows) {
    return {
      available: false,
      connections: {
        north: false,
        south: false,
        east: false,
        west: false,
        northEast: false,
        northWest: false,
        southEast: false,
        southWest: false
      }
    };
  }

  const layerMeta = Array.isArray(mapData.layers)
    ? mapData.layers.find(l => l.id === layerId)
    : null;

  if (!layerMeta || layerMeta.active === false) {
    return {
      available: false,
      connections: {
        north: false,
        south: false,
        east: false,
        west: false,
        northEast: false,
        northWest: false,
        southEast: false,
        southWest: false
      }
    };
  }

  const key = `${x},${y},${layerId}`;
  const cell = lookup.get(key);

  if (!cell) {
    // No explicit cell data -> treat as a default available cell with all connections open
    return {
      available: true,
      connections: {
        north: true,
        south: true,
        east: true,
        west: true,
        // Diagonals default to open unless explicitly blocked
        northEast: undefined,
        northWest: undefined,
        southEast: undefined,
        southWest: undefined
      }
    };
  }

  const connections = cell.connections || {};

  return {
    available: cell.available !== false,
    connections: {
      north: connections.north !== false,
      south: connections.south !== false,
      east: connections.east !== false,
      west: connections.west !== false,
      // Diagonal flags are interpreted as: false => blocked, anything else => open
      northEast: connections.northEast,
      northWest: connections.northWest,
      southEast: connections.southEast,
      southWest: connections.southWest
    }
  };
}

function canCardinalMove(mapData, lookup, x, y, layerId, direction) {
  const deltas = CARDINAL_DELTAS[direction];
  if (!deltas) return false;

  const fromState = getCellState(mapData, lookup, x, y, layerId);
  if (!fromState.available) return false;

  const targetX = x + deltas.dx;
  const targetY = y + deltas.dy;
  const toState = getCellState(mapData, lookup, targetX, targetY, layerId);

  if (!toState.available) return false;

  const opposite = OPPOSITE_DIRECTION[direction];
  return !!fromState.connections[direction] && !!toState.connections[opposite];
}

function canDiagonalMove(mapData, lookup, x, y, layerId, direction) {
  const deltas = DIAGONAL_DELTAS[direction];
  if (!deltas) return false;

  const fromState = getCellState(mapData, lookup, x, y, layerId);
  if (!fromState.available) return false;

  const targetX = x + deltas.dx;
  const targetY = y + deltas.dy;
  const toState = getCellState(mapData, lookup, targetX, targetY, layerId);
  if (!toState.available) return false;

  // Enforce no corner cutting: diagonal move only if both related
  // cardinal moves are possible from the source cell.
  const requires = {
    northEast: ['north', 'east'],
    northWest: ['north', 'west'],
    southEast: ['south', 'east'],
    southWest: ['south', 'west']
  };

  const deps = requires[direction] || [];
  if (deps.length === 2) {
    if (
      !canCardinalMove(mapData, lookup, x, y, layerId, deps[0]) ||
      !canCardinalMove(mapData, lookup, x, y, layerId, deps[1])
    ) {
      return false;
    }
  }

  // Diagonal flags: if either side explicitly blocks this diagonal,
  // the move is not allowed. When undefined, it is treated as open.
  const fromDiag = fromState.connections && fromState.connections[direction];
  const oppositeDiag = OPPOSITE_DIAGONAL_DIRECTION[direction];
  const toDiag = oppositeDiag && toState.connections
    ? toState.connections[oppositeDiag]
    : undefined;

  if (fromDiag === false || toDiag === false) {
    return false;
  }

  return true;
}

function buildMovementEdges(mapData) {
  if (!mapData || !mapData.grid || !Array.isArray(mapData.layers)) {
    return [];
  }

  const { columns, rows } = mapData.grid;
  const lookup = buildCellLookup(mapData.cells || []);
  const edges = [];

  mapData.layers.forEach(layerMeta => {
    if (!layerMeta || layerMeta.active === false) return;

    const layerId = layerMeta.id;

    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < columns; x++) {
        const fromState = getCellState(mapData, lookup, x, y, layerId);
        if (!fromState.available) continue;

        // Cardinal edges
        Object.keys(CARDINAL_DELTAS).forEach(direction => {
          if (canCardinalMove(mapData, lookup, x, y, layerId, direction)) {
            const { dx, dy } = CARDINAL_DELTAS[direction];
            edges.push({
              from: { x, y, layer: layerId },
              to: { x: x + dx, y: y + dy, layer: layerId },
              direction
            });
          }
        });

        // Diagonal edges derived from cardinal movement
        const diagonals = [
          { direction: 'northEast', dx: 1, dy: -1 },
          { direction: 'northWest', dx: -1, dy: -1 },
          { direction: 'southEast', dx: 1, dy: 1 },
          { direction: 'southWest', dx: -1, dy: 1 }
        ];

        diagonals.forEach(({ direction, dx, dy }) => {
          if (canDiagonalMove(mapData, lookup, x, y, layerId, direction)) {
            const targetState = getCellState(mapData, lookup, x + dx, y + dy, layerId);
            if (!targetState.available) return;

            edges.push({
              from: { x, y, layer: layerId },
              to: { x: x + dx, y: y + dy, layer: layerId },
              direction
            });
          }
        });
      }
    }
  });

  return edges;
}

export default {
  name: 'TabletopMapEditor',
  components: {
    MapCanvas,
    LayerSelector,
    ToolPanel,
    PropertiesPanel,
    GridConfigPanel
  },
  data() {
    return {
      showNewMapDialog: false,
      newMapName: '',
      newMapAuthor: ''
    };
  },
  computed: {
    ...mapGetters('tabletopEditor', [
      'currentMap',
      'isDirty',
      'editorMode'
    ])
  },
  methods: {
    ...mapActions('tabletopEditor', [
      'createNewMap',
      'loadMap',
      'saveMap',
      'setBackgroundImage',
      'updateGridConfig',
      'autoGenerateEdges'
    ]),

    handleCreateNewMap() {
      if (!this.newMapName.trim()) {
        return;
      }

      this.createNewMap({
        name: this.newMapName.trim(),
        author: this.newMapAuthor.trim() || 'Unknown'
      });

      this.showNewMapDialog = false;
      this.newMapName = '';
      this.newMapAuthor = '';
    },

    importMap() {
      this.$refs.importInput.click();
    },

    async handleImportFile(event) {
      const file = event.target.files[0];
      if (!file) return;

      console.log('[Import] Starting import process for file:', file.name, 'Type:', file.type);

      try {
        // Check if it's a PNG file
        if (file.type === 'image/png' || file.name.toLowerCase().endsWith('.png')) {
          console.log('[Import] Detected PNG file, extracting metadata...');

          // Extract metadata from PNG
          const { mapData, imageDataURL, hasMetadata, imageWidth, imageHeight } = await extractMetadataFromPNG(file);

          if (hasMetadata && mapData) {
            // PNG has embedded map data - load it
            console.log('[Import] ✅ PNG has metadata - loading existing map data');
            console.log('[Import] Calling loadMap with mapData:', {
              name: mapData.metadata?.name,
              grid: mapData.grid,
              layersCount: mapData.layers?.length,
              cellsCount: mapData.cells?.length,
              edgesCount: mapData.edges?.length
            });
            this.loadMap(mapData);

            console.log('[Import] Setting background image...');
            this.setBackgroundImage(imageDataURL);

            console.log('[Import] ✅ Map import completed successfully!');
          } else {
            // PNG has no metadata - create default map based on image size
            console.log('[Import] ⚠️ PNG has no metadata - creating default map from image');

            const defaultCellSize = 64; // Default cell size in pixels
            const columns = Math.max(5, Math.floor(imageWidth / defaultCellSize));
            const rows = Math.max(5, Math.floor(imageHeight / defaultCellSize));

            console.log('[Import] Calculated grid:', { columns, rows, cellSize: defaultCellSize });

            // Create a new map with calculated dimensions
            const mapName = file.name.replace(/\.(png|PNG)$/, '') || 'Imported Map';
            console.log('[Import] Creating new map:', mapName);
            this.createNewMap({
              name: mapName,
              author: 'Unknown'
            });

            // Update grid configuration to match image dimensions
            console.log('[Import] Updating grid config...');
            this.updateGridConfig({
              columns,
              rows,
              cellWidth: defaultCellSize,
              cellHeight: defaultCellSize
            });

            // Set the PNG as background
            console.log('[Import] Setting background image...');
            this.setBackgroundImage(imageDataURL);

            console.log('[Import] ✅ Default map created successfully!');
          }
        } else if (file.type === 'application/json' || file.name.toLowerCase().endsWith('.json')) {
          // Legacy JSON import support
          console.log('[Import] Detected JSON file, loading...');
          const reader = new FileReader();
          reader.onload = (e) => {
            try {
              const mapData = JSON.parse(e.target.result);
              console.log('[Import] JSON parsed, loading map...');
              this.loadMap(mapData);
              console.log('[Import] ✅ JSON map imported successfully!');
            } catch (error) {
              console.error('[Import] ❌ Error parsing JSON:', error);
            }
          };
          reader.readAsText(file);
        } else {
          console.warn('[Import] ❌ Unsupported file format:', file.type);
        }
      } catch (error) {
        console.error('[Import] ❌ Import error:', error);
      }

      // Reset input
      event.target.value = '';
    },

    async exportMap() {
      if (!this.currentMap) return;

      try {
        console.log('[Export] Starting export process...');
        console.log('[Export] Current map data:', {
          hasMetadata: !!this.currentMap.metadata,
          metadataName: this.currentMap.metadata?.name,
          hasGrid: !!this.currentMap.grid,
          gridConfig: this.currentMap.grid,
          hasLayers: !!this.currentMap.layers,
          layersCount: this.currentMap.layers?.length,
          hasCells: !!this.currentMap.cells,
          cellsCount: this.currentMap.cells?.length,
          hasBackgroundImage: !!this.currentMap.backgroundImage
        });

        // Get the current map data from the getter (not from saveMap action which returns undefined)
        const mapData = this.currentMap;
        console.log('[Export] Map data retrieved:', mapData ? 'valid object' : 'null/undefined');

        // Create a clean copy of mapData WITHOUT the backgroundImage property
        // The backgroundImage should not be embedded in metadata since the image IS the PNG itself
        const { backgroundImage, ...mapDataWithoutImage } = mapData;
        console.log('[Export] Map data after removing backgroundImage:', {
          hasMetadata: !!mapDataWithoutImage.metadata,
          hasGrid: !!mapDataWithoutImage.grid,
          hasLayers: !!mapDataWithoutImage.layers,
          hasCells: !!mapDataWithoutImage.cells,
          cellsCount: mapDataWithoutImage.cells?.length
        });

        // Use existing edges from store instead of rebuilding
        // This preserves the exact state of edges including manual edits and auto-generated paths
        console.log('[Export] Using existing edges from store...');
        const edges = this.currentMap.edges || [];
        mapDataWithoutImage.edges = edges;
        console.log('[Export] Edges count:', Array.isArray(edges) ? edges.length : 0);

        // Log detailed cell data to verify changes are captured
        if (mapDataWithoutImage.cells && mapDataWithoutImage.cells.length > 0) {
          console.log('[Export] First 5 cells data:', mapDataWithoutImage.cells.slice(0, 5).map(cell => ({
            x: cell.x,
            y: cell.y,
            layer: cell.layer,
            available: cell.available,
            hasSpawner: !!cell.spawner,
            spawnerType: cell.spawner?.type,
            hasGameObject: !!cell.gameObject,
            connections: cell.connections
          })));
        }

        // Deep clone to ensure we're not passing references
        console.log('[Export] Creating deep clone of mapDataWithoutImage for export...');
        const mapDataToExport = JSON.parse(JSON.stringify(mapDataWithoutImage));
        console.log('[Export] Deep clone created, cells count:', mapDataToExport.cells?.length);

        let imageSource;

        // Use the original background image if available
        if (this.currentMap.backgroundImage) {
          // Export the clean background image with metadata embedded
          imageSource = this.currentMap.backgroundImage;
        } else {
          // No background image - create a blank PNG based on grid dimensions
          const { cellWidth, cellHeight, columns, rows } = this.currentMap.grid;
          const canvas = document.createElement('canvas');
          canvas.width = columns * cellWidth;
          canvas.height = rows * cellHeight;
          const ctx = canvas.getContext('2d');

          // Fill with dark background
          ctx.fillStyle = '#1a1a1a';
          ctx.fillRect(0, 0, canvas.width, canvas.height);

          imageSource = canvas;
        }

        // Embed metadata in PNG (using original background, not rendered overlays)
        // Use mapDataToExport (deep cloned) to ensure no reference issues
        const pngBlob = await embedMetadataInPNG(imageSource, mapDataToExport);

        // Download the PNG file
        const url = URL.createObjectURL(pngBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.currentMap.metadata.name.replace(/\s+/g, '_')}.png`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        // Mark map as clean (not dirty) after successful export
        this.saveMap();
        console.log('[Export] ✅ Export completed successfully!');

      } catch (error) {
        console.error('Export error:', error);
      }
    },

    importBackground() {
      this.$refs.backgroundInput.click();
    },

    handleBackgroundFile(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        this.setBackgroundImage(e.target.result);
      };
      reader.readAsDataURL(file);

      // Reset input
      event.target.value = '';
    },

    handleSaveMap() {
      this.saveMap();
    },

    handleAutoMap() {
      if (!this.currentMap) return;

      const message =
        'Auto-map will automatically generate movement paths for all passable cells.\n\n' +
        '⚠️ WARNING: This will REPLACE all existing edges/connections!\n\n' +
        'The system will:\n' +
        '• Create edges between all adjacent passable cells\n' +
        '• Include both cardinal (N, S, E, W) and diagonal (NE, NW, SE, SW) connections\n' +
        '• Skip impassable cells (rock, water, mountain, etc.)\n' +
        '• Work on all active layers\n\n' +
        'Do you want to continue?';

      if (confirm(message)) {
        console.log('[Auto-map] User confirmed, generating edges...');
        this.autoGenerateEdges();
        console.log('[Auto-map] ✅ Edge generation complete! Check console for details.');
        alert('Auto-map complete! Edges have been generated for all passable cells. Don\'t forget to save your map.');
      } else {
        console.log('[Auto-map] User cancelled edge generation');
      }
    }
  },
  beforeUnmount() {
    // Warn if there are unsaved changes
    if (this.isDirty) {
      const confirmLeave = confirm('You have unsaved changes. Are you sure you want to leave?');
      if (!confirmLeave) {
        return false;
      }
    }
  }
};
</script>

<style scoped>
.tabletop-map-editor {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #0a0a0a;
  color: #e0e0e0;
  overflow: hidden;
}

/* Toolbar */
.editor-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(20, 20, 30, 0.95);
  border-bottom: 2px solid rgba(0, 212, 255, 0.3);
  padding: 12px 20px;
  gap: 20px;
}

.toolbar-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

.editor-title {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
  color: #00d4ff;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.map-name {
  font-size: 14px;
  color: #aaa;
  font-style: italic;
}

.toolbar-actions {
  display: flex;
  gap: 10px;
}

.toolbar-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(40, 40, 60, 0.8);
  border: 2px solid rgba(100, 100, 150, 0.3);
  border-radius: 6px;
  padding: 8px 16px;
  color: #e0e0e0;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  font-weight: 600;
}

.toolbar-btn:hover:not(:disabled) {
  background: rgba(60, 60, 80, 0.9);
  border-color: rgba(0, 212, 255, 0.5);
  transform: translateY(-2px);
}

.toolbar-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.toolbar-btn.save-btn {
  background: rgba(0, 212, 255, 0.2);
  border-color: #00d4ff;
  color: #00d4ff;
}

.toolbar-btn.save-btn:hover:not(:disabled) {
  background: rgba(0, 212, 255, 0.3);
}

.toolbar-btn.automap-btn {
  background: rgba(255, 165, 0, 0.2);
  border-color: #ffa500;
  color: #ffa500;
}

.toolbar-btn.automap-btn:hover:not(:disabled) {
  background: rgba(255, 165, 0, 0.3);
  box-shadow: 0 4px 12px rgba(255, 165, 0, 0.3);
}

.btn-icon {
  font-size: 16px;
}

/* Main Content */
.editor-content {
  display: flex;
  flex: 1;
  overflow: hidden;
  gap: 10px;
  padding: 10px;
}

.left-panel,
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 280px;
  overflow-y: auto;
}

.center-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(20, 20, 30, 0.5);
  border: 1px solid rgba(100, 100, 150, 0.3);
  border-radius: 8px;
  overflow: hidden;
}

/* No Map Message */
.no-map-message {
  text-align: center;
  padding: 40px;
  color: #888;
}

.no-map-message h2 {
  margin: 0 0 15px 0;
  font-size: 24px;
  color: #00d4ff;
}

.no-map-message p {
  margin: 0 0 25px 0;
  font-size: 16px;
}

.create-map-btn {
  background: rgba(0, 212, 255, 0.2);
  border: 2px solid #00d4ff;
  border-radius: 8px;
  padding: 12px 24px;
  color: #00d4ff;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
  font-weight: 600;
}

.create-map-btn:hover {
  background: rgba(0, 212, 255, 0.3);
  transform: scale(1.05);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-dialog {
  background: rgba(20, 20, 30, 0.98);
  border: 2px solid rgba(0, 212, 255, 0.5);
  border-radius: 12px;
  padding: 25px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.modal-title {
  margin: 0 0 20px 0;
  font-size: 22px;
  font-weight: bold;
  color: #00d4ff;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.modal-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 25px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #aaa;
}

.form-input {
  background: rgba(40, 40, 60, 0.8);
  border: 2px solid rgba(100, 100, 150, 0.3);
  border-radius: 6px;
  padding: 10px 12px;
  color: #fff;
  font-size: 14px;
}

.form-input:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.modal-btn {
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn {
  background: rgba(100, 100, 100, 0.3);
  border: 2px solid rgba(150, 150, 150, 0.3);
  color: #aaa;
}

.cancel-btn:hover {
  background: rgba(100, 100, 100, 0.5);
  border-color: rgba(150, 150, 150, 0.5);
}

.create-btn {
  background: rgba(0, 212, 255, 0.2);
  border: 2px solid #00d4ff;
  color: #00d4ff;
}

.create-btn:hover {
  background: rgba(0, 212, 255, 0.3);
  transform: scale(1.05);
}

/* Scrollbar styling */
.left-panel::-webkit-scrollbar,
.right-panel::-webkit-scrollbar {
  width: 6px;
}

.left-panel::-webkit-scrollbar-track,
.right-panel::-webkit-scrollbar-track {
  background: rgba(20, 20, 30, 0.5);
  border-radius: 3px;
}

.left-panel::-webkit-scrollbar-thumb,
.right-panel::-webkit-scrollbar-thumb {
  background: rgba(0, 212, 255, 0.3);
  border-radius: 3px;
}

.left-panel::-webkit-scrollbar-thumb:hover,
.right-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 212, 255, 0.5);
}
</style>
