<template>
  <div class="impact">
    <SmallCharPreview :char="impact.target" @select="handleSelect" />
    <span class="impact-type">Type: {{ impact.type }}</span>
    <span class="impact-violation">Violation: {{ impact.violation }}</span>
    <span class="impact-size">Size: {{ impact.size }}</span>

    <DiceRollResult v-if="impact.dice_roll_result" :result="impact.dice_roll_result" />
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
    handleSelect(id) {
      this.$emit('selectTarget', id);
    },
  },
};
</script>

<style scoped>
.impact {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: 1px solid #444;
  border-radius: 4px;
  padding: 0.3rem;
  background: #202020;
  font-size: 0.8rem;
}

.impact-type, .impact-violation, .impact-size {
  font-weight: bold;
  color: #e0e0e0;
}

.impact-type {
  color: #ffcc00;
}

.impact-violation {
  color: #00ccff;
}

.impact-size {
  color: #ff6666;
}
</style>
