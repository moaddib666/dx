<template>
  <div class="dice-roll-result compact">
    <span class="dice">🎲 {{ result.dice_side }}-sided</span>
    <span class="multiplier">x{{ result.multiplier }}</span>
    <span class="outcome">→ {{ result.outcome }}</span>
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #444;
  border-radius: 4px;
  background: #1e1e1e;
  font-size: 0.9rem;
  color: #e0e0e0;
}

.dice-roll-result .dice {
  font-weight: bold;
  color: #ffcc00;
}

.dice-roll-result .multiplier {
  font-weight: bold;
  color: #00ccff;
}

.dice-roll-result .outcome {
  font-weight: bold;
  color: #ff6666;
}
</style>
