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
}

.trigger__cta {
  position: absolute;
  transition: transform 0.2s ease-in-out;
}

/* Big component - Bottom Left */
.trigger__next-turn {
  width: 80%;
  aspect-ratio: 1;
  bottom: 0;
  left: 0;
  z-index: 1;
}

/* Medium component - Bottom Right */
.trigger__safe-place {
  width: 53%;
  aspect-ratio: 1;
  bottom: 0;
  margin-bottom: -8%;
  z-index: 0;
  left: 67%;
}

/* Small component - Top Left */
.trigger__roll-dice {
  width: 32%;
  aspect-ratio: 1;
  bottom: 40%;
  left: 5%;
  z-index: 3;
}

</style>