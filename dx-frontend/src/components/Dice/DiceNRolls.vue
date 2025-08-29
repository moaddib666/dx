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

<style>
.dice-container {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer; /* Indicate interactivity */
}

.dice {
  width: 2em;
  height: 2em;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, silver, lightgray);
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  font-weight: bold;
  color: #000;
  transition: all 0.3s ease-in-out; /* Smooth transition */
  position: absolute;
  z-index: 10;
}

.dice.hidden {
  display: none; /* Completely remove from layout */
}

.dice.faded {
  opacity: 0.7;
  color: #555;
  background: linear-gradient(135deg, rgba(200, 200, 200, 0.9), rgba(160, 160, 160, 0.9)) !important;
  border: 1px solid rgba(0, 0, 0, 0.3);
}

.dice.summary {
  width: 3em;
  height: 3em;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, silver, lightgray);
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  font-weight: bold;
  color: #000;
  position: relative;
  z-index: 5;
}

.dice:not(.summary):not(.hidden) {
  /* Position expanded dice to the left of the summary */
}

.dice:not(.summary):not(.hidden):nth-child(2) {
  right: 3.5em; /* Position first expanded dice */
  top: 50%;
  transform: translateY(-50%);
}

.dice:not(.summary):not(.hidden):nth-child(3) {
  right: 6em; /* Position second expanded dice */
  top: 50%;
  transform: translateY(-50%);
}

.dice:not(.summary):not(.hidden):nth-child(4) {
  right: 8.5em; /* Position third expanded dice */
  top: 50%;
  transform: translateY(-50%);
}

.dice:not(.summary):not(.hidden):nth-child(5) {
  right: 11em; /* Position fourth expanded dice */
  top: 50%;
  transform: translateY(-50%);
}

.dice:not(.summary):not(.hidden):nth-child(6) {
  right: 13.5em; /* Position fifth expanded dice */
  top: 50%;
  transform: translateY(-50%);
}

.dice:not(.summary):not(.hidden):nth-child(7) {
  right: 16em; /* Position sixth expanded dice */
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
