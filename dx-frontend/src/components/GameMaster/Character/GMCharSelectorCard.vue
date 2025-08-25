<script setup lang="ts">
import {OpenaiCharacter} from "@/api/dx-backend";

interface Props {
  character: OpenaiCharacter
  selected: boolean
}

const props = defineProps<Props>();
</script>

<template>
  <div class="selector-card" :class="{selected: props.selected}">
    <img :src="props.character.biography.avatar" :alt="props.character.name" class="w-16 h-16 rounded-full object-cover"/>
    <div class="ml-4">
      <h3 class="text-lg font-semibold">{{ props.character.name }}</h3>
      <p class="text-sm text-gray-500">{{ props.character.rank.name }}</p>
    </div>
  </div>
</template>

<style scoped>
.selector-card {
  aspect-ratio: 4 / 1;
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 2px solid transparent;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: border-color 0.3s, background-color 0.3s;
}

.selector-card.selected {
  border-color: #7fff16; /* Blue border when selected */
}
</style>