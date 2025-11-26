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
        <PropertiesPanel />
        <GridConfigPanel />
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
      'isDirty'
    ])
  },
  methods: {
    ...mapActions('tabletopEditor', [
      'createNewMap',
      'loadMap',
      'saveMap',
      'setBackgroundImage',
      'updateGridConfig'
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
              cellsCount: mapData.cells?.length
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
        // Use mapDataWithoutImage to exclude the backgroundImage property
        const pngBlob = await embedMetadataInPNG(imageSource, mapDataWithoutImage);

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
