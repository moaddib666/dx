<template>
  <div class="impact">
    <SmallCharPreview
        :char="{
      id: impact.target,
    }"
    />
    <span class="impact-type">Type: {{ impact.type }}</span>
    <span class="impact-violation">Violation: {{ impact.violation }}</span>
    <span class="impact-size">Size: {{ impact.size }}</span>

    <DiceRollResult v-if="impact.dice_roll_result" :result="impact.dice_roll_result" />
  </div>
</template>

<script>

import SmallCharPreview from "@/components/GameMaster/ActionLog/SmallCharPreview.vue";
import DiceRollResult from "@/components/GameMaster/ActionLog/DiceRollResult.vue";

export default {
  name: 'ImpactComponent',
  components: {
    SmallCharPreview,
    DiceRollResult,
  },
  props: {
    impact: Object,
  },
};
</script>

<style scoped>
.impact {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: 1rem;
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
