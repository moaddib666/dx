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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useMapInteraction } from '@/composables/GlobalWorldMap/useMapInteraction'
import type { MapData, MapPoint, MapContinent, MapRoute, MapMarker, MapLabel } from '@/composables/GlobalWorldMap/useMapData'

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
  distanceToLine
} = useMapInteraction()

// State
const canvasWidth = ref(800)
const canvasHeight = ref(600)
const cursorPosition = ref({ x: 0, y: 0 })
const needsRedraw = ref(true)
const isDragging = ref(false)
const dragStart = ref<{ x: number, y: number } | null>(null)

// Computed
const showCrosshair = computed(() => {
  return ['draw-polygon', 'draw-route', 'add-marker', 'add-label'].includes(props.activeTool)
})

const drawingPointsString = computed(() => {
  return drawingPoints.value.map(p => `${p.x},${p.y}`).join(' ')
})

// Canvas context
let ctx: CanvasRenderingContext2D | null = null

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

const render = () => {
  if (!ctx || !canvasRef.value) return

  // Clear canvas
  ctx.clearRect(0, 0, canvasWidth.value, canvasHeight.value)

  // Save context state
  ctx.save()

  // Apply zoom and pan transformations
  ctx.scale(props.zoom, props.zoom)
  ctx.translate(props.pan.x / props.zoom, props.pan.y / props.zoom)

  // Render layers in order
  renderBackgroundImage()
  renderContinents()
  renderRoutes()
  renderMarkers()
  renderLabels()
  renderSelection()

  // Restore context state
  ctx.restore()

  needsRedraw.value = false
}

const renderBackgroundImage = () => {
  if (!ctx || !backgroundImage.value) return

  const img = backgroundImage.value
  const canvasAspect = canvasWidth.value / canvasHeight.value
  const imageAspect = img.width / img.height

  let drawWidth = canvasWidth.value / props.zoom
  let drawHeight = canvasHeight.value / props.zoom
  let drawX = 0
  let drawY = 0

  // Scale image to fill canvas completely (cover behavior)
  if (imageAspect > canvasAspect) {
    // Image is wider than canvas - scale by height and crop sides
    drawHeight = canvasHeight.value / props.zoom
    drawWidth = drawHeight * imageAspect
    drawX = (canvasWidth.value / props.zoom - drawWidth) / 2
  } else {
    // Image is taller than canvas - scale by width and crop top/bottom
    drawWidth = canvasWidth.value / props.zoom
    drawHeight = drawWidth / imageAspect
    drawY = (canvasHeight.value / props.zoom - drawHeight) / 2
  }

  ctx.drawImage(img, drawX, drawY, drawWidth, drawHeight)
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
    if (!marker.visible) return

    renderMarker(marker.position, {
      color: marker.color,
      size: marker.size,
      type: marker.type,
      icon: marker.icon,
      isSelected: props.selectedItem?.id === marker.id
    })

    // Render marker label
    if (marker.labelVisible) {
      const labelY = marker.position.y - (marker.size + 5) / 100 * canvasHeight.value
      renderLabel({ x: marker.position.x, y: labelY }, marker.name, {
        fontSize: 11,
        color: '#ffffff',
        background: true,
        backgroundColor: 'rgba(0, 0, 0, 0.7)'
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
    renderPolygonOutline(item.points, '#60a5fa', 3)
    renderVertexHandles(item.points)
  } else if (item.position) {
    // Point selection
    renderCircleOutline(item.position, (item.size || 6) + 4, '#60a5fa', 2)
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

  ctx.beginPath()

  // Convert percentage points to canvas coordinates
  const canvasPoints = points.map(p => ({
    x: (p.x / 100) * canvasWidth.value / props.zoom,
    y: (p.y / 100) * canvasHeight.value / props.zoom
  }))

  ctx.moveTo(canvasPoints[0].x, canvasPoints[0].y)
  for (let i = 1; i < canvasPoints.length; i++) {
    ctx.lineTo(canvasPoints[i].x, canvasPoints[i].y)
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

  ctx.beginPath()

  // Convert percentage points to canvas coordinates
  const canvasPoints = points.map(p => ({
    x: (p.x / 100) * canvasWidth.value / props.zoom,
    y: (p.y / 100) * canvasHeight.value / props.zoom
  }))

  ctx.moveTo(canvasPoints[0].x, canvasPoints[0].y)
  for (let i = 1; i < canvasPoints.length; i++) {
    ctx.lineTo(canvasPoints[i].x, canvasPoints[i].y)
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
}) => {
  if (!ctx) return

  const x = (position.x / 100) * canvasWidth.value / props.zoom
  const y = (position.y / 100) * canvasHeight.value / props.zoom
  const radius = options.size

  ctx.fillStyle = options.color
  ctx.strokeStyle = '#ffffff'
  ctx.lineWidth = 2

  if (options.type === 'hazard') {
    // Triangle for hazards
    ctx.beginPath()
    ctx.moveTo(x, y - radius)
    ctx.lineTo(x - radius * 0.866, y + radius * 0.5)
    ctx.lineTo(x + radius * 0.866, y + radius * 0.5)
    ctx.closePath()
    ctx.fill()
    ctx.stroke()
  } else {
    // Circle for other markers
    ctx.beginPath()
    ctx.arc(x, y, radius, 0, Math.PI * 2)
    ctx.fill()
    ctx.stroke()
  }

  // Render icon if provided
  if (options.icon) {
    ctx.font = `${radius * 1.2}px Arial`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillStyle = '#ffffff'
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

  const x = (position.x / 100) * canvasWidth.value / props.zoom
  const y = (position.y / 100) * canvasHeight.value / props.zoom

  ctx.font = `${options.fontWeight || 'normal'} ${options.fontSize}px Arial`
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'

  // Measure text
  const metrics = ctx.measureText(text)
  const textWidth = metrics.width
  const textHeight = options.fontSize

  // Draw background if enabled
  if (options.background && options.backgroundColor) {
    ctx.fillStyle = options.backgroundColor
    ctx.fillRect(
      x - textWidth / 2 - 4,
      y - textHeight / 2 - 2,
      textWidth + 8,
      textHeight + 4
    )
  }

  // Draw text
  ctx.fillStyle = options.color
  ctx.fillText(text, x, y)
}

const renderPolygonOutline = (points: MapPoint[], color: string, width: number) => {
  if (!ctx || points.length < 3) return

  ctx.beginPath()

  const canvasPoints = points.map(p => ({
    x: (p.x / 100) * canvasWidth.value / props.zoom,
    y: (p.y / 100) * canvasHeight.value / props.zoom
  }))

  ctx.moveTo(canvasPoints[0].x, canvasPoints[0].y)
  for (let i = 1; i < canvasPoints.length; i++) {
    ctx.lineTo(canvasPoints[i].x, canvasPoints[i].y)
  }
  ctx.closePath()

  ctx.strokeStyle = color
  ctx.lineWidth = width
  ctx.stroke()
}

const renderCircleOutline = (position: MapPoint, radius: number, color: string, width: number) => {
  if (!ctx) return

  const x = (position.x / 100) * canvasWidth.value / props.zoom
  const y = (position.y / 100) * canvasHeight.value / props.zoom

  ctx.beginPath()
  ctx.arc(x, y, radius, 0, Math.PI * 2)
  ctx.strokeStyle = color
  ctx.lineWidth = width
  ctx.stroke()
}

const renderVertexHandles = (points: MapPoint[]) => {
  if (!ctx) return

  points.forEach(point => {
    const x = (point.x / 100) * canvasWidth.value / props.zoom
    const y = (point.y / 100) * canvasHeight.value / props.zoom

    ctx.beginPath()
    ctx.arc(x, y, 4, 0, Math.PI * 2)
    ctx.fillStyle = '#60a5fa'
    ctx.fill()
    ctx.strokeStyle = '#ffffff'
    ctx.lineWidth = 1
    ctx.stroke()
  })
}

// Event handlers
const handleMouseDown = (event: MouseEvent) => {
  if (!canvasRef.value) return

  const rect = canvasRef.value.getBoundingClientRect()
  const screenPoint = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }

  // Start dragging for pan (when using select tool and not clicking on an item)
  if (props.activeTool === 'select') {
    const percentPoint = screenToPercent(screenPoint, canvasWidth.value, canvasHeight.value)
    const hitItem = findItemAtPoint(percentPoint)

    if (!hitItem) {
      // Start panning
      isDragging.value = true
      dragStart.value = screenPoint
    } else {
      // Select the item
      emit('item-select', hitItem)
    }
  } else if (props.activeTool === 'draw-polygon') {
    handleDrawPolygonTool(event)
  } else if (props.activeTool === 'draw-route') {
    handleDrawRouteTool(event)
  } else if (props.activeTool === 'add-marker') {
    handleAddMarkerTool(event)
  } else if (props.activeTool === 'add-label') {
    handleAddLabelTool(event)
  }
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

  // Handle panning
  if (isDragging.value && dragStart.value) {
    const deltaX = currentPoint.x - dragStart.value.x
    const deltaY = currentPoint.y - dragStart.value.y

    const newPan = {
      x: props.pan.x + deltaX,
      y: props.pan.y + deltaY
    }

    emit('pan-change', newPan)
    dragStart.value = currentPoint
    needsRedraw.value = true
  }
}

const handleMouseUp = () => {
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
  const MIN_ZOOM = 0.1
  const MAX_ZOOM = 5.0
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

    // Emit changes to parent
    emit('zoom-change', newZoom)
    emit('pan-change', newPan)
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
  // Handle single clicks for tools that need them
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

  const percentPoint = screenToPercent(screenPoint, canvasWidth.value, canvasHeight.value)
  const hitItem = findItemAtPoint(percentPoint)

  emit('item-select', hitItem)
}

const handleDrawPolygonTool = (event: MouseEvent) => {
  // Implementation for polygon drawing
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

  const percentPoint = screenToPercent(screenPoint, canvasWidth.value, canvasHeight.value)

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

  const percentPoint = screenToPercent(screenPoint, canvasWidth.value, canvasHeight.value)

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

const finishDrawing = () => {
  // Implementation for finishing drawing operations
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
}, { deep: true })

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
}, { deep: true })

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
  background: #60a5fa;
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
</style>