<template>
  <div class="test-screen-user">
    <MapCanvas
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
.test-screen-user {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
</style>