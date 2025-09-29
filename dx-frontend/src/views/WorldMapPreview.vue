<template>
  <div class="world-map-preview">
    <!-- Generic loader overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loader">
        <div class="spinner"></div>
        <p class="loading-text">Loading World Map...</p>
      </div>
    </div>

    <MapCanvas
      v-if="!isLoading"
      :map-data="mapData"
      :active-tool="activeTool"
      :zoom="zoom"
      :pan="pan"
      @zoom-change="handleZoomChange"
      @pan-change="handlePanChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import MapCanvas from '@/components/GlobalWorldMap/MapCanvas.vue'
import { useMapData } from '@/composables/GlobalWorldMap/useMapData'
import { useMapInteraction } from '@/composables/GlobalWorldMap/useMapInteraction'

// Initial map data (can be null to use default sample data)
const initialMapData = ref(null)

// Composables
const { mapData, importMapData } = useMapData(initialMapData.value)
const { zoom, pan, handleZoomChange, handlePanChange } = useMapInteraction()

// Set tool to view-only mode (no editing capabilities)
const activeTool = ref('select')

// Loading state
const isLoading = ref(true)

// Load map data from public folder
const loadMapDataFromPublic = async () => {
  try {
    isLoading.value = true
    const response = await fetch('/worldmap/map-data-2025-09-29-fixed.json')

    if (!response.ok) {
      throw new Error(`Failed to fetch map data: ${response.status} ${response.statusText}`)
    }

    const jsonData = await response.json()
    const success = importMapData(jsonData)

    if (!success) {
      throw new Error('Failed to import map data')
    }

    console.log('Map data loaded successfully from public folder')
  } catch (error) {
    console.error('Error loading map data:', error)
    // Keep using default/sample data if loading fails
  } finally {
    isLoading.value = false
  }
}

// Load map data on component mount
onMounted(() => {
  loadMapDataFromPublic()
})
</script>

<style scoped>
.world-map-preview {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loader {
  text-align: center;
  color: white;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 18px;
  font-weight: 500;
  margin: 0;
  opacity: 0.9;
}
</style>