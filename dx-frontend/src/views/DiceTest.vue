<template>
  <div>
    <DiceVisualizer :highlightedDice="highlightedDice" @rollResult="handleRollResult"/>
    <button @click="unlockNextDice">Unlock Next Dice</button>
  </div>
</template>

<script>
import DiceVisualizer from "@/components/Dice/DiceVisualizer.vue";
import {ensureConnection} from "@/api/dx-websocket/index.ts";

export default {
  components: { DiceVisualizer },
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
    handleRollResult({ dice, result }) {
      console.log(`Rolled ${dice.type}: ${result}`);
    },
    handleCentrifugoEvent(data) {
      // Debug incoming Centrifugo events
      console.log("Debug Centrifugo event:", data);

      // Optionally, if the event contains a roll result, trigger your roll handler
      if (data && data.eventType === "roll") {
        this.handleRollResult(data);
      }
    },
  },
  mounted() {
    const bus = ensureConnection();
    // Subscribe to the event bus when component mounts
  },
  unmounted() {
    // Unsubscribe to prevent memory leaks
  },
};
</script>
