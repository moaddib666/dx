<script setup lang="ts">

import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import {OpenaiCharacter} from "@/api/dx-backend";
import GmCharSelectorCard from "@/components/GameMaster/Character/GMCharSelectorCard.vue";
import {ref, computed} from "vue";

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
  filterByPosition: [positionId: string];
  filterByOrganisation: [orgId: string];
}>();

// Filter state
const searchQuery = ref('');
const selectedOrgId = ref('');
const selectedNpcFilter = ref('');
const selectedPositionId = ref('');

// Get unique organizations from characters
const organizations = computed(() => {
  const orgs = new Set<string>();
  props.characters.forEach(char => {
    if (char.organization?.id) {
      orgs.add(char.organization.id);
    }
  });
  return Array.from(orgs).map(id => {
    const char = props.characters.find(c => c.organization?.id === id);
    return {
      id,
      name: char?.organization?.name || `Organization ${id.slice(0, 8)}`
    };
  });
});

// Filtered characters based on search and filters
const filteredCharacters = computed(() => {
  let filtered = props.characters;

  // Apply search query (name, id, or position)
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    filtered = filtered.filter(char =>
      char.name.toLowerCase().includes(query) ||
      char.id.toLowerCase().includes(query) ||
      char.path?.id?.toLowerCase().includes(query) ||
      char.rank?.name?.toLowerCase().includes(query)
    );
  }

  // Apply organization filter
  if (selectedOrgId.value) {
    filtered = filtered.filter(char => char.organization?.id === selectedOrgId.value);
  }

  // Apply position filter
  if (selectedPositionId.value) {
    filtered = filtered.filter(char => char.path?.id === selectedPositionId.value);
  }

  // Apply NPC filter
  if (selectedNpcFilter.value !== '') {
    const isNpc = selectedNpcFilter.value === 'true';
    filtered = filtered.filter(char => char.npc === isNpc);
  }

  return filtered;
});

// Fast action handlers
const copyCharacterId = (characterId: string) => {
  navigator.clipboard.writeText(characterId);
};

const filterByCharacterPosition = (character: OpenaiCharacter) => {
  if (character.path?.id) {
    selectedPositionId.value = character.path.id;
    emit('filterByPosition', character.path.id);
  }
};

const filterByCharacterOrganisation = (character: OpenaiCharacter) => {
  if (character.organization?.id) {
    selectedOrgId.value = character.organization.id;
    emit('filterByOrganisation', character.organization.id);
  }
};
</script>

<template>
  <RPGContainer class="char-selector-container">
    <div class="header">
      <h2 class="title">Character Selector</h2>

      <!-- Filter Controls -->
      <div class="filters">
        <!-- Search Input -->
        <div class="filter-group">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by name, ID, position..."
            class="search-input"
          />
        </div>

        <!-- Organization Filter -->
        <div class="filter-group">
          <select v-model="selectedOrgId" class="filter-select">
            <option value="">All Organizations</option>
            <option v-for="org in organizations" :key="org.id" :value="org.id">
              {{ org.name }}
            </option>
          </select>
        </div>

        <!-- NPC Filter -->
        <div class="filter-group">
          <select v-model="selectedNpcFilter" class="filter-select">
            <option value="">All Characters</option>
            <option value="true">NPCs Only</option>
            <option value="false">Players Only</option>
          </select>
        </div>
      </div>
    </div>

    <div class="characters-grid-wrapper">
      <div class="characters-grid">
        <GmCharSelectorCard
          v-for="character in filteredCharacters"
          :key="character.id"
          :character="character"
          :selected="character.id === props.selectedCharacterId"
          class="character-card"
          @click="emit('select', character.id)"
          @copy-id="copyCharacterId"
          @filter-by-position="filterByCharacterPosition"
          @filter-by-organisation="filterByCharacterOrganisation"
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
  margin: 0 0 0.7rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  text-align: center;
}

.filters {
  display: flex;
  gap: 0.525rem;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.filter-group {
  flex: 1;
  min-width: 140px;
}

.search-input,
.filter-select {
  width: 100%;
  padding: 0.35rem 0.525rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 400;
  transition: border-color 0.3s, background-color 0.3s;
}

.search-input::placeholder {
  color: rgba(250, 218, 149, 0.5);
}

.search-input:focus,
.filter-select:focus {
  outline: none;
  border-color: #7fff16;
  background: rgba(0, 0, 0, 0.6);
}

.filter-select option {
  background: rgba(0, 0, 0, 0.9);
  color: #fada95;
}

/* Responsive filters */
@media (max-width: 640px) {
  .filters {
    flex-direction: column;
  }

  .filter-group {
    min-width: 100%;
  }
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