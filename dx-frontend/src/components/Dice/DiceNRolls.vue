<template>
  <div class="dice-container" @click="toggleExpanded">
    <!-- Display the total result -->
    <div class="dice summary" aria-label="Dice Roll Summary">
      {{ calculateTotal(diceRolls) }}
    </div>

    <!-- Display each dice roll, hidden by default -->
    <div
        v-for="(dice, index) in diceRolls"
        :key="index"
        class="dice"
        :class="{ faded: isFaded(index), hidden: !isExpanded }"
        :aria-label="'Dice Roll: ' + dice.dice_side"
    >
      {{ dice.dice_side }}
    </div>
  </div>
</template>

<script>
export default {
  name: "DiceNRolls",
  props: {
    wide: {
      type: Boolean,
      default: false,
    },
    stat: {
      type: String,
      required: true,
    },
    diceRolls: {
      type: Array,
      required: true,
    },
    fadeCount: {
      type: Number,
      default: 1, // Number of lowest values to fade out
    },
  },
  data() {
    return {
      isExpanded: this.wide, // Controls the visibility of dice rolls
      fadedIndexes: [],
    };
  },
  computed: {
    sortedDice() {
      // Sort the dice values once for performance
      return [...this.diceRolls.map(d => d.dice_side)].sort((a, b) => a - b);
    },
  },
  methods: {
    calculateFadeIndexes() {
      // Calculate the indexes of the lowest dice rolls
      const fadeCount = Math.min(this.fadeCount, this.diceRolls.length);
      const diceToFade = this.sortedDice.slice(0, fadeCount);
      const usedIndexes = new Set(); // Track used indexes to handle duplicates
      this.fadedIndexes = diceToFade.map((value) => {
        const index = this.diceRolls.findIndex(
            (d, i) => d.dice_side === value && !usedIndexes.has(i)
        );
        usedIndexes.add(index); // Mark this index as used
        return index;
      });
    },
    isFaded(index) {
      // Check if the dice roll should be faded
      return this.fadedIndexes.includes(index);
    },
    calculateTotal(diceRolls) {
      if (!diceRolls.length) return 0; // Handle empty dice rolls
      const fadeCount = Math.min(this.fadeCount, diceRolls.length);
      const sorted = [...diceRolls.map(d => d.dice_side)].sort((a, b) => a - b);
      return sorted.slice(fadeCount).reduce((sum, roll) => sum + roll, 0);
    },
    toggleExpanded() {
      this.isExpanded = !this.isExpanded;
    },
  },
  watch: {
    // Recalculate faded indexes whenever diceRolls or fadeCount changes
    diceRolls: {
      handler: "calculateFadeIndexes",
      immediate: true,
    },
    fadeCount: "calculateFadeIndexes",
  },
};
</script>

<style scoped>
.dice-container {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer; /* Indicate interactivity */
  padding: 0.2em; /* Proper padding from parent */
}

.dice {
  width: 1.5em;
  height: 1.5em;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fada95, #e8c478);
  border: 1px solid #333;
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  font-weight: 600;
  color: #222;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.75em;
  transition: all 0.3s ease-in-out; /* Smooth transition */
  position: absolute;
  z-index: 10;
}

.dice.hidden {
  display: none; /* Completely remove from layout */
}

.dice.faded {
  color: #666;
  background: linear-gradient(135deg, #c4b085, #b5a078) !important;
  border: 1px solid #888;
}

.dice.summary {
  width: 2.25em;
  height: 2.25em;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fada95, #e8c478);
  border: 2px solid #333;
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  font-weight: 700;
  color: #222;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.9em;
  position: relative;
  z-index: 5;
}

.dice:not(.summary):not(.hidden) {
  /* Position expanded dice to the left of the summary */
}

.dice:not(.summary):not(.hidden):nth-child(2) {
  right: 2.625em; /* Position first expanded dice (3.5 * 0.75) */
  top: 50%;
  transform: translateY(-50%);
}

.dice:not(.summary):not(.hidden):nth-child(3) {
  right: 4.5em; /* Position second expanded dice (6 * 0.75) */
  top: 50%;
  transform: translateY(-50%);
}

.dice:not(.summary):not(.hidden):nth-child(4) {
  right: 6.375em; /* Position third expanded dice (8.5 * 0.75) */
  top: 50%;
  transform: translateY(-50%);
}

.dice:not(.summary):not(.hidden):nth-child(5) {
  right: 8.25em; /* Position fourth expanded dice (11 * 0.75) */
  top: 50%;
  transform: translateY(-50%);
}

.dice:not(.summary):not(.hidden):nth-child(6) {
  right: 10.125em; /* Position fifth expanded dice (13.5 * 0.75) */
  top: 50%;
  transform: translateY(-50%);
}

.dice:not(.summary):not(.hidden):nth-child(7) {
  right: 12em; /* Position sixth expanded dice (16 * 0.75) */
  top: 50%;
  transform: translateY(-50%);
}

.dice:hover {
  box-shadow: 0 0 0.5em rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.dice.summary:hover {
  transform: scale(1.1);
}

.dice:not(.summary):not(.hidden):hover {
  transform: translateY(-50%) scale(1.1);
}
</style>
