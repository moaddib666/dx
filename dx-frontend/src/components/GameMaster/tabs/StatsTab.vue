<template>
  <div class="stats-tab">
    <h3>Base Stats ({{ totalStatsPoints }}/{{ maxStatsPoints }} points)</h3>

    <div class="stats-grid">
      <div
        v-for="stat in template.data.stats"
        :key="stat.name"
        class="stat-item"
      >
        <label>{{ stat.name }}</label>
        <input
          type="number"
          :value="stat.value"
          @input="updateStat(stat.name, $event)"
          min="1"
        />
      </div>
    </div>

    <div class="stats-info">
      <div class="points-display">
        <span :class="['points-used', { 'over-limit': totalStatsPoints > maxStatsPoints }]">
          Points Used: {{ totalStatsPoints }} / {{ maxStatsPoints }}
        </span>
      </div>
      <div v-if="totalStatsPoints > maxStatsPoints" class="warning">
        Warning: You have exceeded the maximum allowed stat points!
      </div>
    </div>
  </div>
</template>

<script>
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
  computed: {
    totalStatsPoints() {
      if (!this.template) return 0;
      return this.template.data.stats.reduce((sum, stat) => sum + stat.value, 0);
    },
    maxStatsPoints() {
      if (!this.template) return 100;
      return this.template.validation.max_stats_points_count;
    }
  },
  methods: {
    updateStat(statName, event) {
      const value = parseInt(event.target.value, 10);
      if (!isNaN(value)) {
        this.service.updateStat(statName, value);
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-item label {
  margin-bottom: 5px;
  color: #ccc;
  font-weight: bold;
}

.stat-item input {
  padding: 8px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.stat-item input:focus {
  border-color: #1E90FF;
  outline: none;
}

.stats-info {
  background: #2d2d2d;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #444;
}

.points-display {
  margin-bottom: 10px;
}

.points-used {
  font-weight: bold;
  color: #4CAF50;
}

.points-used.over-limit {
  color: #f44336;
}

.warning {
  color: #ff9800;
  font-weight: bold;
  background: rgba(255, 152, 0, 0.1);
  padding: 8px;
  border-radius: 4px;
  border-left: 4px solid #ff9800;
}

h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.2rem;
}
</style>