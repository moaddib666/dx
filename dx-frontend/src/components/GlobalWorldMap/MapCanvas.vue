<template>
  <div class="map-canvas-container" ref="containerRef">
    <canvas
        ref="canvasRef"
        class="map-canvas"
        :width="canvasWidth"
        :height="canvasHeight"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
        @mouseleave="handleMouseUp"
        @wheel="handleWheel"
        @touchstart="handleTouchStart"
        @touchmove="handleTouchMove"
        @touchend="handleTouchEnd"
        @click="handleClick"
        @dblclick="handleDoubleClick"
    />

    <!-- Crosshair cursor for drawing tools -->
    <div
        v-if="showCrosshair"
        class="crosshair"
        :style="{ left: cursorPosition.x + 'px', top: cursorPosition.y + 'px' }"
    />

    <!-- Drawing preview -->
    <svg
        v-if="isDrawing && drawingPoints.length > 0"
        class="drawing-preview"
        :width="canvasWidth"
        :height="canvasHeight"
    >
      <polyline
          :points="drawingPointsString"
          fill="none"
          stroke="#60a5fa"
          stroke-width="2"
          stroke-dasharray="5,5"
      />
    </svg>

    <!-- Scale counter -->
    <div class="scale-counter">
      <div class="scale-label">Scale</div>
      <div class="scale-value">{{ Math.round(zoom * 100) }}%</div>
      <div class="scale-range">
        {{ Math.round((mapData.metadata.minZoom ?? 0.1) * 100) }}% -
        {{ Math.round((mapData.metadata.maxZoom ?? 5.0) * 100) }}%
      </div>
    </div>

    <!-- Label Meta Card -->
    <LabelMetaCard
      :visible="labelMetaCard.visible"
      :metadata="labelMetaCard.metadata"
      :position="labelMetaCard.position"
      :loading="labelMetaCard.loading"
      @close="closeLabelMetaCard"
    />
  </div>
</template>

<script setup lang="ts">
import {ref, computed, onMounted, onUnmounted, watch, nextTick} from 'vue'
import {useMapInteraction} from '@/composables/GlobalWorldMap/useMapInteraction'
import type {
  MapData,
  MapPoint,
  MapContinent,
  MapRoute,
  MapMarker,
  MapLabel
} from '@/composables/GlobalWorldMap/useMapData'
import {createFogMask, createEdgePerlinMask} from '@/utils/perlinNoise'
import LabelMetaCard from './LabelMetaCard.vue'
import { FileMetadataResolver } from '@/services/metadata/FileMetadataResolver'
import type { PlaceMetadata } from '@/services/metadata/MetadataResolver'

// Props
interface Props {
  mapData: MapData
  activeTool: string
  zoom: number
  pan: MapPoint
  selectedItem?: any
}

const props = withDefaults(defineProps<Props>(), {
  selectedItem: null
})

// Emits
const emit = defineEmits<{
  'zoom-change': [zoom: number]
  'pan-change': [pan: MapPoint]
  'item-select': [item: any]
  'item-create': [item: any]
  'item-update': [item: any]
  'item-delete': [item: any]
}>()

// Refs
const containerRef = ref<HTMLDivElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const backgroundImage = ref<HTMLImageElement | null>(null)
const fogTexture = ref<HTMLImageElement | null>(null)
const fogMaskCanvas = ref<HTMLCanvasElement | null>(null)
const edgeMaskCanvas = ref<HTMLCanvasElement | null>(null)

// Track highlighted markers for fog clearing
const highlightedMarkers = ref<Array<{position: MapPoint, size: number}>>([])

// Track hovered marker for hover visibility
const hoveredMarker = ref<any>(null)

// Label Meta Card state
const labelMetaCard = ref({
  visible: false,
  metadata: null as PlaceMetadata | null,
  position: { x: 0, y: 0 },
  loading: false
})

// Metadata resolver instance
const metadataResolver = new FileMetadataResolver()

// Composables
const {
  drawingPoints,
  isDrawing,
  handleMouseDown: interactionMouseDown,
  handleMouseMove: interactionMouseMove,
  handleMouseUp: interactionMouseUp,
  handleWheel: interactionWheel,
  handleTouchStart: interactionTouchStart,
  handleTouchMove: interactionTouchMove,
  handleTouchEnd: interactionTouchEnd,
  screenToPercent,
  percentToScreen,
  pointInPolygon,
  pointInCircle,
  distanceToLine,
  startDrawing,
  addDrawingPoint,
  finishDrawing: finishDrawingPoints,
  cancelDrawing
} = useMapInteraction()

// State
const canvasWidth = ref(800)
const canvasHeight = ref(600)
const cursorPosition = ref({x: 0, y: 0})
const needsRedraw = ref(true)
const isDragging = ref(false)
const dragStart = ref<{ x: number, y: number } | null>(null)

// Stable coordinate system state
const baseAspectRatio = ref(16 / 9) // Default aspect ratio for coordinate system
const coordinateScale = ref(1) // Scale factor for coordinate system
const viewportOffset = ref({x: 0, y: 0}) // Offset for letterboxing/pillarboxing

// Object movement state
const isMovingObject = ref(false)
const movingItem = ref<any>(null)
const moveStartPosition = ref<MapPoint | null>(null)

// Computed
const showCrosshair = computed(() => {
  return ['draw-polygon', 'draw-route', 'add-marker', 'add-label', 'move'].includes(props.activeTool)
})

const drawingPointsString = computed(() => {
  return drawingPoints.value.map(p => `${p.x},${p.y}`).join(' ')
})

// Canvas context
let ctx: CanvasRenderingContext2D | null = null

// Stable coordinate system calculations
const getStableCoordinateSystem = () => {
  const containerAspect = canvasWidth.value / canvasHeight.value
  const baseAspect = baseAspectRatio.value

  let stableWidth, stableHeight, offsetX, offsetY, scale

  if (containerAspect > baseAspect) {
    // Container is wider than base aspect - fit by height
    stableHeight = canvasHeight.value
    stableWidth = stableHeight * baseAspect
    offsetX = (canvasWidth.value - stableWidth) / 2
    offsetY = 0
    scale = stableHeight / 600 // Base height reference
  } else {
    // Container is taller than base aspect - fit by width
    stableWidth = canvasWidth.value
    stableHeight = stableWidth / baseAspect
    offsetX = 0
    offsetY = (canvasHeight.value - stableHeight) / 2
    scale = stableWidth / (600 * baseAspect) // Base width reference
  }

  return {stableWidth, stableHeight, offsetX, offsetY, scale}
}

// Map bounds calculation for preventing out-of-bounds movement
const calculateMapBounds = () => {
  if (!backgroundImage.value) return null

  // Calculate scaled image dimensions for full canvas approach
  const scaledImageWidth = canvasWidth.value * props.zoom
  const scaledImageHeight = canvasHeight.value * props.zoom

  // Calculate bounds to prevent panning outside the map image
  // When zoomed out (zoom < 1), prevent showing areas beyond the map
  // When zoomed in (zoom > 1), allow panning within the larger image

  const minPanX = Math.min(0, canvasWidth.value - scaledImageWidth)
  const maxPanX = 0
  const minPanY = Math.min(0, canvasHeight.value - scaledImageHeight)
  const maxPanY = 0

  return {
    minX: minPanX,
    maxX: maxPanX,
    minY: minPanY,
    maxY: maxPanY
  }
}

// Apply bounds constraints to pan values
const constrainPan = (pan: MapPoint): MapPoint => {
  const bounds = calculateMapBounds()
  if (!bounds) return pan

  return {
    x: Math.max(bounds.minX, Math.min(bounds.maxX, pan.x)),
    y: Math.max(bounds.minY, Math.min(bounds.maxY, pan.y))
  }
}

// Local coordinate transformation methods (using full viewport)
const screenToPercentLocal = (screenPoint: MapPoint): MapPoint => {
  // Convert screen coordinates to world coordinates using component's pan/zoom
  const worldX = (screenPoint.x - props.pan.x) / props.zoom
  const worldY = (screenPoint.y - props.pan.y) / props.zoom

  // Convert world coordinates to percentage using full canvas dimensions
  return {
    x: (worldX / canvasWidth.value) * 100,
    y: (worldY / canvasHeight.value) * 100
  }
}

const percentToScreenLocal = (percentPoint: MapPoint): MapPoint => {
  // Convert percentage to world coordinates using full canvas dimensions
  const worldX = (percentPoint.x / 100) * canvasWidth.value
  const worldY = (percentPoint.y / 100) * canvasHeight.value

  // Convert world coordinates to screen coordinates using component's pan/zoom
  const screenX = worldX * props.zoom + props.pan.x
  const screenY = worldY * props.zoom + props.pan.y

  return {
    x: screenX,
    y: screenY
  }
}

// Methods
const initCanvas = () => {
  if (!canvasRef.value || !containerRef.value) return

  ctx = canvasRef.value.getContext('2d')
  if (!ctx) return

  // Set up canvas size
  updateCanvasSize()

  // Load background image if exists
  if (props.mapData.metadata.backgroundImage) {
    loadBackgroundImage(props.mapData.metadata.backgroundImage)
  }

  // Load fog of war texture
  loadFogTexture()

  // Create edge mask for map edge transparency
  createEdgeMaskCanvas()

  // Initial render
  render()
}

const updateCanvasSize = () => {
  if (!containerRef.value || !canvasRef.value) return

  const container = containerRef.value
  const rect = container.getBoundingClientRect()

  canvasWidth.value = rect.width
  canvasHeight.value = rect.height

  // Set canvas size
  canvasRef.value.width = canvasWidth.value
  canvasRef.value.height = canvasHeight.value

  // Recreate edge mask for new canvas size
  createEdgeMaskCanvas()

  needsRedraw.value = true
}

const loadBackgroundImage = (imageSrc: string) => {
  if (!imageSrc) return

  const img = new Image()
  img.onload = () => {
    backgroundImage.value = img
    needsRedraw.value = true
    render()
  }
  img.onerror = () => {
    console.error('Failed to load background image')
    backgroundImage.value = null
  }
  img.src = imageSrc
}

const loadFogTexture = () => {
  const img = new Image()
  img.onload = () => {
    fogTexture.value = img
    createFogMaskCanvas()
    needsRedraw.value = true
  }
  img.onerror = () => {
    console.error('Failed to load fog of war texture')
    fogTexture.value = null
  }
  img.src = '/src/assets/world-map/fog-of-war.png'
}

const createFogMaskCanvas = () => {
  if (!fogTexture.value) return

  const maskCanvas = document.createElement('canvas')
  const {stableWidth, stableHeight} = getStableCoordinateSystem()

  // Create mask at a reasonable resolution for performance
  const maskWidth = Math.min(512, stableWidth)
  const maskHeight = Math.min(512, stableHeight)

  maskCanvas.width = maskWidth
  maskCanvas.height = maskHeight

  const maskCtx = maskCanvas.getContext('2d')
  if (!maskCtx) return

  // Generate Perlin noise mask
  const fogMask = createFogMask(maskWidth, maskHeight, 0.02, 4, 0.5, 42)
  maskCtx.putImageData(fogMask, 0, 0)

  fogMaskCanvas.value = maskCanvas
}

const createEdgeMaskCanvas = (cursorX?: number, cursorY?: number) => {
  const maskCanvas = document.createElement('canvas')

  // Create edge mask at full canvas resolution for proper viewport edge effects
  maskCanvas.width = canvasWidth.value
  maskCanvas.height = canvasHeight.value

  const maskCtx = maskCanvas.getContext('2d')
  if (!maskCtx) return

  // Use cursor position or default to center for dynamic dark overlay
  const centerX = cursorX !== undefined ? cursorX : canvasWidth.value / 2
  const centerY = cursorY !== undefined ? cursorY : canvasHeight.value / 2
  const maxRadius = Math.max(canvasWidth.value, canvasHeight.value) * 0.6 // 60% of canvas for more prominent effect

  // Create radial gradient for dark overlay effect
  const gradient = maskCtx.createRadialGradient(
    centerX, centerY, 0,           // Inner circle (cursor/center)
    centerX, centerY, maxRadius    // Outer circle (edges)
  )

  // Gradient creates dark overlay with light area around cursor
  gradient.addColorStop(0, 'rgba(255, 255, 255, 0)')     // Fully transparent at cursor
  gradient.addColorStop(0.3, 'rgba(255, 255, 255, 0.2)') // Light overlay starts
  gradient.addColorStop(0.6, 'rgba(255, 255, 255, 0.6)') // Medium dark overlay
  gradient.addColorStop(1, 'rgba(255, 255, 255, 0.8)')   // Strong dark overlay at edges

  // Fill the canvas with the gradient
  maskCtx.fillStyle = gradient
  maskCtx.fillRect(0, 0, canvasWidth.value, canvasHeight.value)

  // Create transparent areas around highlighted items for shiny effect
  if (highlightedMarkers.value.length > 0) {
    // Use destination-out to create transparent holes in the overlay
    maskCtx.globalCompositeOperation = 'destination-out'

    highlightedMarkers.value.forEach(marker => {
      // Convert marker position from percentage to screen coordinates using full canvas coordinates
      // This matches how markers are positioned in renderMarker function
      const worldX = (marker.position.x / 100) * canvasWidth.value
      const worldY = (marker.position.y / 100) * canvasHeight.value

      // Apply zoom and pan transformations (matching the render transformations)
      const markerScreenX = worldX * props.zoom + props.pan.x
      const markerScreenY = worldY * props.zoom + props.pan.y

      // Create highlight radius that scales with marker size
      const highlightRadius = Math.max(marker.size * 12, 80) // Slightly larger than fog clearing for better effect

      // Create radial gradient for smooth transparent area around highlighted item
      const markerGradient = maskCtx.createRadialGradient(
        markerScreenX, markerScreenY, 0,           // Inner circle (marker center)
        markerScreenX, markerScreenY, highlightRadius // Outer circle
      )

      // Gradient creates transparent area with smooth edges
      markerGradient.addColorStop(0, 'rgba(255, 255, 255, 1)')     // Fully transparent at center
      markerGradient.addColorStop(0.7, 'rgba(255, 255, 255, 0.8)') // Gradual transition
      markerGradient.addColorStop(1, 'rgba(255, 255, 255, 0)')     // Preserve overlay at edge

      maskCtx.fillStyle = markerGradient
      maskCtx.beginPath()
      maskCtx.arc(markerScreenX, markerScreenY, highlightRadius, 0, Math.PI * 2)
      maskCtx.fill()
    })
  }

  edgeMaskCanvas.value = maskCanvas
}

const render = () => {
  if (!ctx || !canvasRef.value) return

  // Clear highlighted markers from previous render
  highlightedMarkers.value = []

  // Clear entire canvas
  ctx.clearRect(0, 0, canvasWidth.value, canvasHeight.value)

  // Fill entire canvas with fog of war texture
  renderBackgroundFog()

  // Save context state
  ctx.save()

  // Apply zoom and pan transformations to fill entire viewport
  ctx.scale(props.zoom, props.zoom)
  ctx.translate(props.pan.x / props.zoom, props.pan.y / props.zoom)

  // Render layers in order to fill entire viewport
  renderBackgroundImage()
  renderContinents()
  renderRoutes()
  renderMarkers()
  renderLabels()
  renderFogOfWar()
  renderSelection()

  // Restore context state
  ctx.restore()

  // Apply edge mask to entire canvas (outside transformed coordinate system)
  renderMapEdgeMask()

  needsRedraw.value = false
}

const renderBackgroundFog = () => {
  if (!ctx) return

  // Fallback to black solid color if fog texture is not available
  if (!fogTexture.value || !fogMaskCanvas.value) {
    ctx.fillStyle = '#000'
    ctx.fillRect(0, 0, canvasWidth.value, canvasHeight.value)
    return
  }

  // Calculate tile size that responds to zoom for natural movement
  const baseTileSize = 256 // Base tile size in world coordinates
  const tileSize = baseTileSize / props.zoom // Adjust for current zoom to maintain world size

  // Calculate how many tiles we need to cover the entire canvas
  const tilesX = Math.ceil(canvasWidth.value / tileSize) + 2 // Extra tiles for seamless coverage
  const tilesY = Math.ceil(canvasHeight.value / tileSize) + 2

  // Calculate starting offset based on pan to make fog move with the view
  const startX = -((props.pan.x / props.zoom) % tileSize)
  const startY = -((props.pan.y / props.zoom) % tileSize)

  // Create a temporary canvas for compositing with Perlin noise transparency
  const tempCanvas = document.createElement('canvas')
  tempCanvas.width = canvasWidth.value
  tempCanvas.height = canvasHeight.value
  const tempCtx = tempCanvas.getContext('2d')
  if (!tempCtx) return

  // Draw repeating fog texture on temporary canvas with pan/zoom offsets
  for (let x = 0; x < tilesX; x++) {
    for (let y = 0; y < tilesY; y++) {
      const drawX = startX + x * tileSize
      const drawY = startY + y * tileSize
      tempCtx.drawImage(fogTexture.value, drawX, drawY, tileSize, tileSize)
    }
  }

  // Apply Perlin noise mask using composite operation for organic transparency
  tempCtx.globalCompositeOperation = 'destination-in'

  // Scale the fog mask to cover the entire canvas
  const maskScaleX = canvasWidth.value / fogMaskCanvas.value.width
  const maskScaleY = canvasHeight.value / fogMaskCanvas.value.height
  tempCtx.scale(maskScaleX, maskScaleY)
  tempCtx.drawImage(fogMaskCanvas.value, 0, 0)

  // Draw the final fog background with full opacity
  ctx.drawImage(tempCanvas, 0, 0)
}

const renderBackgroundImage = () => {
  if (!ctx || !backgroundImage.value) return

  const img = backgroundImage.value

  // Fill entire canvas with the map image, stretching to cover full viewport
  // This ensures no background is visible and the map takes all available space
  ctx.drawImage(img, 0, 0, canvasWidth.value, canvasHeight.value)
}

const renderFogOfWar = () => {
  if (!ctx || !fogTexture.value || !fogMaskCanvas.value) return

  const {stableWidth, stableHeight} = getStableCoordinateSystem()

  // Calculate tile size that doesn't scale with zoom
  // Use a fixed world-space size for consistent fog appearance
  const baseTileSize = 256 // Base tile size in world coordinates
  const tileSize = baseTileSize / props.zoom // Adjust for current zoom to maintain world size

  // Calculate how many tiles we need to cover the visible area
  const tilesX = Math.ceil(stableWidth / tileSize) + 2 // Extra tiles for seamless coverage
  const tilesY = Math.ceil(stableHeight / tileSize) + 2

  // Calculate starting offset to center the tiling
  const startX = -((props.pan.x / props.zoom) % tileSize)
  const startY = -((props.pan.y / props.zoom) % tileSize)

  // Save context state
  ctx.save()

  // Create a temporary canvas for compositing with Perlin noise transparency
  const tempCanvas = document.createElement('canvas')
  tempCanvas.width = stableWidth
  tempCanvas.height = stableHeight
  const tempCtx = tempCanvas.getContext('2d')
  if (!tempCtx) return

  // Draw repeating fog texture on temporary canvas
  for (let x = 0; x < tilesX; x++) {
    for (let y = 0; y < tilesY; y++) {
      const drawX = startX + x * tileSize
      const drawY = startY + y * tileSize
      tempCtx.drawImage(fogTexture.value, drawX, drawY, tileSize, tileSize)
    }
  }

  // Apply Perlin noise mask using composite operation for organic transparency
  tempCtx.globalCompositeOperation = 'destination-in'
  tempCtx.drawImage(fogMaskCanvas.value, 0, 0, stableWidth, stableHeight)

  // Apply fog clearing for mouse cursor and highlighted markers
  tempCtx.globalCompositeOperation = 'destination-out'

  // Clear fog around mouse cursor
  if (cursorPosition.value) {
    // Convert cursor screen position to stable coordinate system
    const {offsetX, offsetY} = getStableCoordinateSystem()

    // Adjust cursor position relative to stable coordinate system
    const cursorX = cursorPosition.value.x - offsetX
    const cursorY = cursorPosition.value.y - offsetY

    // Only clear fog if cursor is within the stable area
    if (cursorX >= 0 && cursorX <= stableWidth && cursorY >= 0 && cursorY <= stableHeight) {
      const cursorRadius = 80 // Fixed radius for mouse cursor fog clearing

      // Create radial gradient for smooth fog clearing around cursor
      const cursorGradient = tempCtx.createRadialGradient(
        cursorX, cursorY, 0,           // Inner circle (cursor center)
        cursorX, cursorY, cursorRadius // Outer circle
      )

      // Gradient goes from fully opaque (clear fog) to fully transparent (preserve fog)
      cursorGradient.addColorStop(0, 'rgba(0, 0, 0, 1)')     // Fully opaque at center (clear fog)
      cursorGradient.addColorStop(0.6, 'rgba(0, 0, 0, 0.8)') // Gradual transition
      cursorGradient.addColorStop(1, 'rgba(0, 0, 0, 0)')     // Fully transparent at edge (preserve fog)

      tempCtx.fillStyle = cursorGradient
      tempCtx.beginPath()
      tempCtx.arc(cursorX, cursorY, cursorRadius, 0, Math.PI * 2)
      tempCtx.fill()
    }
  }

  // Clear fog around highlighted markers
  if (highlightedMarkers.value.length > 0) {
    highlightedMarkers.value.forEach(marker => {
      // Convert marker position to stable coordinate system for fog canvas
      // Use stable coordinate system for fog rendering (this is correct for fog layer)
      const centerX = (marker.position.x / 100) * stableWidth
      const centerY = (marker.position.y / 100) * stableHeight

      // Create highlight radius that scales with marker size
      const highlightRadius = Math.max(marker.size * 8, 60) // Minimum 60px radius

      // Create radial gradient for smooth fog clearing
      const gradient = tempCtx.createRadialGradient(
        centerX, centerY, 0,           // Inner circle (center point)
        centerX, centerY, highlightRadius // Outer circle
      )

      // Gradient goes from fully transparent (clear fog) to fully opaque (preserve fog)
      gradient.addColorStop(0, 'rgba(0, 0, 0, 1)')     // Fully opaque at center (clear fog)
      gradient.addColorStop(0.7, 'rgba(0, 0, 0, 0.7)') // Gradual transition
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)')     // Fully transparent at edge (preserve fog)

      tempCtx.fillStyle = gradient
      tempCtx.beginPath()
      tempCtx.arc(centerX, centerY, highlightRadius, 0, Math.PI * 2)
      tempCtx.fill()
    })
  }

  // Draw the final fog layer with reduced opacity to allow map to show through
  ctx.globalAlpha = 0.6
  ctx.drawImage(tempCanvas, 0, 0)

  // Restore context state
  ctx.restore()
}

const renderMapEdgeMask = () => {
  if (!ctx || !edgeMaskCanvas.value) return

  // Save context state
  ctx.save()

  // Apply edge mask using destination-out to create transparency at edges
  ctx.globalCompositeOperation = 'destination-out'

  // Draw the edge mask to create organic transparency at canvas edges
  // Now using full canvas dimensions since we're outside the transformed coordinate system
  ctx.drawImage(edgeMaskCanvas.value, 0, 0, canvasWidth.value, canvasHeight.value)

  // Restore context state
  ctx.restore()
}

const renderContinents = () => {
  if (!ctx) return

  props.mapData.continents.forEach(continent => {
    if (!continent.visible) return

    renderPolygon(continent.points, {
      fillColor: continent.fillVisible ? continent.color : 'transparent',
      strokeColor: continent.borderVisible ? continent.borderColor : 'transparent',
      strokeWidth: continent.borderWidth,
      isSelected: props.selectedItem?.id === continent.id
    })

    // Render countries within continent
    continent.countries.forEach(country => {
      if (!country.visible) return

      renderPolygon(country.points, {
        fillColor: country.fillVisible ? country.color : 'transparent',
        strokeColor: country.borderVisible ? country.borderColor : 'transparent',
        strokeWidth: country.borderWidth,
        isSelected: props.selectedItem?.id === country.id
      })

      // Render cities within country
      country.cities.forEach(city => {
        if (!city.visible) return

        // Render highlight effect if city has highlight property enabled
        if (city.highlight && city.position) {
          renderMarkerHighlight(city.position, city.size || 6)
        }

        if (city.cityType === 'area' && city.points) {
          renderPolygon(city.points, {
            fillColor: city.fillVisible ? city.color : 'transparent',
            strokeColor: city.borderVisible ? city.borderColor || city.color : 'transparent',
            strokeWidth: 1,
            isSelected: props.selectedItem?.id === city.id
          })
        } else if (city.cityType === 'point' && city.position) {
          renderMarker(city.position, {
            color: city.color,
            size: city.size || 6,
            type: 'city',
            isSelected: props.selectedItem?.id === city.id
          })
        }

        // Render city label
        if (city.labelVisible && city.position) {
          renderLabel(city.position, city.name, {
            fontSize: 12,
            color: '#ffffff',
            background: true,
            backgroundColor: 'rgba(0, 0, 0, 0.7)'
          })
        }
      })
    })
  })
}

const renderRoutes = () => {
  if (!ctx) return

  props.mapData.routes.forEach(route => {
    if (!route.visible || route.points.length < 2) return

    renderPath(route.points, {
      strokeColor: route.color,
      strokeWidth: route.width,
      strokeStyle: route.style,
      isSelected: props.selectedItem?.id === route.id
    })
  })
}

const renderMarkers = () => {
  if (!ctx) return

  props.mapData.markers.forEach(marker => {
    const isHovered = hoveredMarker.value?.id === marker.id
    const shouldRender = marker.visible || isHovered

    if (!shouldRender) return

    // Render highlight effect if marker has highlight property enabled
    if (marker.highlight) {
      renderMarkerHighlight(marker.position, marker.size)
    }

    // Set transparency for hovered but normally hidden markers
    const originalAlpha = ctx.globalAlpha
    if (isHovered && !marker.visible) {
      ctx.globalAlpha = 0.7 // Semi-transparent for hovered hidden markers
    }

    renderMarker(marker.position, {
      color: marker.color,
      size: marker.size,
      type: marker.type,
      icon: marker.icon,
      isSelected: props.selectedItem?.id === marker.id,
      isHovered: isHovered
    })

    // Restore original alpha
    ctx.globalAlpha = originalAlpha

    // Render marker label (show for hovered markers even if normally hidden)
    if (marker.labelVisible || isHovered) {
      const labelOffsetPercent = (marker.size + 5) / canvasHeight.value * 100
      const labelY = marker.position.y - labelOffsetPercent
      renderLabel({x: marker.position.x, y: labelY}, marker.name, {
        fontSize: 11,
        color: '#ffffff',
        background: true,
        backgroundColor: isHovered && !marker.visible ? 'rgba(255, 255, 0, 0.8)' : 'rgba(0, 0, 0, 0.7)'
      })
    }
  })
}

const renderLabels = () => {
  if (!ctx) return

  props.mapData.labels.forEach(label => {
    if (!label.visible) return

    renderLabel(label.position, label.text, {
      fontSize: label.fontSize,
      color: label.color,
      fontWeight: label.fontWeight,
      background: label.background,
      backgroundColor: label.backgroundColor,
      isSelected: props.selectedItem?.id === label.id
    })
  })
}

const renderSelection = () => {
  if (!ctx || !props.selectedItem) return

  // Render selection highlight based on item type
  const item = props.selectedItem

  if (item.points) {
    // Polygon selection
    renderPolygonOutline(item.points, '#7fff16', 3)
    renderVertexHandles(item.points)
  } else if (item.position) {
    // Point selection
    renderCircleOutline(item.position, (item.size || 6) + 4, '#7fff16', 2)
  }
}

// Rendering utilities
const renderPolygon = (points: MapPoint[], options: {
  fillColor: string
  strokeColor: string
  strokeWidth: number
  isSelected?: boolean
}) => {
  if (!ctx || points.length < 3) return

  const {stableWidth, stableHeight} = getStableCoordinateSystem()

  ctx.beginPath()

  // Convert percentage points to stable coordinate system
  const stablePoints = points.map(p => ({
    x: (p.x / 100) * stableWidth,
    y: (p.y / 100) * stableHeight
  }))

  ctx.moveTo(stablePoints[0].x, stablePoints[0].y)
  for (let i = 1; i < stablePoints.length; i++) {
    ctx.lineTo(stablePoints[i].x, stablePoints[i].y)
  }
  ctx.closePath()

  // Fill
  if (options.fillColor !== 'transparent') {
    ctx.fillStyle = options.fillColor
    ctx.fill()
  }

  // Stroke
  if (options.strokeColor !== 'transparent') {
    ctx.strokeStyle = options.strokeColor
    ctx.lineWidth = options.strokeWidth
    ctx.stroke()
  }
}

const renderPath = (points: MapPoint[], options: {
  strokeColor: string
  strokeWidth: number
  strokeStyle: string
  isSelected?: boolean
}) => {
  if (!ctx || points.length < 2) return

  const {stableWidth, stableHeight} = getStableCoordinateSystem()

  ctx.beginPath()

  // Convert percentage points to stable coordinate system
  const stablePoints = points.map(p => ({
    x: (p.x / 100) * stableWidth,
    y: (p.y / 100) * stableHeight
  }))

  ctx.moveTo(stablePoints[0].x, stablePoints[0].y)
  for (let i = 1; i < stablePoints.length; i++) {
    ctx.lineTo(stablePoints[i].x, stablePoints[i].y)
  }

  // Set line style
  switch (options.strokeStyle) {
    case 'dashed':
      ctx.setLineDash([10, 5])
      break
    case 'dotted':
      ctx.setLineDash([2, 3])
      break
    default:
      ctx.setLineDash([])
  }

  ctx.strokeStyle = options.strokeColor
  ctx.lineWidth = options.strokeWidth
  ctx.stroke()

  // Reset line dash
  ctx.setLineDash([])
}

const renderMarker = (position: MapPoint, options: {
  color: string
  size: number
  type: string
  icon?: string
  isSelected?: boolean
  isHovered?: boolean
}) => {
  if (!ctx) return

  // Use full canvas coordinates to match background image scaling
  const x = (position.x / 100) * canvasWidth.value
  const y = (position.y / 100) * canvasHeight.value
  const radius = options.size

  // RPG-style marker with enhanced visual effects for different states
  const markerColor = options.color || '#8b5cf6'
  let borderColor = '#fada95'
  let glowColor = 'rgba(250, 218, 149, 0.3)'
  let shadowBlur = 8

  // Priority: Selected > Hovered > Default
  if (options.isSelected) {
    borderColor = '#7fff16'
    glowColor = 'rgba(127, 255, 22, 0.3)'
    shadowBlur = 10
  } else if (options.isHovered) {
    borderColor = '#00ffff'  // Cyan for hover
    glowColor = 'rgba(0, 255, 255, 0.4)'  // Cyan glow
    shadowBlur = 12  // Enhanced glow for hover
  }

  // Add glow effect
  ctx.shadowColor = glowColor
  ctx.shadowBlur = shadowBlur
  ctx.shadowOffsetX = 0
  ctx.shadowOffsetY = 0

  ctx.fillStyle = markerColor
  ctx.strokeStyle = borderColor
  ctx.lineWidth = 0.7

  if (options.type === 'hazard') {
    // Triangle for hazards with RPG styling
    ctx.beginPath()
    ctx.moveTo(x, y - radius)
    ctx.lineTo(x - radius * 0.866, y + radius * 0.5)
    ctx.lineTo(x + radius * 0.866, y + radius * 0.5)
    ctx.closePath()
    ctx.fill()
    ctx.stroke()
  } else {
    // Circle for other markers with RPG styling
    ctx.beginPath()
    ctx.arc(x, y, radius, 0, Math.PI * 2)
    ctx.fill()
    ctx.stroke()
  }

  // Reset shadow for icon rendering
  ctx.shadowColor = 'transparent'
  ctx.shadowBlur = 0

  // Render icon if provided with RPG font styling
  if (options.icon) {
    ctx.font = `${radius * 1.2}px 'Cinzel', 'Times New Roman', 'Georgia', serif`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillStyle = '#fada95'
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.8)'
    ctx.lineWidth = 0.1
    ctx.strokeText(options.icon, x, y)
    ctx.fillText(options.icon, x, y)
  }
}

const renderLabel = (position: MapPoint, text: string, options: {
  fontSize: number
  color: string
  fontWeight?: string
  background?: boolean
  backgroundColor?: string
  isSelected?: boolean
}) => {
  if (!ctx) return

  // Use full canvas coordinates to match background image scaling
  const x = (position.x / 100) * canvasWidth.value
  const y = (position.y / 100) * canvasHeight.value

  // Scale font size inversely with zoom to prevent labels from becoming too large
  const scaledFontSize = Math.max(8, Math.min(24, options.fontSize / Math.sqrt(props.zoom))) * 0.75
  ctx.font = `${options.fontWeight || 'normal'} ${scaledFontSize}px 'Cinzel', 'Times New Roman', 'Georgia', serif`
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'

  // Measure text
  const metrics = ctx.measureText(text)
  const textWidth = metrics.width
  const textHeight = scaledFontSize

  // RPG-style background with golden border
  if (options.background) {
    const bgColor = options.backgroundColor || 'rgba(0, 0, 0, 0.7)'
    const borderColor = options.isSelected ? '#7fff16' : '#fada95'
    const padding = 6

    // Add glow effect for background
    ctx.shadowColor = options.isSelected ? 'rgba(127, 255, 22, 0.3)' : 'rgba(250, 218, 149, 0.3)'
    ctx.shadowBlur = 4
    ctx.shadowOffsetX = 0
    ctx.shadowOffsetY = 0

    // Draw background with rounded corners effect
    ctx.fillStyle = bgColor
    ctx.fillRect(
        x - textWidth / 2 - padding,
        y - textHeight / 2 - 3,
        textWidth + padding * 2,
        textHeight + 6
    )

    // Draw border
    ctx.strokeStyle = borderColor
    ctx.lineWidth = 0.3
    ctx.strokeRect(
        x - textWidth / 2 - padding,
        y - textHeight / 2 - 3,
        textWidth + padding * 2,
        textHeight + 6
    )

    // Reset shadow
    ctx.shadowColor = 'transparent'
    ctx.shadowBlur = 0
  }

  // Draw text with RPG styling
  const textColor = options.color === '#ffffff' ? '#fada95' : options.color
  ctx.fillStyle = textColor
  ctx.strokeStyle = 'rgba(0, 0, 0, 0.8)'
  ctx.lineWidth = 1
  ctx.strokeText(text, x, y)
  ctx.fillText(text, x, y)
}

const renderPolygonOutline = (points: MapPoint[], color: string, width: number) => {
  if (!ctx || points.length < 3) return

  const {stableWidth, stableHeight} = getStableCoordinateSystem()

  // Add RPG-style glow effect
  ctx.shadowColor = 'rgba(127, 255, 22, 0.4)'
  ctx.shadowBlur = 6
  ctx.shadowOffsetX = 0
  ctx.shadowOffsetY = 0

  ctx.beginPath()

  const stablePoints = points.map(p => ({
    x: (p.x / 100) * stableWidth,
    y: (p.y / 100) * stableHeight
  }))

  ctx.moveTo(stablePoints[0].x, stablePoints[0].y)
  for (let i = 1; i < stablePoints.length; i++) {
    ctx.lineTo(stablePoints[i].x, stablePoints[i].y)
  }
  ctx.closePath()

  ctx.strokeStyle = color
  ctx.lineWidth = width
  ctx.stroke()

  // Reset shadow
  ctx.shadowColor = 'transparent'
  ctx.shadowBlur = 0
}

const renderCircleOutline = (position: MapPoint, radius: number, color: string, width: number) => {
  if (!ctx) return

  const {stableWidth, stableHeight} = getStableCoordinateSystem()
  const x = (position.x / 100) * stableWidth
  const y = (position.y / 100) * stableHeight

  // Add RPG-style glow effect
  ctx.shadowColor = 'rgba(127, 255, 22, 0.4)'
  ctx.shadowBlur = 8
  ctx.shadowOffsetX = 0
  ctx.shadowOffsetY = 0

  ctx.beginPath()
  ctx.arc(x, y, radius, 0, Math.PI * 2)
  ctx.strokeStyle = color
  ctx.lineWidth = width
  ctx.stroke()

  // Reset shadow
  ctx.shadowColor = 'transparent'
  ctx.shadowBlur = 0
}

const renderVertexHandles = (points: MapPoint[]) => {
  if (!ctx) return

  const {stableWidth, stableHeight} = getStableCoordinateSystem()

  points.forEach(point => {
    const x = (point.x / 100) * stableWidth
    const y = (point.y / 100) * stableHeight

    // Add RPG-style glow effect
    ctx.shadowColor = 'rgba(250, 218, 149, 0.4)'
    ctx.shadowBlur = 6
    ctx.shadowOffsetX = 0
    ctx.shadowOffsetY = 0

    ctx.beginPath()
    ctx.arc(x, y, 4, 0, Math.PI * 2)
    ctx.fillStyle = '#fada95'
    ctx.fill()
    ctx.strokeStyle = '#7fff16'
    ctx.lineWidth = 2
    ctx.stroke()

    // Reset shadow
    ctx.shadowColor = 'transparent'
    ctx.shadowBlur = 0
  })
}

const renderMarkerHighlight = (position: MapPoint, markerSize: number) => {
  // Add this highlighted marker to the collection for fog rendering
  highlightedMarkers.value.push({
    position: position,
    size: markerSize
  })
}

// Label Meta Card functions
const openLabelMetaCard = async (label: MapLabel, screenPosition: { x: number, y: number }) => {
  // Close any existing card first
  closeLabelMetaCard()

  // Set position and show loading
  labelMetaCard.value.position = screenPosition
  labelMetaCard.value.visible = true
  labelMetaCard.value.loading = true

  console.log(`🎯 openLabelMetaCard called for:`, {
    id: label.id,
    text: label.text,
    type: label.type
  })

  try {
    // Try to load existing metadata
    console.log(`🔍 Calling metadataResolver.loadMetadata with ID: "${label.id}"`)
    let metadata = await metadataResolver.loadMetadata(label.id)

    // If no metadata exists, create default metadata
    if (!metadata) {
      const { createDefaultMetadata } = await import('@/services/metadata/MetadataResolver')
      metadata = createDefaultMetadata(label.id, label.text)
      // Save the default metadata
      await metadataResolver.saveMetadata(metadata)
    }

    labelMetaCard.value.metadata = metadata
  } catch (error) {
    console.error('Failed to load label metadata:', error)
    // Create fallback metadata
    const { createDefaultMetadata } = await import('@/services/metadata/MetadataResolver')
    labelMetaCard.value.metadata = createDefaultMetadata(label.id, label.text)
  } finally {
    labelMetaCard.value.loading = false
  }
}

const closeLabelMetaCard = () => {
  labelMetaCard.value.visible = false
  labelMetaCard.value.metadata = null
  labelMetaCard.value.loading = false
}

// Event handlers
const handleMouseDown = (event: MouseEvent) => {
  if (!canvasRef.value) return

  const rect = canvasRef.value.getBoundingClientRect()
  const screenPoint = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }

  // Only handle panning for select tool when not clicking on an item
  if (props.activeTool === 'select') {
    const percentPoint = screenToPercentLocal(screenPoint)
    const hitItem = findItemAtPoint(percentPoint)

    if (!hitItem) {
      // Start panning
      isDragging.value = true
      dragStart.value = screenPoint
    }
    // Note: Item selection is handled in handleClick, not here
  }
  // Note: All other tools are handled in handleClick, not on mousedown
}

const handleMouseMove = (event: MouseEvent) => {
  if (!canvasRef.value) return

  // Update cursor position
  const rect = canvasRef.value.getBoundingClientRect()
  const currentPoint = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }
  cursorPosition.value = currentPoint

  // Check for hovered markers (including hidden ones)
  const percentPoint = screenToPercentLocal(currentPoint)
  const newHoveredMarker = findMarkerAtPoint(percentPoint)

  // Update hovered marker state if changed
  if (newHoveredMarker !== hoveredMarker.value) {
    hoveredMarker.value = newHoveredMarker
    needsRedraw.value = true

    // Handle place card display for hovered markers
    if (newHoveredMarker) {
      // Open place card for the hovered marker
      console.log(`🎯 Hovered marker data:`, {
        id: newHoveredMarker.id,
        name: newHoveredMarker.name,
        type: newHoveredMarker.type,
        fullMarker: newHoveredMarker
      })
      const markerAsLabel = {
        id: newHoveredMarker.id,
        text: newHoveredMarker.name,
        type: 'marker'
      }
      openLabelMetaCard(markerAsLabel as MapLabel, currentPoint)
    } else {
      // Close place card when no marker is hovered
      closeLabelMetaCard()
    }
  }

  // Regenerate edge mask to follow cursor for dynamic dark overlay
  createEdgeMaskCanvas(currentPoint.x, currentPoint.y)
  needsRedraw.value = true

  // Handle object movement
  if (isMovingObject.value && movingItem.value && moveStartPosition.value) {
    const currentPercentPoint = screenToPercentLocal(currentPoint)
    const deltaX = currentPercentPoint.x - moveStartPosition.value.x
    const deltaY = currentPercentPoint.y - moveStartPosition.value.y

    // Update object position based on type
    updateObjectPosition(movingItem.value, deltaX, deltaY)

    // Update start position for next move
    moveStartPosition.value = currentPercentPoint
    needsRedraw.value = true
  }
  // Handle panning
  else if (isDragging.value && dragStart.value) {
    const deltaX = currentPoint.x - dragStart.value.x
    const deltaY = currentPoint.y - dragStart.value.y

    const newPan = {
      x: props.pan.x + deltaX,
      y: props.pan.y + deltaY
    }

    // Apply bounds constraints to prevent map from moving out of view
    const constrainedPan = constrainPan(newPan)

    emit('pan-change', constrainedPan)
    dragStart.value = currentPoint
    needsRedraw.value = true
  }
}

const handleMouseUp = () => {
  // Note: Object movement is now finished by clicking with move tool, not on mouse up
  // This allows for proper click-drag-click workflow

  // Finish panning
  isDragging.value = false
  dragStart.value = null
}

const handleWheel = (event: WheelEvent) => {
  if (!canvasRef.value) return

  event.preventDefault()

  const rect = canvasRef.value.getBoundingClientRect()
  const mouseX = event.clientX - rect.left
  const mouseY = event.clientY - rect.top

  // Calculate zoom factor
  const zoomFactor = event.deltaY > 0 ? 0.9 : 1.1
  const MIN_ZOOM = props.mapData.metadata.minZoom ?? 0.1
  const MAX_ZOOM = props.mapData.metadata.maxZoom ?? 5.0
  const newZoom = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, props.zoom * zoomFactor))

  if (newZoom !== props.zoom) {
    // Calculate world point before zoom
    const worldPointBefore = {
      x: (mouseX - props.pan.x) / props.zoom,
      y: (mouseY - props.pan.y) / props.zoom
    }

    // Calculate world point after zoom
    const worldPointAfter = {
      x: (mouseX - props.pan.x) / newZoom,
      y: (mouseY - props.pan.y) / newZoom
    }

    // Adjust pan to keep the point under the mouse cursor in the same place
    const newPan = {
      x: props.pan.x + (worldPointAfter.x - worldPointBefore.x) * newZoom,
      y: props.pan.y + (worldPointAfter.y - worldPointBefore.y) * newZoom
    }

    // Apply bounds constraints to prevent map from moving out of view during zoom
    const constrainedPan = constrainPan(newPan)

    // Emit changes to parent
    emit('zoom-change', newZoom)
    emit('pan-change', constrainedPan)
  }

  needsRedraw.value = true
}

const handleTouchStart = (event: TouchEvent) => {
  if (!canvasRef.value) return
  interactionTouchStart(event, canvasRef.value)
}

const handleTouchMove = (event: TouchEvent) => {
  if (!canvasRef.value) return
  interactionTouchMove(event, canvasRef.value)
}

const handleTouchEnd = (event: TouchEvent) => {
  interactionTouchEnd(event)
}

const handleClick = (event: MouseEvent) => {
  if (!canvasRef.value) return

  // Handle tool-specific click actions
  switch (props.activeTool) {
    case 'select':
      handleSelectTool(event)
      break
    case 'move':
      handleMoveTool(event)
      break
    case 'draw-polygon':
      handleDrawPolygonTool(event)
      break
    case 'draw-route':
      handleDrawRouteTool(event)
      break
    case 'add-marker':
      handleAddMarkerTool(event)
      break
    case 'add-label':
      handleAddLabelTool(event)
      break
  }
}

const handleDoubleClick = (event: MouseEvent) => {
  // Handle double clicks (e.g., finish drawing)
  if (props.activeTool === 'draw-polygon' || props.activeTool === 'draw-route') {
    finishDrawing()
  }
}

// Tool handlers
const handleSelectTool = (event: MouseEvent) => {
  if (!canvasRef.value) return

  const rect = canvasRef.value.getBoundingClientRect()
  const screenPoint = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }

  const percentPoint = screenToPercentLocal(screenPoint)
  const hitItem = findItemAtPoint(percentPoint)

  // Check if the clicked item is a label and trigger LabelMeta card
  if (hitItem && (hitItem.type === 'label' || hitItem.text !== undefined)) {
    // Close any existing card first
    closeLabelMetaCard()

    // Open the LabelMeta card for this label
    openLabelMetaCard(hitItem as MapLabel, screenPoint)
  } else {
    // Close the card if clicking elsewhere
    closeLabelMetaCard()
  }

  emit('item-select', hitItem)
}

const handleDrawPolygonTool = (event: MouseEvent) => {
  if (!canvasRef.value) return

  const rect = canvasRef.value.getBoundingClientRect()
  const screenPoint = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }

  const percentPoint = screenToPercentLocal(screenPoint)

  if (!isDrawing.value) {
    // Start drawing a new polygon
    startDrawing(percentPoint)
  } else {
    // Add point to current polygon
    addDrawingPoint(percentPoint)
  }
}

const handleDrawRouteTool = (event: MouseEvent) => {
  // Implementation for route drawing
}

const handleAddMarkerTool = (event: MouseEvent) => {
  if (!canvasRef.value) return

  const rect = canvasRef.value.getBoundingClientRect()
  const screenPoint = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }

  const percentPoint = screenToPercentLocal(screenPoint)

  const marker = {
    type: 'marker',
    name: 'New Marker',
    position: percentPoint,
    color: '#8b5cf6',
    icon: '📍',
    size: 6,
    visible: true,
    labelVisible: true,
    description: ''
  }

  emit('item-create', marker)
}

const handleAddLabelTool = (event: MouseEvent) => {
  if (!canvasRef.value) return

  const rect = canvasRef.value.getBoundingClientRect()
  const screenPoint = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }

  const percentPoint = screenToPercentLocal(screenPoint)

  const label = {
    type: 'label',
    text: 'New Label',
    position: percentPoint,
    fontSize: 14,
    color: '#ffffff',
    fontWeight: 'normal',
    visible: true,
    background: true,
    backgroundColor: 'rgba(0, 0, 0, 0.7)'
  }

  emit('item-create', label)
}

const handleMoveTool = (event: MouseEvent) => {
  if (!canvasRef.value) return

  const rect = canvasRef.value.getBoundingClientRect()
  const screenPoint = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }

  const percentPoint = screenToPercentLocal(screenPoint)

  // If already moving an object, finish the move operation
  if (isMovingObject.value && movingItem.value) {
    // Emit the updated item
    emit('item-update', movingItem.value)

    // Reset movement state
    isMovingObject.value = false
    movingItem.value = null
    moveStartPosition.value = null
    return
  }

  // Otherwise, start moving a new object
  const hitItem = findItemAtPoint(percentPoint)

  if (hitItem) {
    // Start moving the object
    isMovingObject.value = true
    movingItem.value = hitItem
    moveStartPosition.value = {...percentPoint}

    // Select the item being moved
    emit('item-select', hitItem)
  }
}

const updateObjectPosition = (item: any, deltaX: number, deltaY: number) => {
  if (!item) return

  // Update position based on object type
  if (item.position) {
    // Markers and labels have a position property
    item.position.x += deltaX
    item.position.y += deltaY
  } else if (item.points) {
    // Continents, countries, and routes have points arrays
    item.points.forEach((point: MapPoint) => {
      point.x += deltaX
      point.y += deltaY
    })

    // Also update nested countries and cities for continents
    if (item.countries) {
      item.countries.forEach((country: any) => {
        if (country.points) {
          country.points.forEach((point: MapPoint) => {
            point.x += deltaX
            point.y += deltaY
          })
        }

        // Update cities within countries
        if (country.cities) {
          country.cities.forEach((city: any) => {
            if (city.position) {
              city.position.x += deltaX
              city.position.y += deltaY
            } else if (city.points) {
              city.points.forEach((point: MapPoint) => {
                point.x += deltaX
                point.y += deltaY
              })
            }
          })
        }
      })
    }
  }
}

const finishDrawing = () => {
  if (!isDrawing.value || drawingPoints.value.length < 3) {
    // Need at least 3 points for a polygon
    cancelDrawing()
    return
  }

  // Get the completed drawing points
  const points = finishDrawingPoints()

  if (points.length < 3) return

  // Create polygon object based on active tool
  if (props.activeTool === 'draw-polygon') {
    const polygon = {
      type: 'continent',
      id: `continent-${Date.now()}`,
      name: 'New Continent',
      points: points,
      color: 'rgba(42, 42, 62, 0.6)',
      visible: true,
      borderVisible: true,
      fillVisible: true,
      borderWidth: 3,
      borderColor: '#4a5a6a',
      countries: []
    }

    emit('item-create', polygon)
  } else if (props.activeTool === 'draw-route') {
    const route = {
      type: 'route',
      id: `route-${Date.now()}`,
      name: 'New Route',
      points: points,
      color: '#8b5cf6',
      width: 3,
      style: 'solid',
      visible: true,
      description: ''
    }

    emit('item-create', route)
  }
}

// Hit testing for hover (includes hidden markers)
const findMarkerAtPoint = (point: MapPoint): any => {
  // Check all markers (including hidden ones) for hover detection
  for (const marker of props.mapData.markers) {
    const distance = Math.sqrt(
        Math.pow(point.x - marker.position.x, 2) +
        Math.pow(point.y - marker.position.y, 2)
    )

    if (distance <= (marker.size / canvasWidth.value) * 100) {
      return marker
    }
  }
  return null
}

// Hit testing
const findItemAtPoint = (point: MapPoint): any => {
  // Check markers first (smallest targets)
  for (const marker of props.mapData.markers) {
    if (!marker.visible) continue

    const distance = Math.sqrt(
        Math.pow(point.x - marker.position.x, 2) +
        Math.pow(point.y - marker.position.y, 2)
    )

    if (distance <= (marker.size / canvasWidth.value) * 100) {
      return marker
    }
  }

  // Check labels
  for (const label of props.mapData.labels) {
    if (!label.visible) continue

    // Simple bounding box check for labels
    const labelWidth = (label.text.length * label.fontSize * 0.6) / canvasWidth.value * 100
    const labelHeight = (label.fontSize * 1.2) / canvasHeight.value * 100

    if (point.x >= label.position.x - labelWidth / 2 &&
        point.x <= label.position.x + labelWidth / 2 &&
        point.y >= label.position.y - labelHeight / 2 &&
        point.y <= label.position.y + labelHeight / 2) {
      return label
    }
  }

  // Check routes
  for (const route of props.mapData.routes) {
    if (!route.visible || route.points.length < 2) continue

    for (let i = 0; i < route.points.length - 1; i++) {
      const distance = distanceToLine(point, route.points[i], route.points[i + 1])
      if (distance <= (route.width / canvasWidth.value) * 100) {
        return route
      }
    }
  }

  // Check continents and their children
  for (const continent of props.mapData.continents) {
    if (!continent.visible) continue

    if (pointInPolygon(point, continent.points)) {
      // Check countries within continent
      for (const country of continent.countries) {
        if (!country.visible) continue

        if (pointInPolygon(point, country.points)) {
          // Check cities within country
          for (const city of country.cities) {
            if (!city.visible) continue

            if (city.cityType === 'area' && city.points && pointInPolygon(point, city.points)) {
              return city
            } else if (city.cityType === 'point' && city.position) {
              const distance = Math.sqrt(
                  Math.pow(point.x - city.position.x, 2) +
                  Math.pow(point.y - city.position.y, 2)
              )

              if (distance <= ((city.size || 6) / canvasWidth.value) * 100) {
                return city
              }
            }
          }

          return country
        }
      }

      return continent
    }
  }

  return null
}

// Export functionality
const exportToPNG = () => {
  if (!canvasRef.value) return

  const link = document.createElement('a')
  link.download = `world-map-${new Date().toISOString().split('T')[0]}.png`
  link.href = canvasRef.value.toDataURL()
  link.click()
}

// Watchers
watch(() => props.mapData, () => {
  needsRedraw.value = true
}, {deep: true})

watch(() => props.mapData.metadata.backgroundImage, (newImage) => {
  if (newImage) {
    loadBackgroundImage(newImage)
  } else {
    backgroundImage.value = null
    needsRedraw.value = true
  }
})

watch([() => props.zoom, () => props.pan], () => {
  needsRedraw.value = true
}, {deep: true})

watch(needsRedraw, (shouldRedraw) => {
  if (shouldRedraw) {
    nextTick(() => {
      render()
    })
  }
})

// Lifecycle
onMounted(() => {
  initCanvas()

  // Handle window resize
  const handleResize = () => {
    updateCanvasSize()
  }

  window.addEventListener('resize', handleResize)

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
  })
})

// Expose methods for parent component
defineExpose({
  exportToPNG,
  render: () => {
    needsRedraw.value = true
  }
})
</script>

<style scoped>
.map-canvas-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #0f0f0f;
}

.map-canvas {
  display: block;
  cursor: grab;
  user-select: none;
}

.map-canvas:active {
  cursor: grabbing;
}

.crosshair {
  position: absolute;
  width: 20px;
  height: 20px;
  pointer-events: none;
  z-index: 10;
}

.crosshair::before,
.crosshair::after {
  content: '';
  position: absolute;
  background: #fada95;
  box-shadow: 0 0 4px rgba(250, 218, 149, 0.5);
}

.crosshair::before {
  left: 50%;
  top: 0;
  width: 1px;
  height: 100%;
  transform: translateX(-50%);
}

.crosshair::after {
  top: 50%;
  left: 0;
  width: 100%;
  height: 1px;
  transform: translateY(-50%);
}

.drawing-preview {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 5;
}

.scale-counter {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #fada95;
  border-radius: 4px;
  padding: 8px 12px;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  font-size: 12px;
  line-height: 1.2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  pointer-events: none;
  z-index: 15;
  min-width: 80px;
}

.scale-label {
  font-weight: bold;
  text-align: center;
  margin-bottom: 2px;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.scale-value {
  font-size: 14px;
  font-weight: bold;
  text-align: center;
  color: #ffffff;
  margin-bottom: 2px;
}

.scale-range {
  font-size: 9px;
  text-align: center;
  opacity: 0.7;
  color: #fada95;
}
</style>