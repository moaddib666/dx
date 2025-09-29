<template>
  <div class="properties-panel">
    <div class="properties-panel__header">
      <h3>Properties</h3>
      <button
        v-if="selectedItem"
        @click="clearSelection"
        class="btn-icon"
        title="Clear Selection"
      >
        <i class="fas fa-times"></i>
      </button>
    </div>

    <div class="properties-panel__content">
      <!-- No Selection State -->
      <div v-if="!selectedItem" class="no-selection">
        <div class="no-selection__icon">
          <i class="fas fa-mouse-pointer"></i>
        </div>
        <p>Select an item to edit its properties</p>

        <!-- Map Statistics -->
        <div class="map-stats">
          <h4>Map Statistics</h4>
          <div class="stat-grid">
            <div class="stat-item">
              <span class="stat-label">Continents:</span>
              <span class="stat-value">{{ statistics.continents }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Countries:</span>
              <span class="stat-value">{{ statistics.countries }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Cities:</span>
              <span class="stat-value">{{ statistics.cities }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Routes:</span>
              <span class="stat-value">{{ statistics.routes }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Markers:</span>
              <span class="stat-value">{{ statistics.markers }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Labels:</span>
              <span class="stat-value">{{ statistics.labels }}</span>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="quick-actions">
          <h4>Quick Actions</h4>
          <button @click="$emit('add-item', 'continent')" class="action-btn">
            <i class="fas fa-globe-americas"></i>
            Add Continent
          </button>
          <button @click="$emit('add-item', 'route')" class="action-btn">
            <i class="fas fa-route"></i>
            Add Route
          </button>
          <button @click="$emit('add-item', 'marker')" class="action-btn">
            <i class="fas fa-map-pin"></i>
            Add Marker
          </button>
          <button @click="$emit('add-item', 'label')" class="action-btn">
            <i class="fas fa-tag"></i>
            Add Label
          </button>
        </div>
      </div>

      <!-- Continent Properties -->
      <div v-else-if="selectedItem.type === 'continent' || (selectedItem.countries !== undefined)" class="properties-form">
        <div class="form-header">
          <i class="fas fa-globe-americas"></i>
          <span>Continent Properties</span>
        </div>

        <div class="form-group">
          <label>Name</label>
          <input
            v-model="localItem.name"
            type="text"
            @input="updateItem"
            placeholder="Continent name"
          />
        </div>

        <div class="form-group">
          <label>Fill Color</label>
          <div class="color-input-group">
            <input
              v-model="localItem.color"
              type="color"
              @input="updateItem"
            />
            <input
              v-model="localItem.color"
              type="text"
              @input="updateItem"
              placeholder="#2a4a2a"
            />
          </div>
        </div>

        <div class="form-group">
          <label>Border Color</label>
          <div class="color-input-group">
            <input
              v-model="localItem.borderColor"
              type="color"
              @input="updateItem"
            />
            <input
              v-model="localItem.borderColor"
              type="text"
              @input="updateItem"
              placeholder="#4a6a4a"
            />
          </div>
        </div>

        <div class="form-group">
          <label>Border Width</label>
          <input
            v-model.number="localItem.borderWidth"
            type="range"
            min="1"
            max="10"
            @input="updateItem"
          />
          <span class="range-value">{{ localItem.borderWidth }}px</span>
        </div>

        <div class="form-group">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input
                v-model="localItem.visible"
                type="checkbox"
                @change="updateItem"
              />
              Visible
            </label>
            <label class="checkbox-label">
              <input
                v-model="localItem.fillVisible"
                type="checkbox"
                @change="updateItem"
              />
              Show Fill
            </label>
            <label class="checkbox-label">
              <input
                v-model="localItem.borderVisible"
                type="checkbox"
                @change="updateItem"
              />
              Show Border
            </label>
          </div>
        </div>

        <div class="form-group">
          <label>Countries ({{ localItem.countries?.length || 0 }})</label>
          <button @click="$emit('add-item', 'country', selectedItem.id)" class="add-btn">
            <i class="fas fa-plus"></i>
            Add Country
          </button>
        </div>
      </div>

      <!-- Country Properties -->
      <div v-else-if="selectedItem.type === 'country' || (selectedItem.cities !== undefined && selectedItem.countries === undefined)" class="properties-form">
        <div class="form-header">
          <i class="fas fa-flag"></i>
          <span>Country Properties</span>
        </div>

        <div class="form-group">
          <label>Name</label>
          <input
            v-model="localItem.name"
            type="text"
            @input="updateItem"
            placeholder="Country name"
          />
        </div>

        <div class="form-group">
          <label>Fill Color</label>
          <div class="color-input-group">
            <input
              v-model="localItem.color"
              type="color"
              @input="updateItem"
            />
            <input
              v-model="localItem.color"
              type="text"
              @input="updateItem"
              placeholder="#3a5a3a"
            />
          </div>
        </div>

        <div class="form-group">
          <label>Border Color</label>
          <div class="color-input-group">
            <input
              v-model="localItem.borderColor"
              type="color"
              @input="updateItem"
            />
            <input
              v-model="localItem.borderColor"
              type="text"
              @input="updateItem"
              placeholder="#5a7a5a"
            />
          </div>
        </div>

        <div class="form-group">
          <label>Border Width</label>
          <input
            v-model.number="localItem.borderWidth"
            type="range"
            min="1"
            max="10"
            @input="updateItem"
          />
          <span class="range-value">{{ localItem.borderWidth }}px</span>
        </div>

        <div class="form-group">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input
                v-model="localItem.visible"
                type="checkbox"
                @change="updateItem"
              />
              Visible
            </label>
            <label class="checkbox-label">
              <input
                v-model="localItem.fillVisible"
                type="checkbox"
                @change="updateItem"
              />
              Show Fill
            </label>
            <label class="checkbox-label">
              <input
                v-model="localItem.borderVisible"
                type="checkbox"
                @change="updateItem"
              />
              Show Border
            </label>
          </div>
        </div>

        <div class="form-group">
          <label>Cities ({{ localItem.cities?.length || 0 }})</label>
          <button @click="$emit('add-item', 'city', selectedItem.id)" class="add-btn">
            <i class="fas fa-plus"></i>
            Add City
          </button>
        </div>
      </div>

      <!-- City Properties -->
      <div v-else-if="selectedItem.type === 'city' || selectedItem.cityType !== undefined" class="properties-form">
        <div class="form-header">
          <i :class="['fas', getCityIcon(localItem.type)]"></i>
          <span>City Properties</span>
        </div>

        <div class="form-group">
          <label>Name</label>
          <input
            v-model="localItem.name"
            type="text"
            @input="updateItem"
            placeholder="City name"
          />
        </div>

        <div class="form-group">
          <label>City Type</label>
          <select v-model="localItem.type" @change="updateItem">
            <option value="major">Major City</option>
            <option value="medium">Medium City</option>
            <option value="small">Small City</option>
          </select>
        </div>

        <div class="form-group">
          <label>Display Type</label>
          <select v-model="localItem.cityType" @change="updateItem">
            <option value="point">Point Marker</option>
            <option value="area">Area Polygon</option>
          </select>
        </div>

        <div class="form-group">
          <label>Color</label>
          <div class="color-input-group">
            <input
              v-model="localItem.color"
              type="color"
              @input="updateItem"
            />
            <input
              v-model="localItem.color"
              type="text"
              @input="updateItem"
              placeholder="#fbbf24"
            />
          </div>
        </div>

        <div v-if="localItem.cityType === 'point'" class="form-group">
          <label>Size</label>
          <input
            v-model.number="localItem.size"
            type="range"
            min="3"
            max="20"
            @input="updateItem"
          />
          <span class="range-value">{{ localItem.size }}px</span>
        </div>

        <div class="form-group">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input
                v-model="localItem.visible"
                type="checkbox"
                @change="updateItem"
              />
              Visible
            </label>
            <label class="checkbox-label">
              <input
                v-model="localItem.labelVisible"
                type="checkbox"
                @change="updateItem"
              />
              Show Label
            </label>
            <label v-if="localItem.cityType === 'area'" class="checkbox-label">
              <input
                v-model="localItem.fillVisible"
                type="checkbox"
                @change="updateItem"
              />
              Show Fill
            </label>
            <label v-if="localItem.cityType === 'area'" class="checkbox-label">
              <input
                v-model="localItem.borderVisible"
                type="checkbox"
                @change="updateItem"
              />
              Show Border
            </label>
          </div>
        </div>
      </div>

      <!-- Route Properties -->
      <div v-else-if="selectedItem.type === 'route' || selectedItem.points !== undefined" class="properties-form">
        <div class="form-header">
          <i class="fas fa-route"></i>
          <span>Route Properties</span>
        </div>

        <div class="form-group">
          <label>Name</label>
          <input
            v-model="localItem.name"
            type="text"
            @input="updateItem"
            placeholder="Route name"
          />
        </div>

        <div class="form-group">
          <label>Route Type</label>
          <select v-model="localItem.type" @change="updateItem">
            <option value="road">Road</option>
            <option value="maritime">Maritime</option>
            <option value="aerial">Aerial</option>
            <option value="dimensional">Dimensional</option>
          </select>
        </div>

        <div class="form-group">
          <label>Color</label>
          <div class="color-input-group">
            <input
              v-model="localItem.color"
              type="color"
              @input="updateItem"
            />
            <input
              v-model="localItem.color"
              type="text"
              @input="updateItem"
              placeholder="#60a5fa"
            />
          </div>
        </div>

        <div class="form-group">
          <label>Width</label>
          <input
            v-model.number="localItem.width"
            type="range"
            min="1"
            max="10"
            @input="updateItem"
          />
          <span class="range-value">{{ localItem.width }}px</span>
        </div>

        <div class="form-group">
          <label>Line Style</label>
          <select v-model="localItem.style" @change="updateItem">
            <option value="solid">Solid</option>
            <option value="dashed">Dashed</option>
            <option value="dotted">Dotted</option>
          </select>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input
              v-model="localItem.visible"
              type="checkbox"
              @change="updateItem"
            />
            Visible
          </label>
        </div>

        <div class="form-group">
          <label>Points ({{ localItem.points?.length || 0 }})</label>
          <div class="points-info">
            <small>Use the drawing tool to modify route points</small>
          </div>
        </div>
      </div>

      <!-- Marker Properties -->
      <div v-else-if="selectedItem.type === 'marker' || (selectedItem.position !== undefined && selectedItem.icon !== undefined)" class="properties-form">
        <div class="form-header">
          <i class="fas fa-map-pin"></i>
          <span>Marker Properties</span>
        </div>

        <div class="form-group">
          <label>Name</label>
          <input
            v-model="localItem.name"
            type="text"
            @input="updateItem"
            placeholder="Marker name"
          />
        </div>

        <div class="form-group">
          <label>Type</label>
          <select v-model="localItem.type" @change="updateItem">
            <option value="landmark">Landmark</option>
            <option value="hazard">Hazard</option>
            <option value="city">City</option>
            <option value="custom">Custom</option>
          </select>
        </div>

        <div class="form-group">
          <label>Icon</label>
          <div class="icon-input-group">
            <input
              v-model="localItem.icon"
              type="text"
              @input="updateItem"
              placeholder="📍"
              maxlength="2"
            />
            <div class="icon-preview">{{ localItem.icon }}</div>
          </div>
          <div class="icon-suggestions">
            <button
              v-for="icon in getIconSuggestions(localItem.type)"
              :key="icon"
              @click="setIcon(icon)"
              class="icon-btn"
            >
              {{ icon }}
            </button>
          </div>
        </div>

        <div class="form-group">
          <label>Color</label>
          <div class="color-input-group">
            <input
              v-model="localItem.color"
              type="color"
              @input="updateItem"
            />
            <input
              v-model="localItem.color"
              type="text"
              @input="updateItem"
              placeholder="#8b5cf6"
            />
          </div>
        </div>

        <div class="form-group">
          <label>Size</label>
          <input
            v-model.number="localItem.size"
            type="range"
            min="3"
            max="20"
            @input="updateItem"
          />
          <span class="range-value">{{ localItem.size }}px</span>
        </div>

        <div class="form-group">
          <label>Description</label>
          <textarea
            v-model="localItem.description"
            @input="updateItem"
            placeholder="Optional description"
            rows="3"
          ></textarea>
        </div>

        <div class="form-group">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input
                v-model="localItem.visible"
                type="checkbox"
                @change="updateItem"
              />
              Visible
            </label>
            <label class="checkbox-label">
              <input
                v-model="localItem.labelVisible"
                type="checkbox"
                @change="updateItem"
              />
              Show Label
            </label>
          </div>
        </div>

        <div class="form-group">
          <label>Position</label>
          <div class="position-inputs">
            <div class="position-input">
              <label>X (%)</label>
              <input
                v-model.number="localItem.position.x"
                type="number"
                min="0"
                max="100"
                step="0.1"
                @input="updateItem"
              />
            </div>
            <div class="position-input">
              <label>Y (%)</label>
              <input
                v-model.number="localItem.position.y"
                type="number"
                min="0"
                max="100"
                step="0.1"
                @input="updateItem"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Label Properties -->
      <div v-else-if="selectedItem.type === 'label' || selectedItem.text !== undefined" class="properties-form">
        <div class="form-header">
          <i class="fas fa-tag"></i>
          <span>Label Properties</span>
        </div>

        <div class="form-group">
          <label>Text</label>
          <input
            v-model="localItem.text"
            type="text"
            @input="updateItem"
            placeholder="Label text"
          />
        </div>

        <div class="form-group">
          <label>Font Size</label>
          <input
            v-model.number="localItem.fontSize"
            type="range"
            min="8"
            max="48"
            @input="updateItem"
          />
          <span class="range-value">{{ localItem.fontSize }}px</span>
        </div>

        <div class="form-group">
          <label>Font Weight</label>
          <select v-model="localItem.fontWeight" @change="updateItem">
            <option value="normal">Normal</option>
            <option value="bold">Bold</option>
          </select>
        </div>

        <div class="form-group">
          <label>Text Color</label>
          <div class="color-input-group">
            <input
              v-model="localItem.color"
              type="color"
              @input="updateItem"
            />
            <input
              v-model="localItem.color"
              type="text"
              @input="updateItem"
              placeholder="#ffffff"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input
              v-model="localItem.background"
              type="checkbox"
              @change="updateItem"
            />
            Show Background
          </label>
        </div>

        <div v-if="localItem.background" class="form-group">
          <label>Background Color</label>
          <div class="color-input-group">
            <input
              v-model="localItem.backgroundColor"
              type="color"
              @input="updateItem"
            />
            <input
              v-model="localItem.backgroundColor"
              type="text"
              @input="updateItem"
              placeholder="rgba(0, 0, 0, 0.7)"
            />
          </div>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input
              v-model="localItem.visible"
              type="checkbox"
              @change="updateItem"
            />
            Visible
          </label>
        </div>

        <div class="form-group">
          <label>Position</label>
          <div class="position-inputs">
            <div class="position-input">
              <label>X (%)</label>
              <input
                v-model.number="localItem.position.x"
                type="number"
                min="0"
                max="100"
                step="0.1"
                @input="updateItem"
              />
            </div>
            <div class="position-input">
              <label>Y (%)</label>
              <input
                v-model.number="localItem.position.y"
                type="number"
                min="0"
                max="100"
                step="0.1"
                @input="updateItem"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Delete Button -->
      <div v-if="selectedItem" class="form-actions">
        <button @click="deleteItem" class="delete-btn">
          <i class="fas fa-trash"></i>
          Delete {{ getItemTypeName(selectedItem) }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { MapData } from '@/composables/GlobalWorldMap/useMapData'

// Props
interface Props {
  selectedItem?: any
  mapData: MapData
}

const props = withDefaults(defineProps<Props>(), {
  selectedItem: null
})

// Emits
const emit = defineEmits<{
  'item-update': [item: any]
  'item-delete': [item: any]
  'clear-selection': []
  'add-item': [type: string, parentId?: string]
}>()

// Local state for editing
const localItem = ref<any>({})

// Computed
const statistics = computed(() => {
  let continents = props.mapData.continents.length
  let countries = props.mapData.continents.reduce((sum, continent) => sum + continent.countries.length, 0)
  let cities = props.mapData.continents.reduce((sum, continent) =>
    sum + continent.countries.reduce((citySum, country) => citySum + country.cities.length, 0), 0)
  let routes = props.mapData.routes.length
  let markers = props.mapData.markers.length
  let labels = props.mapData.labels.length

  return { continents, countries, cities, routes, markers, labels }
})

// Methods
const clearSelection = () => {
  emit('clear-selection')
}

const updateItem = () => {
  if (localItem.value && props.selectedItem) {
    emit('item-update', { ...localItem.value })
  }
}

const deleteItem = () => {
  if (props.selectedItem) {
    const itemName = props.selectedItem.name || props.selectedItem.text || 'item'
    if (confirm(`Are you sure you want to delete "${itemName}"?`)) {
      emit('item-delete', props.selectedItem)
    }
  }
}

const getCityIcon = (type: string): string => {
  switch (type) {
    case 'major': return 'fa-city'
    case 'medium': return 'fa-building'
    case 'small': return 'fa-home'
    default: return 'fa-map-marker-alt'
  }
}

const getItemTypeName = (item: any): string => {
  if (item.countries !== undefined) return 'Continent'
  if (item.cities !== undefined && item.countries === undefined) return 'Country'
  if (item.cityType !== undefined) return 'City'
  if (item.points !== undefined && item.style !== undefined) return 'Route'
  if (item.icon !== undefined) return 'Marker'
  if (item.text !== undefined) return 'Label'
  return 'Item'
}

const getIconSuggestions = (type: string): string[] => {
  switch (type) {
    case 'landmark':
      return ['🏛️', '🗿', '🏰', '🏯', '🗼', '⛩️', '🕌', '⛪']
    case 'hazard':
      return ['⚠️', '☠️', '🔥', '⚡', '🌋', '💀', '☢️', '☣️']
    case 'city':
      return ['🏙️', '🏘️', '🏠', '🏢', '🏛️', '🏰', '🕌', '⛪']
    default:
      return ['📍', '📌', '🎯', '⭐', '💎', '🔮', '🗺️', '🧭']
  }
}

const setIcon = (icon: string) => {
  localItem.value.icon = icon
  updateItem()
}

// Watch for selected item changes
watch(() => props.selectedItem, (newItem) => {
  if (newItem) {
    // Deep clone the selected item for local editing
    localItem.value = JSON.parse(JSON.stringify(newItem))
  } else {
    localItem.value = {}
  }
}, { immediate: true, deep: true })
</script>

<style scoped>
.properties-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #2a2a2a;
  color: #ffffff;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.properties-panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 2px solid rgba(250, 218, 149, 0.3);
  background: rgba(0, 0, 0, 0.3);
}

.properties-panel__header h3 {
  margin: 0;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  text-shadow: 0 0 8px rgba(250, 218, 149, 0.3);
}

.properties-panel__content {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.no-selection {
  text-align: center;
  color: #9ca3af;
}

.no-selection__icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.map-stats {
  margin: 2rem 0;
  text-align: left;
}

.map-stats h4 {
  margin-bottom: 1rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  text-shadow: 0 0 6px rgba(250, 218, 149, 0.3);
}

.stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(250, 218, 149, 0.2);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  border-color: rgba(250, 218, 149, 0.4);
  box-shadow: 0 0 6px rgba(250, 218, 149, 0.2);
}

.stat-label {
  font-size: 0.875rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.stat-value {
  font-weight: bold;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.quick-actions {
  margin-top: 2rem;
  text-align: left;
}

.quick-actions h4 {
  margin-bottom: 1rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  text-shadow: 0 0 6px rgba(250, 218, 149, 0.3);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(250, 218, 149, 0.3);
  border-radius: 4px;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(250, 218, 149, 0.1);
  border-color: #fada95;
  box-shadow: 0 0 8px rgba(250, 218, 149, 0.3);
  transform: scale(1.02);
}

.properties-form {
  text-align: left;
}

.form-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid rgba(250, 218, 149, 0.3);
  font-weight: bold;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-shadow: 0 0 6px rgba(250, 218, 149, 0.3);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(250, 218, 149, 0.3);
  border-radius: 4px;
  color: #fada95;
  font-size: 0.875rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  transition: all 0.3s ease;
}

.form-group input[type="text"]:focus,
.form-group input[type="number"]:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #fada95;
  box-shadow: 0 0 8px rgba(250, 218, 149, 0.3);
  background: rgba(250, 218, 149, 0.05);
}

.form-group input[type="range"] {
  width: 100%;
  margin-bottom: 0.25rem;
}

.range-value {
  font-size: 0.75rem;
  color: #9ca3af;
}

.color-input-group {
  display: flex;
  gap: 0.5rem;
}

.color-input-group input[type="color"] {
  width: 40px;
  height: 38px;
  padding: 0;
  border: 1px solid #4a4a4a;
  border-radius: 4px;
  cursor: pointer;
}

.color-input-group input[type="text"] {
  flex: 1;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-label {
  display: flex !important;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0 !important;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin: 0;
}

.icon-input-group {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.icon-input-group input {
  flex: 1;
}

.icon-preview {
  width: 40px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1a1a1a;
  border: 1px solid #4a4a4a;
  border-radius: 4px;
  font-size: 1.2rem;
}

.icon-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-top: 0.5rem;
}

.icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #3a3a3a;
  border: 1px solid #4a4a4a;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.icon-btn:hover {
  background: #4a4a4a;
}

.position-inputs {
  display: flex;
  gap: 0.5rem;
}

.position-input {
  flex: 1;
}

.position-input label {
  font-size: 0.75rem;
  margin-bottom: 0.25rem;
}

.points-info {
  padding: 0.5rem;
  background: #1a1a1a;
  border-radius: 4px;
  border: 1px solid #4a4a4a;
}

.points-info small {
  color: #9ca3af;
  font-style: italic;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #10b981;
  border: none;
  border-radius: 4px;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  background: #059669;
}

.form-actions {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #3a3a3a;
}

.delete-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem;
  background: #ef4444;
  border: none;
  border-radius: 4px;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s;
}

.delete-btn:hover {
  background: #dc2626;
}

.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: #9ca3af;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: #4a5568;
  color: #ffffff;
}
</style>