<script setup lang="ts">

import ActionTrigger from "@/components/ActionArea/ActionTrigger/ActionTrigger.vue";
</script>

<template>
<div class="trigger__group__holder">
  <!-- EndTurn 100% - Left,Bottom -->
  <ActionTrigger image="EndTurn" class="trigger__cta trigger__next-turn"/>
  <!-- ToSafe 75%  Right, Bottom-->
  <ActionTrigger image="ToSafe" class="trigger__cta trigger__safe-place"/>
  <!-- RollDice 50% Left,Top -->
  <ActionTrigger image="RollDice" class="trigger__cta trigger__roll-dice"/>
</div>
</template>

<style scoped>
.trigger__group__holder {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 1rem;
  background: #00e5ff;
}

.trigger__next-turn {
  display: flex;
  align-items: center;
  justify-content: center;
  bottom: 0;
  left: 0;
}
.trigger__safe-place {
  display: flex;
  align-items: center;
  justify-content: center;
  bottom: 0;
  right: 0;
}
.trigger__roll-dice {
  display: flex;
  align-items: center;
  justify-content: center;
  top: 0;
  left: 0;
}
</style>