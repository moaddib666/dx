<script setup lang="ts">
import {type ChallengeModifier} from "@/api/dx-backend";
import DiceModifier from "@/components/DiceRoller/DiceModifier/DiceModifier.vue";

interface Props {
  modifiers: ChallengeModifier[]
}

const props = withDefaults(defineProps<Props>(), {
  modifiers: () => []
})
</script>

<template>
  <div class="container">
    <DiceModifier
        v-for="(modifier, index) in props.modifiers"
        :key="index"
        :modifier="modifier"
    />
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 0.3em;
  width: 100%;
  padding: 1em;
}
</style>