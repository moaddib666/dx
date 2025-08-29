<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal">
      <div class="header">
        <div class="header-top">
          <h2 class="title">Switch Base Values</h2>
          <button @click="closeModal" class="close-btn" title="Close Modal">
            ×
          </button>
        </div>
        <p class="modal-description">Select the stats to swap their base values.</p>
      </div>

      <!-- From Stat and To Stat Selection Row -->
      <div class="stat-row">
        <!-- From Stat -->
        <div class="stat-item">
          <label for="fromStat" class="stat-label">From:</label>
          <select
              id="fromStat"
              v-model="fromStatId"
              class="filter-select"
              @change="updateSelectedFromStat"
          >
            <option
                v-for="stat in stats"
                :key="stat.id"
                :value="stat.id"
            >
              {{ stat.name }}
            </option>
          </select>
          <div class="dice-wrapper" v-if="selectedFromStat">
            <DiceNRolls
                :dice-rolls="selectedFromStat.dice_rolls"
                :stat="selectedFromStat.name"
                :wide="true"
                class="base-value"
            />
          </div>
        </div>

        <!-- To Stat -->
        <div class="stat-item">
          <label for="toStat" class="stat-label">To:</label>
          <select
              id="toStat"
              v-model="toStatId"
              class="filter-select"
              @change="updateSelectedToStat"
          >
            <option
                v-for="stat in stats"
                :key="stat.id"
                :value="stat.id"
            >
              {{ stat.name }}
            </option>
          </select>
          <div class="dice-wrapper" v-if="selectedToStat">
            <DiceNRolls
                :dice-rolls="selectedToStat.dice_rolls"
                :stat="selectedToStat.name"
                :wide="true"
                class="base-value"
            />
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="modal-actions">
        <button @click="closeModal" class="action-btn cancel-btn">
          Cancel
        </button>
        <button @click="confirmSwitch" :disabled="!fromStatId || !toStatId" class="action-btn confirm-btn">
          Swap
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import DiceNRolls from "@/components/Dice/DiceNRolls.vue";
import LandingButton from "@/components/btn/LandingButton.vue";

export default {
  name: "SwitchBaseValuesModal",
  components: {
    LandingButton,
    DiceNRolls,
  },
  props: {
    stats: {
      type: Array,
      required: true,
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
    initialFromStatId: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      fromStatId: this.initialFromStatId,
      toStatId: null,
    };
  },
  watch: {
    initialFromStatId(newVal) {
      this.fromStatId = newVal;
    },
  },
  computed: {
    selectedFromStat() {
      return this.stats.find((stat) => stat.id === this.fromStatId);
    },
    selectedToStat() {
      return this.stats.find((stat) => stat.id === this.toStatId);
    },
  },
  methods: {
    updateSelectedFromStat() {
      if (this.toStatId === this.fromStatId) {
        this.toStatId = null;
      }
    },
    updateSelectedToStat() {
      if (this.toStatId === this.fromStatId) {
        this.toStatId = null;
      }
    },
    confirmSwitch() {
      this.$emit("switchBaseValues", {
        fromStatId: this.fromStatId,
        toStatId: this.toStatId,
      });
    },
    closeModal() {
      this.$emit("closeModal");
    },
  },
};
</script>

<style scoped>
/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* Modal */
.modal {
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.5rem;
  padding: 1.5rem;
  width: 90%;
  max-width: 600px;
  color: #fada95;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
}

/* Header */
.header {
  margin-bottom: 1.5rem;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.7rem;
  position: relative;
}

.title {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  flex: 1;
  text-align: center;
}

.close-btn {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  line-height: 1;
}

.close-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-50%) scale(1.1);
  color: #7fff16;
}

.close-btn:active {
  transform: translateY(-50%) scale(0.95);
}

.modal-description {
  font-size: 0.9rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: rgba(250, 218, 149, 0.8);
  text-align: center;
  margin: 0;
}

/* Stat Row */
.stat-row {
  display: flex;
  gap: 2rem;
  justify-content: center;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.7rem;
  min-width: 200px;
}

.stat-label {
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 500;
  color: #fada95;
  font-size: 0.9rem;
}

/* Select Styling */
.filter-select {
  width: 100%;
  padding: 0.5rem 0.7rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.3rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.9rem;
  font-weight: 400;
  transition: border-color 0.3s, background-color 0.3s;
}

.filter-select:focus {
  outline: none;
  border-color: #7fff16;
  background: rgba(0, 0, 0, 0.6);
}

.filter-select option {
  background: rgba(0, 0, 0, 0.9);
  color: #fada95;
}

/* Dice Wrapper for proper positioning */
.dice-wrapper {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  width: 100%;
  min-height: 3rem;
  position: relative;
  padding-right: 1rem;
}

/* Action Buttons */
.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.6rem 1.5rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.3rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 100px;
}

.action-btn:hover:not(:disabled) {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-1px);
}

.action-btn:active:not(:disabled) {
  transform: translateY(0);
}

.confirm-btn:hover:not(:disabled) {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.2);
  color: #7fff16;
}

.cancel-btn:hover:not(:disabled) {
  border-color: rgba(255, 100, 100, 0.6);
  background: rgba(255, 100, 100, 0.1);
  color: rgba(255, 150, 150, 0.9);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border-color: rgba(127, 255, 22, 0.1);
}

/* Responsive Design */
@media (max-width: 640px) {
  .stat-row {
    flex-direction: column;
    gap: 1.5rem;
  }

  .stat-item {
    min-width: 100%;
  }

  .modal-actions {
    flex-direction: column;
  }

  .action-btn {
    min-width: 100%;
  }
}
</style>
