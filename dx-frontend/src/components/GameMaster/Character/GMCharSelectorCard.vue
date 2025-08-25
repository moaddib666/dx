<script setup lang="ts">
import {OpenaiCharacter} from "@/api/dx-backend";
import {computed} from "vue";

interface Props {
  character: OpenaiCharacter
  selected: boolean
}


const props = defineProps<Props>();
const avatarUrl = computed(() => {
  return props.character?.biography?.avatar || 'https://via.placeholder.com/150';
})
</script>

<template>
  <div class="selector-card" :class="{selected: props.selected}">
    <div class="avatar-container">
      <img :src="avatarUrl" :alt="props.character.name" class="avatar"/>
    </div>
    <div class="character-info">
      <h3 class="character-name">{{ props.character.name }}</h3>
      <p class="character-rank">{{ props.character.rank.name }}</p>
    </div>
  </div>
</template>

<style scoped>
.selector-card {
  aspect-ratio: 4 / 5;
  display: flex;
  flex-direction: column;
  padding: 0.525rem;
  border: 2px solid transparent;
  border-radius: 0.35rem;
  cursor: pointer;
  transition: border-color 0.3s, background-color 0.3s, transform 0.2s ease;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(4px);
  height: 100%;
}

.selector-card:hover {
  background: rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}

.selector-card.selected {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
}

.avatar-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.35rem;
  overflow: hidden;
  border-radius: 0.263rem;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.263rem;
}

.character-info {
  flex-shrink: 0;
  text-align: center;
  padding-top: 0.175rem;
}

.character-name {
  margin: 0 0 0.175rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  line-height: 1.2;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.character-rank {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 400;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: rgba(250, 218, 149, 0.7);
  line-height: 1.1;
}
</style>