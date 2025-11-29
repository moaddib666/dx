<template>
  <div class="tabletop-map-player">
    <!-- Top Toolbar -->
    <div class="player-toolbar">
      <div class="toolbar-section">
        <h1 class="player-title">Tabletop Map Player</h1>
        <span v-if="currentMap?.metadata?.name" class="map-name">{{ currentMap.metadata.name }}</span>
      </div>

      <div class="toolbar-section toolbar-actions">
        <button class="toolbar-btn" @click="importMap">
          <span class="btn-icon">📂</span>
          Import Map
        </button>
        <button class="toolbar-btn" @click="clearAll" :disabled="!currentMap">
          <span class="btn-icon">🗑️</span>
          Clear All
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="player-content">
      <!-- Center Panel - Canvas -->
      <div class="center-panel">
        <div v-if="!currentMap" class="no-map-message">
          <h2>No Map Loaded</h2>
          <p>Import a map from the Tabletop Map Editor to start testing</p>
          <button class="import-map-btn" @click="importMap">
            Import Map
          </button>
        </div>
        <PlayerCanvas v-else :key="currentMap?.metadata?.created || 'default'" />
      </div>

      <!-- Right Panel - Controls -->
      <div class="right-panel">
        <PlayerControlPanel />
      </div>
    </div>

    <!-- Hidden file input -->
    <input
      ref="importInput"
      type="file"
      accept=".png,.json,image/png,application/json"
      style="display: none"
      @change="handleImportFile"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import PlayerCanvas from '@/components/TabletopPlayer/PlayerCanvas.vue';
import PlayerControlPanel from '@/components/TabletopPlayer/PlayerControlPanel.vue';
import { extractMetadataFromPNG } from '@/utils/pngMetadata.js';

export default {
  name: 'TabletopMapPlayer',
  components: {
    PlayerCanvas,
    PlayerControlPanel
  },
  computed: {
    ...mapGetters('tabletopPlayer', [
      'currentMap',
      'players'
    ])
  },
  methods: {
    ...mapActions('tabletopPlayer', [
      'loadMap',
      'setBackgroundImage'
    ]),

    importMap() {
      this.$refs.importInput.click();
    },

    async handleImportFile(event) {
      const file = event.target.files[0];
      if (!file) return;

      console.log('[Player Import] Starting import process for file:', file.name, 'Type:', file.type);

      try {
        // Check if it's a PNG file
        if (file.type === 'image/png' || file.name.toLowerCase().endsWith('.png')) {
          console.log('[Player Import] Detected PNG file, extracting metadata...');

          // Extract metadata from PNG
          const { mapData, imageDataURL, hasMetadata } = await extractMetadataFromPNG(file);

          if (hasMetadata && mapData) {
            // PNG has embedded map data - load it
            console.log('[Player Import] ✅ PNG has metadata - loading map data');
            this.loadMap(mapData);

            // Set the background image from the PNG
            console.log('[Player Import] Setting background image...');
            this.setBackgroundImage(imageDataURL);

            console.log('[Player Import] ✅ Map import completed successfully!');
          } else {
            // PNG has no metadata
            console.log('[Player Import] ⚠️ PNG has no metadata - cannot load map');
            alert('This PNG file does not contain map data. Please export a map from the Tabletop Map Editor first.');
          }
        } else if (file.type === 'application/json' || file.name.toLowerCase().endsWith('.json')) {
          // Legacy JSON import support
          console.log('[Player Import] Detected JSON file, loading...');
          const reader = new FileReader();
          reader.onload = (e) => {
            try {
              const mapData = JSON.parse(e.target.result);
              console.log('[Player Import] JSON parsed, loading map...');
              this.loadMap(mapData);
              console.log('[Player Import] ✅ JSON map imported successfully!');
            } catch (error) {
              console.error('[Player Import] ❌ Error parsing JSON:', error);
              alert('Error parsing JSON file: ' + error.message);
            }
          };
          reader.readAsText(file);
        } else {
          alert('Please select a PNG file exported from the Tabletop Map Editor or a JSON map file.');
        }
      } catch (error) {
        console.error('[Player Import] ❌ Error importing map:', error);
        alert('Error importing map: ' + error.message);
      }

      // Reset file input
      event.target.value = '';
    },

    clearAll() {
      if (confirm('Are you sure you want to clear the map and all players?')) {
        this.loadMap(null);
      }
    }
  }
};
</script>

<style scoped>
.tabletop-map-player {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #e0e0e0;
  overflow: hidden;
}

/* Toolbar */
.player-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: rgba(20, 20, 30, 0.95);
  border-bottom: 2px solid rgba(0, 212, 255, 0.3);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.toolbar-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

.player-title {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
  color: #00d4ff;
  text-transform: uppercase;
  letter-spacing: 1.5px;
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
  background: rgba(0, 212, 255, 0.2);
  border: 2px solid #00d4ff;
  border-radius: 6px;
  padding: 8px 16px;
  color: #00d4ff;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.toolbar-btn:hover:not(:disabled) {
  background: rgba(0, 212, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
}

.toolbar-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-icon {
  font-size: 18px;
}

/* Main Content */
.player-content {
  flex: 1;
  display: flex;
  gap: 15px;
  padding: 15px;
  overflow: hidden;
}

.center-panel {
  flex: 1;
  background: rgba(20, 20, 30, 0.8);
  border: 2px solid rgba(100, 100, 150, 0.3);
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.right-panel {
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  overflow-y: auto;
}

/* No Map Message */
.no-map-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  padding: 40px;
}

.no-map-message h2 {
  margin: 0 0 15px 0;
  font-size: 28px;
  color: #00d4ff;
}

.no-map-message p {
  margin: 0 0 30px 0;
  font-size: 16px;
  color: #aaa;
  max-width: 400px;
}

.import-map-btn {
  background: rgba(0, 212, 255, 0.2);
  border: 2px solid #00d4ff;
  border-radius: 6px;
  padding: 12px 24px;
  color: #00d4ff;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 16px;
  font-weight: 600;
}

.import-map-btn:hover {
  background: rgba(0, 212, 255, 0.3);
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(0, 212, 255, 0.4);
}

/* Scrollbar styling for right panel */
.right-panel::-webkit-scrollbar {
  width: 8px;
}

.right-panel::-webkit-scrollbar-track {
  background: rgba(20, 20, 30, 0.5);
  border-radius: 4px;
}

.right-panel::-webkit-scrollbar-thumb {
  background: rgba(0, 212, 255, 0.3);
  border-radius: 4px;
}

.right-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 212, 255, 0.5);
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .right-panel {
    width: 280px;
  }
}

@media (max-width: 768px) {
  .player-content {
    flex-direction: column;
  }

  .right-panel {
    width: 100%;
    max-height: 300px;
  }

  .center-panel {
    min-height: 400px;
  }
}
</style>
