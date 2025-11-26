# Interactive Layered Map Editor - Implementation Guide
## Vue.js + TypeScript + Canvas

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture](#architecture)
4. [Data Structure (JSON Schema)](#data-structure-json-schema)
5. [Core Components](#core-components)
6. [Canvas Implementation](#canvas-implementation)
7. [Layer System](#layer-system)
8. [Infinite Canvas (Globe Wrapping)](#infinite-canvas-globe-wrapping)
9. [Interaction System](#interaction-system)
10. [Step-by-Step Implementation](#step-by-step-implementation)
11. [Code Examples](#code-examples)
12. [Advanced Features](#advanced-features)

---

## Project Overview

### Goal
Create an interactive, layered map editor that allows:
- Background image as base layer
- Editable continent boundaries
- Country boundaries within continents
- City areas within countries
- Trade routes/paths
- Point markers (cities, hazards)
- Labels and annotations
- Zoom and pan with infinite wrapping (globe effect)
- Layer visibility controls
- Export/import JSON data

### Key Features
- ✅ Canvas-based rendering for performance
- ✅ Multi-layer system (background, continents, countries, cities, routes, markers)
- ✅ Infinite scrolling canvas (wrapping edges like a globe)
- ✅ Interactive editing (drag, resize, add/remove)
- ✅ JSON-driven data structure
- ✅ Zoom and pan controls
- ✅ Toggle layer visibility
- ✅ Export annotated map

---

## Technology Stack

```json
{
  "framework": "Vue 3 (Composition API)",
  "language": "TypeScript",
  "rendering": "HTML5 Canvas",
  "state": "Pinia (optional) or Vue Reactive",
  "utilities": [
    "lodash (for deep cloning)",
    "file-saver (for export)",
    "chroma-js (for colors)"
  ]
}
```

### Install Dependencies
```bash
npm install --save-dev @types/lodash
npm install lodash file-saver chroma-js
npm install -D @types/file-saver
```

---

## Architecture

### Component Structure
```
src/
├── components/GlobalWorldMap/
│   ├── MapEditor.vue          # Main editor component
│   ├── MapCanvas.vue           # Canvas rendering component
│   ├── LayerControls.vue       # Layer visibility controls
│   ├── ToolPanel.vue           # Drawing/editing tools
│   ├── PropertiesPanel.vue     # Selected item properties
│   └── ExportImport.vue        # JSON import/export
├── composables/GlobalWorldMap/
│   ├── useCanvas.ts            # Canvas utilities
│   ├── useMapData.ts           # Map data management
│   ├── useInteraction.ts       # Mouse/touch interactions
│   ├── useInfiniteCanvas.ts    # Wrapping logic
│   └── useLayerRenderer.ts     # Layer rendering
├── types/GlobalWorldMap/
│   └── map.types.ts            # TypeScript interfaces
└── utils/GlobalWorldMap/
    ├── geometry.ts             # Geometric calculations
    └── export.ts               # Export utilities
```

---

## Data Structure (JSON Schema)

### Complete Map Data Structure
```typescript
// types/map.types.ts

export interface Point {
  x: number; // 0-100 (percentage of canvas width)
  y: number; // 0-100 (percentage of canvas height)
}

export interface MapMetadata {
  width: number;
  height: number;
  backgroundImage?: string; // Base64 or URL
  version: string;
}

export interface Continent {
  id: string;
  name: string;
  points: Point[]; // Polygon points
  color: string;
  visible: boolean;
  borderVisible: boolean;
  fillVisible: boolean;
  countries: Country[];
}

export interface Country {
  id: string;
  name: string;
  continentId: string;
  points: Point[];
  color: string;
  visible: boolean;
  borderVisible: boolean;
  fillVisible: boolean;
  cities: City[];
}

export interface City {
  id: string;
  name: string;
  countryId: string;
  points: Point[]; // Area polygon or single point
  isArea: boolean; // true for area, false for point marker
  color: string;
  visible: boolean;
  borderVisible: boolean;
  fillVisible: boolean;
  labelVisible: boolean;
  type: 'major' | 'medium' | 'small';
}

export interface Route {
  id: string;
  name: string;
  points: Point[];
  color: string;
  width: number;
  style: 'solid' | 'dashed' | 'dotted';
  visible: boolean;
  type: 'maritime' | 'aerial' | 'dimensional';
}

export interface Marker {
  id: string;
  name: string;
  position: Point;
  type: 'city' | 'hazard' | 'landmark' | 'custom';
  color: string;
  icon: string; // Icon name or emoji
  size: number;
  visible: boolean;
  labelVisible: boolean;
  description?: string;
}

export interface Label {
  id: string;
  text: string;
  position: Point;
  fontSize: number;
  color: string;
  fontWeight: 'normal' | 'bold';
  visible: boolean;
  background: boolean;
  backgroundColor?: string;
}

export interface MapData {
  metadata: MapMetadata;
  continents: Continent[];
  routes: Route[];
  markers: Marker[];
  labels: Label[];
}
```

### Example JSON
```json
{
  "metadata": {
    "width": 1920,
    "height": 1080,
    "backgroundImage": "data:image/png;base64,...",
    "version": "1.0.0"
  },
  "continents": [
    {
      "id": "mainland-primus",
      "name": "Mainland Primus",
      "points": [
        { "x": 20, "y": 30 },
        { "x": 60, "y": 25 },
        { "x": 70, "y": 60 },
        { "x": 30, "y": 70 }
      ],
      "color": "#2a2a3e",
      "visible": true,
      "borderVisible": true,
      "fillVisible": true,
      "countries": [
        {
          "id": "central-region",
          "name": "Central Region",
          "continentId": "mainland-primus",
          "points": [
            { "x": 35, "y": 40 },
            { "x": 50, "y": 38 },
            { "x": 52, "y": 55 },
            { "x": 38, "y": 58 }
          ],
          "color": "#3a3a4e",
          "visible": true,
          "borderVisible": true,
          "fillVisible": false,
          "cities": [
            {
              "id": "city-of-memories",
              "name": "City of Memories",
              "countryId": "central-region",
              "points": [{ "x": 45, "y": 50 }],
              "isArea": false,
              "color": "#fbbf24",
              "visible": true,
              "borderVisible": false,
              "fillVisible": false,
              "labelVisible": true,
              "type": "major"
            }
          ]
        }
      ]
    }
  ],
  "routes": [
    {
      "id": "maritime-route-1",
      "name": "Ocean Trade Route",
      "points": [
        { "x": 45, "y": 50 },
        { "x": 55, "y": 45 },
        { "x": 65, "y": 48 }
      ],
      "color": "#60a5fa",
      "width": 3,
      "style": "dashed",
      "visible": true,
      "type": "maritime"
    }
  ],
  "markers": [
    {
      "id": "hazard-death-valley",
      "name": "Death Valley",
      "position": { "x": 72, "y": 78 },
      "type": "hazard",
      "color": "#ef4444",
      "icon": "⚠️",
      "size": 8,
      "visible": true,
      "labelVisible": true,
      "description": "Extreme danger zone"
    }
  ],
  "labels": [
    {
      "id": "label-mainland",
      "text": "MAINLAND PRIMUS",
      "position": { "x": 45, "y": 50 },
      "fontSize": 24,
      "color": "#ffffff",
      "fontWeight": "bold",
      "visible": true,
      "background": true,
      "backgroundColor": "rgba(0,0,0,0.5)"
    }
  ]
}
```

---

## Core Components

### 1. MapEditor.vue (Main Container)

```vue
<template>
  <div class="map-editor">
    <div class="editor-header">
      <ToolPanel 
        :active-tool="activeTool"
        @tool-change="handleToolChange"
      />
      <ExportImport
        @import="handleImport"
        @export="handleExport"
      />
    </div>
    
    <div class="editor-body">
      <LayerControls
        :map-data="mapData"
        @toggle-layer="handleLayerToggle"
      />
      
      <MapCanvas
        ref="canvasRef"
        :map-data="mapData"
        :active-tool="activeTool"
        :zoom="zoom"
        :pan="pan"
        @update:zoom="zoom = $event"
        @update:pan="pan = $event"
        @select-item="handleSelectItem"
      />
      
      <PropertiesPanel
        :selected-item="selectedItem"
        @update="handleItemUpdate"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { MapData } from '@/types/map.types';

const mapData = ref<MapData>(/* initial data */);
const activeTool = ref<string>('select');
const zoom = ref(1);
const pan = ref({ x: 0, y: 0 });
const selectedItem = ref(null);

// Handlers...
</script>
```

### 2. MapCanvas.vue (Core Canvas Component)

```vue
<template>
  <div class="canvas-container" ref="containerRef">
    <canvas
      ref="canvasRef"
      :width="canvasWidth"
      :height="canvasHeight"
      @mousedown="handleMouseDown"
      @mousemove="handleMouseMove"
      @mouseup="handleMouseUp"
      @wheel="handleWheel"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useCanvas } from '@/composables/useCanvas';
import { useInfiniteCanvas } from '@/composables/useInfiniteCanvas';
import { useLayerRenderer } from '@/composables/useLayerRenderer';
import type { MapData } from '@/types/map.types';

const props = defineProps<{
  mapData: MapData;
  activeTool: string;
  zoom: number;
  pan: { x: number; y: number };
}>();

const canvasRef = ref<HTMLCanvasElement>();
const containerRef = ref<HTMLDivElement>();
const canvasWidth = ref(1920);
const canvasHeight = ref(1080);

const { ctx, clear, drawImage } = useCanvas(canvasRef);
const { wrapPosition } = useInfiniteCanvas(canvasWidth, canvasHeight);
const { renderLayers } = useLayerRenderer(ctx);

onMounted(() => {
  initCanvas();
  renderMap();
});

watch(() => [props.mapData, props.zoom, props.pan], renderMap, { deep: true });

function renderMap() {
  if (!ctx.value) return;
  
  clear();
  
  // Apply transformations
  ctx.value.save();
  ctx.value.translate(props.pan.x, props.pan.y);
  ctx.value.scale(props.zoom, props.zoom);
  
  // Render layers
  renderLayers(props.mapData);
  
  ctx.value.restore();
}
</script>
```

---

## Canvas Implementation

### useCanvas.ts Composable

```typescript
// composables/useCanvas.ts
import { ref, computed, type Ref } from 'vue';

export function useCanvas(canvasRef: Ref<HTMLCanvasElement | undefined>) {
  const ctx = computed(() => canvasRef.value?.getContext('2d') || null);

  function clear() {
    if (!ctx.value || !canvasRef.value) return;
    ctx.value.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);
  }

  function drawImage(
    img: HTMLImageElement,
    x: number = 0,
    y: number = 0,
    width?: number,
    height?: number
  ) {
    if (!ctx.value || !canvasRef.value) return;
    const w = width || canvasRef.value.width;
    const h = height || canvasRef.value.height;
    ctx.value.drawImage(img, x, y, w, h);
  }

  function drawPolygon(
    points: { x: number; y: number }[],
    fillColor?: string,
    strokeColor?: string,
    lineWidth: number = 2
  ) {
    if (!ctx.value || points.length < 2) return;

    ctx.value.beginPath();
    ctx.value.moveTo(points[0].x, points[0].y);
    
    for (let i = 1; i < points.length; i++) {
      ctx.value.lineTo(points[i].x, points[i].y);
    }
    
    ctx.value.closePath();

    if (fillColor) {
      ctx.value.fillStyle = fillColor;
      ctx.value.fill();
    }

    if (strokeColor) {
      ctx.value.strokeStyle = strokeColor;
      ctx.value.lineWidth = lineWidth;
      ctx.value.stroke();
    }
  }

  function drawCircle(
    x: number,
    y: number,
    radius: number,
    fillColor?: string,
    strokeColor?: string,
    lineWidth: number = 2
  ) {
    if (!ctx.value) return;

    ctx.value.beginPath();
    ctx.value.arc(x, y, radius, 0, Math.PI * 2);

    if (fillColor) {
      ctx.value.fillStyle = fillColor;
      ctx.value.fill();
    }

    if (strokeColor) {
      ctx.value.strokeStyle = strokeColor;
      ctx.value.lineWidth = lineWidth;
      ctx.value.stroke();
    }
  }

  function drawLine(
    points: { x: number; y: number }[],
    color: string,
    width: number = 2,
    style: 'solid' | 'dashed' | 'dotted' = 'solid'
  ) {
    if (!ctx.value || points.length < 2) return;

    ctx.value.strokeStyle = color;
    ctx.value.lineWidth = width;

    if (style === 'dashed') {
      ctx.value.setLineDash([10, 5]);
    } else if (style === 'dotted') {
      ctx.value.setLineDash([2, 3]);
    } else {
      ctx.value.setLineDash([]);
    }

    ctx.value.beginPath();
    ctx.value.moveTo(points[0].x, points[0].y);

    for (let i = 1; i < points.length; i++) {
      ctx.value.lineTo(points[i].x, points[i].y);
    }

    ctx.value.stroke();
    ctx.value.setLineDash([]);
  }

  function drawText(
    text: string,
    x: number,
    y: number,
    options: {
      fontSize?: number;
      fontWeight?: string;
      color?: string;
      background?: boolean;
      backgroundColor?: string;
      align?: CanvasTextAlign;
    } = {}
  ) {
    if (!ctx.value) return;

    const {
      fontSize = 14,
      fontWeight = 'normal',
      color = '#ffffff',
      background = false,
      backgroundColor = 'rgba(0,0,0,0.7)',
      align = 'center'
    } = options;

    ctx.value.font = `${fontWeight} ${fontSize}px Arial`;
    ctx.value.textAlign = align;
    ctx.value.textBaseline = 'middle';

    if (background) {
      const metrics = ctx.value.measureText(text);
      const padding = 5;
      const bgX = x - metrics.width / 2 - padding;
      const bgY = y - fontSize / 2 - padding;
      const bgWidth = metrics.width + padding * 2;
      const bgHeight = fontSize + padding * 2;

      ctx.value.fillStyle = backgroundColor;
      ctx.value.fillRect(bgX, bgY, bgWidth, bgHeight);
    }

    ctx.value.fillStyle = color;
    ctx.value.fillText(text, x, y);
  }

  return {
    ctx,
    clear,
    drawImage,
    drawPolygon,
    drawCircle,
    drawLine,
    drawText
  };
}
```

---

## Layer System

### useLayerRenderer.ts

```typescript
// composables/useLayerRenderer.ts
import { type Ref } from 'vue';
import type { MapData } from '@/types/map.types';
import { useCanvas } from './useCanvas';

export function useLayerRenderer(
  ctx: Ref<CanvasRenderingContext2D | null>
) {
  const canvas = useCanvas({ value: ctx.value?.canvas });

  function percentToPixel(
    value: number,
    dimension: 'width' | 'height'
  ): number {
    if (!ctx.value?.canvas) return 0;
    const size = dimension === 'width' 
      ? ctx.value.canvas.width 
      : ctx.value.canvas.height;
    return (value / 100) * size;
  }

  function convertPoints(points: { x: number; y: number }[]) {
    return points.map(p => ({
      x: percentToPixel(p.x, 'width'),
      y: percentToPixel(p.y, 'height')
    }));
  }

  function renderBackground(imageUrl?: string) {
    if (!imageUrl || !ctx.value) return;
    
    const img = new Image();
    img.onload = () => {
      canvas.drawImage(img);
    };
    img.src = imageUrl;
  }

  function renderContinents(mapData: MapData) {
    mapData.continents.forEach(continent => {
      if (!continent.visible) return;

      const points = convertPoints(continent.points);
      
      canvas.drawPolygon(
        points,
        continent.fillVisible ? continent.color : undefined,
        continent.borderVisible ? '#4a5a6a' : undefined,
        2
      );

      // Render countries within continent
      renderCountries(continent.countries);
    });
  }

  function renderCountries(countries: any[]) {
    countries.forEach(country => {
      if (!country.visible) return;

      const points = convertPoints(country.points);
      
      canvas.drawPolygon(
        points,
        country.fillVisible ? country.color : undefined,
        country.borderVisible ? '#5a6a7a' : undefined,
        1.5
      );

      // Render cities within country
      renderCities(country.cities);
    });
  }

  function renderCities(cities: any[]) {
    cities.forEach(city => {
      if (!city.visible) return;

      if (city.isArea) {
        // Render city as area
        const points = convertPoints(city.points);
        canvas.drawPolygon(
          points,
          city.fillVisible ? city.color : undefined,
          city.borderVisible ? '#ffffff' : undefined,
          1
        );
      } else {
        // Render city as point marker
        const pos = convertPoints([city.points[0]])[0];
        const radius = city.type === 'major' ? 8 : city.type === 'medium' ? 5 : 3;
        
        canvas.drawCircle(pos.x, pos.y, radius, city.color, '#ffffff', 2);
      }

      // Render label
      if (city.labelVisible) {
        const labelPos = city.isArea 
          ? getCentroid(convertPoints(city.points))
          : convertPoints([city.points[0]])[0];
        
        canvas.drawText(city.name, labelPos.x, labelPos.y - 15, {
          fontSize: 12,
          fontWeight: 'bold',
          background: true
        });
      }
    });
  }

  function renderRoutes(mapData: MapData) {
    mapData.routes.forEach(route => {
      if (!route.visible) return;

      const points = convertPoints(route.points);
      canvas.drawLine(points, route.color, route.width, route.style);
    });
  }

  function renderMarkers(mapData: MapData) {
    mapData.markers.forEach(marker => {
      if (!marker.visible) return;

      const pos = convertPoints([marker.position])[0];

      if (marker.type === 'hazard') {
        // Draw triangle for hazards
        const size = marker.size;
        if (!ctx.value) return;
        
        ctx.value.fillStyle = marker.color;
        ctx.value.strokeStyle = '#ffffff';
        ctx.value.lineWidth = 2;
        ctx.value.beginPath();
        ctx.value.moveTo(pos.x, pos.y - size);
        ctx.value.lineTo(pos.x - size, pos.y + size);
        ctx.value.lineTo(pos.x + size, pos.y + size);
        ctx.value.closePath();
        ctx.value.fill();
        ctx.value.stroke();
      } else {
        // Draw circle for other markers
        canvas.drawCircle(pos.x, pos.y, marker.size, marker.color, '#ffffff', 2);
      }

      if (marker.labelVisible) {
        canvas.drawText(marker.name, pos.x, pos.y - marker.size - 10, {
          fontSize: 11,
          color: marker.type === 'hazard' ? '#ff6b6b' : '#ffffff',
          background: true
        });
      }
    });
  }

  function renderLabels(mapData: MapData) {
    mapData.labels.forEach(label => {
      if (!label.visible) return;

      const pos = convertPoints([label.position])[0];
      canvas.drawText(label.text, pos.x, pos.y, {
        fontSize: label.fontSize,
        fontWeight: label.fontWeight,
        color: label.color,
        background: label.background,
        backgroundColor: label.backgroundColor
      });
    });
  }

  function renderLayers(mapData: MapData) {
    // Render in correct order (bottom to top)
    renderBackground(mapData.metadata.backgroundImage);
    renderContinents(mapData);
    renderRoutes(mapData);
    renderMarkers(mapData);
    renderLabels(mapData);
  }

  function getCentroid(points: { x: number; y: number }[]) {
    const x = points.reduce((sum, p) => sum + p.x, 0) / points.length;
    const y = points.reduce((sum, p) => sum + p.y, 0) / points.length;
    return { x, y };
  }

  return {
    renderLayers,
    renderBackground,
    renderContinents,
    renderRoutes,
    renderMarkers,
    renderLabels
  };
}
```

---

## Infinite Canvas (Globe Wrapping)

### useInfiniteCanvas.ts

```typescript
// composables/useInfiniteCanvas.ts
import { type Ref, ref } from 'vue';

export function useInfiniteCanvas(
  canvasWidth: Ref<number>,
  canvasHeight: Ref<number>
) {
  const virtualPan = ref({ x: 0, y: 0 });

  /**
   * Wrap position to create infinite canvas effect
   * When reaching edge, wrap to opposite side
   */
  function wrapPosition(x: number, y: number) {
    const wrappedX = ((x % canvasWidth.value) + canvasWidth.value) % canvasWidth.value;
    const wrappedY = ((y % canvasHeight.value) + canvasHeight.value) % canvasHeight.value;
    
    return { x: wrappedX, y: wrappedY };
  }

  /**
   * Calculate which "tiles" of the canvas should be rendered
   * to create seamless wrapping effect
   */
  function getTilesToRender(
    viewportWidth: number,
    viewportHeight: number,
    pan: { x: number; y: number },
    zoom: number
  ) {
    const tiles: Array<{ offsetX: number; offsetY: number }> = [];
    
    // Determine how many repetitions we need based on zoom and pan
    const tilesX = Math.ceil(viewportWidth / (canvasWidth.value * zoom)) + 1;
    const tilesY = Math.ceil(viewportHeight / (canvasHeight.value * zoom)) + 1;
    
    const startTileX = Math.floor(-pan.x / (canvasWidth.value * zoom));
    const startTileY = Math.floor(-pan.y / (canvasHeight.value * zoom));
    
    for (let ty = startTileY; ty < startTileY + tilesY; ty++) {
      for (let tx = startTileX; tx < startTileX + tilesX; tx++) {
        tiles.push({
          offsetX: tx * canvasWidth.value,
          offsetY: ty * canvasHeight.value
        });
      }
    }
    
    return tiles;
  }

  /**
   * Render map with wrapping - draw multiple instances
   */
  function renderWithWrapping(
    ctx: CanvasRenderingContext2D,
    renderFunction: () => void,
    viewportWidth: number,
    viewportHeight: number,
    pan: { x: number; y: number },
    zoom: number
  ) {
    const tiles = getTilesToRender(viewportWidth, viewportHeight, pan, zoom);
    
    tiles.forEach(tile => {
      ctx.save();
      ctx.translate(tile.offsetX, tile.offsetY);
      renderFunction();
      ctx.restore();
    });
  }

  /**
   * Handle pan update with wrapping
   */
  function updatePan(deltaX: number, deltaY: number, currentPan: { x: number; y: number }) {
    const newX = currentPan.x + deltaX;
    const newY = currentPan.y + deltaY;
    
    // Allow infinite panning - wrapping happens in render
    virtualPan.value = { x: newX, y: newY };
    
    return virtualPan.value;
  }

  /**
   * Convert screen coordinates to canvas coordinates with wrapping
   */
  function screenToCanvas(
    screenX: number,
    screenY: number,
    pan: { x: number; y: number },
    zoom: number
  ) {
    const canvasX = (screenX - pan.x) / zoom;
    const canvasY = (screenY - pan.y) / zoom;
    
    // Wrap to 0-100% range
    const wrappedX = ((canvasX % canvasWidth.value) + canvasWidth.value) % canvasWidth.value;
    const wrappedY = ((canvasY % canvasHeight.value) + canvasHeight.value) % canvasHeight.value;
    
    // Convert to percentage
    return {
      x: (wrappedX / canvasWidth.value) * 100,
      y: (wrappedY / canvasHeight.value) * 100
    };
  }

  return {
    wrapPosition,
    getTilesToRender,
    renderWithWrapping,
    updatePan,
    screenToCanvas,
    virtualPan
  };
}
```

### Update MapCanvas.vue to use wrapping

```typescript
// Inside MapCanvas.vue setup
const { renderWithWrapping, updatePan, screenToCanvas } = useInfiniteCanvas(
  canvasWidth,
  canvasHeight
);

function renderMap() {
  if (!ctx.value || !containerRef.value) return;
  
  clear();
  
  // Render with wrapping effect
  renderWithWrapping(
    ctx.value,
    () => {
      ctx.value!.save();
      ctx.value!.scale(props.zoom, props.zoom);
      renderLayers(props.mapData);
      ctx.value!.restore();
    },
    containerRef.value.clientWidth,
    containerRef.value.clientHeight,
    props.pan,
    props.zoom
  );
}

function handleMouseMove(e: MouseEvent) {
  if (isDragging.value) {
    const deltaX = e.clientX - lastMousePos.value.x;
    const deltaY = e.clientY - lastMousePos.value.y;
    
    const newPan = updatePan(deltaX, deltaY, props.pan);
    emit('update:pan', newPan);
    
    lastMousePos.value = { x: e.clientX, y: e.clientY };
  }
}
```

---

## Interaction System

### useInteraction.ts

```typescript
// composables/useInteraction.ts
import { ref, type Ref } from 'vue';
import type { MapData, Point } from '@/types/map.types';

export function useInteraction(
  canvasRef: Ref<HTMLCanvasElement | undefined>,
  mapData: Ref<MapData>
) {
  const selectedItem = ref<any>(null);
  const hoveredItem = ref<any>(null);
  const isDragging = ref(false);
  const isDrawing = ref(false);
  const currentTool = ref<string>('select');
  const drawingPoints = ref<Point[]>([]);

  function findItemAtPosition(x: number, y: number) {
    // Check markers first (smallest targets)
    for (const marker of mapData.value.markers) {
      if (isPointNearMarker(x, y, marker)) {
        return { type: 'marker', item: marker };
      }
    }

    // Check cities
    for (const continent of mapData.value.continents) {
      for (const country of continent.countries) {
        for (const city of country.cities) {
          if (city.isArea) {
            if (isPointInPolygon({ x, y }, city.points)) {
              return { type: 'city', item: city };
            }
          } else {
            if (isPointNearMarker(x, y, { position: city.points[0], size: 8 })) {
              return { type: 'city', item: city };
            }
          }
        }
      }
    }

    // Check countries
    for (const continent of mapData.value.continents) {
      for (const country of continent.countries) {
        if (isPointInPolygon({ x, y }, country.points)) {
          return { type: 'country', item: country };
        }
      }
    }

    // Check continents
    for (const continent of mapData.value.continents) {
      if (isPointInPolygon({ x, y }, continent.points)) {
        return { type: 'continent', item: continent };
      }
    }

    return null;
  }

  function isPointInPolygon(point: Point, polygon: Point[]): boolean {
    let inside = false;
    for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
      const xi = polygon[i].x;
      const yi = polygon[i].y;
      const xj = polygon[j].x;
      const yj = polygon[j].y;

      const intersect = ((yi > point.y) !== (yj > point.y))
        && (point.x < (xj - xi) * (point.y - yi) / (yj - yi) + xi);
      
      if (intersect) inside = !inside;
    }
    return inside;
  }

  function isPointNearMarker(
    x: number,
    y: number,
    marker: { position: Point; size: number }
  ): boolean {
    const distance = Math.sqrt(
      Math.pow(x - marker.position.x, 2) + Math.pow(y - marker.position.y, 2)
    );
    return distance <= marker.size + 5; // 5px tolerance
  }

  function handleClick(x: number, y: number) {
    if (currentTool.value === 'select') {
      const found = findItemAtPosition(x, y);
      selectedItem.value = found;
    } else if (currentTool.value === 'draw-polygon') {
      drawingPoints.value.push({ x, y });
    } else if (currentTool.value === 'add-marker') {
      addMarker(x, y);
    }
  }

  function addMarker(x: number, y: number) {
    const newMarker = {
      id: `marker-${Date.now()}`,
      name: 'New Marker',
      position: { x, y },
      type: 'custom',
      color: '#60a5fa',
      icon: '📍',
      size: 6,
      visible: true,
      labelVisible: true
    };
    mapData.value.markers.push(newMarker);
  }

  function finishDrawing() {
    if (drawingPoints.value.length < 3) {
      drawingPoints.value = [];
      return null;
    }

    const polygon = [...drawingPoints.value];
    drawingPoints.value = [];
    return polygon;
  }

  function deleteSelected() {
    if (!selectedItem.value) return;

    const { type, item } = selectedItem.value;

    if (type === 'marker') {
      const index = mapData.value.markers.findIndex(m => m.id === item.id);
      if (index !== -1) mapData.value.markers.splice(index, 1);
    }
    // Add similar logic for other types

    selectedItem.value = null;
  }

  return {
    selectedItem,
    hoveredItem,
    isDragging,
    isDrawing,
    currentTool,
    drawingPoints,
    findItemAtPosition,
    handleClick,
    addMarker,
    finishDrawing,
    deleteSelected
  };
}
```

---

## Step-by-Step Implementation

### Phase 1: Basic Setup (Day 1)

1. **Create project structure**
```bash
# Create folders
mkdir -p src/components src/composables src/types src/utils

# Create files
touch src/components/MapEditor.vue
touch src/components/MapCanvas.vue
touch src/composables/useCanvas.ts
touch src/types/map.types.ts
```

2. **Setup TypeScript interfaces** (copy from Data Structure section)

3. **Create basic MapCanvas component**
    - Canvas element
    - Basic mouse events
    - Clear and render functions

4. **Test with static background image**

### Phase 2: Layer Rendering (Day 2-3)

1. **Implement useCanvas composable**
    - Drawing primitives (polygon, circle, line, text)
    - Copy all functions from Canvas Implementation section

2. **Implement useLayerRenderer**
    - Background rendering
    - Continent rendering
    - Country rendering
    - City rendering
    - Route rendering
    - Marker rendering
    - Label rendering

3. **Create sample JSON data**
    - Test with 1-2 continents
    - Add a few cities and markers

4. **Verify layer order and visibility**

### Phase 3: Zoom & Pan (Day 4)

1. **Add zoom functionality**
```typescript
function handleWheel(e: WheelEvent) {
  e.preventDefault();
  const delta = e.deltaY > 0 ? 0.9 : 1.1;
  const newZoom = Math.max(0.1, Math.min(5, zoom.value * delta));
  emit('update:zoom', newZoom);
}
```

2. **Add pan functionality**
```typescript
let isDragging = false;
let lastPos = { x: 0, y: 0 };

function handleMouseDown(e: MouseEvent) {
  isDragging = true;
  lastPos = { x: e.clientX, y: e.clientY };
}

function handleMouseMove(e: MouseEvent) {
  if (!isDragging) return;
  
  const deltaX = e.clientX - lastPos.x;
  const deltaY = e.clientY - lastPos.y;
  
  emit('update:pan', {
    x: pan.value.x + deltaX,
    y: pan.value.y + deltaY
  });
  
  lastPos = { x: e.clientX, y: e.clientY };
}

function handleMouseUp() {
  isDragging = false;
}
```

3. **Test zoom and pan together**

### Phase 4: Infinite Canvas (Day 5)

1. **Implement useInfiniteCanvas composable** (copy from section above)

2. **Update rendering to use wrapping**
    - Modify MapCanvas to call `renderWithWrapping`
    - Test edge wrapping (scroll to edge and continue)

3. **Fix coordinate conversion**
    - Ensure mouse clicks work with wrapping
    - Update `screenToCanvas` function

### Phase 5: Layer Controls (Day 6)

1. **Create LayerControls component**
```vue
<template>
  <div class="layer-controls">
    <h3>Layers</h3>
    
    <div class="layer-group">
      <h4>Continents</h4>
      <div v-for="continent in mapData.continents" :key="continent.id">
        <label>
          <input 
            type="checkbox" 
            v-model="continent.visible"
          />
          {{ continent.name }}
        </label>
        <label class="sub-control">
          <input 
            type="checkbox" 
            v-model="continent.borderVisible"
            :disabled="!continent.visible"
          />
          Border
        </label>
        <label class="sub-control">
          <input 
            type="checkbox" 
            v-model="continent.fillVisible"
            :disabled="!continent.visible"
          />
          Fill
        </label>
      </div>
    </div>
    
    <div class="layer-group">
      <h4>Routes</h4>
      <div v-for="route in mapData.routes" :key="route.id">
        <label>
          <input type="checkbox" v-model="route.visible" />
          {{ route.name }}
        </label>
      </div>
    </div>
    
    <div class="layer-group">
      <h4>Markers</h4>
      <div v-for="marker in mapData.markers" :key="marker.id">
        <label>
          <input type="checkbox" v-model="marker.visible" />
          {{ marker.name }}
        </label>
      </div>
    </div>
  </div>
</template>
```

2. **Style layer controls panel**

### Phase 6: Tool Panel (Day 7)

1. **Create ToolPanel component**
```vue
<template>
  <div class="tool-panel">
    <button 
      :class="{ active: activeTool === 'select' }"
      @click="$emit('tool-change', 'select')"
    >
      Select
    </button>
    
    <button 
      :class="{ active: activeTool === 'draw-polygon' }"
      @click="$emit('tool-change', 'draw-polygon')"
    >
      Draw Polygon
    </button>
    
    <button 
      :class="{ active: activeTool === 'add-marker' }"
      @click="$emit('tool-change', 'add-marker')"
    >
      Add Marker
    </button>
    
    <button 
      :class="{ active: activeTool === 'add-route' }"
      @click="$emit('tool-change', 'add-route')"
    >
      Add Route
    </button>
    
    <button 
      :class="{ active: activeTool === 'add-label' }"
      @click="$emit('tool-change', 'add-label')"
    >
      Add Label
    </button>
  </div>
</template>
```

2. **Implement tool behaviors in useInteraction**

### Phase 7: Editing Features (Day 8-9)

1. **Selection system**
    - Click to select items
    - Highlight selected item
    - Show selection handles

2. **Polygon editing**
    - Drag vertices
    - Add new vertices
    - Delete vertices

3. **Properties panel**
```vue
<template>
  <div v-if="selectedItem" class="properties-panel">
    <h3>Properties</h3>
    
    <div v-if="selectedItem.type === 'marker'">
      <label>
        Name:
        <input v-model="selectedItem.item.name" />
      </label>
      
      <label>
        Color:
        <input type="color" v-model="selectedItem.item.color" />
      </label>
      
      <label>
        Size:
        <input 
          type="range" 
          v-model.number="selectedItem.item.size" 
          min="3" 
          max="20"
        />
      </label>
      
      <label>
        Type:
        <select v-model="selectedItem.item.type">
          <option value="city">City</option>
          <option value="hazard">Hazard</option>
          <option value="landmark">Landmark</option>
          <option value="custom">Custom</option>
        </select>
      </label>
    </div>
    
    <!-- Similar for other types -->
  </div>
</template>
```

### Phase 8: Import/Export (Day 10)

1. **Create ExportImport component**
```vue
<template>
  <div class="import-export">
    <button @click="handleExport">Export JSON</button>
    <button @click="handleImport">Import JSON</button>
    <button @click="handleExportImage">Export as PNG</button>
    
    <input 
      ref="fileInput"
      type="file" 
      accept=".json"
      @change="handleFileSelect"
      style="display: none"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { saveAs } from 'file-saver';

const emit = defineEmits(['import', 'export', 'export-image']);
const fileInput = ref<HTMLInputElement>();

function handleExport() {
  emit('export');
}

function handleImport() {
  fileInput.value?.click();
}

function handleFileSelect(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;
  
  const reader = new FileReader();
  reader.onload = (event) => {
    try {
      const data = JSON.parse(event.target?.result as string);
      emit('import', data);
    } catch (err) {
      console.error('Invalid JSON file', err);
    }
  };
  reader.readAsText(file);
}

function handleExportImage() {
  emit('export-image');
}
</script>
```

2. **Implement export functions in MapEditor**
```typescript
function handleExport() {
  const dataStr = JSON.stringify(mapData.value, null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  saveAs(blob, 'map-data.json');
}

function handleImport(data: MapData) {
  mapData.value = data;
}

function handleExportImage() {
  const canvas = canvasRef.value?.canvasRef;
  if (!canvas) return;
  
  canvas.toBlob((blob) => {
    if (blob) saveAs(blob, 'map-export.png');
  });
}
```

### Phase 9: Polish & Optimization (Day 11-12)

1. **Performance optimization**
    - Implement dirty checking (only re-render when needed)
    - Use requestAnimationFrame for smooth animations
    - Debounce expensive operations

2. **Keyboard shortcuts**
```typescript
onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});

function handleKeyDown(e: KeyboardEvent) {
  if (e.key === 'Delete' && selectedItem.value) {
    deleteSelected();
  }
  
  if (e.key === 'Escape') {
    selectedItem.value = null;
    drawingPoints.value = [];
  }
  
  if (e.ctrlKey || e.metaKey) {
    if (e.key === 'z') {
      undo();
    }
    if (e.key === 's') {
      e.preventDefault();
      handleExport();
    }
  }
}
```

3. **Undo/Redo system**
```typescript
const history = ref<MapData[]>([]);
const historyIndex = ref(-1);

function saveState() {
  // Remove any states after current index
  history.value = history.value.slice(0, historyIndex.value + 1);
  
  // Add new state
  history.value.push(JSON.parse(JSON.stringify(mapData.value)));
  historyIndex.value++;
  
  // Limit history size
  if (history.value.length > 50) {
    history.value.shift();
    historyIndex.value--;
  }
}

function undo() {
  if (historyIndex.value > 0) {
    historyIndex.value--;
    mapData.value = JSON.parse(JSON.stringify(history.value[historyIndex.value]));
  }
}

function redo() {
  if (historyIndex.value < history.value.length - 1) {
    historyIndex.value++;
    mapData.value = JSON.parse(JSON.stringify(history.value[historyIndex.value]));
  }
}
```

---

## Advanced Features

### Snap to Grid

```typescript
function snapToGrid(point: Point, gridSize: number = 5): Point {
  return {
    x: Math.round(point.x / gridSize) * gridSize,
    y: Math.round(point.y / gridSize) * gridSize
  };
}
```

### Minimap

```vue
<template>
  <div class="minimap">
    <canvas 
      ref="minimapCanvas"
      :width="200"
      :height="120"
      @click="handleMinimapClick"
    />
  </div>
</template>

<script setup lang="ts">
function renderMinimap() {
  const ctx = minimapCanvas.value?.getContext('2d');
  if (!ctx) return;
  
  // Scale down and render entire map
  const scale = 200 / canvasWidth.value;
  ctx.save();
  ctx.scale(scale, scale);
  renderLayers(mapData.value);
  ctx.restore();
  
  // Draw viewport indicator
  const viewX = (-pan.value.x / zoom.value) * scale;
  const viewY = (-pan.value.y / zoom.value) * scale;
  const viewW = (containerWidth / zoom.value) * scale;
  const viewH = (containerHeight / zoom.value) * scale;
  
  ctx.strokeStyle = '#ff0000';
  ctx.lineWidth = 2;
  ctx.strokeRect(viewX, viewY, viewW, viewH);
}
```

### Auto-save

```typescript
import { watchDebounced } from '@vueuse/core';

watchDebounced(
  mapData,
  (newData) => {
    localStorage.setItem('map-autosave', JSON.stringify(newData));
  },
  { debounce: 2000, deep: true }
);

// On mount, restore autosave
onMounted(() => {
  const saved = localStorage.getItem('map-autosave');
  if (saved) {
    try {
      mapData.value = JSON.parse(saved);
    } catch (err) {
      console.error('Failed to restore autosave');
    }
  }
});
```

### Touch Support

```typescript
function handleTouchStart(e: TouchEvent) {
  if (e.touches.length === 1) {
    // Single touch = pan
    isDragging.value = true;
    lastPos.value = {
      x: e.touches[0].clientX,
      y: e.touches[0].clientY
    };
  } else if (e.touches.length === 2) {
    // Two finger = zoom
    isZooming.value = true;
    initialPinchDistance.value = getPinchDistance(e.touches);
  }
}

function getPinchDistance(touches: TouchList): number {
  const dx = touches[0].clientX - touches[1].clientX;
  const dy = touches[0].clientY - touches[1].clientY;
  return Math.sqrt(dx * dx + dy * dy);
}
```

---

## Testing Strategy

### Unit Tests
```typescript
// useCanvas.test.ts
import { describe, it, expect } from 'vitest';
import { useCanvas } from '@/composables/useCanvas';

describe('useCanvas', () => {
  it('should draw polygon correctly', () => {
    const canvas = document.createElement('canvas');
    const canvasRef = ref(canvas);
    const { drawPolygon } = useCanvas(canvasRef);
    
    const points = [
      { x: 10, y: 10 },
      { x: 50, y: 10 },
      { x: 50, y: 50 },
      { x: 10, y: 50 }
    ];
    
    drawPolygon(points, '#ff0000', '#000000', 2);
    // Assert canvas has been drawn to
  });
});
```

### Integration Tests
```typescript
// MapEditor.test.ts
import { mount } from '@vue/test-utils';
import MapEditor from '@/components/MapEditor.vue';

describe('MapEditor', () => {
  it('should load and render map data', async () => {
    const wrapper = mount(MapEditor);
    
    // Simulate file upload
    await wrapper.vm.handleImport(mockMapData);
    
    // Check if continents are rendered
    expect(wrapper.vm.mapData.continents.length).toBe(3);
  });
});
```

---

## Performance Tips

1. **Use OffscreenCanvas for background** (if supported)
```typescript
const offscreenCanvas = new OffscreenCanvas(width, height);
const offscreenCtx = offscreenCanvas.getContext('2d');
// Render static background once
// Use it as image in main canvas
```

2. **Implement viewport culling**
```typescript
function isInViewport(item: any, viewport: Rect): boolean {
  // Only render items visible in current viewport
  return !(
    item.bounds.right < viewport.left ||
    item.bounds.left > viewport.right ||
    item.bounds.bottom < viewport.top ||
    item.bounds.top > viewport.bottom
  );
}
```

3. **Use requestAnimationFrame**
```typescript
let frameId: number;

function render() {
  renderMap();
  frameId = requestAnimationFrame(render);
}

onMounted(() => {
  frameId = requestAnimationFrame(render);
});

onUnmounted(() => {
  cancelAnimationFrame(frameId);
});
```

---

## Conclusion

This guide provides a complete roadmap for building an interactive, layered map editor in Vue.js with TypeScript. Follow the phases sequentially for best results.

### Timeline Summary
- **Days 1-3**: Basic setup + layer rendering
- **Days 4-5**: Zoom, pan, infinite canvas
- **Days 6-7**: UI controls and tools
- **Days 8-9**: Editing features
- **Days 10-12**: Export/import and polish

### Next Steps
1. Start with Phase 1 - create basic structure
2. Implement one feature at a time
3. Test thoroughly before moving to next phase
4. Iterate based on user feedback

### Resources
- [Canvas API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [Vue 3 Documentation](https://vuejs.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

Good luck with your map editor!