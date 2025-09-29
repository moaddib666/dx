import { ref, reactive, computed } from 'vue'
import type { MapPoint } from './useMapData'

export interface ViewState {
  zoom: number
  pan: MapPoint
}

export interface InteractionState {
  isDragging: boolean
  isDrawing: boolean
  dragStart: MapPoint | null
  drawingPoints: MapPoint[]
  selectedItem: any | null
  hoveredItem: any | null
}

export function useMapInteraction() {
  // View state
  const zoom = ref<number>(1.0)
  const pan = ref<MapPoint>({ x: 0, y: 0 })

  // Interaction state
  const selectedItem = ref<any | null>(null)
  const hoveredItem = ref<any | null>(null)
  const isDragging = ref<boolean>(false)
  const isDrawing = ref<boolean>(false)
  const dragStart = ref<MapPoint | null>(null)
  const drawingPoints = ref<MapPoint[]>([])

  // Zoom constraints
  const MIN_ZOOM = 0.1
  const MAX_ZOOM = 5.0
  const ZOOM_STEP = 0.1

  // Pan constraints (for infinite wrapping)
  const wrapCoordinate = (value: number, max: number): number => {
    return ((value % max) + max) % max
  }

  // Zoom methods
  const setZoom = (newZoom: number) => {
    zoom.value = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, newZoom))
  }

  const zoomIn = (step: number = ZOOM_STEP) => {
    setZoom(zoom.value + step)
  }

  const zoomOut = (step: number = ZOOM_STEP) => {
    setZoom(zoom.value - step)
  }

  const zoomToFit = (canvasWidth: number, canvasHeight: number, contentWidth: number, contentHeight: number) => {
    const scaleX = canvasWidth / contentWidth
    const scaleY = canvasHeight / contentHeight
    const scale = Math.min(scaleX, scaleY) * 0.9 // 90% to leave some margin
    setZoom(scale)

    // Center the content
    pan.value = {
      x: (canvasWidth - contentWidth * scale) / 2,
      y: (canvasHeight - contentHeight * scale) / 2
    }
  }

  const resetView = () => {
    zoom.value = 1.0
    pan.value = { x: 0, y: 0 }
  }

  // Pan methods with bounds checking
  const setPan = (newPan: MapPoint, canvasWidth?: number, canvasHeight?: number, imageWidth?: number, imageHeight?: number) => {
    if (canvasWidth && canvasHeight && imageWidth && imageHeight) {
      // Calculate bounds to prevent panning outside the map image
      const scaledImageWidth = imageWidth * zoom.value
      const scaledImageHeight = imageHeight * zoom.value

      // Calculate maximum pan values to keep image within viewport
      const maxPanX = Math.max(0, scaledImageWidth - canvasWidth)
      const maxPanY = Math.max(0, scaledImageHeight - canvasHeight)

      // Constrain pan values to keep map image within bounds
      pan.value = {
        x: Math.max(-maxPanX, Math.min(0, newPan.x)),
        y: Math.max(-maxPanY, Math.min(0, newPan.y))
      }
    } else {
      pan.value = { ...newPan }
    }
  }

  const panBy = (deltaX: number, deltaY: number, canvasWidth?: number, canvasHeight?: number, imageWidth?: number, imageHeight?: number) => {
    const newPan = {
      x: pan.value.x + deltaX,
      y: pan.value.y + deltaY
    }
    setPan(newPan, canvasWidth, canvasHeight, imageWidth, imageHeight)
  }

  // For infinite wrapping, we'll handle this in the canvas rendering
  const getWrappedPan = (canvasWidth: number, canvasHeight: number): MapPoint => {
    return {
      x: wrapCoordinate(pan.value.x, canvasWidth),
      y: wrapCoordinate(pan.value.y, canvasHeight)
    }
  }

  // Coordinate transformation methods
  const screenToWorld = (screenPoint: MapPoint, canvasWidth: number, canvasHeight: number): MapPoint => {
    return {
      x: (screenPoint.x - pan.value.x) / zoom.value,
      y: (screenPoint.y - pan.value.y) / zoom.value
    }
  }

  const worldToScreen = (worldPoint: MapPoint): MapPoint => {
    return {
      x: worldPoint.x * zoom.value + pan.value.x,
      y: worldPoint.y * zoom.value + pan.value.y
    }
  }

  const screenToPercent = (screenPoint: MapPoint, canvasWidth: number, canvasHeight: number): MapPoint => {
    const worldPoint = screenToWorld(screenPoint, canvasWidth, canvasHeight)
    return {
      x: (worldPoint.x / canvasWidth) * 100,
      y: (worldPoint.y / canvasHeight) * 100
    }
  }

  const percentToScreen = (percentPoint: MapPoint, canvasWidth: number, canvasHeight: number): MapPoint => {
    const worldPoint = {
      x: (percentPoint.x / 100) * canvasWidth,
      y: (percentPoint.y / 100) * canvasHeight
    }
    return worldToScreen(worldPoint)
  }

  // Selection methods
  const selectItem = (item: any) => {
    selectedItem.value = item
  }

  const clearSelection = () => {
    selectedItem.value = null
  }

  const setHoveredItem = (item: any) => {
    hoveredItem.value = item
  }

  const clearHover = () => {
    hoveredItem.value = null
  }

  // Drag methods
  const startDrag = (startPoint: MapPoint) => {
    isDragging.value = true
    dragStart.value = { ...startPoint }
  }

  const updateDrag = (currentPoint: MapPoint) => {
    if (!isDragging.value || !dragStart.value) return

    const deltaX = currentPoint.x - dragStart.value.x
    const deltaY = currentPoint.y - dragStart.value.y

    panBy(deltaX, deltaY)
    dragStart.value = { ...currentPoint }
  }

  const endDrag = () => {
    isDragging.value = false
    dragStart.value = null
  }

  // Drawing methods
  const startDrawing = (startPoint: MapPoint) => {
    isDrawing.value = true
    drawingPoints.value = [{ ...startPoint }]
  }

  const addDrawingPoint = (point: MapPoint) => {
    if (!isDrawing.value) return
    drawingPoints.value.push({ ...point })
  }

  const updateLastDrawingPoint = (point: MapPoint) => {
    if (!isDrawing.value || drawingPoints.value.length === 0) return
    drawingPoints.value[drawingPoints.value.length - 1] = { ...point }
  }

  const finishDrawing = (): MapPoint[] => {
    if (!isDrawing.value) return []

    const points = [...drawingPoints.value]
    isDrawing.value = false
    drawingPoints.value = []
    return points
  }

  const cancelDrawing = () => {
    isDrawing.value = false
    drawingPoints.value = []
  }

  // Mouse/touch event handlers
  const handleMouseDown = (event: MouseEvent, canvas: HTMLCanvasElement) => {
    const rect = canvas.getBoundingClientRect()
    const screenPoint = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    }

    startDrag(screenPoint)
  }

  const handleMouseMove = (event: MouseEvent, canvas: HTMLCanvasElement) => {
    const rect = canvas.getBoundingClientRect()
    const screenPoint = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    }

    if (isDragging.value) {
      updateDrag(screenPoint)
    }
  }

  const handleMouseUp = () => {
    endDrag()
  }

  const handleWheel = (event: WheelEvent, canvas: HTMLCanvasElement) => {
    event.preventDefault()

    const rect = canvas.getBoundingClientRect()
    const mouseX = event.clientX - rect.left
    const mouseY = event.clientY - rect.top

    // Calculate zoom factor
    const zoomFactor = event.deltaY > 0 ? 0.9 : 1.1
    const newZoom = Math.max(MIN_ZOOM, Math.min(MAX_ZOOM, zoom.value * zoomFactor))

    if (newZoom !== zoom.value) {
      // Calculate zoom ratio for pan adjustment
      const zoomRatio = newZoom / zoom.value

      // Calculate pan adjustment to keep mouse cursor position stable
      const offsetX = mouseX * (1 - zoomRatio)
      const offsetY = mouseY * (1 - zoomRatio)

      // Apply zoom and pan adjustment
      zoom.value = newZoom
      panBy(offsetX, offsetY)
    }
  }

  // Touch event handlers for mobile support
  const handleTouchStart = (event: TouchEvent, canvas: HTMLCanvasElement) => {
    event.preventDefault()

    if (event.touches.length === 1) {
      const touch = event.touches[0]
      const rect = canvas.getBoundingClientRect()
      const screenPoint = {
        x: touch.clientX - rect.left,
        y: touch.clientY - rect.top
      }

      startDrag(screenPoint)
    }
  }

  const handleTouchMove = (event: TouchEvent, canvas: HTMLCanvasElement) => {
    event.preventDefault()

    if (event.touches.length === 1 && isDragging.value) {
      const touch = event.touches[0]
      const rect = canvas.getBoundingClientRect()
      const screenPoint = {
        x: touch.clientX - rect.left,
        y: touch.clientY - rect.top
      }

      updateDrag(screenPoint)
    }
  }

  const handleTouchEnd = (event: TouchEvent) => {
    event.preventDefault()
    endDrag()
  }

  // Keyboard event handlers
  const handleKeyDown = (event: KeyboardEvent) => {
    const PAN_STEP = 20
    const ZOOM_KEYBOARD_STEP = 0.2

    switch (event.key) {
      case 'ArrowUp':
        event.preventDefault()
        panBy(0, PAN_STEP)
        break
      case 'ArrowDown':
        event.preventDefault()
        panBy(0, -PAN_STEP)
        break
      case 'ArrowLeft':
        event.preventDefault()
        panBy(PAN_STEP, 0)
        break
      case 'ArrowRight':
        event.preventDefault()
        panBy(-PAN_STEP, 0)
        break
      case '+':
      case '=':
        event.preventDefault()
        zoomIn(ZOOM_KEYBOARD_STEP)
        break
      case '-':
        event.preventDefault()
        zoomOut(ZOOM_KEYBOARD_STEP)
        break
      case 'Home':
        event.preventDefault()
        resetView()
        break
      case 'Escape':
        event.preventDefault()
        clearSelection()
        cancelDrawing()
        break
    }
  }

  // Event handler wrappers for Vue components
  const handleZoomChange = (newZoom: number) => {
    setZoom(newZoom)
  }

  const handlePanChange = (newPan: MapPoint) => {
    setPan(newPan)
  }

  // Computed properties
  const viewState = computed((): ViewState => ({
    zoom: zoom.value,
    pan: pan.value
  }))

  const interactionState = computed((): InteractionState => ({
    isDragging: isDragging.value,
    isDrawing: isDrawing.value,
    dragStart: dragStart.value,
    drawingPoints: drawingPoints.value,
    selectedItem: selectedItem.value,
    hoveredItem: hoveredItem.value
  }))

  const isInteracting = computed(() => isDragging.value || isDrawing.value)

  // Hit testing utilities
  const pointInPolygon = (point: MapPoint, polygon: MapPoint[]): boolean => {
    let inside = false
    for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
      if (((polygon[i].y > point.y) !== (polygon[j].y > point.y)) &&
          (point.x < (polygon[j].x - polygon[i].x) * (point.y - polygon[i].y) / (polygon[j].y - polygon[i].y) + polygon[i].x)) {
        inside = !inside
      }
    }
    return inside
  }

  const pointInCircle = (point: MapPoint, center: MapPoint, radius: number): boolean => {
    const dx = point.x - center.x
    const dy = point.y - center.y
    return (dx * dx + dy * dy) <= (radius * radius)
  }

  const distanceToLine = (point: MapPoint, lineStart: MapPoint, lineEnd: MapPoint): number => {
    const A = point.x - lineStart.x
    const B = point.y - lineStart.y
    const C = lineEnd.x - lineStart.x
    const D = lineEnd.y - lineStart.y

    const dot = A * C + B * D
    const lenSq = C * C + D * D

    if (lenSq === 0) return Math.sqrt(A * A + B * B)

    let param = dot / lenSq

    let xx, yy

    if (param < 0) {
      xx = lineStart.x
      yy = lineStart.y
    } else if (param > 1) {
      xx = lineEnd.x
      yy = lineEnd.y
    } else {
      xx = lineStart.x + param * C
      yy = lineStart.y + param * D
    }

    const dx = point.x - xx
    const dy = point.y - yy
    return Math.sqrt(dx * dx + dy * dy)
  }

  return {
    // State
    zoom,
    pan,
    selectedItem,
    hoveredItem,
    isDragging,
    isDrawing,
    dragStart,
    drawingPoints,

    // Computed
    viewState,
    interactionState,
    isInteracting,

    // Zoom methods
    setZoom,
    zoomIn,
    zoomOut,
    zoomToFit,
    resetView,

    // Pan methods
    setPan,
    panBy,
    getWrappedPan,

    // Coordinate transformation
    screenToWorld,
    worldToScreen,
    screenToPercent,
    percentToScreen,

    // Selection methods
    selectItem,
    clearSelection,
    setHoveredItem,
    clearHover,

    // Drag methods
    startDrag,
    updateDrag,
    endDrag,

    // Drawing methods
    startDrawing,
    addDrawingPoint,
    updateLastDrawingPoint,
    finishDrawing,
    cancelDrawing,

    // Event handlers
    handleMouseDown,
    handleMouseMove,
    handleMouseUp,
    handleWheel,
    handleTouchStart,
    handleTouchMove,
    handleTouchEnd,
    handleKeyDown,
    handleZoomChange,
    handlePanChange,

    // Hit testing
    pointInPolygon,
    pointInCircle,
    distanceToLine
  }
}