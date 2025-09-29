<template>
  <div class="map-editor">
    <!-- Header with tools and export/import -->
    <div class="map-editor__header">
      <div class="map-editor__title">
        <h2>World Map Editor</h2>
      </div>

      <!-- Tool Panel -->
      <div class="map-editor__tools">
        <button
          v-for="tool in tools"
          :key="tool.id"
          :class="['tool-btn', { active: activeTool === tool.id }]"
          @click="setActiveTool(tool.id)"
          :title="tool.name"
        >
          <i :class="tool.icon"></i>
          {{ tool.name }}
        </button>
      </div>

      <!-- Export/Import Controls -->
      <div class="map-editor__actions">
        <input
          ref="fileInput"
          type="file"
          accept=".json"
          @change="handleImportJSON"
          style="display: none"
        />
        <input
          ref="imageInput"
          type="file"
          accept="image/*"
          @change="handleImageUpload"
          style="display: none"
        />

        <button @click="handleNewMap" class="btn btn-warning">
          <i class="fas fa-plus"></i>
          New Map
        </button>
        <button @click="$refs.imageInput.click()" class="btn btn-secondary">
          <i class="fas fa-image"></i>
          Upload Background
        </button>
        <button @click="$refs.fileInput.click()" class="btn btn-secondary">
          <i class="fas fa-upload"></i>
          Import JSON
        </button>
        <button @click="exportJSON" class="btn btn-primary">
          <i class="fas fa-download"></i>
          Export JSON
        </button>
        <button @click="exportPNG" class="btn btn-success">
          <i class="fas fa-image"></i>
          Export PNG
        </button>
      </div>
    </div>

    <!-- Main Editor Area -->
    <div class="map-editor__content">
      <!-- Layer Controls Panel -->
      <div class="map-editor__sidebar map-editor__sidebar--left">
        <LayerControls
          :map-data="mapData"
          @toggle-layer="handleLayerToggle"
          @select-item="handleSelectItem"
          @delete-item="handleItemDelete"
        />
      </div>

      <!-- Canvas Area -->
      <div class="map-editor__canvas-container">
        <MapCanvas
          ref="mapCanvas"
          :map-data="mapData"
          :active-tool="activeTool"
          :zoom="zoom"
          :pan="pan"
          :selected-item="selectedItem"
          @zoom-change="handleZoomChange"
          @pan-change="handlePanChange"
          @item-select="handleSelectItem"
          @item-create="handleItemCreate"
          @item-update="handleItemUpdate"
          @item-delete="handleItemDelete"
        />

        <!-- Status Bar -->
        <div class="map-editor__status">
          <span>Zoom: {{ Math.round(zoom * 100) }}%</span>
          <span>Tool: {{ currentTool?.name || 'None' }}</span>
          <span v-if="selectedItem">Selected: {{ selectedItem.name || selectedItem.type }}</span>
          <span>{{ statusMessage }}</span>
        </div>
      </div>

      <!-- Properties Panel -->
      <div class="map-editor__sidebar map-editor__sidebar--right">
        <PropertiesPanel
          :selected-item="selectedItem"
          :map-data="mapData"
          @item-update="handleItemUpdate"
          @map-metadata-update="handleMapMetadataUpdate"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import MapCanvas from './MapCanvas.vue'
import LayerControls from './LayerControls.vue'
import PropertiesPanel from './PropertiesPanel.vue'
import { useMapData } from '@/composables/GlobalWorldMap/useMapData'
import { useMapInteraction } from '@/composables/GlobalWorldMap/useMapInteraction'

// Props
interface Props {
  initialData?: any
}

const props = withDefaults(defineProps<Props>(), {
  initialData: null
})

// Emits
const emit = defineEmits<{
  'data-change': [data: any]
  'save': [data: any]
}>()

// Composables
const { mapData, loadMapData, exportMapData, importMapData, removeItem, resetMapData } = useMapData(props.initialData)
const { zoom, pan, selectedItem, handleZoomChange, handlePanChange } = useMapInteraction()

// Refs
const mapCanvas = ref<InstanceType<typeof MapCanvas> | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const imageInput = ref<HTMLInputElement | null>(null)

// State
const activeTool = ref<string>('select')
const statusMessage = ref<string>('Ready')

// Tools configuration
const tools = [
  { id: 'select', name: 'Select', icon: 'fas fa-mouse-pointer' },
  { id: 'move', name: 'Move', icon: 'fas fa-arrows-alt' },
  { id: 'draw-polygon', name: 'Draw Polygon', icon: 'fas fa-draw-polygon' },
  { id: 'draw-route', name: 'Draw Route', icon: 'fas fa-route' },
  { id: 'add-marker', name: 'Add Marker', icon: 'fas fa-map-pin' },
  { id: 'add-label', name: 'Add Label', icon: 'fas fa-tag' },
  { id: 'edit', name: 'Edit', icon: 'fas fa-edit' },
  { id: 'delete', name: 'Delete', icon: 'fas fa-trash' }
]

// Computed
const currentTool = computed(() => tools.find(tool => tool.id === activeTool.value))

// Methods
const setActiveTool = (toolId: string) => {
  activeTool.value = toolId
  statusMessage.value = `Tool changed to: ${tools.find(t => t.id === toolId)?.name}`
}

const handleLayerToggle = (layerType: string, itemId?: string, property?: string) => {
  // Toggle layer visibility
  if (itemId) {
    // Toggle specific item
    const item = findItemById(itemId, layerType)
    if (item && property) {
      item[property] = !item[property]
    }
  } else {
    // Toggle entire layer type
    toggleLayerType(layerType)
  }

  emit('data-change', mapData.value)
}

const handleSelectItem = (item: any) => {
  selectedItem.value = item
  statusMessage.value = item ? `Selected: ${item.name || item.type}` : 'Selection cleared'
}

const handleItemCreate = (itemData: any) => {
  // Add to local map data directly without API calls and get the created item
  const newItem = addItemToMapData(itemData)

  // Automatically select the newly created item
  selectedItem.value = newItem
  statusMessage.value = `Created and selected: ${itemData.name || itemData.text || itemData.type}`

  emit('data-change', mapData.value)
}

const handleItemUpdate = (itemData: any) => {
  // Update local map data directly without API calls
  updateItemInMapData(itemData)

  statusMessage.value = `Updated: ${itemData.name || itemData.type}`
  emit('data-change', mapData.value)
}

const handleMapMetadataUpdate = (metadata: any) => {
  // Update map metadata directly
  mapData.value.metadata = { ...mapData.value.metadata, ...metadata }

  statusMessage.value = 'Map settings updated'
  emit('data-change', mapData.value)
}

const handleItemDelete = (item: any) => {
  // Remove from local map data directly without API calls
  removeItem(item.id)

  if (selectedItem.value === item) {
    selectedItem.value = null
  }

  statusMessage.value = `Deleted: ${item.name || item.type}`
  emit('data-change', mapData.value)
}

const handleImageUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    const result = e.target?.result as string
    if (result) {
      mapData.value.metadata.backgroundImage = result
      statusMessage.value = 'Background image uploaded'
      emit('data-change', mapData.value)
    }
  }
  reader.readAsDataURL(file)
}

const handleImportJSON = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const result = e.target?.result as string
      const data = JSON.parse(result)
      importMapData(data)
      statusMessage.value = 'Map data imported successfully'
      emit('data-change', mapData.value)
    } catch (error) {
      console.error('Failed to import JSON:', error)
      statusMessage.value = 'Failed to import JSON file'
    }
  }
  reader.readAsText(file)
}

const exportJSON = () => {
  try {
    const data = exportMapData()
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `map-data-${new Date().toISOString().split('T')[0]}.json`
    link.click()
    URL.revokeObjectURL(url)
    statusMessage.value = 'Map data exported'
    emit('save', data)
  } catch (error) {
    console.error('Failed to export JSON:', error)
    statusMessage.value = 'Failed to export JSON'
  }
}

const exportPNG = () => {
  try {
    if (mapCanvas.value) {
      mapCanvas.value.exportToPNG()
      statusMessage.value = 'Map exported as PNG'
    }
  } catch (error) {
    console.error('Failed to export PNG:', error)
    statusMessage.value = 'Failed to export PNG'
  }
}

const handleNewMap = () => {
  const hasContent = mapData.value.continents.length > 0 ||
                    mapData.value.routes.length > 0 ||
                    mapData.value.markers.length > 0 ||
                    mapData.value.labels.length > 0

  if (hasContent) {
    if (confirm('Are you sure you want to create a new map? This will clear all current map data and cannot be undone.')) {
      resetMapData()
      selectedItem.value = null
      statusMessage.value = 'New map created'
      emit('data-change', mapData.value)
    }
  } else {
    resetMapData()
    selectedItem.value = null
    statusMessage.value = 'New map created'
    emit('data-change', mapData.value)
  }
}

// Helper methods
const findItemById = (id: string, layerType: string) => {
  // Implementation to find item by ID in specific layer
  switch (layerType) {
    case 'continents':
      return mapData.value.continents.find((item: any) => item.id === id)
    case 'markers':
      return mapData.value.markers.find((item: any) => item.id === id)
    case 'routes':
      return mapData.value.routes.find((item: any) => item.id === id)
    case 'labels':
      return mapData.value.labels.find((item: any) => item.id === id)
    default:
      return null
  }
}

const toggleLayerType = (layerType: string) => {
  // Implementation to toggle entire layer visibility
  switch (layerType) {
    case 'continents':
      mapData.value.continents.forEach((item: any) => item.visible = !item.visible)
      break
    case 'markers':
      mapData.value.markers.forEach((item: any) => item.visible = !item.visible)
      break
    case 'routes':
      mapData.value.routes.forEach((item: any) => item.visible = !item.visible)
      break
    case 'labels':
      mapData.value.labels.forEach((item: any) => item.visible = !item.visible)
      break
  }
}

const addItemToMapData = (itemData: any) => {
  // Add item to appropriate layer in map data
  const id = `${itemData.type}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  const item = { ...itemData, id }

  switch (itemData.type) {
    case 'continent':
      mapData.value.continents.push(item)
      break
    case 'marker':
    case 'city':
    case 'hazard':
      mapData.value.markers.push(item)
      break
    case 'route':
      mapData.value.routes.push(item)
      break
    case 'label':
      mapData.value.labels.push(item)
      break
  }

  return item
}

const updateItemInMapData = (itemData: any) => {
  // Update item in appropriate layer
  const layers = ['continents', 'markers', 'routes', 'labels']

  for (const layerName of layers) {
    const layer = mapData.value[layerName]
    const index = layer.findIndex((item: any) => item.id === itemData.id)
    if (index !== -1) {
      layer[index] = { ...layer[index], ...itemData }
      break
    }
  }
}

const removeItemFromMapData = (item: any) => {
  // Remove item from appropriate layer
  const layers = ['continents', 'markers', 'routes', 'labels']

  for (const layerName of layers) {
    const layer = mapData.value[layerName]
    const index = layer.findIndex((layerItem: any) => layerItem.id === item.id)
    if (index !== -1) {
      layer.splice(index, 1)
      break
    }
  }
}

// Keyboard shortcuts
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.ctrlKey || event.metaKey) {
    switch (event.key) {
      case 's':
        event.preventDefault()
        exportJSON()
        break
      case 'z':
        event.preventDefault()
        // TODO: Implement undo
        break
      case 'y':
        event.preventDefault()
        // TODO: Implement redo
        break
    }
  } else {
    switch (event.key) {
      case 'Delete':
      case 'Backspace':
        // Check if an input field is currently focused
        const activeElement = document.activeElement
        const isInputFocused = activeElement && (
          activeElement.tagName === 'INPUT' ||
          activeElement.tagName === 'TEXTAREA' ||
          activeElement.contentEditable === 'true'
        )

        // Only delete the selected item if no input field is focused
        if (selectedItem.value && !isInputFocused) {
          handleItemDelete(selectedItem.value)
        }
        break
      case 'Escape':
        selectedItem.value = null
        setActiveTool('select')
        break
    }
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('keydown', handleKeyDown)
  statusMessage.value = 'Map editor ready'
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
.map-editor {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #1a1a1a;
  color: #ffffff;
}

.map-editor__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: #2a2a2a;
  border-bottom: 1px solid #3a3a3a;
  gap: 1rem;
}

.map-editor__title h2 {
  margin: 0;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  text-shadow: 0 0 8px rgba(250, 218, 149, 0.3);
}

.map-editor__tools {
  display: flex;
  gap: 0.5rem;
}

.tool-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(250, 218, 149, 0.3);
  border-radius: 4px;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tool-btn:hover {
  background: rgba(250, 218, 149, 0.1);
  border-color: #fada95;
  box-shadow: 0 0 8px rgba(250, 218, 149, 0.3);
  transform: scale(1.05);
}

.tool-btn.active {
  background: rgba(127, 255, 22, 0.1);
  border-color: #7fff16;
  color: #7fff16;
  box-shadow: 0 0 12px rgba(127, 255, 22, 0.4);
}

.map-editor__actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 2px solid rgba(250, 218, 149, 0.3);
  border-radius: 4px;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
}

.btn-primary:hover {
  background: rgba(250, 218, 149, 0.1);
  border-color: #fada95;
  box-shadow: 0 0 8px rgba(250, 218, 149, 0.3);
  transform: scale(1.05);
}

.btn-secondary {
  background: rgba(0, 0, 0, 0.3);
  color: #fada95;
  border-color: rgba(250, 218, 149, 0.2);
}

.btn-secondary:hover {
  background: rgba(250, 218, 149, 0.05);
  border-color: rgba(250, 218, 149, 0.4);
  box-shadow: 0 0 6px rgba(250, 218, 149, 0.2);
}

.btn-success {
  background: rgba(127, 255, 22, 0.1);
  color: #7fff16;
  border-color: rgba(127, 255, 22, 0.3);
}

.btn-success:hover {
  background: rgba(127, 255, 22, 0.2);
  border-color: #7fff16;
  box-shadow: 0 0 10px rgba(127, 255, 22, 0.4);
  transform: scale(1.05);
}

.map-editor__content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.map-editor__sidebar {
  width: 300px;
  background: #2a2a2a;
  border-right: 1px solid #3a3a3a;
  overflow-y: auto;
}

.map-editor__sidebar--right {
  border-right: none;
  border-left: 1px solid #3a3a3a;
}

.map-editor__canvas-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  background: #1a1a1a;
}

.map-editor__status {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 1rem;
  background: #2a2a2a;
  border-top: 1px solid #3a3a3a;
  font-size: 0.875rem;
  color: #9ca3af;
}

.map-editor__status span {
  white-space: nowrap;
}
</style>