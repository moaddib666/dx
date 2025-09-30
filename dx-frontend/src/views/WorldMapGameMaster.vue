<template>
  <div class="world-map-game-master">
    <!-- Editor: keep in DOM to preserve state; hide when previewing -->
    <MapEditor
      v-show="!isPreview || !currentMapData"
      :initial-data="initialMapData"
      @data-change="handleDataChange"
      @save="handleSave"
    />

    <!-- Read-only Canvas Preview (same data) -->
    <MapCanvas
      v-if="isPreview && currentMapData"
      :map-data="currentMapData"
      :active-tool="activeTool"
      :zoom="zoom"
      :pan="pan"
      @zoom-change="handleZoomChange"
      @pan-change="handlePanChange"
    />

    <!-- Preview toggle overlay button -->
    <button
      class="preview-overlay-button"
      type="button"
      :aria-pressed="isPreview ? 'true' : 'false'"
      @click="togglePreview"
      :title="isPreview ? 'Exit preview' : 'Enter preview'"
      :aria-label="isPreview ? 'Exit preview mode' : 'Enter preview mode'"
    >
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M4 9V5a1 1 0 0 1 1-1h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <path d="M20 9V5a1 1 0 0 0-1-1h-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <path d="M4 15v4a1 1 0 0 0 1 1h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <path d="M20 15v4a1 1 0 0 1-1 1h-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import MapEditor from '@/components/GlobalWorldMap/MapEditor.vue'
import MapCanvas from '@/components/GlobalWorldMap/MapCanvas.vue'
import { useMapInteraction } from '@/composables/GlobalWorldMap/useMapInteraction'

// Preview state
const isPreview = ref(false)
const activeTool = ref('select') // read-only tool for preview

// Interaction composable for preview canvas
const { zoom, pan, handleZoomChange, handlePanChange } = useMapInteraction()

// Map data bridging between editor and preview
const initialMapData = ref<any>(null)
const currentMapData = ref<any>(null)

onMounted(() => {
  try {
    const stored = localStorage.getItem('worldMapData')
    if (stored) {
      const parsed = JSON.parse(stored)
      initialMapData.value = parsed
      currentMapData.value = parsed
    }
  } catch (e) {
    console.warn('Failed to read initial map data from localStorage', e)
  }
})

// Event handlers
const handleDataChange = (data: any) => {
  currentMapData.value = data
  console.log('Map data changed:', data)
}

const handleSave = (data: any) => {
  console.log('Map data saved:', data)
}

const togglePreview = () => {
  isPreview.value = !isPreview.value
}
</script>

<style scoped>
.world-map-game-master {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.preview-overlay-button {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 4000;
  width: 44px;
  height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.75);
  color: #fff;
  border: 2px solid rgba(255,255,255,0.15);
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(0,0,0,0.35);
  backdrop-filter: saturate(120%) blur(2px);
  transition: background 0.2s ease, transform 0.1s ease, border-color 0.2s ease;
}

.preview-overlay-button:hover {
  background: rgba(0, 0, 0, 0.9);
  border-color: rgba(255,255,255,0.3);
}

.preview-overlay-button:active {
  transform: translateY(1px) scale(0.98);
}

.preview-overlay-button:focus-visible {
  outline: 2px solid #7fff16;
  outline-offset: 2px;
}

.preview-overlay-button[aria-pressed="true"] {
  background: rgba(20, 20, 20, 0.9);
  border-color: #7fff16;
}
</style>