<template>
  <div class="world-map-viewer">
    <!-- Header Controls -->
    <div class="map-header">
      <div class="map-title">
        <h2>World Map Viewer</h2>
        <div class="mode-toggle">
          <button
            :class="{ active: mode === 'view' }"
            @click="setMode('view')"
          >
            View Mode
          </button>
          <button
            :class="{ active: mode === 'edit' }"
            @click="setMode('edit')"
          >
            Edit Mode
          </button>
        </div>
      </div>

      <!-- Search -->
      <div class="search-bar">
        <input
          v-model="searchQuery"
          @input="onSearch"
          placeholder="Search locations..."
          class="search-input"
        />
        <div v-if="searchResults.length > 0" class="search-results">
          <div
            v-for="result in searchResults"
            :key="result.name"
            @click="selectNode(result)"
            class="search-result-item"
          >
            <span class="node-type">{{ result.type }}</span>
            <span class="node-name">{{ result.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="map-content">
      <!-- Layer Controls -->
      <div class="layer-controls">
        <h3>Layers</h3>
        <div
          v-for="layer in layers"
          :key="layer.id"
          class="layer-control"
        >
          <label class="layer-checkbox">
            <input
              type="checkbox"
              :checked="layer.visible"
              @change="toggleLayer(layer.id)"
            />
            <span>{{ layer.name }}</span>
          </label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            :value="layer.opacity"
            @input="setLayerOpacity(layer.id, $event.target.value)"
            class="opacity-slider"
          />
        </div>
      </div>

      <!-- Map Visualization -->
      <div class="map-visualization">
        <div class="map-container" ref="mapContainer">
          <svg
            id="world-map-svg"
            viewBox="0 0 800 600"
            class="world-map-svg"
            :style="{
              transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
              transition: isDragging ? 'none' : 'transform 0.1s'
            }"
            @mousedown="handleMouseDown"
            @mousemove="handleMouseMove"
            @mouseup="handleMouseUp"
            @mouseleave="handleMouseUp"
            @wheel="handleWheel"
          >
            <!-- Background -->
            <rect width="800" height="600" fill="#0d1117" />

            <!-- Oceans -->
            <g v-for="ocean in oceans" :key="ocean.name" :style="getLayerStyle('oceans')">
              <path
                :d="ocean.path"
                :fill="ocean.color"
                stroke="#1a3a5a"
                stroke-width="2"
                opacity="0.8"
              />
              <text
                v-if="showLabels && getLayerStyle('labels').display !== 'none'"
                :x="ocean.labelX"
                :y="ocean.labelY"
                fill="#4a7a9a"
                font-size="12"
                font-style="italic"
                text-anchor="middle"
                :style="getLayerStyle('labels')"
              >
                {{ ocean.name }}
              </text>
              <g v-for="island in ocean.islands" :key="island.name">
                <circle
                  :cx="island.x"
                  :cy="island.y"
                  r="3"
                  fill="#2a2a2a"
                  stroke="#666"
                />
                <text
                  v-if="showLabels && getLayerStyle('labels').display !== 'none'"
                  :x="island.x"
                  :y="island.y - 8"
                  fill="#888"
                  font-size="8"
                  text-anchor="middle"
                  :style="getLayerStyle('labels')"
                >
                  {{ island.name }}
                </text>
              </g>
            </g>

            <!-- Continents -->
            <g v-for="continent in continents" :key="continent.name" :style="getLayerStyle('continents')">
              <!-- Continent shape -->
              <path
                :d="continent.path"
                :fill="continent.color"
                stroke="#4a5a6a"
                stroke-width="2"
              />

              <!-- Continent name -->
              <text
                v-if="showLabels && getLayerStyle('labels').display !== 'none'"
                :x="continent.labelX"
                :y="continent.labelY"
                fill="#7a8a9a"
                font-size="16"
                font-weight="bold"
                text-anchor="middle"
                :style="getLayerStyle('labels')"
              >
                {{ continent.name }}
              </text>

              <!-- Cities -->
              <g v-for="city in continent.cities" :key="city.name" :style="getLayerStyle('cities')">
                <circle
                  :cx="city.x"
                  :cy="city.y"
                  :r="city.type === 'major' ? 6 : 4"
                  :fill="city.type === 'major' ? '#fbbf24' : '#60a5fa'"
                  stroke="#fff"
                  stroke-width="1"
                  @click="selectNodeByName(city.name)"
                  :class="{ 'selected': selectedNode?.name === city.name }"
                  style="cursor: pointer"
                />
                <text
                  v-if="showLabels && getLayerStyle('labels').display !== 'none'"
                  :x="city.x"
                  :y="city.y - 10"
                  fill="#e5e7eb"
                  font-size="10"
                  text-anchor="middle"
                  style="pointer-events: none"
                  :style="getLayerStyle('labels')"
                >
                  {{ city.name }}
                </text>
              </g>

              <!-- Hazards -->
              <g v-for="hazard in continent.hazards" :key="hazard.name" :style="getLayerStyle('hazards')">
                <circle
                  :cx="hazard.x"
                  :cy="hazard.y"
                  r="5"
                  :fill="hazard.type === 'danger' ? '#ef4444' : '#9333ea'"
                  opacity="0.7"
                  @click="selectNodeByName(hazard.name)"
                  :class="{ 'selected': selectedNode?.name === hazard.name }"
                  style="cursor: pointer"
                />
                <text
                  v-if="showLabels && getLayerStyle('labels').display !== 'none'"
                  :x="hazard.x"
                  :y="hazard.y - 10"
                  fill="#fca5a5"
                  font-size="9"
                  text-anchor="middle"
                  style="pointer-events: none"
                  :style="getLayerStyle('labels')"
                >
                  {{ hazard.name }}
                </text>
              </g>
            </g>

            <!-- Trade routes -->
            <g opacity="0.3">
              <line x1="330" y1="380" x2="220" y2="280" stroke="#60a5fa" stroke-width="1" stroke-dasharray="3,3" />
              <line x1="220" y1="280" x2="95" y2="120" stroke="#60a5fa" stroke-width="1" stroke-dasharray="3,3" />
              <line x1="220" y1="280" x2="505" y2="210" stroke="#60a5fa" stroke-width="1" stroke-dasharray="3,3" />
            </g>
          </svg>

          <!-- Zoom Controls -->
          <div class="zoom-controls">
            <button @click="handleZoomIn" class="zoom-btn" title="Zoom In">+</button>
            <button @click="handleZoomOut" class="zoom-btn" title="Zoom Out">-</button>
            <button @click="handleReset" class="zoom-btn" title="Reset View">⌂</button>
          </div>
        </div>
      </div>

      <!-- Node Details Panel -->
      <div v-if="selectedNode" class="node-details">
        <div class="details-header">
          <h3>{{ selectedNode.name }}</h3>
          <button @click="closeDetails" class="close-btn">×</button>
        </div>

        <div class="details-content">
          <div class="detail-section">
            <label>Type:</label>
            <span>{{ selectedNode.type }}</span>
          </div>

          <div class="detail-section">
            <label>Size:</label>
            <span>{{ selectedNode.size }}</span>
          </div>

          <div class="detail-section">
            <label>Description:</label>
            <p>{{ selectedNode.description }}</p>
          </div>

          <div v-if="selectedNode.tags?.length" class="detail-section">
            <label>Tags:</label>
            <div class="tags">
              <span
                v-for="tag in selectedNode.tags"
                :key="tag"
                class="tag"
              >
                {{ tag }}
              </span>
            </div>
          </div>

          <div v-if="selectedNode.borders_with?.length" class="detail-section">
            <label>Borders With:</label>
            <ul class="borders-list">
              <li v-for="border in selectedNode.borders_with" :key="border">
                {{ border }}
              </li>
            </ul>
          </div>

          <!-- Edit Mode Controls -->
          <div v-if="mode === 'edit'" class="edit-controls">
            <button @click="editNodeInline" class="edit-btn">
              Edit Node
            </button>
            <button @click="editNodeAsJson" class="edit-btn">
              Edit as JSON
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Mode Controls -->
    <div v-if="mode === 'edit'" class="edit-mode-controls">
      <div class="edit-actions">
        <button @click="saveChanges" :disabled="!hasChanges" class="save-btn">
          Save Changes ({{ changeCount }})
        </button>
        <button @click="discardChanges" :disabled="!hasChanges" class="discard-btn">
          Discard Changes
        </button>
        <button @click="editWholeMap" class="edit-all-btn">
          Edit Whole Map (JSON/YAML)
        </button>
      </div>
    </div>

    <!-- Inline Node Editor Modal -->
    <div v-if="showNodeEditor" class="modal-overlay" @click="closeNodeEditor">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Edit {{ editingNode?.name }}</h3>
          <button @click="closeNodeEditor" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveNodeEdit">
            <div class="form-group">
              <label>Name:</label>
              <input v-model="nodeEditForm.name" type="text" required />
            </div>
            <div class="form-group">
              <label>Description:</label>
              <textarea v-model="nodeEditForm.description" rows="4"></textarea>
            </div>
            <div class="form-group">
              <label>Size:</label>
              <select v-model="nodeEditForm.size">
                <option value="tiny">Tiny</option>
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
                <option value="massive">Massive</option>
                <option value="vast">Vast</option>
              </select>
            </div>
            <div class="form-group">
              <label>Tags (comma-separated):</label>
              <input v-model="nodeEditForm.tagsString" type="text" />
            </div>
            <div class="form-actions">
              <button type="submit" class="save-btn">Save</button>
              <button type="button" @click="closeNodeEditor" class="cancel-btn">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- JSON/YAML Editor Modal -->
    <div v-if="showJsonEditor" class="modal-overlay" @click="closeJsonEditor">
      <div class="modal-content large" @click.stop>
        <div class="modal-header">
          <h3>{{ jsonEditorMode === 'node' ? `Edit ${editingNode?.name} as JSON` : 'Edit Whole Map' }}</h3>
          <div class="editor-format-toggle">
            <button
              :class="{ active: jsonFormat === 'json' }"
              @click="jsonFormat = 'json'"
            >
              JSON
            </button>
            <button
              :class="{ active: jsonFormat === 'yaml' }"
              @click="jsonFormat = 'yaml'"
            >
              YAML
            </button>
          </div>
          <button @click="closeJsonEditor" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <textarea
            v-model="jsonEditorContent"
            class="json-editor"
            rows="20"
            spellcheck="false"
          ></textarea>
          <div class="form-actions">
            <button @click="saveJsonEdit" class="save-btn">Save</button>
            <button @click="closeJsonEditor" class="cancel-btn">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">Loading world map...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { worldMapService, MapNode, MapLayer, ServiceMode, WorldMapEvent } from '@/services/world-map';

// Reactive state
const loading = ref(true);
const mode = ref<ServiceMode>('view');
const layers = ref<MapLayer[]>([
  { id: 'oceans', name: 'Oceans', visible: true, opacity: 1 },
  { id: 'continents', name: 'Continents', visible: true, opacity: 1 },
  { id: 'cities', name: 'Cities', visible: true, opacity: 1 },
  { id: 'hazards', name: 'Hazards', visible: true, opacity: 1 },
  { id: 'labels', name: 'Labels', visible: true, opacity: 1 }
]);
const selectedNode = ref<MapNode | null>(null);
const searchQuery = ref('');
const searchResults = ref<MapNode[]>([]);

// SVG Map state
const zoom = ref(1);
const pan = ref({ x: 0, y: 0 });
const isDragging = ref(false);
const dragStart = ref({ x: 0, y: 0 });
const showLabels = ref(true);

// Map data with proper scaling and positioning for better visualization
const continents = ref([
  {
    name: 'Mainland Primus',
    path: 'M 150 100 Q 200 80 300 90 L 450 120 Q 500 180 480 280 L 450 380 Q 400 420 320 410 L 200 390 Q 150 340 140 240 L 150 100 Z',
    color: '#2a2a3e',
    labelX: 320,
    labelY: 250,
    layer: 'continents',
    cities: [
      { name: 'City of Memories', x: 420, y: 350, type: 'major' },
      { name: 'Crossroads Bastion', x: 320, y: 220, type: 'major' },
      { name: 'Meteor\'s End', x: 380, y: 180, type: 'major' },
      { name: 'Shadowveil', x: 250, y: 280, type: 'medium' },
      { name: 'Forge Haven', x: 200, y: 160, type: 'medium' }
    ],
    hazards: [
      { name: 'Death Valley', x: 450, y: 380, type: 'danger' },
      { name: 'Black Deserts', x: 280, y: 320, type: 'corrupted' }
    ]
  },
  {
    name: 'TechnoEdge',
    path: 'M 50 50 Q 80 30 120 40 L 180 60 Q 200 90 190 130 L 170 180 Q 140 200 100 190 L 60 170 Q 40 140 50 50 Z',
    color: '#1a3a4a',
    labelX: 125,
    labelY: 115,
    layer: 'continents',
    cities: [
      { name: 'Techno-City Prime', x: 125, y: 115, type: 'major' }
    ],
    hazards: []
  },
  {
    name: 'Mystory Heaven',
    path: 'M 520 80 Q 560 70 600 90 L 650 130 Q 670 170 660 220 L 630 280 Q 590 300 550 290 L 510 260 Q 500 200 520 80 Z',
    color: '#2a4a2a',
    labelX: 580,
    labelY: 185,
    layer: 'continents',
    cities: [
      { name: 'JSon\'s Sanctuary', x: 580, y: 200, type: 'major' },
      { name: 'Temple City', x: 600, y: 240, type: 'medium' }
    ],
    hazards: []
  }
]);

const oceans = ref([
  {
    name: 'Dark Ocean',
    path: 'M 0 0 L 800 0 L 800 600 L 0 600 Z M 150 100 Q 200 80 300 90 L 450 120 Q 500 180 480 280 L 450 380 Q 400 420 320 410 L 200 390 Q 150 340 140 240 L 150 100 Z M 50 50 Q 80 30 120 40 L 180 60 Q 200 90 190 130 L 170 180 Q 140 200 100 190 L 60 170 Q 40 140 50 50 Z M 520 80 Q 560 70 600 90 L 650 130 Q 670 170 660 220 L 630 280 Q 590 300 550 290 L 510 260 Q 500 200 520 80 Z',
    color: '#0a1a2a',
    labelX: 100,
    labelY: 500,
    layer: 'oceans',
    islands: [
      { name: 'Black Rock Island', x: 400, y: 450 }
    ]
  }
]);

// Edit mode state
const showNodeEditor = ref(false);
const showJsonEditor = ref(false);
const jsonEditorMode = ref<'node' | 'whole'>('node');
const jsonFormat = ref<'json' | 'yaml'>('json');
const editingNode = ref<MapNode | null>(null);
const nodeEditForm = ref({
  name: '',
  description: '',
  size: 'medium',
  tagsString: ''
});
const jsonEditorContent = ref('');

// Computed properties
const visibleLayers = computed(() =>
  layers.value.filter(layer => layer.visible)
);

const hasChanges = computed(() => {
  const editSession = worldMapService.getEditSession();
  return editSession && editSession.changes.length > 0;
});

const changeCount = computed(() => {
  const editSession = worldMapService.getEditSession();
  return editSession ? editSession.changes.length : 0;
});

// Methods
const setMode = (newMode: ServiceMode) => {
  mode.value = newMode;
  worldMapService.setMode(newMode);
};

const toggleLayer = (layerId: string) => {
  const layer = layers.value.find(l => l.id === layerId);
  if (layer) {
    layer.visible = !layer.visible;
  }
};

const setLayerOpacity = (layerId: string, opacity: string) => {
  const layer = layers.value.find(l => l.id === layerId);
  if (layer) {
    layer.opacity = parseFloat(opacity);
  }
};

const getLayerStyle = (layerId: string) => {
  const layer = layers.value.find(l => l.id === layerId);
  if (!layer || !layer.visible) {
    return { display: 'none' };
  }
  return { opacity: layer.opacity };
};

const selectNode = (node: MapNode) => {
  selectedNode.value = node;
  worldMapService.selectNode(node);
  searchResults.value = [];
  searchQuery.value = '';
};

const closeDetails = () => {
  selectedNode.value = null;
  worldMapService.selectNode(null);
};

const onSearch = () => {
  if (searchQuery.value.trim()) {
    searchResults.value = worldMapService.searchNodes(searchQuery.value);
  } else {
    searchResults.value = [];
  }
};

const isNodeEditing = (node: MapNode) => {
  const editSession = worldMapService.getEditSession();
  return editSession?.changes.some(change => change.name === node.name) || false;
};

// SVG Map Methods
const handleMouseDown = (e: MouseEvent) => {
  isDragging.value = true;
  dragStart.value = { x: e.clientX - pan.value.x, y: e.clientY - pan.value.y };
};

const handleMouseMove = (e: MouseEvent) => {
  if (isDragging.value) {
    pan.value = {
      x: e.clientX - dragStart.value.x,
      y: e.clientY - dragStart.value.y
    };
  }
};

const handleMouseUp = () => {
  isDragging.value = false;
};

const handleWheel = (e: WheelEvent) => {
  e.preventDefault();

  const rect = (e.currentTarget as SVGElement).getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  const delta = e.deltaY > 0 ? -0.1 : 0.1;
  const newZoom = Math.min(Math.max(zoom.value + delta, 0.1), 10);

  if (newZoom !== zoom.value) {
    const zoomFactor = newZoom / zoom.value;

    // Zoom towards mouse position
    pan.value = {
      x: mouseX - (mouseX - pan.value.x) * zoomFactor,
      y: mouseY - (mouseY - pan.value.y) * zoomFactor
    };

    zoom.value = newZoom;
  }
};

const handleZoomIn = () => {
  zoom.value = Math.min(zoom.value + 0.2, 10);
};

const handleZoomOut = () => {
  zoom.value = Math.max(zoom.value - 0.2, 0.1);
};

const handleReset = () => {
  zoom.value = 1;
  pan.value = { x: 0, y: 0 };
};

const selectNodeByName = (nodeName: string) => {
  // Find node in continents data
  for (const continent of continents.value) {
    const city = continent.cities.find(c => c.name === nodeName);
    if (city) {
      // Create a MapNode-like object for compatibility
      const mapNode = {
        name: city.name,
        type: 'city',
        size: city.type,
        description: `${city.type} city in ${continent.name}`,
        tags: [continent.name, 'city', city.type]
      } as MapNode;
      selectNode(mapNode);
      return;
    }

    const hazard = continent.hazards.find(h => h.name === nodeName);
    if (hazard) {
      const mapNode = {
        name: hazard.name,
        type: 'hazard',
        size: 'medium',
        description: `${hazard.type} hazard in ${continent.name}`,
        tags: [continent.name, 'hazard', hazard.type]
      } as MapNode;
      selectNode(mapNode);
      return;
    }
  }

  // Find in oceans
  for (const ocean of oceans.value) {
    const island = ocean.islands.find(i => i.name === nodeName);
    if (island) {
      const mapNode = {
        name: island.name,
        type: 'island',
        size: 'small',
        description: `Island in ${ocean.name}`,
        tags: [ocean.name, 'island']
      } as MapNode;
      selectNode(mapNode);
      return;
    }
  }
};

// Edit functions
const editNodeInline = () => {
  if (!selectedNode.value) return;

  editingNode.value = selectedNode.value;
  nodeEditForm.value = {
    name: selectedNode.value.name,
    description: selectedNode.value.description,
    size: selectedNode.value.size,
    tagsString: selectedNode.value.tags.join(', ')
  };
  showNodeEditor.value = true;
};

const editNodeAsJson = () => {
  if (!selectedNode.value) return;

  editingNode.value = selectedNode.value;
  jsonEditorMode.value = 'node';
  updateJsonEditorContent();
  showJsonEditor.value = true;
};

const editWholeMap = () => {
  jsonEditorMode.value = 'whole';
  updateJsonEditorContent();
  showJsonEditor.value = true;
};

const updateJsonEditorContent = () => {
  const data = jsonEditorMode.value === 'node'
    ? editingNode.value
    : worldMapService.getData();

  if (jsonFormat.value === 'json') {
    jsonEditorContent.value = JSON.stringify(data, null, 2);
  } else {
    // For YAML, we'll use JSON for now (would need js-yaml for proper YAML formatting)
    jsonEditorContent.value = JSON.stringify(data, null, 2);
  }
};

const saveNodeEdit = () => {
  if (!editingNode.value) return;

  const changes = {
    name: nodeEditForm.value.name,
    description: nodeEditForm.value.description,
    size: nodeEditForm.value.size,
    tags: nodeEditForm.value.tagsString.split(',').map(tag => tag.trim()).filter(tag => tag)
  };

  worldMapService.editNode(editingNode.value, changes);
  closeNodeEditor();
  updateLayers();
};

const saveJsonEdit = () => {
  try {
    const parsedData = JSON.parse(jsonEditorContent.value);

    if (jsonEditorMode.value === 'node' && editingNode.value) {
      worldMapService.editNode(editingNode.value, parsedData);
    } else {
      // For whole map editing, we'd need more complex logic
      console.log('Whole map editing not fully implemented yet');
    }

    closeJsonEditor();
    updateLayers();
  } catch (error) {
    alert('Invalid JSON format');
  }
};

const closeNodeEditor = () => {
  showNodeEditor.value = false;
  editingNode.value = null;
};

const closeJsonEditor = () => {
  showJsonEditor.value = false;
  editingNode.value = null;
};

const saveChanges = async () => {
  try {
    await worldMapService.saveChanges();
    alert('Changes saved successfully!');
  } catch (error) {
    alert('Failed to save changes: ' + error);
  }
};

const discardChanges = () => {
  worldMapService.discardChanges();
  updateLayers();
};

// Event handlers
const handleWorldMapEvent = (event: WorldMapEvent) => {
  switch (event.type) {
    case 'data_loaded':
      updateLayers();
      loading.value = false;
      break;
    case 'layer_toggled':
      updateLayers();
      break;
    case 'mode_changed':
      mode.value = event.data.mode;
      break;
    case 'node_selected':
      selectedNode.value = event.data.node;
      break;
    case 'node_edited':
      updateLayers();
      break;
  }
};

// Lifecycle
onMounted(async () => {
  try {
    // Subscribe to events
    worldMapService.on('data_loaded', handleWorldMapEvent);
    worldMapService.on('layer_toggled', handleWorldMapEvent);
    worldMapService.on('mode_changed', handleWorldMapEvent);
    worldMapService.on('node_selected', handleWorldMapEvent);
    worldMapService.on('node_edited', handleWorldMapEvent);

    // Initialize service
    await worldMapService.initialize();
  } catch (error) {
    console.error('Failed to initialize world map:', error);
    loading.value = false;
  }
});

onUnmounted(() => {
  // Cleanup event listeners
  worldMapService.off('data_loaded', handleWorldMapEvent);
  worldMapService.off('layer_toggled', handleWorldMapEvent);
  worldMapService.off('mode_changed', handleWorldMapEvent);
  worldMapService.off('node_selected', handleWorldMapEvent);
  worldMapService.off('node_edited', handleWorldMapEvent);
});
</script>

<style scoped>
.world-map-viewer {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #1a1a1a;
  color: #ffffff;
  font-family: 'Arial', sans-serif;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #2a2a2a;
  border-bottom: 1px solid #444;
}

.map-title {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.map-title h2 {
  margin: 0;
  color: #00ff88;
}

.mode-toggle {
  display: flex;
  gap: 0.5rem;
}

.mode-toggle button {
  padding: 0.5rem 1rem;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.mode-toggle button.active {
  background: #00ff88;
  color: #000;
}

.search-bar {
  position: relative;
}

.search-input {
  padding: 0.5rem;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  width: 300px;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #2a2a2a;
  border: 1px solid #555;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
}

.search-result-item {
  padding: 0.5rem;
  cursor: pointer;
  display: flex;
  gap: 0.5rem;
  border-bottom: 1px solid #444;
}

.search-result-item:hover {
  background: #333;
}

.node-type {
  color: #888;
  font-size: 0.8em;
  text-transform: uppercase;
}

.node-name {
  color: #00ff88;
}

.map-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.layer-controls {
  width: 250px;
  background: #2a2a2a;
  padding: 1rem;
  border-right: 1px solid #444;
  overflow-y: auto;
}

.layer-controls h3 {
  margin: 0 0 1rem 0;
  color: #00ff88;
}

.layer-control {
  margin-bottom: 1rem;
  padding: 0.5rem;
  background: #333;
  border-radius: 4px;
}

.layer-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
}

.opacity-slider {
  width: 100%;
}

.map-visualization {
  flex: 1;
  position: relative;
  overflow: auto;
}

.map-container {
  position: relative;
  min-height: 100%;
  background: #0a0a0a;
  overflow: hidden;
  cursor: move;
}

.world-map-svg {
  width: 100%;
  height: 100%;
  display: block;
}

.world-map-svg circle.selected {
  stroke: #00ff88 !important;
  stroke-width: 3 !important;
  filter: drop-shadow(0 0 8px rgba(0, 255, 136, 0.8));
}

.zoom-controls {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 10;
}

.zoom-btn {
  width: 40px;
  height: 40px;
  background: rgba(42, 42, 42, 0.9);
  border: 1px solid #444;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  transition: all 0.2s;
}

.zoom-btn:hover {
  background: rgba(0, 255, 136, 0.2);
  border-color: #00ff88;
}

.node-details {
  width: 300px;
  background: #2a2a2a;
  border-left: 1px solid #444;
  overflow-y: auto;
}

.details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #333;
  border-bottom: 1px solid #444;
}

.details-header h3 {
  margin: 0;
  color: #00ff88;
}

.close-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.details-content {
  padding: 1rem;
}

.detail-section {
  margin-bottom: 1rem;
}

.detail-section label {
  display: block;
  color: #888;
  font-size: 0.9em;
  margin-bottom: 0.25rem;
}

.detail-section p {
  margin: 0;
  line-height: 1.4;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.tag {
  background: #444;
  color: #00ff88;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8em;
}

.borders-list {
  margin: 0;
  padding-left: 1rem;
}

.edit-controls {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.edit-btn {
  padding: 0.5rem 1rem;
  background: #ff8800;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.edit-mode-controls {
  padding: 1rem;
  background: #2a2a2a;
  border-top: 1px solid #444;
}

.edit-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.save-btn {
  padding: 0.75rem 1.5rem;
  background: #00ff88;
  color: #000;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.save-btn:disabled {
  background: #444;
  color: #888;
  cursor: not-allowed;
}

.discard-btn {
  padding: 0.75rem 1.5rem;
  background: #ff4444;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.discard-btn:disabled {
  background: #444;
  color: #888;
  cursor: not-allowed;
}

.edit-all-btn {
  padding: 0.75rem 1.5rem;
  background: #8844ff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

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
  z-index: 2000;
}

.modal-content {
  background: #2a2a2a;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-content.large {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #333;
  border-bottom: 1px solid #444;
}

.modal-header h3 {
  margin: 0;
  color: #00ff88;
}

.editor-format-toggle {
  display: flex;
  gap: 0.5rem;
}

.editor-format-toggle button {
  padding: 0.25rem 0.5rem;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8em;
}

.editor-format-toggle button.active {
  background: #00ff88;
  color: #000;
}

.modal-body {
  padding: 1rem;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  color: #888;
  margin-bottom: 0.25rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
}

.json-editor {
  width: 100%;
  height: 400px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
  background: #1a1a1a;
  color: #00ff88;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 1rem;
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.cancel-btn {
  padding: 0.5rem 1rem;
  background: #666;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
}

.loading-spinner {
  color: #00ff88;
  font-size: 1.2rem;
}
</style>