<script setup lang="ts">

import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import {OpenaiCharacter} from "@/api/dx-backend";
import GmCharSelectorCard from "@/components/GameMaster/Character/GMCharSelectorCard.vue";

interface Filter {
  name?: string;
  id?: string;
  positionId?: string;
  orgId?: string;
  npc?: boolean;
}

interface Props {
  characters: OpenaiCharacter[];
  isDraggable?: boolean;
  filtered?: Filter;
  selectedCharacterId?: string;
}

const props = withDefaults(defineProps<Props>(), {
  isDraggable: false,
  filtered: () => ({} as Filter),
  selectedCharacterId: undefined,
});
</script>

<template>
  <RPGContainer class="container">
    <!--  H2 Character GmCharSelector  -->
    <!--  Input for search/filter {name,id, positionId}  -->
    <!--  Drop Down for filter organisation(orgId) -->
    <!--  Drop Down for filter npc(bool) -->
    <!--  Character Grid  -->
    <!-- Character Avatar -->
    <!-- CopyId,  FilterByThisCharacterPosition,  FilterByThisCharacterOrganisation -->
    <!-- Infinite Scroll -->
    <GmCharSelectorCard class="character-card"
        v-for="character in props.characters"
        :key="character.id"
        :character="character"
        :selected="character.id === props.selectedCharacterId"
    />
  </RPGContainer>

</template>

<style scoped>
.container {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  overflow-y: auto;
}
.character-card {
  margin: 0.5rem 0;
  cursor: pointer;
  transition: transform 0.2s;
}
.character-card:hover {
  transform: scale(1.05);
}
.character-card:active {
  transform: scale(0.95);
}


</style>