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
    ></canvas>
    <!-- Brush Mode Indicator -->
    <div v-if="isShiftPressed" class="brush-mode-indicator">
      <span class="indicator-icon">🖌️</span>
      <span class="indicator-text">BRUSH MODE</span>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

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
      canvasWidth: 0,
      canvasHeight: 0,
      offsetX: 0,
      offsetY: 0,
      scale: 1.0,
      backgroundImage: null
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
      'currentLayerCells',
      'gridConfig',
      'getCurrentLayerMetadata'
    ])
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

      // Draw hovered cell highlight
      if (this.hoveredCell) {
        this.drawCellHighlight(this.hoveredCell.x, this.hoveredCell.y, 'rgba(255, 255, 0, 0.3)');
      }

      // Draw selected cell highlight
      if (this.selectedCell && this.selectedCell.layer === this.currentLayer) {
        this.drawCellHighlight(this.selectedCell.x, this.selectedCell.y, 'rgba(0, 255, 255, 0.5)');
      }
    },

    drawBackground() {
      if (!this.backgroundImage) return;

      const imgAspect = this.backgroundImage.width / this.backgroundImage.height;
      const canvasAspect = this.canvasWidth / this.canvasHeight;

      let drawWidth, drawHeight, drawX, drawY;

      if (imgAspect > canvasAspect) {
        drawHeight = this.canvasHeight;
        drawWidth = drawHeight * imgAspect;
        drawX = (this.canvasWidth - drawWidth) / 2 + this.offsetX;
        drawY = 0 + this.offsetY;
      } else {
        drawWidth = this.canvasWidth;
        drawHeight = drawWidth / imgAspect;
        drawX = 0 + this.offsetX;
        drawY = (this.canvasHeight - drawHeight) / 2 + this.offsetY;
      }

      this.ctx.globalAlpha = 0.5;
      this.ctx.drawImage(this.backgroundImage, drawX, drawY, drawWidth, drawHeight);
      this.ctx.globalAlpha = 1.0;
    },

    // Apply perspective morph transformation to a point
    // xMorph and yMorph range from -1.0 to 1.0
    // Positive xMorph: perspective vanishing to the right
    // Negative xMorph: perspective vanishing to the left
    // Positive yMorph: perspective vanishing to the bottom
    // Negative yMorph: perspective vanishing to the top
    applyMorph(x, y, gridWidth, gridHeight, startX, startY) {
      const { xMorph, yMorph } = this.gridConfig;

      // Calculate relative position within grid (0 to 1)
      const relX = (x - startX) / gridWidth;
      const relY = (y - startY) / gridHeight;

      // Apply perspective transformation
      // X morph: compress/expand based on Y position
      const xOffset = xMorph * gridWidth * 0.3 * (relY - 0.5);

      // Y morph: compress/expand based on X position
      const yOffset = yMorph * gridHeight * 0.3 * (relX - 0.5);

      return {
        x: x + xOffset,
        y: y + yOffset
      };
    },

    // Inverse morph transformation for mouse position to grid coordinates
    inverseMorph(screenX, screenY, gridWidth, gridHeight, startX, startY) {
      const { xMorph, yMorph } = this.gridConfig;

      // If no morph, return as-is
      if (Math.abs(xMorph) < 0.001 && Math.abs(yMorph) < 0.001) {
        return { x: screenX, y: screenY };
      }

      // Iterative approximation to find the unmorphed position
      let x = screenX;
      let y = screenY;

      // Newton's method iterations
      for (let i = 0; i < 5; i++) {
        const morphed = this.applyMorph(x, y, gridWidth, gridHeight, startX, startY);
        const errorX = morphed.x - screenX;
        const errorY = morphed.y - screenY;
        x -= errorX;
        y -= errorY;
      }

      return { x, y };
    },

    drawGrid() {
      const { cellWidth, cellHeight, columns, rows, xMorph, yMorph } = this.gridConfig;

      // Calculate grid offset to center it
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

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
      if (!this.currentLayerCells || !this.gridConfig) return;

      const { cellWidth, cellHeight, columns, rows } = this.gridConfig;
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

      this.currentLayerCells.forEach(cell => {
        const x = startX + cell.x * cellWidth;
        const y = startY + cell.y * cellHeight;

        // Calculate the four corners of the cell with morph applied
        const topLeft = this.applyMorph(x, y, gridWidth, gridHeight, startX, startY);
        const topRight = this.applyMorph(x + cellWidth, y, gridWidth, gridHeight, startX, startY);
        const bottomLeft = this.applyMorph(x, y + cellHeight, gridWidth, gridHeight, startX, startY);
        const bottomRight = this.applyMorph(x + cellWidth, y + cellHeight, gridWidth, gridHeight, startX, startY);

        // Draw unavailable cells as a morphed quad
        if (!cell.available) {
          this.ctx.fillStyle = 'rgba(255, 0, 0, 0.3)';
          this.ctx.beginPath();
          this.ctx.moveTo(topLeft.x, topLeft.y);
          this.ctx.lineTo(topRight.x, topRight.y);
          this.ctx.lineTo(bottomRight.x, bottomRight.y);
          this.ctx.lineTo(bottomLeft.x, bottomLeft.y);
          this.ctx.closePath();
          this.ctx.fill();
        }

        // Draw walls (blocked connections) with morph
        this.ctx.strokeStyle = 'rgba(255, 0, 0, 0.8)';
        this.ctx.lineWidth = 3;

        if (!cell.connections.north) {
          this.ctx.beginPath();
          this.ctx.moveTo(topLeft.x, topLeft.y);
          this.ctx.lineTo(topRight.x, topRight.y);
          this.ctx.stroke();
        }
        if (!cell.connections.south) {
          this.ctx.beginPath();
          this.ctx.moveTo(bottomLeft.x, bottomLeft.y);
          this.ctx.lineTo(bottomRight.x, bottomRight.y);
          this.ctx.stroke();
        }
        if (!cell.connections.west) {
          this.ctx.beginPath();
          this.ctx.moveTo(topLeft.x, topLeft.y);
          this.ctx.lineTo(bottomLeft.x, bottomLeft.y);
          this.ctx.stroke();
        }
        if (!cell.connections.east) {
          this.ctx.beginPath();
          this.ctx.moveTo(topRight.x, topRight.y);
          this.ctx.lineTo(bottomRight.x, bottomRight.y);
          this.ctx.stroke();
        }

        // Draw spawners with morph
        if (cell.spawner) {
          this.drawSpawner(x, y, cellWidth, cellHeight, cell.spawner, gridWidth, gridHeight, startX, startY);
        }

        // Draw game objects with morph
        if (cell.gameObject) {
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
      if (!this.gridConfig) return;

      const { cellWidth, cellHeight, columns, rows } = this.gridConfig;
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

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
      if (!this.gridConfig) return null;

      const { cellWidth, cellHeight, columns, rows } = this.gridConfig;
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

      // Apply inverse morph to convert screen coordinates to grid coordinates
      const unmorphed = this.inverseMorph(mouseX, mouseY, gridWidth, gridHeight, startX, startY);

      const cellX = Math.floor((unmorphed.x - startX) / cellWidth);
      const cellY = Math.floor((unmorphed.y - startY) / cellHeight);

      if (cellX >= 0 && cellX < columns && cellY >= 0 && cellY < rows) {
        return { x: cellX, y: cellY };
      }

      return null;
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
        this.handleCellInteraction(cell.x, cell.y);
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
          this.handleCellInteraction(cell.x, cell.y);
          this.lastPaintedCell = { x: cell.x, y: cell.y };
        }
        // Legacy drag mode: only for availability and wall tools without Shift
        else if (this.isDragging && !this.isShiftPressed && (this.selectedTool === 'availability' || this.selectedTool === 'wall') && isDifferentCell) {
          this.handleCellInteraction(cell.x, cell.y);
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
      this.render();
    },

    handleCellInteraction(x, y) {
      const layer = this.currentLayer;

      switch (this.selectedTool) {
        case 'select':
          this.selectCell({ x, y, layer });
          break;
        case 'availability':
          this.toggleCellAvailability({ x, y, layer });
          break;
        case 'wall':
          // Toggle all connections for the cell (block/unblock all walls)
          this.toggleCellConnection({ x, y, layer, direction: 'north' });
          this.toggleCellConnection({ x, y, layer, direction: 'south' });
          this.toggleCellConnection({ x, y, layer, direction: 'east' });
          this.toggleCellConnection({ x, y, layer, direction: 'west' });
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
</style>
