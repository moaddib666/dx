<template>
  <div class="stats-tab">
    <h3>Base Stats ({{ totalStatsPoints }}/{{ maxStatsPoints }} points)</h3>

    <!-- Loading indicator -->
    <div v-if="isLoading" class="loading-message">
      Loading stats...
    </div>

    <!-- Stats list using StatPresenter pattern -->
    <div v-else class="stats-container">
      <div class="stats-list">
        <div
          v-for="stat in templateStats"
          :key="stat.name"
          class="stat-presenter-wrapper"
        >
          <div class="gm-stat-presenter">
            <img
              class="stat-icon"
              :src="getStatIcon(stat.name)"
              :alt="stat.name"
              :title="stat.name"
            />
            <span class="stat-name">{{ stat.name }}</span>
            <div class="stat-controls">
              <button
                class="adjust-button decrement"
                @click="decrementStat(stat.name)"
                :disabled="stat.value <= 1"
                title="Decrease stat"
              >
                -
              </button>
              <input
                type="number"
                class="stat-value-input"
                :value="stat.value"
                @input="updateStat(stat.name, $event)"
                @blur="validateStatValue(stat.name, $event)"
                min="1"
                :max="maxStatsPoints"
                title="Click to edit value directly"
              />
              <button
                class="adjust-button increment"
                @click="incrementStat(stat.name)"
                :disabled="totalStatsPoints >= maxStatsPoints"
                title="Increase stat"
              >
                +
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats summary and validation -->
    <div class="stats-info">
      <div class="points-display">
        <span :class="['points-used', { 'over-limit': totalStatsPoints > maxStatsPoints }]">
          Points Used: {{ totalStatsPoints }} / {{ maxStatsPoints }}
        </span>
      </div>
      <div v-if="totalStatsPoints > maxStatsPoints" class="warning">
        Warning: You have exceeded the maximum allowed stat points!
      </div>
      <div v-else-if="totalStatsPoints < maxStatsPoints" class="info">
        Remaining Points: {{ maxStatsPoints - totalStatsPoints }}
      </div>
    </div>

    <!-- Reset all stats option -->
    <div class="reset-section">
      <button class="reset-button" @click="resetAllStats" title="Reset all stats to minimum values">
        Reset All Stats
      </button>
      <button class="distribute-button" @click="distributeEvenly" title="Distribute points evenly across all stats">
        Distribute Evenly
      </button>
    </div>
  </div>
</template>

<script>
import StatsGameService from '@/services/statService.js';

export default {
  name: 'StatsTab',
  props: {
    template: {
      type: Object,
      required: true
    },
    service: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      statsService: StatsGameService,
      isLoading: false,
      availableStats: []
    };
  },
  computed: {
    totalStatsPoints() {
      if (!this.template) return 0;
      return this.template.data.stats.reduce((sum, stat) => sum + stat.value, 0);
    },
    maxStatsPoints() {
      if (!this.template) return 100;
      return this.template.validation.max_stats_points_count;
    },
    templateStats() {
      if (!this.template) return [];
      // Ensure all stats have proper values and are displayed
      return this.template.data.stats.map(stat => ({
        ...stat,
        value: Math.max(1, stat.value || 1) // Ensure minimum value of 1
      }));
    }
  },
  async created() {
    await this.initializeStats();
  },
  methods: {
    async initializeStats() {
      try {
        this.isLoading = true;
        await this.statsService.refreshStats();
        this.availableStats = this.statsService.listCachedStats();
        
        // Ensure all template stats have icons
        this.ensureAllStatsHaveValues();
      } catch (error) {
        console.error('Failed to initialize stats:', error);
      } finally {
        this.isLoading = false;
      }
    },

    ensureAllStatsHaveValues() {
      // Make sure all available stats are included in the template
      const currentStatNames = this.template.data.stats.map(stat => stat.name);
      
      this.availableStats.forEach(availableStat => {
        if (!currentStatNames.includes(availableStat.name)) {
          // Add missing stat with default value
          this.service.updateStat(availableStat.name, 1);
        }
      });
    },

    getStatIcon(statName) {
      const cachedIcon = this.statsService.getCachedStatImage(statName);
      if (cachedIcon) {
        return cachedIcon;
      }
      
      // Fallback to default icon or generate from stat name
      return this.getDefaultStatIcon(statName);
    },

    getDefaultStatIcon(statName) {
      // Fallback icon mapping for common stats
      const iconMap = {
        'strength': '/src/assets/images/stats/strength.webp',
        'dexterity': '/src/assets/images/stats/dexterity.webp',
        'constitution': '/src/assets/images/stats/constitution.webp',
        'intelligence': '/src/assets/images/stats/intelligence.webp',
        'wisdom': '/src/assets/images/stats/wisdom.webp',
        'charisma': '/src/assets/images/stats/charisma.webp',
        'agility': '/src/assets/images/stats/agility.webp',
        'endurance': '/src/assets/images/stats/endurance.webp',
        'perception': '/src/assets/images/stats/perception.webp',
        'luck': '/src/assets/images/stats/luck.webp'
      };

      const lowerStatName = statName.toLowerCase();
      return iconMap[lowerStatName] || '/src/assets/images/stats/default.webp';
    },

    updateStat(statName, event) {
      const value = parseInt(event.target.value, 10);
      if (!isNaN(value) && value >= 1) {
        this.service.updateStat(statName, Math.max(1, value));
        this.$emit('update');
      }
    },

    incrementStat(statName) {
      const currentStat = this.template.data.stats.find(stat => stat.name === statName);
      if (currentStat && this.totalStatsPoints < this.maxStatsPoints) {
        this.service.updateStat(statName, currentStat.value + 1);
        this.$emit('update');
      }
    },

    decrementStat(statName) {
      const currentStat = this.template.data.stats.find(stat => stat.name === statName);
      if (currentStat && currentStat.value > 1) {
        this.service.updateStat(statName, currentStat.value - 1);
        this.$emit('update');
      }
    },

    resetAllStats() {
      if (confirm('Are you sure you want to reset all stats to minimum values?')) {
        this.template.data.stats.forEach(stat => {
          this.service.updateStat(stat.name, 1);
        });
        this.$emit('update');
      }
    },

    distributeEvenly() {
      if (confirm('This will distribute available points evenly across all stats. Continue?')) {
        const statsCount = this.template.data.stats.length;
        const pointsPerStat = Math.floor(this.maxStatsPoints / statsCount);
        const remainingPoints = this.maxStatsPoints % statsCount;

        this.template.data.stats.forEach((stat, index) => {
          const value = pointsPerStat + (index < remainingPoints ? 1 : 0);
          this.service.updateStat(stat.name, Math.max(1, value));
        });
        this.$emit('update');
      }
    },

    validateStatValue(statName, event) {
      const value = parseInt(event.target.value, 10);
      if (isNaN(value) || value < 1) {
        // Reset to minimum value if invalid
        this.service.updateStat(statName, 1);
        this.$emit('update');
      } else if (value > this.maxStatsPoints) {
        // Cap at maximum if too high
        this.service.updateStat(statName, this.maxStatsPoints);
        this.$emit('update');
      }
    }
  }
};
</script>

<style scoped>
.stats-tab {
  padding: 20px 0;
}

/* Loading message */
.loading-message {
  text-align: center;
  color: #888;
  padding: 40px;
  font-style: italic;
}

/* Stats container */
.stats-container {
  margin-bottom: 30px;
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* GameMaster StatPresenter inspired styling */
.gm-stat-presenter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(43, 43, 43, 0.9);
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  border: 1px solid #444;
  gap: 16px;
  transition: all 0.3s ease;
}

.gm-stat-presenter:hover {
  background: rgba(50, 50, 50, 0.9);
  border-color: #1E90FF;
}

/* Stat icon */
.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: contain;
  flex-shrink: 0;
  border: 2px solid #555;
}

/* Stat name */
.stat-name {
  flex: 1;
  color: white;
  font-weight: bold;
  font-size: 16px;
  text-transform: capitalize;
  min-width: 120px;
}

/* Stat controls (+/-) */
.stat-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 4px;
}

.adjust-button {
  background: rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.adjust-button:disabled {
  cursor: not-allowed;
  opacity: 0.3;
  background: rgba(255, 255, 255, 0.1);
}

.adjust-button:not(:disabled):hover {
  background: rgba(255, 255, 255, 0.4);
  transform: scale(1.1);
}

.adjust-button.increment:not(:disabled):hover {
  background: rgba(76, 175, 80, 0.6);
}

.adjust-button.decrement:not(:disabled):hover {
  background: rgba(244, 67, 54, 0.6);
}

/* Editable stat value input */
.stat-value-input {
  font-size: 18px;
  font-weight: bold;
  color: white;
  min-width: 60px;
  width: 60px;
  text-align: center;
  background: rgba(30, 144, 255, 0.2);
  border-radius: 4px;
  padding: 6px 8px;
  border: 1px solid rgba(30, 144, 255, 0.3);
  transition: all 0.3s ease;
  outline: none;
  -moz-appearance: textfield; /* Firefox: hide spinner arrows */
}

/* Hide native number input spinner arrows in webkit browsers */
.stat-value-input::-webkit-outer-spin-button,
.stat-value-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.stat-value-input:focus {
  background: rgba(30, 144, 255, 0.4);
  border-color: #1E90FF;
  box-shadow: 0 0 8px rgba(30, 144, 255, 0.5);
}

.stat-value-input:hover {
  background: rgba(30, 144, 255, 0.3);
  border-color: rgba(30, 144, 255, 0.6);
}

/* Stats info section */
.stats-info {
  background: #2d2d2d;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #444;
  margin-bottom: 20px;
}

.points-display {
  margin-bottom: 12px;
}

.points-used {
  font-weight: bold;
  color: #4CAF50;
  font-size: 16px;
}

.points-used.over-limit {
  color: #f44336;
}

.warning {
  color: #ff9800;
  font-weight: bold;
  background: rgba(255, 152, 0, 0.1);
  padding: 12px;
  border-radius: 6px;
  border-left: 4px solid #ff9800;
  margin-top: 8px;
}

.info {
  color: #4CAF50;
  font-weight: bold;
  background: rgba(76, 175, 80, 0.1);
  padding: 12px;
  border-radius: 6px;
  border-left: 4px solid #4CAF50;
  margin-top: 8px;
}

/* Reset section */
.reset-section {
  display: flex;
  gap: 12px;
  justify-content: center;
  padding: 20px 0;
}

.reset-button, .distribute-button {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
}

.reset-button {
  background: #f44336;
  color: white;
}

.reset-button:hover {
  background: #d32f2f;
  transform: translateY(-2px);
}

.distribute-button {
  background: #4CAF50;
  color: white;
}

.distribute-button:hover {
  background: #3d8b40;
  transform: translateY(-2px);
}

/* Header styling */
h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 25px;
  font-size: 1.3rem;
  text-align: center;
  padding-bottom: 10px;
  border-bottom: 2px solid #444;
}

/* Responsive design */
@media (max-width: 768px) {
  .gm-stat-presenter {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .stat-name {
    text-align: center;
    min-width: auto;
  }
  
  .stat-controls {
    justify-content: center;
  }
  
  .reset-section {
    flex-direction: column;
    align-items: center;
  }
}
</style>