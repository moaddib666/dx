<template>
  <div class="action-points-component">
    <h2>{{ t('playerComponents.actionPoints.title') }}</h2>
    <p>{{ t('playerComponents.actionPoints.description') }}</p>

    <div class="characteristics-container">
      <div
          v-for="stat in stats"
          :key="stat.name"
          class="characteristic-item"
      >
<!--        <img :alt="stat.name" :src="stat.image" class="characteristic-image" />-->
        <div class="characteristic-details">
          <h3>{{ stat.name }}</h3>
          <p>{{ stat.description }}</p>
          <div class="action-bar">
            <div
                :style="{ width: baseValue + '%' }"
                class="base-bar"
            ></div>
            <div
                :style="{ width: (allocatedPoints[stat.name] || 0) * 10 + '%' }"
                class="allocated-bar"
            ></div>
          </div>
          <div class="actions">
            <button
                :disabled="!(allocatedPoints[stat.name] > 0)"
                @click="decreasePoint(stat.name)"
            >
              -
            </button>
            <span>{{ allocatedPoints[stat.name] || 0 }}</span>
            <button
                :disabled="remainingPoints <= 0"
                @click="increasePoint(stat.name)"
            >
              +
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer Controls -->
    <div class="footer-controls">
      <button class="reset-button" @click="resetPoints">{{ t('playerComponents.actionPoints.reset') }}</button>
      <button
          :disabled="remainingPoints <= 0"
          class="auto-button"
          @click="autoAllocate"
      >
        {{ t('playerComponents.actionPoints.autoAllocate') }}
      </button>
      <p>{{ t('playerComponents.actionPoints.remainingPoints') }}{{ remainingPoints }}</p>
    </div>
  </div>
</template>

<script>
import { useI18n } from 'vue-i18n';

export default {
  name: "ActionPointsComponent",
  props: {
    stats: {
      type: Array, // Array of objects with 'name', 'description', and optionally 'image'
      required: true,
    },
    currentPlayerStats: { // TODO: integrate this prop into the component so that it auto-allocates points if currentPlayerStats is not empty
      type: Array, // Array of objects with 'name' and 'value'
      default: () => [],
    },
    totalPoints: {
      type: Number,
      default: 100,
    },
    setPlayerStats: {
      type: Function, // Function to set the player's stats as an array of { name, value }
      required: true,
    },
    baseValue: {
      type: Number,
      default: 10, // Default base value for each stat
    },
  },
  setup() {
    const { t } = useI18n();
    return { t };
  },
  data() {
    return {
      allocatedPoints: {}, // Tracks allocated points per characteristic
    };
  },
  computed: {
    remainingPoints() {
      return (
          this.totalPoints -
          Object.values(this.allocatedPoints).reduce((sum, value) => sum + value, 0)
      );
    },
  },
  methods: {
    increasePoint(statName) {
      if (this.remainingPoints > 0) {
        this.allocatedPoints[statName] = (this.allocatedPoints[statName] || 0) + 1;
        this.updatePlayerStats();
      }
    },
    decreasePoint(statName) {
      if (this.allocatedPoints[statName] > 0) {
        this.allocatedPoints[statName] -= 1;
        this.updatePlayerStats();
      }
    },
    resetPoints() {
      this.allocatedPoints = {};
      this.updatePlayerStats();
    },
    autoAllocate() {
      const keys = this.stats.map((stat) => stat.name);
      let pointsToAllocate = this.remainingPoints;

      while (pointsToAllocate > 0) {
        for (const key of keys) {
          if (pointsToAllocate > 0) {
            this.increasePoint(key);
            pointsToAllocate--;
          }
        }
      }
    },
    updatePlayerStats() {
      // Convert allocated points to the expected player stats format
      const updatedStats = this.stats.map((stat) => ({
        name: stat.name,
        value: (this.allocatedPoints[stat.name] || 0),
      }));
      this.setPlayerStats(updatedStats);
    },
  },
  created() {
    this.allocatedPoints = this.currentPlayerStats.reduce((obj, stat) => {
      obj[stat.name] = stat.value;
      return obj;
    }, {});
  },
};
</script>

<style scoped>
.action-points-component {
  padding: 20px;
  border-radius: 8px;
  background-color: #222;
  color: #fff;
  text-align: center;
}

h2 {
  margin-bottom: 10px;
}

p {
  margin-bottom: 20px;
  font-size: 0.9rem;
  color: #ccc;
}

/* Characteristics Container */
.characteristics-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-around;
}

.characteristic-item {
  width: 250px;
  background-color: #333;
  padding: 15px;
  border-radius: 8px;
  text-align: left;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.characteristic-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6);
}

.characteristic-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  margin-bottom: 10px;
}

.characteristic-details h3 {
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.characteristic-details p {
  font-size: 0.9rem;
  color: #ddd;
  margin-bottom: 10px;
}

/* Action Bar */
.action-bar {
  position: relative;
  height: 10px;
  background-color: #444;
  border-radius: 5px;
  margin: 10px 0;
  overflow: hidden;
}

.base-bar {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-color: rgba(0, 0, 255, 0.3);
  z-index: 1;
}

.allocated-bar {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-color: #4caf50;
  z-index: 2;
}

/* Actions */
.actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.actions button {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  background-color: #444;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.actions button:disabled {
  background-color: #555;
  cursor: not-allowed;
}

.actions button:hover:not(:disabled) {
  background-color: #4caf50;
}

/* Footer Controls */
.footer-controls {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reset-button, .auto-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #f44336;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.reset-button:hover, .auto-button:hover {
  background-color: #d32f2f;
}
</style>
