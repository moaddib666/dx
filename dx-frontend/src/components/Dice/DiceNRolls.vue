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
  display: flex;
  gap: 0.5rem;
  flex-direction: row-reverse; /* Reverse to expand left */
  align-items: center;
  justify-content: flex-end;
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
}

.dice.hidden {
  opacity: 0; /* Hidden dice are invisible */
  transform: scale(0); /* Collapse hidden dice */
}

.dice.faded {
  opacity: 0.4;
  color: #888;
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
}

.dice:hover {
  box-shadow: 0 0 0.5em rgba(0, 0, 0, 0.3);
  transform: scale(1.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
</style>
