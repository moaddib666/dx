<template>
  <div class="dice-visualizer">
    <div class="dice-container">
      <div
          v-for="(dice, index) in diceSet"
          :key="index"
          :class="['dice', { highlighted: highlightedDice === index, disabled: highlightedDice !== index }]"
          @click="rollDice(dice, index)"
      >
        <span class="dice-label">{{ dice.type }}</span>
      </div>
    </div>
    <div v-if="rolledDiceIndex !== null" class="roll-result">
      <div :class="{ final: isFinalResult }" class="result-number">
        {{ displayResult }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DiceVisualizer",
  props: {
    diceSet: {
      type: Array,
      default: () => [
        {type: "d4"},
        {type: "d6"},
        {type: "d8"},
        {type: "d10"},
        {type: "d12"},
        {type: "d20"},
        {type: "d100"},
      ],
    },
    highlightedDice: {
      type: Number,
      default: -1,
    },
  },
  data() {
    return {
      rolledResult: null,
      rolledDiceIndex: null,
      displayResult: null,
      isFinalResult: false,
    };
  },
  methods: {
    rollDice(dice, index) {
      if (this.highlightedDice !== index) return;

      this.rolledDiceIndex = index;
      this.rolledResult = null; // Reset result for animation
      this.displayResult = null;
      this.isFinalResult = false;

      const sides = parseInt(dice.type.slice(1));

      // Random result simulation
      let randomInterval = setInterval(() => {
        this.displayResult = Math.floor(Math.random() * sides) + 1;
      }, 100);

      // Final result reveal
      setTimeout(() => {
        clearInterval(randomInterval);
        this.rolledResult = Math.floor(Math.random() * sides) + 1;
        this.displayResult = this.rolledResult;
        this.isFinalResult = true;
        this.$emit("rollResult", {dice, result: this.rolledResult});
      }, 2000); // Let the animation run for 2 seconds
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
  background: radial-gradient(circle, #0d0d0d, #000000);
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
  transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
}

.dice.disabled {
  filter: grayscale(80%) brightness(0.7);
  pointer-events: none;
}

.dice.highlighted:hover {
  transform: scale(1.2) rotate(5deg);
  box-shadow: 0 0 40px rgba(0, 255, 255, 1);
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
