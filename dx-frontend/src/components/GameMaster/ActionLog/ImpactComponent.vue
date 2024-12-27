<template>
  <div class="impact compact">
    <div class="impact-details">
      <span class="type">Type: {{ impact.type }}</span>
      <span class="violation">Violation: {{ impact.violation }}</span>
      <span class="size">Size: {{ impact.size }}</span>
    </div>
    <SmallCharPreview :char="impact.target" @select="selectTarget"/>
    <DiceRollResult v-if="impact.dice_roll_result" :result="impact.dice_roll_result"/>
  </div>
</template>

<script>
import SmallCharPreview from './SmallCharPreview.vue';
import DiceRollResult from './DiceRollResult.vue';

export default {
  name: 'ImpactComponent',
  components: {
    SmallCharPreview,
    DiceRollResult,
  },
  props: {
    impact: Object,
  },
  methods: {
    selectTarget(id) {
      this.$emit('selectTarget', id);
    },
  },
};
</script>

<style scoped>
.impact.compact {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 1px solid #444;
  border-radius: 4px;
  background: #1c1c1c;
}

.impact-details {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #e0e0e0;
}

.impact-details .type {
  font-weight: bold;
  color: #ffcc00;
}

.impact-details .violation {
  font-weight: bold;
  color: #00ccff;
}

.impact-details .size {
  font-weight: bold;
  color: #ff6666;
}
</style>
