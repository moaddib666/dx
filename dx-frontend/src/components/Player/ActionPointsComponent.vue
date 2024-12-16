<template>
  <div class="action-points-component">
    <h2>Allocate Action Points</h2>
    <p>Distribute your action points across the available characteristics.</p>

    <div class="characteristics-container">
      <div
          v-for="(char, key) in characteristics"
          :key="key"
          class="characteristic-item"
      >
        <img :alt="char.name" :src="char.image" class="characteristic-image"/>
        <div class="characteristic-details">
          <h3>{{ char.name }}</h3>
          <p>{{ char.description }}</p>
          <div class="action-bar">
            <div :style="{ width: baseValues[key] + '%' }" class="base-bar"></div>
            <div
                :style="{ width: allocatedPoints[key] * 10 + '%' }"
                class="allocated-bar"
            ></div>
          </div>
          <div class="actions">
            <button
                :disabled="allocatedPoints[key] <= 0"
                @click="decreasePoint(key)"
            >
              -
            </button>
            <span>{{ allocatedPoints[key] }}</span>
            <button
                :disabled="remainingPoints <= 0"
                @click="increasePoint(key)"
            >
              +
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer Controls -->
    <div class="footer-controls">
      <button class="reset-button" @click="resetPoints">Reset</button>
      <button :disabled="remainingPoints <= 0" class="auto-button" @click="autoAllocate">Auto Allocate</button>
      <p>Remaining Points: {{ remainingPoints }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ActionPointsComponent",
  props: {
    characteristics: {
      type: Object,
      required: true,
    },
    totalPoints: {
      type: Number,
      default: 100,
    },
    baseValues: {
      type: Object,
      default: () => ({
        PHYSICAL_STRENGTH: 10,
        MENTAL_STRENGTH: 10,
        LUCK: 10,
        SPEED: 10,
        CONCENTRATION: 10,
        FLOW_MANIPULATION: 10,
        FLOW_CONNECTION: 10,
        KNOWLEDGE: 10,
        FLOW_RESONANCE: 10,
        CHARISMA: 10,
      }),
    },
  },
  data() {
    return {
      allocatedPoints: {}, // Tracks allocated points for each characteristic
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
    increasePoint(key) {
      if (this.remainingPoints > 0) {
        this.allocatedPoints[key] = (this.allocatedPoints[key] || 0) + 1;
      }
    },
    decreasePoint(key) {
      if (this.allocatedPoints[key] > 0) {
        this.allocatedPoints[key] -= 1;
      }
    },
    resetPoints() {
      this.allocatedPoints = Object.keys(this.characteristics).reduce(
          (obj, key) => {
            obj[key] = 0;
            return obj;
          },
          {}
      );
    },
    autoAllocate() {
      const keys = Object.keys(this.characteristics);
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
  },
  created() {
    // Initialize allocated points
    this.allocatedPoints = Object.keys(this.characteristics).reduce((obj, key) => {
      obj[key] = 0;
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
