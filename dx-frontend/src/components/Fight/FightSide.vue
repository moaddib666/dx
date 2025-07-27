<script setup lang="ts">
import FightSideImage from "@/components/Fight/FightSideImage.vue";
import FightCharacter from "@/components/Fight/FightCharacter.vue";

const props = defineProps<{
  direction?: 'left' | 'right';
  side?: "mage" | "tech";
}>();

// Default values if props are not provided
const direction = props.direction || 'left';
const side = props.side || 'mage';
</script>

<template>
<div class="fight-side">
  <FightSideImage :direction="direction" :side="side"></FightSideImage>
  <FightCharacter class="character-info"></FightCharacter>
</div>
</template>

<style scoped>
.fight-side {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}
.character-info {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2; /* Ensure character info is above the background */
}
</style>