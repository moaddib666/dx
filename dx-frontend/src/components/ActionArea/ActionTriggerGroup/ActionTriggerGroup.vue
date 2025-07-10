<script setup lang="ts">

import ActionTrigger from "@/components/ActionArea/ActionTrigger/ActionTrigger.vue";
</script>

<template>
<!--  Group of Composed components with responsive positioning -->
<div class="trigger__group__holder">
  <!-- EndTurn 100% - Big, Bottom Left -->
  <ActionTrigger image="EndTurn" class="trigger__cta trigger__next-turn"/>
  <!-- ToSafe 75%  Medium, Bottom Right-->
  <ActionTrigger image="ToSafe" class="trigger__cta trigger__safe-place"/>
  <!-- RollDice 50% Small, Top Left -->
  <ActionTrigger image="RollDice" class="trigger__cta trigger__roll-dice"/>
</div>
</template>

<style scoped>
.trigger__group__holder {
  position: relative;
  width: 100%;
  aspect-ratio: 10/9;
  background: #ff5252;
}

.trigger__cta {
  position: absolute;
  transition: transform 0.2s ease-in-out;
}

/* Big component - Bottom Left */
.trigger__next-turn {
  width: 30%;
  aspect-ratio: 1;
  bottom: 0;
  left: 0;
  z-index: 1;
}

/* Medium component - Bottom Right */
.trigger__safe-place {
  width: 20%;
  aspect-ratio: 1;
  bottom: 0;
  margin-bottom: -3%;
  z-index: 0;
  left: 25%;
}

/* Small component - Top Left */
.trigger__roll-dice {
  width: 12%;
  aspect-ratio: 1;
  bottom: 23%;
  left: 3%;
  z-index: 3;
}

</style>