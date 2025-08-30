<template>
  <div class="dice-roll-result compact">
    <span class="dice">{{ result.dice_side }}
    </span>
  </div>
</template>

<script>
export default {
  name: 'DiceRollResult',
  props: {
    result: Object,
  },
};
</script>

<style scoped>
.dice-roll-result.compact {
  margin: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #e0e0e0;
  text-align: center;
}

.dice-roll-result .dice {
  flex: 1;
  font-weight: bold;
  color: #ffcc00;
}

.dice-roll-result .multiplier {
  flex: 1;
  font-weight: bold;
  color: #00ccff;
}

.dice-roll-result .outcome {
  flex: 1;
  font-weight: bold;
  font-size: 0.5rem;
  color: #ff6666;
  text-shadow: rgba(0, 0, 0, 0.7) 1px 1px 2px;
}

.dice {
  background: url("@/assets/icons/dice.png") no-repeat center center;
  background-size: contain;
  padding: 0.5rem;
}
</style>
