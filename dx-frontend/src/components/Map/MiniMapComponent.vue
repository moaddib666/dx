<template>
  <div class="mini-map-container">
    <svg :height="svgHeight" :width="svgWidth">
      <defs>
        <clipPath id="circleClip">
          <circle :cx="svgWidth / 2" :cy="svgHeight / 2" :r="circleRadius"/>
        </clipPath>
      </defs>

      <!-- Grid behind everything, inside the clip -->
      <g clip-path="url(#circleClip)">
        <g class="grid">
          <!-- Vertical lines -->
          <line
              v-for="(vLine, idx) in gridData.vLines"
              :key="'vLine' + idx"
              :x1="vLine.x"
              :x2="vLine.x"
              :y1="vLine.y1"
              :y2="vLine.y2"
              stroke="rgba(0,255,0,0.3)"
              stroke-width="1"
          />
          <!-- Horizontal lines -->
          <line
              v-for="(hLine, idx) in gridData.hLines"
              :key="'hLine' + idx"
              :x1="hLine.x1"
              :x2="hLine.x2"
              :y1="hLine.y"
              :y2="hLine.y"
              stroke="rgba(0,255,0,0.3)"
              stroke-width="1"
          />
          <!-- Dots at cell centers -->
          <circle
              v-for="(dot, idx) in gridData.dots"
              :key="'dot' + idx"
              :cx="dot.x"
              :cy="dot.y"
              fill="rgba(0,255,0,0.4)"
              r="1"
          />
        </g>

        <!-- Draw connections -->
        <path
            v-for="(conn, i) in curvedConnections"
            :key="'conn-' + i"
            :d="conn.d"
            fill="none"
            stroke="#aaa"
            stroke-linecap="round"
            stroke-width="2"
        />

        <!-- Draw positions -->
        <g v-for="pos in scaledPositions" :key="pos.id">
          <circle
              :cx="pos.sx"
              :cy="pos.sy"
              :fill="pos.isCurrent
              ? '#1E90FF'
              : pos.hasCharacter
                ? 'gold'
                : '#666'"
              :r="pos.isCurrent ? 9 : (pos.hasCharacter ? 7 : 5)"
              stroke="#333"
              stroke-width="1"
          />
          <text
              v-if="pos.characterCount > 0"
              :x="pos.sx"
              :y="pos.sy + 3"
              fill="#fff"
              font-size="10"
              text-anchor="middle"
          >
            {{ pos.characterCount }}
          </text>
        </g>
      </g>

      <!-- Circular boundary -->
      <circle
          :cx="svgWidth / 2"
          :cy="svgHeight / 2"
          :r="circleRadius"
          fill="none"
          stroke="#555"
          stroke-dasharray="4 4"
          stroke-width="2"
      />
    </svg>
  </div>
</template>

<script>
export default {
  name: "MiniMapCircleStrictMask",
  props: {
    mapData: {type: Object, required: true},
    arcFactor: {type: Number, default: 0},
    minArcFactor: {type: Number, default: 0.25},
    maxArcFactor: {type: Number, default: 0.5},
  },
  data() {
    return {
      svgWidth: 300,
      svgHeight: 300,
      padding: 20,
      // Radius in "map units" for how far around the current position we show
      radius: 2.05,
    };
  },
  methods: {
    calculateArcFactor() {
      // Arc factor randomization if arcFactor not specified
      return (
          this.arcFactor ||
          Math.random() * (this.maxArcFactor - this.minArcFactor) + this.minArcFactor
      );
    },
  },
  computed: {
    // We want the map to center on the current position;
    // circleRadius is how large the circle should be in SVG px.
    circleRadius() {
      return this.radius * this.scaleAndOffset.scale;
    },
    allPositions() {
      return (this.mapData.positions || []).map((p) => p.position);
    },
    allConnections() {
      return this.mapData.connections || [];
    },
    charactersList() {
      return this.mapData.characters || [];
    },
    currentPositionId() {
      return this.mapData.current_position;
    },
    currentPosCoords() {
      const found = this.allPositions.find((pos) => pos.id === this.currentPositionId);
      if (!found) return {x: 0, y: 0};
      return {x: found.grid_x, y: found.grid_y};
    },
    positionCharCount() {
      const result = {};
      for (const ch of this.charactersList) {
        if (!result[ch.position]) result[ch.position] = 0;
        result[ch.position]++;
      }
      return result;
    },
    // Only positions within this.radius distance from current are rendered
    filteredPositions() {
      const {x: cx, y: cy} = this.currentPosCoords;
      return this.allPositions.filter((p) => {
        const dist = Math.sqrt((p.grid_x - cx) ** 2 + (p.grid_y - cy) ** 2);
        return dist <= this.radius + 2;
      });
    },
    // Same for connections
    filteredConnections() {
      const allowedIds = new Set(this.filteredPositions.map((p) => p.id));
      return this.allConnections.filter(
          (c) => allowedIds.has(c.position_from) && allowedIds.has(c.position_to)
      );
    },
    // We'll use a fixed scale based on our radius and place the current position in the middle
    scaleAndOffset() {
      // The largest circle we can draw inside the SVG (account for padding)
      // We'll treat half that dimension as our "usable radius in px."
      const usableRadius = Math.min(
          (this.svgWidth - 2 * this.padding) / 2,
          (this.svgHeight - 2 * this.padding) / 2
      );
      // scale is how many SVG px per "map unit"
      const scale = usableRadius / this.radius;

      // offset so that current position is in center of the SVG
      // (i.e., at svgWidth/2, svgHeight/2)
      const offsetX = (this.svgWidth / 2) - this.currentPosCoords.x * scale;
      const offsetY = (this.svgHeight / 2) - this.currentPosCoords.y * scale;

      return {scale, offsetX, offsetY};
    },
    // Positions scaled according to above logic
    scaledPositions() {
      const {scale, offsetX, offsetY} = this.scaleAndOffset;
      return this.filteredPositions.map((p) => {
        const sx = p.grid_x * scale + offsetX;
        const sy = p.grid_y * scale + offsetY;
        const count = this.positionCharCount[p.id] || 0;
        return {
          ...p,
          sx,
          sy,
          characterCount: count,
          hasCharacter: count > 0,
          isCurrent: p.id === this.currentPositionId,
        };
      });
    },
    // Curved lines between scaled positions
    curvedConnections() {
      const dict = {};
      for (const sp of this.scaledPositions) {
        dict[sp.id] = sp;
      }
      return this.filteredConnections
          .map((c) => {
            const p1 = dict[c.position_from];
            const p2 = dict[c.position_to];
            if (!p1 || !p2) return null;
            if (p1.sx === p2.sx && p1.sy === p2.sy) return null;

            const x1 = p1.sx, y1 = p1.sy;
            const x2 = p2.sx, y2 = p2.sy;
            const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
            const dx = x2 - x1, dy = y2 - y1;
            const dist = Math.sqrt(dx * dx + dy * dy) || 1;
            const offset = this.calculateArcFactor() * dist;
            const nx = -dy / dist, ny = dx / dist;
            const c1x = mx + nx * offset, c1y = my + ny * offset;
            const c2x = mx - nx * offset, c2y = my - ny * offset;

            return {d: `M ${x1},${y1} C ${c1x},${c1y} ${c2x},${c2y} ${x2},${y2}`};
          })
          .filter(Boolean);
    },

    // Grid data, lines offset so each "map cell center" lines up with positions nicely
    gridData() {
      // We'll still find min/max among filtered positions, but the scale/offset
      // is always centered on current position above.
      const {minX, maxX, minY, maxY} = this.miniBounds;
      const {scale, offsetX, offsetY} = this.scaleAndOffset;

      // Shift lines to run at integer + 0.5 in map coords
      const offsetVal = 0.5;
      // Expand a bit so lines fill beyond just the bounding box
      const startX = Math.floor(minX) - 2;
      const endX = Math.ceil(maxX) + 2;
      const startY = Math.floor(minY) - 2;
      const endY = Math.ceil(maxY) + 2;

      const vLines = [];
      const hLines = [];
      const dots = [];

      // Vertical lines
      for (let x = startX; x <= endX; x++) {
        const sx = (x + offsetVal) * scale + offsetX;
        vLines.push({
          x: sx,
          y1: startY * scale + offsetY,
          y2: endY * scale + offsetY,
        });
      }
      // Horizontal lines
      for (let y = startY; y <= endY; y++) {
        const sy = (y + offsetVal) * scale + offsetY;
        hLines.push({
          y: sy,
          x1: startX * scale + offsetX,
          x2: endX * scale + offsetX,
        });
      }
      // Dots at integer coords
      for (let x = startX; x <= endX; x++) {
        for (let y = startY; y <= endY; y++) {
          const sx = x * scale + offsetX;
          const sy = y * scale + offsetY;
          dots.push({x: sx, y: sy});
        }
      }
      return {vLines, hLines, dots};
    },
    // Minimal bounding box for filtered positions,
    // used for drawing the grid large enough
    miniBounds() {
      if (!this.filteredPositions.length) {
        return {minX: 0, maxX: 0, minY: 0, maxY: 0};
      }
      let minX = Infinity;
      let maxX = -Infinity;
      let minY = Infinity;
      let maxY = -Infinity;

      for (const pos of this.filteredPositions) {
        if (pos.grid_x < minX) minX = pos.grid_x;
        if (pos.grid_x > maxX) maxX = pos.grid_x;
        if (pos.grid_y < minY) minY = pos.grid_y;
        if (pos.grid_y > maxY) maxY = pos.grid_y;
      }
      return {minX, maxX, minY, maxY};
    },
  },
};
</script>

<style scoped>
.mini-map-container {
  display: inline-block;
  overflow: hidden;
}
</style>
