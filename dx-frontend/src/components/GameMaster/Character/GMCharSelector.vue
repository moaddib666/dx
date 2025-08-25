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
const emit = defineEmits<{
  select: [characterId: string];
}>();
</script>

<template>
  <RPGContainer class="char-selector-container">
    <div class="header">
      <h2 class="title">Character Selector</h2>
    </div>

    <div class="characters-grid-wrapper">
      <div class="characters-grid">
        <GmCharSelectorCard
          v-for="character in props.characters"
          :key="character.id"
          :character="character"
          :selected="character.id === props.selectedCharacterId"
          class="character-card"
          @click="emit('select', character.id)"
        />
      </div>
    </div>
  </RPGContainer>
</template>

<style scoped>
.char-selector-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 400px;
  max-height: 600px;
}

.header {
  flex-shrink: 0;
  margin-bottom: 0.7rem;
}

.title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  text-align: center;
}

.characters-grid-wrapper {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 0.35rem;
}

.characters-grid {
  display: grid;
  gap: 0.525rem;
  padding: 0.175rem;

  /* Mobile first - 1 column */
  grid-template-columns: 1fr;
}

/* Small tablets and large phones - 2 columns */
@media (min-width: 640px) {
  .characters-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Tablets - 3 columns */
@media (min-width: 768px) {
  .characters-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Small desktops - 4 columns */
@media (min-width: 1024px) {
  .characters-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Large desktops - 5 columns */
@media (min-width: 1280px) {
  .characters-grid {
    grid-template-columns: repeat(5, 1fr);
  }
}

/* Extra large screens - 6 columns */
@media (min-width: 1536px) {
  .characters-grid {
    grid-template-columns: repeat(6, 1fr);
  }
}

.character-card {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 0.5rem;
  overflow: hidden;
}

.character-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.character-card:active {
  transform: translateY(0);
}

/* Custom scrollbar styling for RPG theme */
.characters-grid-wrapper::-webkit-scrollbar {
  width: 8px;
}

.characters-grid-wrapper::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.characters-grid-wrapper::-webkit-scrollbar-thumb {
  background: rgba(127, 255, 22, 0.6);
  border-radius: 4px;
}

.characters-grid-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(127, 255, 22, 0.8);
}
</style>