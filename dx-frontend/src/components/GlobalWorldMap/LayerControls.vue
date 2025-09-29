<template>
  <div class="layer-controls">
    <div class="layer-controls__header">
      <h3>Layers</h3>
      <div class="layer-controls__actions">
        <button
          @click="expandAll"
          class="btn-icon"
          title="Expand All"
        >
          <i class="fas fa-expand-alt"></i>
        </button>
        <button
          @click="collapseAll"
          class="btn-icon"
          title="Collapse All"
        >
          <i class="fas fa-compress-alt"></i>
        </button>
      </div>
    </div>

    <div class="layer-controls__content">
      <!-- Background Layer -->
      <div class="layer-item layer-item--root">
        <div class="layer-item__header">
          <i class="layer-icon fas fa-image"></i>
          <span class="layer-name">Background Image</span>
          <div class="layer-actions">
            <button
              @click="$emit('upload-background')"
              class="btn-icon btn-icon--small"
              title="Upload Background"
            >
              <i class="fas fa-upload"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Continents Layer -->
      <div class="layer-item layer-item--root">
        <div class="layer-item__header" @click="toggleExpanded('continents')">
          <i
            :class="['expand-icon', 'fas', expanded.continents ? 'fa-chevron-down' : 'fa-chevron-right']"
          ></i>
          <i class="layer-icon fas fa-globe-americas"></i>
          <span class="layer-name">Continents ({{ mapData.continents.length }})</span>
          <div class="layer-actions">
            <button
              @click.stop="toggleAllLayerVisibility('continents')"
              class="btn-icon btn-icon--small"
              :title="allContinentsVisible ? 'Hide All' : 'Show All'"
            >
              <i :class="['fas', allContinentsVisible ? 'fa-eye' : 'fa-eye-slash']"></i>
            </button>
            <button
              @click.stop="addNewContinent"
              class="btn-icon btn-icon--small"
              title="Add Continent"
            >
              <i class="fas fa-plus"></i>
            </button>
          </div>
        </div>

        <!-- Continent Items -->
        <div v-if="expanded.continents" class="layer-children">
          <div
            v-for="continent in mapData.continents"
            :key="continent.id"
            class="layer-item layer-item--child"
            :class="{ 'layer-item--selected': selectedItem?.id === continent.id }"
          >
            <div class="layer-item__header" @click="selectItem(continent)">
              <i
                :class="['expand-icon', 'fas', expanded[continent.id] ? 'fa-chevron-down' : 'fa-chevron-right']"
                @click.stop="toggleExpanded(continent.id)"
              ></i>
              <div class="layer-visibility">
                <input
                  type="checkbox"
                  :checked="continent.visible"
                  @change="toggleItemVisibility(continent, 'visible')"
                  @click.stop
                />
              </div>
              <span class="layer-name">{{ continent.name }}</span>
              <div class="layer-actions">
                <button
                  @click.stop="toggleItemVisibility(continent, 'fillVisible')"
                  class="btn-icon btn-icon--small"
                  :class="{ active: continent.fillVisible }"
                  title="Toggle Fill"
                >
                  <i class="fas fa-fill"></i>
                </button>
                <button
                  @click.stop="toggleItemVisibility(continent, 'borderVisible')"
                  class="btn-icon btn-icon--small"
                  :class="{ active: continent.borderVisible }"
                  title="Toggle Border"
                >
                  <i class="fas fa-border-style"></i>
                </button>
                <button
                  @click.stop="deleteItem(continent)"
                  class="btn-icon btn-icon--small btn-icon--danger"
                  title="Delete Continent"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>

            <!-- Countries within Continent -->
            <div v-if="expanded[continent.id]" class="layer-children">
              <div class="layer-item layer-item--subheader">
                <span class="layer-name">Countries ({{ continent.countries.length }})</span>
                <button
                  @click.stop="addNewCountry(continent)"
                  class="btn-icon btn-icon--small"
                  title="Add Country"
                >
                  <i class="fas fa-plus"></i>
                </button>
              </div>

              <div
                v-for="country in continent.countries"
                :key="country.id"
                class="layer-item layer-item--grandchild"
                :class="{ 'layer-item--selected': selectedItem?.id === country.id }"
              >
                <div class="layer-item__header" @click="selectItem(country)">
                  <i
                    :class="['expand-icon', 'fas', expanded[country.id] ? 'fa-chevron-down' : 'fa-chevron-right']"
                    @click.stop="toggleExpanded(country.id)"
                  ></i>
                  <div class="layer-visibility">
                    <input
                      type="checkbox"
                      :checked="country.visible"
                      @change="toggleItemVisibility(country, 'visible')"
                      @click.stop
                    />
                  </div>
                  <span class="layer-name">{{ country.name }}</span>
                  <div class="layer-actions">
                    <button
                      @click.stop="toggleItemVisibility(country, 'fillVisible')"
                      class="btn-icon btn-icon--small"
                      :class="{ active: country.fillVisible }"
                      title="Toggle Fill"
                    >
                      <i class="fas fa-fill"></i>
                    </button>
                    <button
                      @click.stop="toggleItemVisibility(country, 'borderVisible')"
                      class="btn-icon btn-icon--small"
                      :class="{ active: country.borderVisible }"
                      title="Toggle Border"
                    >
                      <i class="fas fa-border-style"></i>
                    </button>
                    <button
                      @click.stop="deleteItem(country)"
                      class="btn-icon btn-icon--small btn-icon--danger"
                      title="Delete Country"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>

                <!-- Cities within Country -->
                <div v-if="expanded[country.id]" class="layer-children">
                  <div class="layer-item layer-item--subheader">
                    <span class="layer-name">Cities ({{ country.cities.length }})</span>
                    <button
                      @click.stop="addNewCity(country)"
                      class="btn-icon btn-icon--small"
                      title="Add City"
                    >
                      <i class="fas fa-plus"></i>
                    </button>
                  </div>

                  <div
                    v-for="city in country.cities"
                    :key="city.id"
                    class="layer-item layer-item--leaf"
                    :class="{ 'layer-item--selected': selectedItem?.id === city.id }"
                  >
                    <div class="layer-item__header" @click="selectItem(city)">
                      <div class="layer-visibility">
                        <input
                          type="checkbox"
                          :checked="city.visible"
                          @change="toggleItemVisibility(city, 'visible')"
                          @click.stop
                        />
                      </div>
                      <i :class="['layer-icon', 'fas', getCityIcon(city.type)]"></i>
                      <span class="layer-name">{{ city.name }}</span>
                      <div class="layer-actions">
                        <button
                          @click.stop="toggleItemVisibility(city, 'labelVisible')"
                          class="btn-icon btn-icon--small"
                          :class="{ active: city.labelVisible }"
                          title="Toggle Label"
                        >
                          <i class="fas fa-tag"></i>
                        </button>
                        <button
                          @click.stop="deleteItem(city)"
                          class="btn-icon btn-icon--small btn-icon--danger"
                          title="Delete City"
                        >
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Routes Layer -->
      <div class="layer-item layer-item--root">
        <div class="layer-item__header" @click="toggleExpanded('routes')">
          <i
            :class="['expand-icon', 'fas', expanded.routes ? 'fa-chevron-down' : 'fa-chevron-right']"
          ></i>
          <i class="layer-icon fas fa-route"></i>
          <span class="layer-name">Routes ({{ mapData.routes.length }})</span>
          <div class="layer-actions">
            <button
              @click.stop="toggleAllLayerVisibility('routes')"
              class="btn-icon btn-icon--small"
              :title="allRoutesVisible ? 'Hide All' : 'Show All'"
            >
              <i :class="['fas', allRoutesVisible ? 'fa-eye' : 'fa-eye-slash']"></i>
            </button>
            <button
              @click.stop="addNewRoute"
              class="btn-icon btn-icon--small"
              title="Add Route"
            >
              <i class="fas fa-plus"></i>
            </button>
          </div>
        </div>

        <div v-if="expanded.routes" class="layer-children">
          <div
            v-for="route in mapData.routes"
            :key="route.id"
            class="layer-item layer-item--child"
            :class="{ 'layer-item--selected': selectedItem?.id === route.id }"
          >
            <div class="layer-item__header" @click="selectItem(route)">
              <div class="layer-visibility">
                <input
                  type="checkbox"
                  :checked="route.visible"
                  @change="toggleItemVisibility(route, 'visible')"
                  @click.stop
                />
              </div>
              <i :class="['layer-icon', 'fas', getRouteIcon(route.type)]"></i>
              <span class="layer-name">{{ route.name }}</span>
              <div class="layer-actions">
                <button
                  @click.stop="deleteItem(route)"
                  class="btn-icon btn-icon--small btn-icon--danger"
                  title="Delete Route"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Markers Layer -->
      <div class="layer-item layer-item--root">
        <div class="layer-item__header" @click="toggleExpanded('markers')">
          <i
            :class="['expand-icon', 'fas', expanded.markers ? 'fa-chevron-down' : 'fa-chevron-right']"
          ></i>
          <i class="layer-icon fas fa-map-pin"></i>
          <span class="layer-name">Markers ({{ mapData.markers.length }})</span>
          <div class="layer-actions">
            <button
              @click.stop="toggleAllLayerVisibility('markers')"
              class="btn-icon btn-icon--small"
              :title="allMarkersVisible ? 'Hide All' : 'Show All'"
            >
              <i :class="['fas', allMarkersVisible ? 'fa-eye' : 'fa-eye-slash']"></i>
            </button>
            <button
              @click.stop="addNewMarker"
              class="btn-icon btn-icon--small"
              title="Add Marker"
            >
              <i class="fas fa-plus"></i>
            </button>
          </div>
        </div>

        <div v-if="expanded.markers" class="layer-children">
          <!-- Group markers by type -->
          <div v-for="(markers, type) in groupedMarkers" :key="type" class="layer-group">
            <div class="layer-item layer-item--subheader">
              <i :class="['layer-icon', 'fas', getMarkerIcon(type)]"></i>
              <span class="layer-name">{{ capitalizeFirst(type) }}s ({{ markers.length }})</span>
              <button
                @click.stop="toggleMarkerTypeVisibility(type)"
                class="btn-icon btn-icon--small"
                :title="isMarkerTypeVisible(type) ? 'Hide All' : 'Show All'"
              >
                <i :class="['fas', isMarkerTypeVisible(type) ? 'fa-eye' : 'fa-eye-slash']"></i>
              </button>
            </div>

            <div
              v-for="marker in markers"
              :key="marker.id"
              class="layer-item layer-item--child"
              :class="{ 'layer-item--selected': selectedItem?.id === marker.id }"
            >
              <div class="layer-item__header" @click="selectItem(marker)">
                <div class="layer-visibility">
                  <input
                    type="checkbox"
                    :checked="marker.visible"
                    @change="toggleItemVisibility(marker, 'visible')"
                    @click.stop
                  />
                </div>
                <span class="marker-icon">{{ marker.icon }}</span>
                <span class="layer-name">{{ marker.name }}</span>
                <div class="layer-actions">
                  <button
                    @click.stop="toggleItemVisibility(marker, 'labelVisible')"
                    class="btn-icon btn-icon--small"
                    :class="{ active: marker.labelVisible }"
                    title="Toggle Label"
                  >
                    <i class="fas fa-tag"></i>
                  </button>
                  <button
                    @click.stop="deleteItem(marker)"
                    class="btn-icon btn-icon--small btn-icon--danger"
                    title="Delete Marker"
                  >
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Labels Layer -->
      <div class="layer-item layer-item--root">
        <div class="layer-item__header" @click="toggleExpanded('labels')">
          <i
            :class="['expand-icon', 'fas', expanded.labels ? 'fa-chevron-down' : 'fa-chevron-right']"
          ></i>
          <i class="layer-icon fas fa-tags"></i>
          <span class="layer-name">Labels ({{ mapData.labels.length }})</span>
          <div class="layer-actions">
            <button
              @click.stop="toggleAllLayerVisibility('labels')"
              class="btn-icon btn-icon--small"
              :title="allLabelsVisible ? 'Hide All' : 'Show All'"
            >
              <i :class="['fas', allLabelsVisible ? 'fa-eye' : 'fa-eye-slash']"></i>
            </button>
            <button
              @click.stop="addNewLabel"
              class="btn-icon btn-icon--small"
              title="Add Label"
            >
              <i class="fas fa-plus"></i>
            </button>
          </div>
        </div>

        <div v-if="expanded.labels" class="layer-children">
          <div
            v-for="label in mapData.labels"
            :key="label.id"
            class="layer-item layer-item--child"
            :class="{ 'layer-item--selected': selectedItem?.id === label.id }"
          >
            <div class="layer-item__header" @click="selectItem(label)">
              <div class="layer-visibility">
                <input
                  type="checkbox"
                  :checked="label.visible"
                  @change="toggleItemVisibility(label, 'visible')"
                  @click.stop
                />
              </div>
              <i class="layer-icon fas fa-tag"></i>
              <span class="layer-name">{{ label.text }}</span>
              <div class="layer-actions">
                <button
                  @click.stop="deleteItem(label)"
                  class="btn-icon btn-icon--small btn-icon--danger"
                  title="Delete Label"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistics -->
    <div class="layer-controls__footer">
      <div class="statistics">
        <div class="stat-item">
          <span class="stat-label">Total Elements:</span>
          <span class="stat-value">{{ totalElements }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import type { MapData } from '@/composables/GlobalWorldMap/useMapData'

// Props
interface Props {
  mapData: MapData
  selectedItem?: any
}

const props = withDefaults(defineProps<Props>(), {
  selectedItem: null
})

// Emits
const emit = defineEmits<{
  'toggle-layer': [layerType: string, itemId?: string, property?: string]
  'select-item': [item: any]
  'add-item': [type: string, parentId?: string]
  'delete-item': [item: any]
  'upload-background': []
}>()

// State
const expanded = reactive<Record<string, boolean>>({
  continents: true,
  routes: false,
  markers: false,
  labels: false
})

// Computed
const allContinentsVisible = computed(() =>
  props.mapData.continents.length > 0 && props.mapData.continents.every(c => c.visible)
)

const allRoutesVisible = computed(() =>
  props.mapData.routes.length > 0 && props.mapData.routes.every(r => r.visible)
)

const allMarkersVisible = computed(() =>
  props.mapData.markers.length > 0 && props.mapData.markers.every(m => m.visible)
)

const allLabelsVisible = computed(() =>
  props.mapData.labels.length > 0 && props.mapData.labels.every(l => l.visible)
)

const groupedMarkers = computed(() => {
  const groups: Record<string, any[]> = {}
  props.mapData.markers.forEach(marker => {
    if (!groups[marker.type]) {
      groups[marker.type] = []
    }
    groups[marker.type].push(marker)
  })
  return groups
})

const totalElements = computed(() => {
  let total = props.mapData.continents.length
  total += props.mapData.continents.reduce((sum, continent) => {
    sum += continent.countries.length
    sum += continent.countries.reduce((citySum, country) => citySum + country.cities.length, 0)
    return sum
  }, 0)
  total += props.mapData.routes.length
  total += props.mapData.markers.length
  total += props.mapData.labels.length
  return total
})

// Methods
const toggleExpanded = (key: string) => {
  expanded[key] = !expanded[key]
}

const expandAll = () => {
  Object.keys(expanded).forEach(key => {
    expanded[key] = true
  })

  // Also expand all continents and countries
  props.mapData.continents.forEach(continent => {
    expanded[continent.id] = true
    continent.countries.forEach(country => {
      expanded[country.id] = true
    })
  })
}

const collapseAll = () => {
  Object.keys(expanded).forEach(key => {
    expanded[key] = false
  })

  // Also collapse all continents and countries
  props.mapData.continents.forEach(continent => {
    expanded[continent.id] = false
    continent.countries.forEach(country => {
      expanded[country.id] = false
    })
  })
}

const selectItem = (item: any) => {
  emit('select-item', item)
}

const toggleItemVisibility = (item: any, property: string) => {
  emit('toggle-layer', 'item', item.id, property)
}

const toggleAllLayerVisibility = (layerType: string) => {
  emit('toggle-layer', layerType)
}

const toggleMarkerTypeVisibility = (type: string) => {
  const markers = props.mapData.markers.filter(m => m.type === type)
  const allVisible = markers.every(m => m.visible)

  markers.forEach(marker => {
    if (marker.visible === allVisible) {
      emit('toggle-layer', 'item', marker.id, 'visible')
    }
  })
}

const isMarkerTypeVisible = (type: string): boolean => {
  const markers = props.mapData.markers.filter(m => m.type === type)
  return markers.length > 0 && markers.every(m => m.visible)
}

const deleteItem = (item: any) => {
  if (confirm(`Are you sure you want to delete "${item.name || item.text}"?`)) {
    emit('delete-item', item)
  }
}

// Add new items
const addNewContinent = () => {
  emit('add-item', 'continent')
}

const addNewCountry = (continent: any) => {
  emit('add-item', 'country', continent.id)
}

const addNewCity = (country: any) => {
  emit('add-item', 'city', country.id)
}

const addNewRoute = () => {
  emit('add-item', 'route')
}

const addNewMarker = () => {
  emit('add-item', 'marker')
}

const addNewLabel = () => {
  emit('add-item', 'label')
}

// Icon helpers
const getCityIcon = (type: string): string => {
  switch (type) {
    case 'major': return 'fa-city'
    case 'medium': return 'fa-building'
    case 'small': return 'fa-home'
    default: return 'fa-map-marker-alt'
  }
}

const getRouteIcon = (type: string): string => {
  switch (type) {
    case 'maritime': return 'fa-ship'
    case 'aerial': return 'fa-plane'
    case 'dimensional': return 'fa-magic'
    case 'road': return 'fa-road'
    default: return 'fa-route'
  }
}

const getMarkerIcon = (type: string): string => {
  switch (type) {
    case 'hazard': return 'fa-exclamation-triangle'
    case 'landmark': return 'fa-monument'
    case 'city': return 'fa-city'
    default: return 'fa-map-pin'
  }
}

const capitalizeFirst = (str: string): string => {
  return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>

<style scoped>
.layer-controls {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #2a2a2a;
  color: #ffffff;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.layer-controls__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 2px solid rgba(250, 218, 149, 0.3);
  background: rgba(0, 0, 0, 0.3);
}

.layer-controls__header h3 {
  margin: 0;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  text-shadow: 0 0 8px rgba(250, 218, 149, 0.3);
}

.layer-controls__actions {
  display: flex;
  gap: 0.5rem;
}

.layer-controls__content {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem 0;
}

.layer-controls__footer {
  padding: 1rem;
  border-top: 2px solid rgba(250, 218, 149, 0.3);
  background: rgba(0, 0, 0, 0.3);
}

.layer-item {
  position: relative;
}

.layer-item__header {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  gap: 0.5rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.layer-item__header:hover {
  background: rgba(250, 218, 149, 0.1);
  border-left: 3px solid rgba(250, 218, 149, 0.5);
}

.layer-item--selected .layer-item__header {
  background: rgba(127, 255, 22, 0.1);
  border-left: 3px solid #7fff16;
  color: #7fff16;
}

.layer-item--root {
  border-bottom: 1px solid #3a3a3a;
}

.layer-item--child {
  padding-left: 1rem;
}

.layer-item--grandchild {
  padding-left: 2rem;
}

.layer-item--leaf {
  padding-left: 3rem;
}

.layer-item--subheader .layer-item__header {
  background: #333333;
  font-weight: bold;
  font-size: 0.875rem;
}

.layer-children {
  background: rgba(0, 0, 0, 0.1);
}

.layer-group {
  margin-bottom: 0.5rem;
}

.expand-icon {
  width: 12px;
  font-size: 0.75rem;
  color: #9ca3af;
  cursor: pointer;
}

.layer-icon {
  width: 16px;
  font-size: 0.875rem;
  color: #fada95;
  text-shadow: 0 0 4px rgba(250, 218, 149, 0.3);
}

.layer-name {
  flex: 1;
  font-size: 0.875rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
}

.layer-visibility {
  display: flex;
  align-items: center;
}

.layer-visibility input[type="checkbox"] {
  margin: 0;
  cursor: pointer;
  accent-color: #fada95;
}

.layer-actions {
  display: flex;
  gap: 0.25rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.layer-item__header:hover .layer-actions {
  opacity: 1;
}

.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border: 1px solid rgba(250, 218, 149, 0.3);
  border-radius: 3px;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-icon:hover {
  background: rgba(250, 218, 149, 0.1);
  border-color: #fada95;
  color: #fada95;
  box-shadow: 0 0 6px rgba(250, 218, 149, 0.3);
  transform: scale(1.1);
}

.btn-icon.active {
  background: rgba(127, 255, 22, 0.1);
  border-color: #7fff16;
  color: #7fff16;
  box-shadow: 0 0 8px rgba(127, 255, 22, 0.4);
}

.btn-icon--small {
  width: 20px;
  height: 20px;
  font-size: 0.75rem;
}

.btn-icon--danger:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
  color: #ef4444;
  box-shadow: 0 0 6px rgba(239, 68, 68, 0.3);
}

.marker-icon {
  width: 16px;
  text-align: center;
  font-size: 0.875rem;
}

.statistics {
  font-size: 0.75rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
  padding: 0.25rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
  border: 1px solid rgba(250, 218, 149, 0.1);
}

.stat-label {
  font-weight: normal;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.stat-value {
  font-weight: bold;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-shadow: 0 0 4px rgba(250, 218, 149, 0.3);
}
</style>