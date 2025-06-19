<template>
  <div class="character-stats-radar-chart">
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <div class="loading-text">Loading stats...</div>
    </div>
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else class="radar-chart-container">
      <svg
          ref="radarChart"
          :height="size"
          :viewBox="`0 0 ${size} ${size}`"
          :width="size"
          class="radar-svg"
      >
        <!-- Grid circles -->
        <g class="grid-lines">
          <circle
              v-for="i in 5"
              :key="`grid-${i}`"
              :cx="center"
              :cy="center"
              :r="(radius * i) / 5"
              fill="none"
              opacity="0.6"
              stroke="#e2e8f0"
              stroke-width="1"
          />
        </g>

        <!-- Axis lines -->
        <g class="axis-lines">
          <line
              v-for="(stat, index) in statOrder"
              :key="`axis-${index}`"
              :x1="center"
              :x2="getAxisEndX(index)"
              :y1="center"
              :y2="getAxisEndY(index)"
              opacity="0.4"
              stroke="#94a3b8"
              stroke-width="1"
          />
        </g>

        <!-- Data area -->
        <g class="data-area">
          <polygon
              :points="getDataPolygonPoints()"
              class="data-polygon"
              fill="url(#radarGradient)"
              stroke="#3b82f6"
              stroke-width="2"
          />

          <!-- Data points -->
          <circle
              v-for="(stat, index) in statOrder"
              :key="`point-${index}`"
              :cx="getDataPointX(index)"
              :cy="getDataPointY(index)"
              class="data-point"
              fill="#1d4ed8"
              r="4"
              stroke="#ffffff"
              stroke-width="2"
              @mouseleave="hideTooltip"
              @mouseover="showTooltip(stat, index, $event)"
          />
        </g>

        <!-- Labels -->
        <g class="labels">
          <text
              v-for="(stat, index) in statOrder"
              :key="`label-${index}`"
              :dominant-baseline="getLabelBaseline(index)"
              :text-anchor="getLabelAnchor(index)"
              :x="getLabelX(index)"
              :y="getLabelY(index)"
              class="stat-label"
              fill="#374151"
              font-size="12"
              font-weight="500"
          >
            {{ stat }}
          </text>
        </g>

        <!-- Gradient definition -->
        <defs>
          <radialGradient id="radarGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#1d4ed8" stop-opacity="0.1"/>
          </radialGradient>
        </defs>
      </svg>

      <!-- Tooltip -->
      <div
          v-if="tooltip.visible"
          ref="tooltip"
          :style="{
          left: tooltip.x + 'px',
          top: tooltip.y + 'px'
        }"
          class="tooltip"
      >
        <div class="tooltip-content">
          <strong>{{ tooltip.stat }}</strong>
          <div class="tooltip-value">{{ tooltip.value }} / {{ maxValue }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CharacterStatsService from '@/services/CharacterStatsService';

export default {
  name: 'CharacterStatsRadarChart',

  props: {
    characterId: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      loading: true,
      error: null,
      statsData: null,
      size: 300,
      tooltip: {
        visible: false,
        x: 0,
        y: 0,
        stat: '',
        value: 0
      },
      statOrder: [
        'Physical Strength',
        'Speed',
        'Mental Strength',
        'Charisma',
        'Knowledge',
        'Concentration',
        'Flow Connection',
        'Flow Manipulation',
        'Flow Resonance',
        'Luck'
      ]
    };
  },

  computed: {
    center() {
      return this.size / 2;
    },

    radius() {
      return this.size * 0.35;
    },

    maxValue() {
      return this.statsData?.maxValue || 20;
    }
  },

  watch: {
    characterId: {
      immediate: true,
      handler: 'fetchStats'
    }
  },

  methods: {
    async fetchStats() {
      this.loading = true;
      this.error = null;

      try {
        const statsData = await CharacterStatsService.fetchCharacterStats(this.characterId);
        this.statsData = CharacterStatsService.processStatsForRadarChart(statsData);
      } catch (error) {
        this.error = 'Failed to load character stats';
        console.error('Error loading character stats:', error);
      } finally {
        this.loading = false;
      }
    },

    getAngle(index) {
      return (index * 2 * Math.PI) / this.statOrder.length - Math.PI / 2;
    },

    getAxisEndX(index) {
      const angle = this.getAngle(index);
      return this.center + this.radius * Math.cos(angle);
    },

    getAxisEndY(index) {
      const angle = this.getAngle(index);
      return this.center + this.radius * Math.sin(angle);
    },

    getStatValue(statName) {
      if (!this.statsData?.stats) return 0;
      const stat = this.statsData.stats.find(s => s.name === statName);
      return stat ? stat.value : 0;
    },

    getDataPointX(index) {
      const angle = this.getAngle(index);
      const statName = this.statOrder[index];
      const value = this.getStatValue(statName);
      const normalizedValue = value / this.maxValue;
      return this.center + this.radius * normalizedValue * Math.cos(angle);
    },

    getDataPointY(index) {
      const angle = this.getAngle(index);
      const statName = this.statOrder[index];
      const value = this.getStatValue(statName);
      const normalizedValue = value / this.maxValue;
      return this.center + this.radius * normalizedValue * Math.sin(angle);
    },

    getDataPolygonPoints() {
      return this.statOrder
          .map((_, index) => `${this.getDataPointX(index)},${this.getDataPointY(index)}`)
          .join(' ');
    },

    getLabelX(index) {
      const angle = this.getAngle(index);
      const labelDistance = this.radius + 25;
      return this.center + labelDistance * Math.cos(angle);
    },

    getLabelY(index) {
      const angle = this.getAngle(index);
      const labelDistance = this.radius + 25;
      return this.center + labelDistance * Math.sin(angle);
    },

    getLabelAnchor(index) {
      const angle = this.getAngle(index);
      const x = Math.cos(angle);
      if (x > 0.1) return 'start';
      if (x < -0.1) return 'end';
      return 'middle';
    },

    getLabelBaseline(index) {
      const angle = this.getAngle(index);
      const y = Math.sin(angle);
      if (y > 0.1) return 'hanging';
      if (y < -0.1) return 'baseline';
      return 'middle';
    },

    showTooltip(statName, index, event) {
      const rect = this.$refs.radarChart.getBoundingClientRect();
      const value = this.getStatValue(statName);

      this.tooltip = {
        visible: true,
        x: event.clientX - rect.left + 10,
        y: event.clientY - rect.top - 10,
        stat: statName,
        value: value
      };
    },

    hideTooltip() {
      this.tooltip.visible = false;
    }
  }
};
</script>

<style scoped>
.character-stats-radar-chart {
  position: relative;
  width: 100%;
  height: 300px;
  margin: 10px 0;
}

.radar-chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.radar-svg {
  max-width: 100%;
  max-height: 100%;
}

.data-polygon {
  transition: all 0.3s ease;
}

.data-point {
  cursor: pointer;
  transition: all 0.2s ease;
}

.data-point:hover {
  r: 6;
  filter: drop-shadow(0 0 4px rgba(59, 130, 246, 0.6));
}

.stat-label {
  font-family: system-ui, -apple-system, sans-serif;
  pointer-events: none;
}

.tooltip {
  position: absolute;
  background: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 12px;
  pointer-events: none;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.tooltip-content {
  white-space: nowrap;
}

.tooltip-value {
  color: #93c5fd;
  font-weight: 600;
  margin-top: 2px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.95);
  z-index: 1;
  backdrop-filter: blur(2px);
}

.loading-spinner {
  border: 3px solid rgba(59, 130, 246, 0.2);
  border-radius: 50%;
  border-top: 3px solid #3b82f6;
  width: 32px;
  height: 32px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-text {
  margin-top: 12px;
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.error-message {
  color: #ef4444;
  text-align: center;
  padding: 20px;
  font-weight: 500;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  margin: 20px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .character-stats-radar-chart {
    height: 250px;
  }

  .stat-label {
    font-size: 10px;
  }
}
</style>