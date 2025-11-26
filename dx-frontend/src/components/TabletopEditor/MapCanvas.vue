<template>
  <div class="map-canvas-container">
    <canvas
      ref="canvas"
      class="map-canvas"
      @mousedown="handleMouseDown"
      @mousemove="handleMouseMove"
      @mouseup="handleMouseUp"
      @mouseleave="handleMouseLeave"
    ></canvas>
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
      panStartX: 0,
      panStartY: 0,
      panStartOffsetX: 0,
      panStartOffsetY: 0,
      hoveredCell: null,
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
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
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

    drawGrid() {
      const { cellWidth, cellHeight, columns, rows, xMorph, yMorph } = this.gridConfig;

      // Calculate grid offset to center it
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

      this.ctx.strokeStyle = 'rgba(100, 100, 100, 0.5)';
      this.ctx.lineWidth = 1;

      // Draw vertical lines
      for (let col = 0; col <= columns; col++) {
        const x = startX + col * cellWidth;
        this.ctx.beginPath();
        this.ctx.moveTo(x, startY);
        this.ctx.lineTo(x, startY + gridHeight);
        this.ctx.stroke();
      }

      // Draw horizontal lines
      for (let row = 0; row <= rows; row++) {
        const y = startY + row * cellHeight;
        this.ctx.beginPath();
        this.ctx.moveTo(startX, y);
        this.ctx.lineTo(startX + gridWidth, y);
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

        // Draw unavailable cells
        if (!cell.available) {
          this.ctx.fillStyle = 'rgba(255, 0, 0, 0.3)';
          this.ctx.fillRect(x, y, cellWidth, cellHeight);
        }

        // Draw walls (blocked connections)
        this.ctx.strokeStyle = 'rgba(255, 0, 0, 0.8)';
        this.ctx.lineWidth = 3;

        if (!cell.connections.north) {
          this.ctx.beginPath();
          this.ctx.moveTo(x, y);
          this.ctx.lineTo(x + cellWidth, y);
          this.ctx.stroke();
        }
        if (!cell.connections.south) {
          this.ctx.beginPath();
          this.ctx.moveTo(x, y + cellHeight);
          this.ctx.lineTo(x + cellWidth, y + cellHeight);
          this.ctx.stroke();
        }
        if (!cell.connections.west) {
          this.ctx.beginPath();
          this.ctx.moveTo(x, y);
          this.ctx.lineTo(x, y + cellHeight);
          this.ctx.stroke();
        }
        if (!cell.connections.east) {
          this.ctx.beginPath();
          this.ctx.moveTo(x + cellWidth, y);
          this.ctx.lineTo(x + cellWidth, y + cellHeight);
          this.ctx.stroke();
        }

        // Draw spawners
        if (cell.spawner) {
          this.drawSpawner(x, y, cellWidth, cellHeight, cell.spawner);
        }

        // Draw game objects
        if (cell.gameObject) {
          this.drawGameObject(x, y, cellWidth, cellHeight, cell.gameObject);
        }
      });
    },

    drawSpawner(x, y, width, height, spawner) {
      const centerX = x + width / 2;
      const centerY = y + height / 2;
      const radius = Math.min(width, height) / 3;

      // Color based on spawner type
      const colors = {
        player: '#00ff00',
        npc: '#ff0000',
        object: '#ffff00',
        effect: '#ff00ff'
      };

      this.ctx.fillStyle = colors[spawner.type] || '#ffffff';
      this.ctx.beginPath();
      this.ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      this.ctx.fill();

      // Draw type indicator
      this.ctx.fillStyle = '#000000';
      this.ctx.font = '12px Arial';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(spawner.type[0].toUpperCase(), centerX, centerY);
    },

    drawGameObject(x, y, width, height, gameObject) {
      const centerX = x + width / 2;
      const centerY = y + height / 2;
      const size = Math.min(width, height) / 3;

      // Color based on object type
      const colors = {
        character: '#0088ff',
        item: '#ffaa00',
        chest: '#8800ff'
      };

      this.ctx.fillStyle = colors[gameObject.type] || '#ffffff';
      this.ctx.fillRect(centerX - size / 2, centerY - size / 2, size, size);

      // Draw type indicator
      this.ctx.fillStyle = '#ffffff';
      this.ctx.font = '10px Arial';
      this.ctx.textAlign = 'center';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(gameObject.type[0].toUpperCase(), centerX, centerY);
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

      this.ctx.fillStyle = color;
      this.ctx.fillRect(x, y, cellWidth, cellHeight);
    },

    getCellFromMousePosition(mouseX, mouseY) {
      if (!this.gridConfig) return null;

      const { cellWidth, cellHeight, columns, rows } = this.gridConfig;
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

      const cellX = Math.floor((mouseX - startX) / cellWidth);
      const cellY = Math.floor((mouseY - startY) / cellHeight);

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
      const cell = this.getCellFromMousePosition(mouseX, mouseY);
      if (!cell) return;

      this.isDragging = true;
      this.handleCellInteraction(cell.x, cell.y);
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
        if (this.isDragging && (this.selectedTool === 'availability' || this.selectedTool === 'wall')) {
          this.handleCellInteraction(cell.x, cell.y);
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
    },

    handleMouseLeave() {
      // Exit pan mode if active
      if (this.isPanning) {
        this.isPanning = false;
        this.canvas.style.cursor = 'crosshair';
      }

      this.isDragging = false;
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
}

.map-canvas {
  display: block;
  cursor: crosshair;
}
</style>
