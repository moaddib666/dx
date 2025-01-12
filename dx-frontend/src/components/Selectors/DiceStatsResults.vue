<template>
  <div class="swap-results">
    <select
        v-if="editable"
        v-model="localSelectedStat"
        id="selectedStat"
        class="dropdown"
        @change="handleSelectionChange"
    >
      <option
          v-for="result in results.results"
          :key="result.stat"
          :value="result.stat"
      >
        {{ result.stat }} ({{ calculateTotal(result.dice_rolls) }})
      </option>
    </select>
    <DiceNRolls
        v-if="selectedResult"
        :stat="selectedResult.stat"
        :diceRolls="selectedResult.dice_rolls"
    />
  </div>
</template>


<script>
import DiceNRolls from "@/components/Dice/DiceNRolls.vue";

export default {
  name: "SwapResults",
  components: {
    DiceNRolls,
  },
  props: {
    results: {
      type: Object,
      required: true,
    },
    selected: {
      type: String,
      required: true,
    },
    editable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      localSelectedStat: this.selected, // Initialize with selected prop
    };
  },
  computed: {
    selectedResult() {
      return this.results.results.find((r) => r.stat === this.localSelectedStat);
    },
  },
  methods: {
    calculateTotal(diceRolls) {
      const sorted = [...diceRolls.map((d) => d.dice_side)].sort((a, b) => a - b);
      return sorted.slice(1).reduce((sum, roll) => sum + roll, 0);
    },
    handleSelectionChange() {
      this.$emit("selectionChanged", {
        oldId: this.resolveIdForStat(this.selected),
        newId: this.resolveIdForStat(this.localSelectedStat),
      });
    },
    resolveIdForStat(stat) {
      return this.results.results.find((r) => r.stat === stat).id;
    },
  },
};
</script>

<style scoped>
.swap-results {
  display: flex;
  flex-direction: row;
  gap: 1rem;
}

.dropdown {
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.swap-results strong {
  font-size: 1rem;
}
</style>
