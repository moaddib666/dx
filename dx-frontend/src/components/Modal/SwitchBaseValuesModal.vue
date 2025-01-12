<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal">
      <h2 class="modal-title">Switch Base Values</h2>
      <p class="modal-description">Select the stats to swap their base values.</p>

      <!-- From Stat and To Stat Selection Row -->
      <div class="stat-row">
        <!-- From Stat -->
        <div class="stat-item">
          <label for="fromStat">From:</label>
          <select
              id="fromStat"
              v-model="fromStatId"
              class="small-select"
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
          <DiceNRolls
              v-if="selectedFromStat"
              :dice-rolls="selectedFromStat.dice_rolls"
              :stat="selectedFromStat.name"
              :wide="true"
              class="base-value"
          />
        </div>

        <!-- To Stat -->
        <div class="stat-item">
          <label for="toStat">To:</label>
          <select
              id="toStat"
              v-model="toStatId"
              class="small-select"
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
          <DiceNRolls
              v-if="selectedToStat"
              :dice-rolls="selectedToStat.dice_rolls"
              :stat="selectedToStat.name"
              :wide="true"
              class="base-value"
          />
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="modal-actions">
        <LandingButton :action="closeModal">
          Cancel
        </LandingButton>
        <LandingButton :action="confirmSwitch"  :disabled="!fromStatId || !toStatId">
          Swap
        </LandingButton>
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
  background: #2a2a2a;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  color: #fff;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
  text-align: center;
}

.modal-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.modal-description {
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

/* Stat Row */
.stat-row {
  display: flex;
  gap: 1rem;
  justify-content: center;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}

/* Smaller Select */
.small-select {
  width: 150px;
  padding: 0.25rem 0.5rem;
  font-size: 0.9rem;
  border: 1px solid #444;
  border-radius: 4px;
  background: #1a1a1a;
  color: #fff;
  outline: none;
}

.small-select option {
  background: #1a1a1a;
  color: #fff;
}

/* Action Buttons */
.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.confirm-button {
  background: #4caf50;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.confirm-button:disabled {
  background: #555;
  cursor: not-allowed;
}

.cancel-button {
  background: #f44336;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}
</style>
