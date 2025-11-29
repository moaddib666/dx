<template>
  <div class="player-canvas-container">
    <canvas
      ref="canvas"
      class="player-canvas"
      @mousedown="handleMouseDown"
      @mousemove="handleMouseMove"
      @mouseleave="handleMouseLeave"
    ></canvas>

    <!-- Character Tokens Overlay -->
    <div class="tokens-overlay">
      <div
        v-for="player in players"
        :key="player.id"
        class="token-wrapper"
        :class="{ 'token-selected': selectedPlayer && selectedPlayer.id === player.id }"
        :style="getTokenStyle(player)"
        @click="handleTokenClick(player.id)"
      >
        <CharacterToken :image="player.image" />
      </div>
    </div>

    <!-- Coordinate Display -->
    <div v-if="hoveredCell" class="coordinate-display">
      <span class="coord-label">Position:</span>
      <span class="coord-value">X: {{ hoveredCell.x }}, Y: {{ hoveredCell.y }}</span>
      <span class="coord-layer">Layer: {{ hoveredCell.layer }}</span>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import { TERRAIN_CONFIGS } from '@/types/tabletop';
import CharacterToken from '@/components/CharacterToken/CharacterToken.vue';

export default {
  name: 'PlayerCanvas',
  components: {
    CharacterToken
  },
  data() {
    return {
      canvas: null,
      ctx: null,
      hoveredCell: null,
      canvasWidth: 0,
      canvasHeight: 0,
      offsetX: 0,
      offsetY: 0,
      backgroundImage: null,
      // Pathfinding cache
      reachableCells: new Map(), // Map of "x,y,layer" -> { x, y, layer, cost, path }
      pathToHovered: null,
      // Animation state
      isAnimating: false,
      animationPlayerId: null,
      animationPath: null,
      animationCurrentStep: 0,
      animationProgress: 0 // 0 to 1, progress within current step
    };
  },
  computed: {
    ...mapGetters('tabletopPlayer', [
      'currentMap',
      'players',
      'selectedPlayer',
      'currentLayer',
      'gridVisible',
      'backgroundVisible',
      'gridConfig'
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
    players: {
      handler() {
        this.render();
      },
      deep: true
    },
    selectedPlayer: {
      handler() {
        this.calculateReachableCells();
        this.render();
      },
      deep: true
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
    ...mapActions('tabletopPlayer', [
      'selectPlayer',
      'movePlayer'
    ]),

    initCanvas() {
      this.canvas = this.$refs.canvas;
      this.ctx = this.canvas.getContext('2d');
      this.handleResize();
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

    // Dijkstra pathfinding to calculate all reachable cells from selected player
    calculateReachableCells() {
      this.reachableCells.clear();

      if (!this.selectedPlayer || !this.currentMap || !this.gridConfig) {
        console.log('[Calculate] Early return - selectedPlayer:', !!this.selectedPlayer, 'currentMap:', !!this.currentMap, 'gridConfig:', !!this.gridConfig);
        return;
      }

      const startX = this.selectedPlayer.x;
      const startY = this.selectedPlayer.y;
      const startLayer = this.selectedPlayer.layer;
      const maxCost = this.selectedPlayer.currentActionPoints;

      console.log(`[Calculate] Starting pathfinding from (${startX}, ${startY}, layer ${startLayer}) with ${maxCost} action points`);
      console.log('[Calculate] Map has', this.currentMap.edges?.length || 0, 'edges total');

      // Priority queue: [cost, x, y, layer, path]
      const queue = [[0, startX, startY, startLayer, []]];
      const visited = new Set();

      while (queue.length > 0) {
        // Sort by cost (simple priority queue)
        queue.sort((a, b) => a[0] - b[0]);
        const [cost, x, y, layer, path] = queue.shift();

        const key = `${x},${y},${layer}`;
        if (visited.has(key)) continue;
        visited.add(key);

        // Store reachable cell with its cost and path
        this.reachableCells.set(key, { x, y, layer, cost, path: [...path, { x, y, layer }] });

        // Don't expand if we've reached max cost
        if (cost >= maxCost) continue;

        // Get all valid edges from this cell
        const edges = this.getEdgesFromCell(x, y, layer);

        edges.forEach(edge => {
          const toKey = `${edge.toX},${edge.toY},${edge.toLayer}`;
          if (visited.has(toKey)) return;

          // Calculate movement cost
          const cellCost = this.getCellMovementCost(edge.toX, edge.toY, edge.toLayer);
          const newCost = cost + cellCost;

          if (newCost <= maxCost) {
            queue.push([newCost, edge.toX, edge.toY, edge.toLayer, [...path, { x, y, layer }]]);
          }
        });
      }

      console.log(`[Calculate] ✅ Pathfinding complete! Found ${this.reachableCells.size} reachable cells`);
      if (this.reachableCells.size <= 1) {
        console.warn('[Calculate] ⚠️ Only starting cell found - no movement possible!');
      }
    },

    // Get all valid (non-blocked) edges from a cell
    getEdgesFromCell(x, y, layer) {
      if (!this.currentMap || !this.currentMap.edges) {
        console.log(`[GetEdges] No map or edges array for (${x}, ${y}, ${layer})`);
        return [];
      }

      const edges = this.currentMap.edges.filter(edge =>
        edge && edge.id &&
        edge.id.fromX === x &&
        edge.id.fromY === y &&
        edge.id.layer === layer &&
        !edge.blocked
      ).map(edge => ({
        toX: edge.id.toX,
        toY: edge.id.toY,
        toLayer: edge.id.layer
      }));

      console.log(`[GetEdges] From (${x}, ${y}, ${layer}): found ${edges.length} edges`);
      return edges;
    },

    // Get movement cost for a cell based on terrain
    getCellMovementCost(x, y, layer) {
      if (!this.currentMap || !this.currentMap.cells) return 1;

      const cell = this.currentMap.cells.find(c =>
        c.x === x && c.y === y && c.layer === layer
      );

      if (!cell) return 1; // Default grass cost

      const terrainConfig = TERRAIN_CONFIGS[cell.terrain];
      return terrainConfig ? terrainConfig.movementCost : 1;
    },

    render() {
      if (!this.ctx || !this.currentMap) return;

      // Clear canvas
      this.ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

      // Draw background
      if (this.backgroundVisible && this.backgroundImage) {
        this.drawBackground();
      } else {
        this.ctx.fillStyle = '#1a1a1a';
        this.ctx.fillRect(0, 0, this.canvasWidth, this.canvasHeight);
      }

      // Draw movement area shadows for selected player
      if (this.selectedPlayer) {
        this.drawMovementArea();
      }

      // Draw grid (only for reachable cells if player is selected)
      if (this.gridVisible && this.gridConfig) {
        this.drawGrid();
      }

      // Draw path to hovered cell
      if (this.pathToHovered && this.pathToHovered.length > 0) {
        this.drawPath(this.pathToHovered);
      }

      // Draw hovered cell shadow
      if (this.hoveredCell) {
        this.drawCellShadow(this.hoveredCell.x, this.hoveredCell.y);
      }

      // Players are now rendered as DOM elements via CharacterToken components
      // (see tokens-overlay in template)
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

    drawMovementArea() {
      console.log(`[DrawMovement] Called - gridConfig: ${!!this.gridConfig}, reachableCells.size: ${this.reachableCells.size}`);

      if (!this.gridConfig || this.reachableCells.size === 0) {
        console.warn('[DrawMovement] ⚠️ Returning early - no grid config or no reachable cells');
        return;
      }

      console.log('[DrawMovement] Drawing movement area for', this.reachableCells.size, 'cells');
      const { cellWidth, cellHeight, columns, rows } = this.gridConfig;
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

      // Check if only starting cell is reachable (no movement possible)
      const hasMovementOptions = this.reachableCells.size > 1;

      this.reachableCells.forEach((cellInfo, key) => {
        const x = startX + cellInfo.x * cellWidth;
        const y = startY + cellInfo.y * cellHeight;

        const topLeft = this.applyMorph(x, y, gridWidth, gridHeight, startX, startY);
        const topRight = this.applyMorph(x + cellWidth, y, gridWidth, gridHeight, startX, startY);
        const bottomLeft = this.applyMorph(x, y + cellHeight, gridWidth, gridHeight, startX, startY);
        const bottomRight = this.applyMorph(x + cellWidth, y + cellHeight, gridWidth, gridHeight, startX, startY);

        // If this is the starting cell (cost === 0)
        if (cellInfo.cost === 0) {
          // Only draw starting cell if there are NO other reachable cells (no movement possible)
          if (!hasMovementOptions) {
            // Cyberpunk style: ultra-lightweight semi-transparent background with subtle glowing border
            this.ctx.fillStyle = 'rgba(255, 100, 0, 0.06)';
            this.ctx.beginPath();
            this.ctx.moveTo(topLeft.x, topLeft.y);
            this.ctx.lineTo(topRight.x, topRight.y);
            this.ctx.lineTo(bottomRight.x, bottomRight.y);
            this.ctx.lineTo(bottomLeft.x, bottomLeft.y);
            this.ctx.closePath();
            this.ctx.fill();

            // Subtle glowing border (cyberpunk style)
            this.ctx.strokeStyle = 'rgba(255, 150, 50, 0.5)';
            this.ctx.lineWidth = 1.5;
            this.ctx.shadowBlur = 4;
            this.ctx.shadowColor = 'rgba(255, 150, 50, 0.3)';
            this.ctx.stroke();
            this.ctx.shadowBlur = 0;

            console.warn('[DrawMovement] ⚠️ Player selected but has NO movement options! Check map edges.');
          }
          return; // Skip starting cell for normal movement area
        }

        // Cyberpunk style: ultra-lightweight semi-transparent background with subtle glowing cyan border
        this.ctx.fillStyle = 'rgba(6, 14, 24, 0.12)';
        this.ctx.beginPath();
        this.ctx.moveTo(topLeft.x, topLeft.y);
        this.ctx.lineTo(topRight.x, topRight.y);
        this.ctx.lineTo(bottomRight.x, bottomRight.y);
        this.ctx.lineTo(bottomLeft.x, bottomLeft.y);
        this.ctx.closePath();
        this.ctx.fill();

        // Subtle glowing cyan border for reachable cells
        this.ctx.strokeStyle = 'rgba(99, 247, 255, 0.45)';
        this.ctx.lineWidth = 1.5;
        this.ctx.shadowBlur = 4;
        this.ctx.shadowColor = 'rgba(34, 211, 238, 0.25)';
        this.ctx.stroke();
        this.ctx.shadowBlur = 0;
      });
    },

    drawGrid() {
      const { cellWidth, cellHeight, columns, rows } = this.gridConfig;
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

      this.ctx.strokeStyle = 'rgba(100, 100, 150, 0.3)';
      this.ctx.lineWidth = 1;

      // Draw grid only for passable cells
      for (let row = 0; row < rows; row++) {
        for (let col = 0; col < columns; col++) {
          // Check if this cell is passable
          if (this.isCellPassable(col, row)) {
            const x = startX + col * cellWidth;
            const y = startY + row * cellHeight;

            const topLeft = this.applyMorph(x, y, gridWidth, gridHeight, startX, startY);
            const topRight = this.applyMorph(x + cellWidth, y, gridWidth, gridHeight, startX, startY);
            const bottomLeft = this.applyMorph(x, y + cellHeight, gridWidth, gridHeight, startX, startY);
            const bottomRight = this.applyMorph(x + cellWidth, y + cellHeight, gridWidth, gridHeight, startX, startY);

            this.ctx.beginPath();
            this.ctx.moveTo(topLeft.x, topLeft.y);
            this.ctx.lineTo(topRight.x, topRight.y);
            this.ctx.lineTo(bottomRight.x, bottomRight.y);
            this.ctx.lineTo(bottomLeft.x, bottomLeft.y);
            this.ctx.closePath();
            this.ctx.stroke();
          }
        }
      }
    },

    isCellPassable(x, y) {
      if (!this.currentMap || !this.currentMap.cells) return true; // Default to passable

      const cell = this.currentMap.cells.find(c =>
        c.x === x && c.y === y && c.layer === this.currentLayer
      );

      // If cell doesn't exist in the cells array, it's passable by default
      // If cell exists, check its passable property (default to true if not explicitly false)
      return !cell || cell.passable !== false;
    },

    drawPath(path) {
      if (!this.gridConfig || path.length < 2) return;

      const { cellWidth, cellHeight, columns, rows } = this.gridConfig;
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

      // First, highlight individual cells along the path
      path.forEach((cell, index) => {
        if (index === 0) return; // Skip starting cell (player's current position)

        const x = startX + cell.x * cellWidth;
        const y = startY + cell.y * cellHeight;

        const topLeft = this.applyMorph(x, y, gridWidth, gridHeight, startX, startY);
        const topRight = this.applyMorph(x + cellWidth, y, gridWidth, gridHeight, startX, startY);
        const bottomLeft = this.applyMorph(x, y + cellHeight, gridWidth, gridHeight, startX, startY);
        const bottomRight = this.applyMorph(x + cellWidth, y + cellHeight, gridWidth, gridHeight, startX, startY);

        // Cyberpunk style: ultra-lightweight semi-transparent background for path cells
        this.ctx.fillStyle = 'rgba(255, 200, 0, 0.05)';
        this.ctx.beginPath();
        this.ctx.moveTo(topLeft.x, topLeft.y);
        this.ctx.lineTo(topRight.x, topRight.y);
        this.ctx.lineTo(bottomRight.x, bottomRight.y);
        this.ctx.lineTo(bottomLeft.x, bottomLeft.y);
        this.ctx.closePath();
        this.ctx.fill();

        // Subtle glowing yellow border for path cells
        this.ctx.strokeStyle = 'rgba(255, 220, 100, 0.55)';
        this.ctx.lineWidth = 1.5;
        this.ctx.shadowBlur = 5;
        this.ctx.shadowColor = 'rgba(255, 220, 100, 0.3)';
        this.ctx.stroke();
        this.ctx.shadowBlur = 0;
      });

      // Then, draw the connecting line through cell centers with subtle cyberpunk glow
      this.ctx.strokeStyle = 'rgba(255, 220, 100, 0.6)';
      this.ctx.lineWidth = 2;
      this.ctx.setLineDash([8, 4]);
      this.ctx.shadowBlur = 6;
      this.ctx.shadowColor = 'rgba(255, 220, 100, 0.4)';

      this.ctx.beginPath();
      path.forEach((cell, index) => {
        const centerX = startX + cell.x * cellWidth + cellWidth / 2;
        const centerY = startY + cell.y * cellHeight + cellHeight / 2;
        const point = this.applyMorph(centerX, centerY, gridWidth, gridHeight, startX, startY);

        if (index === 0) {
          this.ctx.moveTo(point.x, point.y);
        } else {
          this.ctx.lineTo(point.x, point.y);
        }
      });
      this.ctx.stroke();
      this.ctx.setLineDash([]);
      this.ctx.shadowBlur = 0;
    },

    drawCellShadow(x, y) {
      if (!this.gridConfig) return;

      const { cellWidth, cellHeight, columns, rows } = this.gridConfig;
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

      const cellX = startX + x * cellWidth;
      const cellY = startY + y * cellHeight;

      const topLeft = this.applyMorph(cellX, cellY, gridWidth, gridHeight, startX, startY);
      const topRight = this.applyMorph(cellX + cellWidth, cellY, gridWidth, gridHeight, startX, startY);
      const bottomLeft = this.applyMorph(cellX, cellY + cellHeight, gridWidth, gridHeight, startX, startY);
      const bottomRight = this.applyMorph(cellX + cellWidth, cellY + cellHeight, gridWidth, gridHeight, startX, startY);

      // Cyberpunk style: ultra-lightweight semi-transparent background with subtle glowing border for hover
      this.ctx.fillStyle = 'rgba(99, 247, 255, 0.04)';
      this.ctx.beginPath();
      this.ctx.moveTo(topLeft.x, topLeft.y);
      this.ctx.lineTo(topRight.x, topRight.y);
      this.ctx.lineTo(bottomRight.x, bottomRight.y);
      this.ctx.lineTo(bottomLeft.x, bottomLeft.y);
      this.ctx.closePath();
      this.ctx.fill();

      // Subtle glowing cyan border for hover
      this.ctx.strokeStyle = 'rgba(99, 247, 255, 0.4)';
      this.ctx.lineWidth = 1.5;
      this.ctx.shadowBlur = 6;
      this.ctx.shadowColor = 'rgba(34, 211, 238, 0.35)';
      this.ctx.stroke();
      this.ctx.shadowBlur = 0;
    },

    // DEPRECATED: Players are now rendered as DOM elements using CharacterToken components
    // See tokens-overlay in template and getTokenStyle method
    /*
    drawPlayers() {
      if (!this.gridConfig || !this.players) return;

      const { cellWidth, cellHeight, columns, rows } = this.gridConfig;
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

      this.players.forEach(player => {
        const centerX = startX + player.x * cellWidth + cellWidth / 2;
        const centerY = startY + player.y * cellHeight + cellHeight / 2;
        const point = this.applyMorph(centerX, centerY, gridWidth, gridHeight, startX, startY);

        // Draw player token circle
        const radius = Math.min(cellWidth, cellHeight) / 3;

        // Highlight selected player
        if (this.selectedPlayer && this.selectedPlayer.id === player.id) {
          this.ctx.strokeStyle = 'rgba(255, 255, 0, 0.8)';
          this.ctx.lineWidth = 3;
          this.ctx.beginPath();
          this.ctx.arc(point.x, point.y, radius + 5, 0, Math.PI * 2);
          this.ctx.stroke();
        }

        // Draw player circle
        this.ctx.fillStyle = '#4682B4';
        this.ctx.strokeStyle = '#000';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(point.x, point.y, radius, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.stroke();

        // Draw player name
        this.ctx.fillStyle = '#fff';
        this.ctx.font = '12px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(player.name.substring(0, 3), point.x, point.y);

        // Draw action points
        this.ctx.fillStyle = '#ffff00';
        this.ctx.font = '10px Arial';
        this.ctx.fillText(`${player.currentActionPoints}/${player.maxActionPoints}`, point.x, point.y + radius + 12);
      });
    },
    */

    getCellFromMouse(mouseX, mouseY) {
      if (!this.gridConfig) return null;

      const { cellWidth, cellHeight, columns, rows } = this.gridConfig;
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

      const unmorphed = this.inverseMorph(mouseX, mouseY, gridWidth, gridHeight, startX, startY);
      const x = Math.floor((unmorphed.x - startX) / cellWidth);
      const y = Math.floor((unmorphed.y - startY) / cellHeight);

      if (x >= 0 && x < columns && y >= 0 && y < rows) {
        return { x, y, layer: this.currentLayer };
      }

      return null;
    },

    handleMouseDown(event) {
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = event.clientX - rect.left;
      const mouseY = event.clientY - rect.top;

      const cell = this.getCellFromMouse(mouseX, mouseY);
      if (!cell) return;

      // Don't allow new actions during animation
      if (this.isAnimating) return;

      // Check if clicking on a player
      const clickedPlayer = this.players.find(p =>
        p.x === cell.x && p.y === cell.y && p.layer === cell.layer
      );

      if (clickedPlayer) {
        // Select the player
        this.selectPlayer(clickedPlayer.id);
      } else if (this.selectedPlayer) {
        // Try to move selected player to this cell
        const key = `${cell.x},${cell.y},${cell.layer}`;
        const reachableCell = this.reachableCells.get(key);

        if (reachableCell) {
          // Animate movement along the path
          this.animateMovement(
            this.selectedPlayer.id,
            reachableCell.path,
            cell.x,
            cell.y,
            cell.layer,
            reachableCell.cost
          );
        }
      }
    },

    handleMouseMove(event) {
      const rect = this.canvas.getBoundingClientRect();
      const mouseX = event.clientX - rect.left;
      const mouseY = event.clientY - rect.top;

      const cell = this.getCellFromMouse(mouseX, mouseY);

      if (cell) {
        this.hoveredCell = cell;

        // Calculate path to hovered cell if it's reachable
        if (this.selectedPlayer) {
          const key = `${cell.x},${cell.y},${cell.layer}`;
          const reachableCell = this.reachableCells.get(key);

          if (reachableCell) {
            this.pathToHovered = reachableCell.path;
          } else {
            this.pathToHovered = null;
          }
        }
      } else {
        this.hoveredCell = null;
        this.pathToHovered = null;
      }

      this.render();
    },

    handleMouseLeave() {
      this.hoveredCell = null;
      this.pathToHovered = null;
      this.render();
    },

    // Calculate token position with morph transformation applied
    getTokenStyle(player) {
      if (!this.gridConfig) return { display: 'none' };

      const { cellWidth, cellHeight, columns, rows } = this.gridConfig;
      const gridWidth = columns * cellWidth;
      const gridHeight = rows * cellHeight;
      const startX = (this.canvasWidth - gridWidth) / 2 + this.offsetX;
      const startY = (this.canvasHeight - gridHeight) / 2 + this.offsetY;

      let playerX = player.x;
      let playerY = player.y;

      // If this player is being animated, use interpolated position
      if (this.isAnimating && this.animationPlayerId === player.id && this.animationPath) {
        const currentStepIndex = this.animationCurrentStep;
        const nextStepIndex = currentStepIndex + 1;

        if (nextStepIndex < this.animationPath.length) {
          const currentCell = this.animationPath[currentStepIndex];
          const nextCell = this.animationPath[nextStepIndex];

          // Interpolate between current and next cell
          playerX = currentCell.x + (nextCell.x - currentCell.x) * this.animationProgress;
          playerY = currentCell.y + (nextCell.y - currentCell.y) * this.animationProgress;
        } else {
          // Animation complete, use final position
          const finalCell = this.animationPath[this.animationPath.length - 1];
          playerX = finalCell.x;
          playerY = finalCell.y;
        }
      }

      // Calculate center of the cell
      const centerX = startX + playerX * cellWidth + cellWidth / 2;
      const centerY = startY + playerY * cellHeight + cellHeight / 2;

      // Apply morph transformation
      const morphedPoint = this.applyMorph(centerX, centerY, gridWidth, gridHeight, startX, startY);

      // Token size - use the smaller dimension to ensure it fits in the cell
      const tokenSize = Math.min(cellWidth, cellHeight);

      return {
        position: 'absolute',
        left: `${morphedPoint.x}px`,
        top: `${morphedPoint.y}px`,
        width: `${tokenSize}px`,
        height: `${tokenSize}px`,
        transform: 'translate(-50%, -50%)',
        pointerEvents: 'auto',
        cursor: 'pointer',
        transition: this.isAnimating && this.animationPlayerId === player.id ? 'none' : 'all 0.3s ease'
      };
    },

    // Handle clicking on a token
    handleTokenClick(playerId) {
      this.selectPlayer(playerId);
    },

    // Easing function for smooth animation (ease-in-out)
    easeInOutQuad(t) {
      return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    },

    // Animate smooth movement along a path
    animateMovement(playerId, path, destinationX, destinationY, destinationLayer, movementCost) {
      if (!path || path.length < 2) {
        // No path or too short, just move instantly
        this.movePlayer({
          playerId,
          x: destinationX,
          y: destinationY,
          layer: destinationLayer,
          cost: movementCost
        });
        return;
      }

      // Set up animation state
      this.isAnimating = true;
      this.animationPlayerId = playerId;
      this.animationPath = path;
      this.animationCurrentStep = 0;
      this.animationProgress = 0;

      const stepDuration = 250; // milliseconds per cell (slightly faster for smoother feel)
      let lastTimestamp = performance.now();

      const animate = (timestamp) => {
        if (!this.isAnimating) return; // Animation was cancelled

        const deltaTime = timestamp - lastTimestamp;
        lastTimestamp = timestamp;

        // Update progress within current step
        const rawProgress = this.animationProgress + deltaTime / stepDuration;

        if (rawProgress >= 1.0) {
          // Move to next step
          this.animationCurrentStep++;
          this.animationProgress = 0;

          // Check if we've reached the end of the path
          if (this.animationCurrentStep >= this.animationPath.length - 1) {
            // Animation complete
            this.isAnimating = false;
            this.animationPlayerId = null;
            this.animationPath = null;
            this.animationCurrentStep = 0;
            this.animationProgress = 0;

            // Update player position in Vuex store
            this.movePlayer({
              playerId,
              x: destinationX,
              y: destinationY,
              layer: destinationLayer,
              cost: movementCost
            });

            // Re-render to show final position
            this.render();
            return;
          }
        } else {
          // Apply easing to progress for smoother movement
          this.animationProgress = rawProgress;
        }

        // Trigger re-render to update token position
        this.$forceUpdate();

        // Continue animation
        requestAnimationFrame(animate);
      };

      // Start animation loop
      requestAnimationFrame(animate);
    }
  }
};
</script>

<style scoped>
.player-canvas-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.player-canvas {
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.coordinate-display {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(20, 20, 30, 0.9);
  border: 2px solid rgba(0, 212, 255, 0.5);
  border-radius: 6px;
  padding: 8px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  pointer-events: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.coord-label {
  font-size: 11px;
  color: #00d4ff;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.coord-value {
  font-size: 13px;
  color: #fff;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.coord-layer {
  font-size: 11px;
  color: #aaa;
  font-style: italic;
}

/* Tokens overlay - positioned on top of canvas */
.tokens-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 10;
}

/* Individual token wrapper */
.token-wrapper {
  position: absolute;
  pointer-events: auto;
  transition: transform 0.3s ease, filter 0.2s ease;
  z-index: 10;
}

.token-wrapper:hover {
  transform: translate(-50%, -50%) scale(1.1);
  filter: drop-shadow(0 0 8px rgba(0, 212, 255, 0.6));
}

/* Selected token highlight */
.token-selected {
  filter: drop-shadow(0 0 12px rgba(255, 255, 0, 0.8));
  z-index: 11;
}

.token-selected:hover {
  transform: translate(-50%, -50%) scale(1.1);
  filter: drop-shadow(0 0 16px rgba(255, 255, 0, 1));
}
</style>
