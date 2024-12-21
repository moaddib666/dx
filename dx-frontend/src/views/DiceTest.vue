<template>
  <div>
    <DiceVisualizer :highlightedDice="highlightedDice" @rollResult="handleRollResult"/>
    <button @click="unlockNextDice">Unlock Next Dice</button>
  </div>
</template>

<script>
import DiceVisualizer from "@/components/Dice/DiceVisualizer.vue";

export default {
  components: {DiceVisualizer},
  data() {
    return {
      highlightedDice: 0, // Start with the first dice highlighted
    };
  },
  methods: {
    unlockNextDice() {
      // Rotate through the dice indices
      this.highlightedDice = (this.highlightedDice + 1) % 7;
      console.log("New highlightedDice:", this.highlightedDice);
    },
    handleRollResult({dice, result}) {
      console.log(`Rolled ${dice.type}: ${result}`);
    },
  },
};
</script>
