<template>
  <div class="map-canvas-container">
    <canvas
      ref="canvas"
      class="map-canvas"
      :class="{ 'brush-mode': isShiftPressed && isDragging }"
      @mousedown="handleMouseDown"
      @mousemove="handleMouseMove"
      @mouseup="handleMouseUp"
      @mouseleave="handleMouseLeave"
      @wheel.prevent="handleWheel"
    ></canvas>
    <!-- Brush Mode Indicator -->
    <div v-if="isShiftPressed" class="brush-mode-indicator">
      <span class="indicator-icon">🖌️</span>
      <span class="indicator-text">BRUSH MODE</span>
    </div>
    <!-- Zoom HUD -->
    <div class="zoom-hud">
      <button class="zoom-btn" @click="zoomOut" :disabled="zoom <= minZoom" title="Zoom Out">−</button>
      <span class="zoom-display">{{ zoomPercentage }}%</span>
      <button class="zoom-btn" @click="zoomIn" :disabled="zoom >= maxZoom" title="Zoom In">+</button>
      <button class="zoom-btn zoom-reset" @click="resetZoom" title="Reset Zoom">⟲</button>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import { TERRAIN_CONFIGS } from '@/types/tabletop';

const CARDINAL_DELTAS = {
  north: { dx: 0, dy: -1 },
  south: { dx: 0, dy: 1 },
  east: { dx: 1, dy: 0 },
  west: { dx: -1, dy: 0 }
};

const OPPOSITE_DIRECTION = {
  north: 'south',
  south: 'north',
  east: 'west',
  west: 'east'
};

const DIAGONAL_DELTAS = {
  northEast: { dx: 1, dy: -1 },
  northWest: { dx: -1, dy: -1 },
  southEast: { dx: 1, dy: 1 },
  southWest: { dx: -1, dy: 1 }
};

const OPPOSITE_DIAGONAL_DIRECTION = {
  northEast: 'southWest',
  southWest: 'northEast',
  northWest: 'southEast',
  southEast: 'northWest'
};

export default {
  name: 'MapCanvas',
  data() {
    return {
      canvas: null,
      ctx: null,
      isDragging: false,
      isPanning: false,
      isShiftPressed: false,
      panStartX: 0,
      panStartY: 0,
      panStartOffsetX: 0,
      panStartOffsetY: 0,
      hoveredCell: null,
      lastPaintedCell: null,
      // In Path mode, this is the starting cell for click-to-connect edge editing
      edgeStartCell: null,
      canvasWidth: 0,
      canvasHeight: 0,
      offsetX: 0,
      offsetY: 0,
      backgroundImage: null,
      // Zoom state
      zoom: 1.0,
      minZoom: 0.5,
      maxZoom: 3.0,
      zoomStep: 1.1 // Exponential zoom factor
    };
  },
  computed: {
    ...mapGetters('tabletopEditor', [
      'currentMap',
      'currentLayer',
      'selectedTool',
      'selectedCell',
      'gridVisible',
      'backgroundVisible',
      'editorMode',
      'availabilityVisible',
      'pathsVisible',
      'objectsVisible',
      'currentLayerCells',
      'gridConfig',
      'getCurrentLayerMetadata'
    ]),
    zoomPercentage() {
      return Math.round(this.zoom * 100);
    },
    // Scaled grid config - calculates actual cell sizes based on current image dimensions
    // This ensures grid scales proportionally with the image across different resolutions
    scaledGridConfig() {
      if (!this.gridConfig) return null;

      // If no reference dimensions are set, or no background image, use original values
      if (!this.gridConfig.referenceImageWidth || !this.gridConfig.referenceImageHeight || !this.backgroundImage) {
        return this.gridConfig;
      }

      // Calculate scale factors based on current image size vs reference size
      const scaleX = this.backgroundImage.width / this.gridConfig.referenceImageWidth;
      const scaleY = this.backgroundImage.height / this.gridConfig.referenceImageHeight;

      // Return scaled grid config
      return {
        ...this.gridConfig,
        cellWidth: this.gridConfig.cellWidth * scaleX,
        cellHeight: this.gridConfig.cellHeight * scaleY
      };
    }
  },
  watch: {
    currentMap: {
      handler() {
        this.loadBackgroundImage();
        this.render();
      },
      deep: true
    },
    currentLayer() {
      this.render();
    },
    gridVisible() {
      this.render();
    },
    backgroundVisible() {
      this.render();
    },
    availabilityVisible() {
      this.render();
    },
    pathsVisible() {
      this.render();
    },
    objectsVisible() {
      this.render();
    }
  },
  mounted() {
    this.initCanvas();
    this.loadBackgroundImage();
    this.render();
    window.addEventListener('resize', this.handleResize);
    window.addEventListener('keydown', this.handleKeyDown);
    window.addEventListener('keyup', this.handleKeyUp);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
    window.removeEventListener('keydown', this.handleKeyDown);
    window.removeEventListener('keyup', this.handleKeyUp);
  },
  methods: {
    ...mapActions('tabletopEditor', [
      'selectCell',
      'toggleCellAvailability',
      'toggleCellConnection',
      'placeCellSpawner',
      'placeCellGameObject',
      'clearCellContent'
    ]),

    initCanvas() {
      this.canvas = this.$refs.canvas;
      this.ctx = this.canvas.getContext('2d');
      this.handleResize();
    },

    // Expose canvas for export
    getCanvas() {
      return this.canvas;
    },

    handleResize() {
      const container = this.canvas.parentElement;
      this.canvasWidth = container.clientWidth;
      this.canvasHeight = container.clientHeight;
      this.canvas.width = this.canvasWidth;
      this.canvas.height = this.canvasHeight;
      this.render();
    },

    // Zoom methods
    handleWheel(event) {
      const delta = event.deltaY;
      if (delta < 0) {
        this.zoomIn();
      } else {
        this.zoomOut();
      }
    },

    zoomIn() {
      this.setZoom(this.zoom * this.zoomStep);
    },

    zoomOut() {
      this.setZoom(this.zoom / this.zoomStep);
    },

    resetZoom() {
      this.setZoom(1.0);
    },

    setZoom(newZoom) {
      // Clamp zoom to min/max range
      this.zoom = Math.max(this.minZoom, Math.min(this.maxZoom, newZoom));
      this.render();
    },

    loadBackgroundImage() {
      if (this.currentMap?.backgroundImage) {
        const img = new Image();
        img.onload = () => {
          this.backgroundImage = img;
          this.render();
        };
        img.src = this.currentMap.backgroundImage;
      } else {
        this.backgroundImage = null;
        this.render();
      }
    },

    render() {
      if (!this.ctx || !this.currentMap) return;

      // Clear canvas
      this.ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

      // Save context state and apply zoom transformation
      this.ctx.save();

      // Translate to center, apply zoom, translate back
      this.ctx.translate(this.canvasWidth / 2, this.canvasHeight / 2);
      this.ctx.scale(this.zoom, this.zoom);
      this.ctx.translate(-this.canvasWidth / 2, -this.canvasHeight / 2);

      // Draw background
      if (this.backgroundVisible && this.backgroundImage) {
        this.drawBackground();
      } else {
        // Fill with dark background
        this.ctx.fillStyle = '#1a1a1a';
        this.ctx.fillRect(0, 0, this.canvasWidth, this.canvasHeight);
      }

      // Draw grid
      if (this.gridVisible && this.gridConfig) {
        this.drawGrid();
      }

      // Draw cells
      this.drawCells();

      // Draw movement edges/directions for the current layer
      if (this.pathsVisible) {
        this.drawMovementEdgesLayer();
      }

      // Draw hovered cell highlight
      if (this.hoveredCell) {
        this.drawCellHighlight(this.hoveredCell.x, this.hoveredCell.y, 'rgba(255, 255, 0, 0.3)');
      }

      // Draw selected cell highlight
      if (this.selectedCell && this.selectedCell.layer === this.currentLayer) {
        this.drawCellHighlight(this.selectedCell.x, this.selectedCell.y, 'rgba(0, 255, 255, 0.5)');
      }

      // Restore context state
      this.ctx.restore();
    },

    getCellStateForMovement(lookup, x, y, layerId) {
      if (!this.currentMap || !this.gridConfig) {
        return {
          available: false,
          connections: {
            north: false,
            south: false,
            east: false,
            west: false,
            northEast: false,
            northWest: false,
            southEast: false,
            southWest: false
          }
        };
      }

      const { columns, rows } = this.gridConfig;

      if (x < 0 || y < 0 || x >= columns || y >= rows) {
        return {
          available: false,
          connections: {
            north: false,
            south: false,
            east: false,
            west: false,
            northEast: false,
            northWest: false,
            southEast: false,
            southWest: false
          }
        };
      }

      const layers = this.currentMap.layers || [];
      const layerMeta = layers.find(l => l.id === layerId);

      if (!layerMeta || layerMeta.active === false) {
        return {
          available: false,
          connections: {
            north: false,
            south: false,
            east: false,
            west: false,
            northEast: false,
            northWest: false,
            southEast: false,
            southWest: false
          }
        };
      }

      const key = `${x},${y},${layerId}`;
      const cell = lookup.get(key);

      if (!cell) {
        // No explicit cell data -> treat as a default available cell with all connections open
        return {
          available: true,
          connections: {
            north: true,
            south: true,
            east: true,
            west: true,
            // Diagonals default to open unless explicitly blocked
            northEast: undefined,
            northWest: undefined,
            southEast: undefined,
            southWest: undefined
          }
        };
      }

      const connections = cell.connections || {};

      return {
        available: cell.available !== false,
        connections: {
          north: connections.north !== false,
          south: connections.south !== false,
          east: connections.east !== false,
          west: connections.west !== false,
          // Diagonal flags are interpreted as: false => blocked, anything else => open
          northEast: connections.northEast,
          northWest: connections.northWest,
          southEast: connections.southEast,
          southWest: connections.southWest
        }
      };
    },

    canCardinalMoveFrom(lookup, x, y, layerId, direction) {
      const deltas = CARDINAL_DELTAS[direction];
      if (!deltas) return false;

      const fromState = this.getCellStateForMovement(lookup, x, y, layerId);
      if (!fromState.available) return false;

      const targetX = x + deltas.dx;
      const targetY = y + deltas.dy;
      const toState = this.getCellStateForMovement(lookup, targetX, targetY, layerId);

      if (!toState.available) return false;

      const opposite = OPPOSITE_DIRECTION[direction];
      return !!fromState.connections[direction] && !!toState.connections[opposite];
    },

    canDiagonalMoveFrom(lookup, x, y, layerId, direction) {
      const deltas = DIAGONAL_DELTAS[direction];
      if (!deltas) return false;

      const fromState = this.getCellStateForMovement(lookup, x, y, layerId);
      if (!fromState.available) return false;

      const targetX = x + deltas.dx;
      const targetY = y + deltas.dy;
      const toState = this.getCellStateForMovement(lookup, targetX, targetY, layerId);
      if (!toState.available) return false;

      // Enforce no corner cutting: diagonal move only if both related
      // cardinal moves are possible from the source cell.
      const requires = {
        northEast: ['north', 'east'],
        northWest: ['north', 'west'],
        southEast: ['south', 'east'],
        southWest: ['south', 'west']
      };

      const deps = requires[direction] || [];
      if (deps.length === 2) {
        if (
          !this.canCardinalMoveFrom(lookup, x, y, layerId, deps[0]) ||
          !this.canCardinalMoveFrom(lookup, x, y, layerId, deps[1])
        ) {
          return false;
        }
      }

      // Diagonal flags: if either side explicitly blocks this diagonal,
      // the move is not allowed. When undefined, it is treated as open.
      const fromDiag = fromState.connections && fromState.connections[direction];
      const oppositeDiag = OPPOSITE_DIAGONAL_DIRECTION[direction];
      const toDiag = oppositeDiag && toState.connections
        ? toState.connections[oppositeDiag]
        : undefined;

      if (fromDiag === false || toDiag === false) {
        return false;
      }

      return true;
    },

    buildMovementEdgesForCurrentLayer() {
      if (!this.currentMap || !this.gridConfig || !this.currentMap.edges) return [];

      const layerId = this.currentLayer;
      const cells = this.currentMap.cells || [];
      const allEdges = this.currentMap.edges || [];

      // Build cell lookup for quick access
      const cellLookup = new Map();
      cells.forEach(cell => {
        cellLookup.set(`${cell.x},${cell.y},${cell.layer}`, cell);
      });

      // Filter edges for current layer and check cell passability
      const visibleEdges = [];

      allEdges.forEach(edge => {
        // Only show edges for current layer
        if (edge.id.layer !== layerId) return;

        // Check if both cells are passable
        const fromKey = `${edge.id.fromX},${edge.id.fromY},${edge.id.layer}`;
        const toKey = `${edge.id.toX},${edge.id.toY},${edge.id.layer}`;

        const fromCell = cellLookup.get(fromKey);
        const toCell = cellLookup.get(toKey);

        // Default to passable if cell doesn't exist (implicit grass terrain)
        const fromPassable = !fromCell || fromCell.passable !== false;
        const toPassable = !toCell || toCell.passable !== false;

        // Only show edges between passable cells
        if (!fromPassable || !toPassable) return;

        // Convert to rendering format
        visibleEdges.push({
          from: { x: edge.id.fromX, y: edge.id.fromY, layer: edge.id.layer },
          to: { x: edge.id.toX, y: edge.id.toY, layer: edge.id.layer },
          direction: edge.direction,
          enabled: !edge.blocked  // Edge is enabled if not blocked
        });
      });

      return visibleEdges;
    },

    drawMovementEdgesLayer() {
      if (!this.currentMap) return;

      const scaledConfig = this.scaledGridConfig;
      if (!scaledConfig) return;

      const edges = this.buildMovementEdgesForCurrentLayer();
      if (!edges.length) return;

      const { cellWidth, cellHeight, columns, rows } = scaledConfig;

      // Position edges relative to the image, not the canvas
      const imagePos = this.getImagePosition();
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = imagePos.x;
      const startY = imagePos.y;

      edges.forEach(edge => {
        if (!edge || !edge.from || !edge.to) return;

        const fromCenterX = startX + edge.from.x * cellWidth + cellWidth / 2;
        const fromCenterY = startY + edge.from.y * cellHeight + cellHeight / 2;
        const toCenterX = startX + edge.to.x * cellWidth + cellWidth / 2;
        const toCenterY = startY + edge.to.y * cellHeight + cellHeight / 2;

        const fromPoint = this.applyMorph(fromCenterX, fromCenterY, gridWidth, gridHeight, startX, startY);
        const toPoint = this.applyMorph(toCenterX, toCenterY, gridWidth, gridHeight, startX, startY);

        // Set color and style based on enabled status
        if (edge.enabled) {
          // Enabled connections: bright green, solid line
          this.ctx.strokeStyle = 'rgba(0, 255, 0, 0.7)';
          this.ctx.lineWidth = 2;
          this.ctx.fillStyle = 'rgba(0, 255, 0, 0.7)';
          this.ctx.setLineDash([]);
        } else {
          // Disabled connections: red, dashed line
          this.ctx.strokeStyle = 'rgba(255, 50, 50, 0.5)';
          this.ctx.lineWidth = 2;
          this.ctx.fillStyle = 'rgba(255, 50, 50, 0.5)';
          this.ctx.setLineDash([5, 5]);
        }

        // Draw main edge line
        this.ctx.beginPath();
        this.ctx.moveTo(fromPoint.x, fromPoint.y);
        this.ctx.lineTo(toPoint.x, toPoint.y);
        this.ctx.stroke();

        // Draw a small arrow head at the target side to indicate direction
        const angle = Math.atan2(toPoint.y - fromPoint.y, toPoint.x - fromPoint.x);
        const arrowSize = edge.enabled ? 6 : 4;

        this.ctx.beginPath();
        this.ctx.moveTo(toPoint.x, toPoint.y);
        this.ctx.lineTo(
          toPoint.x - arrowSize * Math.cos(angle - Math.PI / 6),
          toPoint.y - arrowSize * Math.sin(angle - Math.PI / 6)
        );
        this.ctx.lineTo(
          toPoint.x - arrowSize * Math.cos(angle + Math.PI / 6),
          toPoint.y - arrowSize * Math.sin(angle + Math.PI / 6)
        );
        this.ctx.closePath();
        this.ctx.fill();
      });

      // Reset line dash to solid for other drawing operations
      this.ctx.setLineDash([]);
    },

    // Calculate the position where the image is drawn in the canvas
    // This is the reference point for all grid and cell positioning
    getImagePosition() {
      if (!this.backgroundImage) {
        return { x: 0, y: 0, width: 0, height: 0 };
      }

      const width = this.backgroundImage.width;
      const height = this.backgroundImage.height;

      // Center the image in the canvas viewport, with pan offset
      const x = (this.canvasWidth - width) / 2 + this.offsetX;
      const y = (this.canvasHeight - height) / 2 + this.offsetY;

      return { x, y, width, height };
    },

    drawBackground() {
      if (!this.backgroundImage) return;

      // Render image at its native size, independent of canvas size
      // The canvas acts as a viewport/camera showing part of the image
      const imagePos = this.getImagePosition();

      this.ctx.globalAlpha = 0.5;
      this.ctx.drawImage(this.backgroundImage, imagePos.x, imagePos.y, imagePos.width, imagePos.height);
      this.ctx.globalAlpha = 1.0;
    },

    // Apply perspective morph transformation to a point
    // Supports both 4-point morphing (cornerOffsets) and legacy 2-axis morphing (xMorph/yMorph)
    applyMorph(x, y, gridWidth, gridHeight, startX, startY) {
      const { xMorph, yMorph, cornerOffsets } = this.gridConfig;

      // Use 4-point morphing if cornerOffsets are defined
      if (cornerOffsets) {
        // Calculate normalized position within the grid (0 to 1)
        const u = (x - startX) / gridWidth;
        const v = (y - startY) / gridHeight;

        // Define the four corners of the grid in screen space
        // Default positions (no morph)
        const topLeftDefault = { x: startX, y: startY };
        const topRightDefault = { x: startX + gridWidth, y: startY };
        const bottomLeftDefault = { x: startX, y: startY + gridHeight };
        const bottomRightDefault = { x: startX + gridWidth, y: startY + gridHeight };

        // Apply corner offsets (scaled by grid dimensions)
        const topLeft = {
          x: topLeftDefault.x + cornerOffsets.topLeft.x * gridWidth,
          y: topLeftDefault.y + cornerOffsets.topLeft.y * gridHeight
        };
        const topRight = {
          x: topRightDefault.x + cornerOffsets.topRight.x * gridWidth,
          y: topRightDefault.y + cornerOffsets.topRight.y * gridHeight
        };
        const bottomLeft = {
          x: bottomLeftDefault.x + cornerOffsets.bottomLeft.x * gridWidth,
          y: bottomLeftDefault.y + cornerOffsets.bottomLeft.y * gridHeight
        };
        const bottomRight = {
          x: bottomRightDefault.x + cornerOffsets.bottomRight.x * gridWidth,
          y: bottomRightDefault.y + cornerOffsets.bottomRight.y * gridHeight
        };

        // Bilinear interpolation
        // Interpolate top edge
        const topX = topLeft.x * (1 - u) + topRight.x * u;
        const topY = topLeft.y * (1 - u) + topRight.y * u;

        // Interpolate bottom edge
        const bottomX = bottomLeft.x * (1 - u) + bottomRight.x * u;
        const bottomY = bottomLeft.y * (1 - u) + bottomRight.y * u;

        // Interpolate between top and bottom
        const finalX = topX * (1 - v) + bottomX * v;
        const finalY = topY * (1 - v) + bottomY * v;

        return {
          x: finalX,
          y: finalY
        };
      }

      // Legacy behavior: simple axis-based morphing
      const relX = (x - startX) / gridWidth;
      const relY = (y - startY) / gridHeight;

      const xOffset = xMorph * gridWidth * 0.3 * (relY - 0.5);
      const yOffset = yMorph * gridHeight * 0.3 * (relX - 0.5);

      return {
        x: x + xOffset,
        y: y + yOffset
      };
    },

    // Inverse morph transformation for mouse position to grid coordinates
    inverseMorph(screenX, screenY, gridWidth, gridHeight, startX, startY) {
      const { xMorph, yMorph, cornerOffsets } = this.gridConfig;

      // Check if we're using 4-point morphing or legacy morphing
      const using4Point = cornerOffsets && (
        cornerOffsets.topLeft.x !== 0 || cornerOffsets.topLeft.y !== 0 ||
        cornerOffsets.topRight.x !== 0 || cornerOffsets.topRight.y !== 0 ||
        cornerOffsets.bottomLeft.x !== 0 || cornerOffsets.bottomLeft.y !== 0 ||
        cornerOffsets.bottomRight.x !== 0 || cornerOffsets.bottomRight.y !== 0
      );

      // If no morphing is applied, return as-is
      if (!using4Point && Math.abs(xMorph) < 0.001 && Math.abs(yMorph) < 0.001) {
        return { x: screenX, y: screenY };
      }

      // Use iterative Newton's method to find the inverse
      let x = screenX;
      let y = screenY;

      for (let i = 0; i < 10; i++) {
        const morphed = this.applyMorph(x, y, gridWidth, gridHeight, startX, startY);
        const errorX = morphed.x - screenX;
        const errorY = morphed.y - screenY;

        // If error is small enough, we're done
        if (Math.abs(errorX) < 0.1 && Math.abs(errorY) < 0.1) {
          break;
        }

        x -= errorX;
        y -= errorY;
      }

      return { x, y };
    },

    drawGrid() {
      const scaledConfig = this.scaledGridConfig;
      if (!scaledConfig) return;

      const { cellWidth, cellHeight, columns, rows, xMorph, yMorph } = scaledConfig;

      // Position grid relative to the image, not the canvas
      const imagePos = this.getImagePosition();
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = imagePos.x;
      const startY = imagePos.y;

      this.ctx.strokeStyle = 'rgba(100, 100, 100, 0.5)';
      this.ctx.lineWidth = 1;

      // Draw vertical lines with morph
      for (let col = 0; col <= columns; col++) {
        const x = startX + col * cellWidth;

        // Apply morph to top and bottom points of the line
        const topPoint = this.applyMorph(x, startY, gridWidth, gridHeight, startX, startY);
        const bottomPoint = this.applyMorph(x, startY + gridHeight, gridWidth, gridHeight, startX, startY);

        this.ctx.beginPath();
        this.ctx.moveTo(topPoint.x, topPoint.y);
        this.ctx.lineTo(bottomPoint.x, bottomPoint.y);
        this.ctx.stroke();
      }

      // Draw horizontal lines with morph
      for (let row = 0; row <= rows; row++) {
        const y = startY + row * cellHeight;

        // Apply morph to left and right points of the line
        const leftPoint = this.applyMorph(startX, y, gridWidth, gridHeight, startX, startY);
        const rightPoint = this.applyMorph(startX + gridWidth, y, gridWidth, gridHeight, startX, startY);

        this.ctx.beginPath();
        this.ctx.moveTo(leftPoint.x, leftPoint.y);
        this.ctx.lineTo(rightPoint.x, rightPoint.y);
        this.ctx.stroke();
      }
    },

    drawCells() {
      if (!this.currentLayerCells) return;

      const scaledConfig = this.scaledGridConfig;
      if (!scaledConfig) return;

      const { cellWidth, cellHeight, columns, rows } = scaledConfig;

      // Position cells relative to the image, not the canvas
      const imagePos = this.getImagePosition();
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = imagePos.x;
      const startY = imagePos.y;

      this.currentLayerCells.forEach(cell => {
        const x = startX + cell.x * cellWidth;
        const y = startY + cell.y * cellHeight;

        // Calculate the four corners of the cell with morph applied
        const topLeft = this.applyMorph(x, y, gridWidth, gridHeight, startX, startY);
        const topRight = this.applyMorph(x + cellWidth, y, gridWidth, gridHeight, startX, startY);
        const bottomLeft = this.applyMorph(x, y + cellHeight, gridWidth, gridHeight, startX, startY);
        const bottomRight = this.applyMorph(x + cellWidth, y + cellHeight, gridWidth, gridHeight, startX, startY);

        // Draw terrain-based background color if availability overlay is visible
        if (this.availabilityVisible && cell.terrain) {
          const terrainConfig = TERRAIN_CONFIGS[cell.terrain];
          if (terrainConfig && terrainConfig.visualStyle) {
            // Convert hex color to rgba with transparency
            const hexColor = terrainConfig.visualStyle;
            const r = parseInt(hexColor.slice(1, 3), 16);
            const g = parseInt(hexColor.slice(3, 5), 16);
            const b = parseInt(hexColor.slice(5, 7), 16);
            this.ctx.fillStyle = `rgba(${r}, ${g}, ${b}, 0.3)`;

            this.ctx.beginPath();
            this.ctx.moveTo(topLeft.x, topLeft.y);
            this.ctx.lineTo(topRight.x, topRight.y);
            this.ctx.lineTo(bottomRight.x, bottomRight.y);
            this.ctx.lineTo(bottomLeft.x, bottomLeft.y);
            this.ctx.closePath();
            this.ctx.fill();
          }
        }

        // Draw impassable cells with red overlay (using passable property)
        if (this.availabilityVisible && cell.passable === false) {
          this.ctx.fillStyle = 'rgba(255, 0, 0, 0.4)';
          this.ctx.beginPath();
          this.ctx.moveTo(topLeft.x, topLeft.y);
          this.ctx.lineTo(topRight.x, topRight.y);
          this.ctx.lineTo(bottomRight.x, bottomRight.y);
          this.ctx.lineTo(bottomLeft.x, bottomLeft.y);
          this.ctx.closePath();
          this.ctx.fill();
        }

        // Draw spawners with morph
        if (this.objectsVisible && cell.spawner) {
          this.drawSpawner(x, y, cellWidth, cellHeight, cell.spawner, gridWidth, gridHeight, startX, startY);
        }

        // Draw game objects with morph
        if (this.objectsVisible && cell.gameObject) {
          this.drawGameObject(x, y, cellWidth, cellHeight, cell.gameObject, gridWidth, gridHeight, startX, startY);
        }
      });
    },

    drawSpawner(x, y, width, height, spawner, gridWidth, gridHeight, startX, startY) {
      const centerX = x + width / 2;
      const centerY = y + height / 2;

      // Apply morph to center point
      const morphedCenter = this.applyMorph(centerX, centerY, gridWidth, gridHeight, startX, startY);

      // Calculate morphed radius based on cell size at this position
      const topLeft = this.applyMorph(x, y, gridWidth, gridHeight, startX, startY);
      const bottomRight = this.applyMorph(x + width, y + height, gridWidth, gridHeight, startX, startY);
      const morphedWidth = Math.abs(bottomRight.x - topLeft.x);
      const morphedHeight = Math.abs(bottomRight.y - topLeft.y);
      const radius = Math.min(morphedWidth, morphedHeight) / 3;

      // Color based on spawner type
      const colors = {
        player: '#00ff00',
        npc: '#ff0000',
        object: '#ffff00',
        effect: '#ff00ff'
      };

      this.ctx.fillStyle = colors[spawner.type] || '#ffffff';
      this.ctx.beginPath();
      this.ctx.arc(morphedCenter.x, morphedCenter.y, radius, 0, Math.PI * 2);
      this.ctx.fill();

      // Draw type indicator
      this.ctx.fillStyle = '#000000';
      this.ctx.font = '12px Arial';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(spawner.type[0].toUpperCase(), morphedCenter.x, morphedCenter.y);
    },

    drawGameObject(x, y, width, height, gameObject, gridWidth, gridHeight, startX, startY) {
      const centerX = x + width / 2;
      const centerY = y + height / 2;

      // Apply morph to center point
      const morphedCenter = this.applyMorph(centerX, centerY, gridWidth, gridHeight, startX, startY);

      // Calculate morphed size based on cell size at this position
      const topLeft = this.applyMorph(x, y, gridWidth, gridHeight, startX, startY);
      const bottomRight = this.applyMorph(x + width, y + height, gridWidth, gridHeight, startX, startY);
      const morphedWidth = Math.abs(bottomRight.x - topLeft.x);
      const morphedHeight = Math.abs(bottomRight.y - topLeft.y);
      const size = Math.min(morphedWidth, morphedHeight) / 3;

      // Color based on object type
      const colors = {
        character: '#0088ff',
        item: '#ffaa00',
        chest: '#8800ff'
      };

      this.ctx.fillStyle = colors[gameObject.type] || '#ffffff';
      this.ctx.fillRect(morphedCenter.x - size / 2, morphedCenter.y - size / 2, size, size);

      // Draw type indicator
      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = '10px Arial';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(gameObject.type[0].toUpperCase(), morphedCenter.x, morphedCenter.y);
    },

    drawCellHighlight(cellX, cellY, color) {
      const scaledConfig = this.scaledGridConfig;
      if (!scaledConfig) return;

      const { cellWidth, cellHeight, columns, rows } = scaledConfig;

      // Position highlight relative to the image, not the canvas
      const imagePos = this.getImagePosition();
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = imagePos.x;
      const startY = imagePos.y;

      const x = startX + cellX * cellWidth;
      const y = startY + cellY * cellHeight;

      // Calculate the four corners of the cell with morph applied
      const topLeft = this.applyMorph(x, y, gridWidth, gridHeight, startX, startY);
      const topRight = this.applyMorph(x + cellWidth, y, gridWidth, gridHeight, startX, startY);
      const bottomLeft = this.applyMorph(x, y + cellHeight, gridWidth, gridHeight, startX, startY);
      const bottomRight = this.applyMorph(x + cellWidth, y + cellHeight, gridWidth, gridHeight, startX, startY);

      // Draw highlight as a morphed quad
      this.ctx.fillStyle = color;
      this.ctx.beginPath();
      this.ctx.moveTo(topLeft.x, topLeft.y);
      this.ctx.lineTo(topRight.x, topRight.y);
      this.ctx.lineTo(bottomRight.x, bottomRight.y);
      this.ctx.lineTo(bottomLeft.x, bottomLeft.y);
      this.ctx.closePath();
      this.ctx.fill();
    },

    getCellFromMousePosition(mouseX, mouseY) {
      const scaledConfig = this.scaledGridConfig;
      if (!scaledConfig) return null;

      // Apply inverse zoom transformation to mouse coordinates
      const centerX = this.canvasWidth / 2;
      const centerY = this.canvasHeight / 2;
      const zoomedMouseX = centerX + (mouseX - centerX) / this.zoom;
      const zoomedMouseY = centerY + (mouseY - centerY) / this.zoom;

      const { cellWidth, cellHeight, columns, rows } = scaledConfig;

      // Use image position as reference for grid, not canvas dimensions
      const imagePos = this.getImagePosition();
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = imagePos.x;
      const startY = imagePos.y;

      // Apply inverse morph to convert screen coordinates to grid coordinates
      const unmorphed = this.inverseMorph(zoomedMouseX, zoomedMouseY, gridWidth, gridHeight, startX, startY);

      const cellX = Math.floor((unmorphed.x - startX) / cellWidth);
      const cellY = Math.floor((unmorphed.y - startY) / cellHeight);

      if (cellX >= 0 && cellX < columns && cellY >= 0 && cellY < rows) {
        return { x: cellX, y: cellY };
      }

      return null;
    },

    // Toggle a movement edge between two neighboring cells (cardinal or diagonal)
    // by flipping the appropriate connection flags on both endpoints.
    toggleEdgeBetweenCells(from, to, layer) {
      const dx = to.x - from.x;
      const dy = to.y - from.y;

      // Only support immediate neighbors (including diagonals)
      if (Math.abs(dx) > 1 || Math.abs(dy) > 1 || (dx === 0 && dy === 0)) {
        return;
      }

      // Do not allow editing edges involving unavailable cells
      if (!this.gridConfig || !this.currentMap) return;

      const { columns, rows } = this.gridConfig;

      // Guard against off-grid coordinates
      if (
        from.x < 0 || from.y < 0 || from.x >= columns || from.y >= rows ||
        to.x < 0 || to.y < 0 || to.x >= columns || to.y >= rows
      ) {
        return;
      }

      const cells = this.currentMap.cells || [];
      const lookup = new Map();
      cells.forEach(cell => {
        lookup.set(`${cell.x},${cell.y},${cell.layer}`, cell);
      });

      const fromCell = lookup.get(`${from.x},${from.y},${layer}`);
      const toCell = lookup.get(`${to.x},${to.y},${layer}`);

      const fromAvailable = !fromCell || fromCell.available !== false;
      const toAvailable = !toCell || toCell.available !== false;

      if (!fromAvailable || !toAvailable) {
        // Cannot create or edit edges that involve unavailable cells
        return;
      }

      const toggleBidirectionalCardinal = (direction) => {
        const opposite = OPPOSITE_DIRECTION[direction];
        this.toggleCellConnection({ x: from.x, y: from.y, layer, direction });
        this.toggleCellConnection({ x: to.x, y: to.y, layer, direction: opposite });
      };

      const toggleBidirectionalDiagonal = (direction) => {
        const oppositeDiag = OPPOSITE_DIAGONAL_DIRECTION[direction];
        this.toggleCellConnection({ x: from.x, y: from.y, layer, direction });
        if (oppositeDiag) {
          this.toggleCellConnection({ x: to.x, y: to.y, layer, direction: oppositeDiag });
        }
      };

      // Cardinal neighbors
      if (dx === 1 && dy === 0) {
        toggleBidirectionalCardinal('east');
      } else if (dx === -1 && dy === 0) {
        toggleBidirectionalCardinal('west');
      } else if (dx === 0 && dy === 1) {
        toggleBidirectionalCardinal('south');
      } else if (dx === 0 && dy === -1) {
        toggleBidirectionalCardinal('north');
      } else if (dx === 1 && dy === -1) {
        // Diagonal neighbors
        toggleBidirectionalDiagonal('northEast');
      } else if (dx === -1 && dy === -1) {
        toggleBidirectionalDiagonal('northWest');
      } else if (dx === 1 && dy === 1) {
        toggleBidirectionalDiagonal('southEast');
      } else if (dx === -1 && dy === 1) {
        toggleBidirectionalDiagonal('southWest');
      }
    },

    handleMouseDown(event) {
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = event.clientX - rect.left;
      const mouseY = event.clientY - rect.top;

      // Middle mouse button (wheel press) - enter pan mode
      if (event.button === 1) {
        event.preventDefault();
        this.isPanning = true;
        this.panStartX = mouseX;
        this.panStartY = mouseY;
        this.panStartOffsetX = this.offsetX;
        this.panStartOffsetY = this.offsetY;
        this.canvas.style.cursor = 'grabbing';
        return;
      }

      // Left mouse button - normal cell interaction
      if (event.button === 0) {
        event.preventDefault(); // Prevent default drag behavior
        const cell = this.getCellFromMousePosition(mouseX, mouseY);
        if (!cell) return;

        this.isDragging = true;
        this.lastPaintedCell = { x: cell.x, y: cell.y };
        this.handleCellInteraction(cell.x, cell.y, null);
      }
    },

    handleMouseMove(event) {
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = event.clientX - rect.left;
      const mouseY = event.clientY - rect.top;

      // Handle pan mode
      if (this.isPanning) {
        const deltaX = mouseX - this.panStartX;
        const deltaY = mouseY - this.panStartY;
        this.offsetX = this.panStartOffsetX + deltaX;
        this.offsetY = this.panStartOffsetY + deltaY;
        this.render();
        return;
      }

      // Normal cell interaction mode
      const cell = this.getCellFromMousePosition(mouseX, mouseY);

      if (cell) {
        this.hoveredCell = cell;

        // Check if this is a different cell from the last painted one
        const isDifferentCell = !this.lastPaintedCell ||
                                this.lastPaintedCell.x !== cell.x ||
                                this.lastPaintedCell.y !== cell.y;

        // Brush mode: when Shift is pressed and dragging, continuously paint cells
        if (this.isDragging && this.isShiftPressed && isDifferentCell) {
          this.handleCellInteraction(cell.x, cell.y, this.lastPaintedCell);
          this.lastPaintedCell = { x: cell.x, y: cell.y };
        }
        // Legacy drag mode: only for availability and wall tools without Shift
        else if (this.isDragging && !this.isShiftPressed && (this.selectedTool === 'availability' || this.selectedTool === 'wall') && isDifferentCell) {
          this.handleCellInteraction(cell.x, cell.y, this.lastPaintedCell);
          this.lastPaintedCell = { x: cell.x, y: cell.y };
        }
      } else {
        this.hoveredCell = null;
      }

      this.render();
    },

    handleMouseUp(event) {
      // Exit pan mode if middle button was released
      if (this.isPanning && event.button === 1) {
        this.isPanning = false;
        this.canvas.style.cursor = 'crosshair';
      }

      this.isDragging = false;
      this.lastPaintedCell = null;
    },

    handleMouseLeave() {
      // Exit pan mode if active
      if (this.isPanning) {
        this.isPanning = false;
        this.canvas.style.cursor = 'crosshair';
      }

      this.isDragging = false;
      this.lastPaintedCell = null;
      this.hoveredCell = null;
      this.edgeStartCell = null;
      this.render();
    },

    handleCellInteraction(x, y, previousCell) {
      const layer = this.currentLayer;

      switch (this.selectedTool) {
        case 'select':
          this.selectCell({ x, y, layer });
          break;
        case 'availability':
          this.toggleCellAvailability({ x, y, layer });
          break;
        case 'wall':
          if (this.editorMode === 'path') {
            // In Path mode, the wall tool becomes the Path/Edge editor.
            // You can drag between neighboring cells or click one cell and
            // then a neighboring cell to toggle that specific edge.

            const current = { x, y };

            // Drag behavior: when previousCell is provided, toggle the edge
            // directly between previousCell and the current cell.
            if (previousCell) {
              this.toggleEdgeBetweenCells(previousCell, current, layer);
              break;
            }

            // Click behavior: first click selects the starting cell; second
            // click on a neighbor toggles the edge between them.
            if (!this.edgeStartCell) {
              this.edgeStartCell = { x, y, layer };
              this.selectCell({ x, y, layer });
              break;
            }

            // If the user clicks the same cell again, clear the start without
            // changing any edges.
            if (
              this.edgeStartCell.x === x &&
              this.edgeStartCell.y === y &&
              this.edgeStartCell.layer === layer
            ) {
              this.edgeStartCell = null;
              break;
            }

            const from = { x: this.edgeStartCell.x, y: this.edgeStartCell.y };
            const to = current;
            this.toggleEdgeBetweenCells(from, to, layer);
            this.edgeStartCell = null;
          } else {
            // Map/availability mode legacy behavior: toggle all walls of the cell
            this.toggleCellConnection({ x, y, layer, direction: 'north' });
            this.toggleCellConnection({ x, y, layer, direction: 'south' });
            this.toggleCellConnection({ x, y, layer, direction: 'east' });
            this.toggleCellConnection({ x, y, layer, direction: 'west' });
          }
          break;
        case 'erase':
          this.clearCellContent({ x, y, layer });
          break;
        case 'spawner-player':
          this.placeCellSpawner({ x, y, layer, spawner: { type: 'player', properties: {} } });
          break;
        case 'spawner-npc':
          this.placeCellSpawner({ x, y, layer, spawner: { type: 'npc', properties: {} } });
          break;
        case 'spawner-object':
          this.placeCellSpawner({ x, y, layer, spawner: { type: 'object', properties: {} } });
          break;
        case 'spawner-effect':
          this.placeCellSpawner({ x, y, layer, spawner: { type: 'effect', properties: {} } });
          break;
      }

      this.render();
    },

    handleKeyDown(event) {
      if (event.key === 'Shift' && !this.isShiftPressed) {
        this.isShiftPressed = true;
        if (this.canvas) {
          this.canvas.style.cursor = 'cell';
        }
      }
    },

    handleKeyUp(event) {
      if (event.key === 'Shift' && this.isShiftPressed) {
        this.isShiftPressed = false;
        if (this.canvas && !this.isPanning) {
          this.canvas.style.cursor = 'crosshair';
        }
      }
    }
  }
};
</script>

<style scoped>
.map-canvas-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #1a1a1a;
  position: relative;
}

.map-canvas {
  display: block;
  cursor: crosshair;
}

.map-canvas.brush-mode {
  cursor: cell;
}

/* Brush Mode Indicator */
.brush-mode-indicator {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 212, 255, 0.95);
  border: 2px solid #00d4ff;
  border-radius: 8px;
  padding: 10px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.5);
  z-index: 100;
  pointer-events: none;
  animation: pulse 1.5s ease-in-out infinite;
}

.indicator-icon {
  font-size: 24px;
  line-height: 1;
}

.indicator-text {
  font-size: 16px;
  font-weight: bold;
  color: #000;
  letter-spacing: 1px;
  text-transform: uppercase;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 4px 15px rgba(0, 212, 255, 0.5);
  }
  50% {
    box-shadow: 0 4px 25px rgba(0, 212, 255, 0.8);
  }
}

/* Zoom HUD */
.zoom-hud {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: rgba(20, 20, 30, 0.95);
  border: 2px solid rgba(0, 212, 255, 0.5);
  border-radius: 8px;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
  z-index: 100;
}

.zoom-btn {
  background: rgba(0, 212, 255, 0.2);
  border: 1px solid rgba(0, 212, 255, 0.5);
  border-radius: 4px;
  color: #00d4ff;
  font-size: 18px;
  font-weight: bold;
  width: 32px;
  height: 32px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.zoom-btn:hover:not(:disabled) {
  background: rgba(0, 212, 255, 0.4);
  border-color: rgba(0, 212, 255, 0.8);
  box-shadow: 0 0 8px rgba(0, 212, 255, 0.4);
  transform: scale(1.05);
}

.zoom-btn:active:not(:disabled) {
  transform: scale(0.95);
}

.zoom-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.zoom-reset {
  font-size: 16px;
  margin-left: 4px;
}

.zoom-display {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Courier New', monospace;
  min-width: 50px;
  text-align: center;
  user-select: none;
}
</style>
