import { ref, reactive, computed } from 'vue'

// Types
export interface MapMetadata {
  width: number
  height: number
  backgroundImage: string
  version: string
  created: string
  modified: string
}

export interface MapPoint {
  x: number
  y: number
}

export interface MapContinent {
  id: string
  name: string
  points: MapPoint[]
  color: string
  visible: boolean
  borderVisible: boolean
  fillVisible: boolean
  borderWidth: number
  borderColor: string
  countries: MapCountry[]
}

export interface MapCountry {
  id: string
  name: string
  points: MapPoint[]
  color: string
  visible: boolean
  borderVisible: boolean
  fillVisible: boolean
  borderWidth: number
  borderColor: string
  cities: MapCity[]
}

export interface MapCity {
  id: string
  name: string
  points?: MapPoint[] // For area type
  position?: MapPoint // For point type
  type: 'major' | 'medium' | 'small'
  cityType: 'area' | 'point'
  color: string
  visible: boolean
  borderVisible: boolean
  fillVisible: boolean
  labelVisible: boolean
  size?: number // For point type
}

export interface MapRoute {
  id: string
  name: string
  points: MapPoint[]
  color: string
  width: number
  style: 'solid' | 'dashed' | 'dotted'
  visible: boolean
  type: 'maritime' | 'aerial' | 'dimensional' | 'road'
}

export interface MapMarker {
  id: string
  name: string
  position: MapPoint
  type: string
  color: string
  icon: string
  size: number
  visible: boolean
  labelVisible: boolean
  description?: string
}

export interface MapLabel {
  id: string
  text: string
  position: MapPoint
  fontSize: number
  color: string
  fontWeight: 'normal' | 'bold'
  visible: boolean
  background: boolean
  backgroundColor?: string
}

export interface MapData {
  metadata: MapMetadata
  continents: MapContinent[]
  routes: MapRoute[]
  markers: MapMarker[]
  labels: MapLabel[]
}

// Default map data
const createDefaultMapData = (): MapData => ({
  metadata: {
    width: 1920,
    height: 1080,
    backgroundImage: '',
    version: '1.0.0',
    created: new Date().toISOString(),
    modified: new Date().toISOString()
  },
  continents: [],
  routes: [],
  markers: [],
  labels: []
})

// Sample map data for testing
const createSampleMapData = (): MapData => ({
  metadata: {
    width: 1920,
    height: 1080,
    backgroundImage: '',
    version: '1.0.0',
    created: new Date().toISOString(),
    modified: new Date().toISOString()
  },
  continents: [
    {
      id: 'continent_1',
      name: 'Mainland Primus',
      points: [
        { x: 30, y: 30 },
        { x: 70, y: 30 },
        { x: 70, y: 70 },
        { x: 30, y: 70 }
      ],
      color: '#2a4a2a',
      visible: true,
      borderVisible: true,
      fillVisible: true,
      borderWidth: 2,
      borderColor: '#4a6a4a',
      countries: [
        {
          id: 'country_1',
          name: 'Central Kingdom',
          points: [
            { x: 40, y: 40 },
            { x: 60, y: 40 },
            { x: 60, y: 60 },
            { x: 40, y: 60 }
          ],
          color: '#3a5a3a',
          visible: true,
          borderVisible: true,
          fillVisible: true,
          borderWidth: 1,
          borderColor: '#5a7a5a',
          cities: [
            {
              id: 'city_1',
              name: 'Capital City',
              position: { x: 50, y: 50 },
              type: 'major',
              cityType: 'point',
              color: '#fbbf24',
              visible: true,
              borderVisible: true,
              fillVisible: true,
              labelVisible: true,
              size: 8
            }
          ]
        }
      ]
    }
  ],
  routes: [
    {
      id: 'route_1',
      name: 'Trade Route 1',
      points: [
        { x: 20, y: 20 },
        { x: 50, y: 50 },
        { x: 80, y: 80 }
      ],
      color: '#60a5fa',
      width: 3,
      style: 'dashed',
      visible: true,
      type: 'maritime'
    }
  ],
  markers: [
    {
      id: 'marker_1',
      name: 'Ancient Ruins',
      position: { x: 25, y: 75 },
      type: 'landmark',
      color: '#8b5cf6',
      icon: '🏛️',
      size: 6,
      visible: true,
      labelVisible: true,
      description: 'Mysterious ancient ruins'
    },
    {
      id: 'marker_2',
      name: 'Dragon Lair',
      position: { x: 75, y: 25 },
      type: 'hazard',
      color: '#ef4444',
      icon: '🐉',
      size: 8,
      visible: true,
      labelVisible: true,
      description: 'Dangerous dragon territory'
    }
  ],
  labels: [
    {
      id: 'label_1',
      text: 'The Great Ocean',
      position: { x: 15, y: 85 },
      fontSize: 16,
      color: '#60a5fa',
      fontWeight: 'bold',
      visible: true,
      background: true,
      backgroundColor: 'rgba(0, 0, 0, 0.7)'
    }
  ]
})

export function useMapData(initialData?: MapData | null) {
  // Reactive map data
  const mapData = ref<MapData>(
    initialData ||
    (localStorage.getItem('worldMapData') ?
      JSON.parse(localStorage.getItem('worldMapData')!) :
      createSampleMapData())
  )

  // Auto-save to localStorage
  const autoSave = () => {
    try {
      mapData.value.metadata.modified = new Date().toISOString()
      localStorage.setItem('worldMapData', JSON.stringify(mapData.value))
    } catch (error) {
      console.error('Failed to auto-save map data:', error)
    }
  }

  // Load map data
  const loadMapData = (data: MapData) => {
    try {
      // Validate data structure
      if (!data.metadata || !data.continents || !data.routes || !data.markers || !data.labels) {
        throw new Error('Invalid map data structure')
      }

      mapData.value = { ...data }
      autoSave()
      return true
    } catch (error) {
      console.error('Failed to load map data:', error)
      return false
    }
  }

  // Import map data from JSON
  const importMapData = (jsonData: any) => {
    try {
      // Basic validation
      if (typeof jsonData !== 'object' || !jsonData.metadata) {
        throw new Error('Invalid JSON structure')
      }

      // Merge with default structure to ensure all required fields exist
      const defaultData = createDefaultMapData()
      const mergedData: MapData = {
        metadata: { ...defaultData.metadata, ...jsonData.metadata },
        continents: jsonData.continents || [],
        routes: jsonData.routes || [],
        markers: jsonData.markers || [],
        labels: jsonData.labels || []
      }

      mapData.value = mergedData
      autoSave()
      return true
    } catch (error) {
      console.error('Failed to import map data:', error)
      return false
    }
  }

  // Export map data to JSON
  const exportMapData = (): MapData => {
    // Update metadata before export
    mapData.value.metadata.modified = new Date().toISOString()
    return JSON.parse(JSON.stringify(mapData.value)) // Deep clone
  }

  // Reset to default
  const resetMapData = () => {
    mapData.value = createDefaultMapData()
    autoSave()
  }

  // Create new item with unique ID
  const createUniqueId = (type: string): string => {
    return `${type}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  // Add continent
  const addContinent = (continentData: Partial<MapContinent>): MapContinent => {
    const continent: MapContinent = {
      id: createUniqueId('continent'),
      name: continentData.name || 'New Continent',
      points: continentData.points || [],
      color: continentData.color || '#2a4a2a',
      visible: continentData.visible !== false,
      borderVisible: continentData.borderVisible !== false,
      fillVisible: continentData.fillVisible !== false,
      borderWidth: continentData.borderWidth || 2,
      borderColor: continentData.borderColor || '#4a6a4a',
      countries: continentData.countries || []
    }

    mapData.value.continents.push(continent)
    autoSave()
    return continent
  }

  // Add route
  const addRoute = (routeData: Partial<MapRoute>): MapRoute => {
    const route: MapRoute = {
      id: createUniqueId('route'),
      name: routeData.name || 'New Route',
      points: routeData.points || [],
      color: routeData.color || '#60a5fa',
      width: routeData.width || 3,
      style: routeData.style || 'solid',
      visible: routeData.visible !== false,
      type: routeData.type || 'road'
    }

    mapData.value.routes.push(route)
    autoSave()
    return route
  }

  // Add marker
  const addMarker = (markerData: Partial<MapMarker>): MapMarker => {
    const marker: MapMarker = {
      id: createUniqueId('marker'),
      name: markerData.name || 'New Marker',
      position: markerData.position || { x: 50, y: 50 },
      type: markerData.type || 'landmark',
      color: markerData.color || '#8b5cf6',
      icon: markerData.icon || '📍',
      size: markerData.size || 6,
      visible: markerData.visible !== false,
      labelVisible: markerData.labelVisible !== false,
      description: markerData.description || ''
    }

    mapData.value.markers.push(marker)
    autoSave()
    return marker
  }

  // Add label
  const addLabel = (labelData: Partial<MapLabel>): MapLabel => {
    const label: MapLabel = {
      id: createUniqueId('label'),
      text: labelData.text || 'New Label',
      position: labelData.position || { x: 50, y: 50 },
      fontSize: labelData.fontSize || 14,
      color: labelData.color || '#ffffff',
      fontWeight: labelData.fontWeight || 'normal',
      visible: labelData.visible !== false,
      background: labelData.background !== false,
      backgroundColor: labelData.backgroundColor || 'rgba(0, 0, 0, 0.7)'
    }

    mapData.value.labels.push(label)
    autoSave()
    return label
  }

  // Remove item by ID
  const removeItem = (id: string): boolean => {
    const layers = ['continents', 'routes', 'markers', 'labels'] as const

    for (const layerName of layers) {
      const layer = mapData.value[layerName] as any[]
      const index = layer.findIndex(item => item.id === id)
      if (index !== -1) {
        layer.splice(index, 1)
        autoSave()
        return true
      }
    }

    return false
  }

  // Update item
  const updateItem = (id: string, updates: any): boolean => {
    const layers = ['continents', 'routes', 'markers', 'labels'] as const

    for (const layerName of layers) {
      const layer = mapData.value[layerName] as any[]
      const index = layer.findIndex(item => item.id === id)
      if (index !== -1) {
        layer[index] = { ...layer[index], ...updates }
        autoSave()
        return true
      }
    }

    return false
  }

  // Find item by ID
  const findItem = (id: string): any | null => {
    const layers = ['continents', 'routes', 'markers', 'labels'] as const

    for (const layerName of layers) {
      const layer = mapData.value[layerName] as any[]
      const item = layer.find(item => item.id === id)
      if (item) {
        return item
      }
    }

    return null
  }

  // Get statistics
  const statistics = computed(() => ({
    continents: mapData.value.continents.length,
    countries: mapData.value.continents.reduce((sum, continent) => sum + continent.countries.length, 0),
    cities: mapData.value.continents.reduce((sum, continent) =>
      sum + continent.countries.reduce((citySum, country) => citySum + country.cities.length, 0), 0),
    routes: mapData.value.routes.length,
    markers: mapData.value.markers.length,
    labels: mapData.value.labels.length
  }))

  // Coordinate conversion utilities
  const percentToPixel = (percent: number, dimension: 'width' | 'height'): number => {
    const size = dimension === 'width' ? mapData.value.metadata.width : mapData.value.metadata.height
    return (percent / 100) * size
  }

  const pixelToPercent = (pixel: number, dimension: 'width' | 'height'): number => {
    const size = dimension === 'width' ? mapData.value.metadata.width : mapData.value.metadata.height
    return (pixel / size) * 100
  }

  const convertPointToPixels = (point: MapPoint): MapPoint => ({
    x: percentToPixel(point.x, 'width'),
    y: percentToPixel(point.y, 'height')
  })

  const convertPointToPercent = (point: MapPoint): MapPoint => ({
    x: pixelToPercent(point.x, 'width'),
    y: pixelToPercent(point.y, 'height')
  })

  return {
    mapData,
    loadMapData,
    importMapData,
    exportMapData,
    resetMapData,
    addContinent,
    addRoute,
    addMarker,
    addLabel,
    removeItem,
    updateItem,
    findItem,
    statistics,
    percentToPixel,
    pixelToPercent,
    convertPointToPixels,
    convertPointToPercent,
    autoSave
  }
}