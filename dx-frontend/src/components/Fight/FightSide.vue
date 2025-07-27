<script setup lang="ts">
import FightSideImage from "@/components/Fight/FightSideImage.vue";

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
</div>
</template>

<style scoped>
.fight-side {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>