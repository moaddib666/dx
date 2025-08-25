<script setup lang="ts">
import {OpenaiCharacter} from "@/api/dx-backend";
import {computed} from "vue";

interface Props {
  character: OpenaiCharacter
  selected: boolean
}

const props = defineProps<Props>();
const emit = defineEmits<{
  'copy-id': [characterId: string];
  'filter-by-position': [character: OpenaiCharacter];
  'filter-by-organisation': [character: OpenaiCharacter];
}>();

const avatarUrl = computed(() => {
  return props.character?.biography?.avatar || 'https://via.placeholder.com/150';
});

// Fast action handlers
const handleCopyId = (event: Event) => {
  event.stopPropagation();
  emit('copy-id', props.character.id);
};

const handleFilterByPosition = (event: Event) => {
  event.stopPropagation();
  emit('filter-by-position', props.character);
};

const handleFilterByOrganisation = (event: Event) => {
  event.stopPropagation();
  emit('filter-by-organisation', props.character);
};
</script>

<template>
  <div class="selector-card" :class="{selected: props.selected}">
    <div class="avatar-container">
      <img :src="avatarUrl" :alt="props.character.name" class="avatar"/>

      <!-- Fast Actions Overlay -->
      <div class="fast-actions">
        <button
          class="action-btn copy-btn"
          title="Copy Character ID"
          @click="handleCopyId"
        >
          📋
        </button>
        <button
          class="action-btn position-btn"
          title="Filter by Position"
          @click="handleFilterByPosition"
          v-if="props.character.path?.id"
        >
          🎯
        </button>
        <button
          class="action-btn org-btn"
          title="Filter by Organisation"
          @click="handleFilterByOrganisation"
          v-if="props.character.campaign?.id"
        >
          🏛️
        </button>
      </div>
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
  position: relative;
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

/* Fast Actions Overlay */
.fast-actions {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 0.263rem;
}

.selector-card:hover .fast-actions {
  opacity: 1;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.1rem;
  height: 2.1rem;
  border: 2px solid rgba(127, 255, 22, 0.6);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.6);
  color: #fada95;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(2px);
}

.action-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.2);
  transform: scale(1.1);
}

.action-btn:active {
  transform: scale(0.95);
}

/* Specific button styling */
.copy-btn:hover {
  background: rgba(100, 149, 237, 0.2);
  border-color: #6495ed;
}

.position-btn:hover {
  background: rgba(255, 165, 0, 0.2);
  border-color: #ffa500;
}

.org-btn:hover {
  background: rgba(138, 43, 226, 0.2);
  border-color: #8a2be2;
}
</style>