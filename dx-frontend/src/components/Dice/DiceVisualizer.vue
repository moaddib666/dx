<template>
  <div class="dice-visualizer">
    <div class="dice-container">
      <!-- Iterate over the dice set -->
      <div
          v-for="(dice, index) in diceSet"
          :key="index"
          class="dice"
          @click="selectDice(dice, index)"
      >
        <span class="dice-label">{{ dice.type }}</span>
      </div>
    </div>
    <div v-if="rolledDiceIndex !== null" class="roll-result">
      <div :class="{ final: isFinalResult }" class="result-number">
        {{ displayResult }}
      </div>
    </div>
    <GlassButton @click="$emit('close')">Done</GlassButton>
  </div>
</template>

<script>
import GlassButton from "@/components/btn/Glass.vue";

export default {
  name: "DiceVisualizer",
  components: {GlassButton},
  props: {
    diceSet: {
      type: Array,
      default: () => [
        {type: "d4", value: 4},
        {type: "d6", value: 6},
        {type: "d8", value: 8},
        {type: "d10", value: 10},
        {type: "d12", value: 12},
        {type: "d20", value: 20},
        {type: "d100", value: 100},
      ],
    },
    result: {
      type: Number,
      default: null, // The final result to display
    },
  },
  data() {
    return {
      rolledDiceIndex: null,
      displayResult: null,
      isFinalResult: false,
      rollInterval: null,
    };
  },
  watch: {
    // Watch for changes in the result prop
    result(newResult) {
      this.stopBlinking(newResult);
    },
  },
  methods: {
    selectDice(dice, index) {
      this.rolledDiceIndex = index;
      this.startBlinking(dice);
      this.$emit("selectedDice", {dice, index});
    },
    startBlinking(dice) {
      const sides = parseInt(dice.type.slice(1));

      // Start random blinking numbers
      this.rollInterval = setInterval(() => {
        this.displayResult = Math.floor(Math.random() * sides) + 1;
      }, 100);
    },
    stopBlinking(finalResult) {
      // Stop blinking and display the final result
      clearInterval(this.rollInterval);
      this.rollInterval = null;
      this.displayResult = finalResult;
      this.isFinalResult = true;

      // Emit the roll result
      const dice = this.diceSet[this.rolledDiceIndex];
      this.$emit("rollResult", {dice, result: finalResult});
    },
  },
};
</script>
<style scoped>
/* Layout and Container Styles */
.dice-visualizer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  padding: 30px;
  background: radial-gradient(circle, rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.5)) fixed;
  border-radius: 15px;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 40px rgba(0, 255, 255, 0.2);
}

.dice-container {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  justify-content: center;
}

.close {
  top: 10px;
  right: 10px;
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: color 0.3s ease;
  background: #00ffcc;
  z-index: 20;
}
/* Futuristic Dice Styles */
.dice {
  width: 100px;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 50%;
  position: relative;
  background-image: url('@/assets/images/dice/dice-bg.png');
  background-size: cover;
  background-position: center;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.dice:hover {
  transform: scale(1.2) rotate(5deg); /* Slight enlargement and rotation */
  box-shadow: 0 0 40px rgba(0, 255, 255, 1); /* Bright glow on hover */
}

.dice-label {
  font-size: 1.5rem;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  text-align: center;
  letter-spacing: 1px;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5), 0 0 20px rgba(0, 255, 255, 0.8);
}

/* Roll Result Styles */
.roll-result {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  animation: fadeIn 0.6s ease forwards;
}

.result-number {
  font-size: 6rem;
  font-weight: bold;
  color: rgba(0, 255, 255, 0.8);
  text-align: center;
  text-shadow: 0 0 30px rgba(0, 255, 255, 0.8), 0 0 60px rgba(0, 255, 255, 0.6);
  transition: transform 0.5s ease, color 0.5s ease;
}

.result-number.final {
  color: rgba(255, 255, 0, 1);
  transform: scale(1.5);
}

/* Animation */
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
