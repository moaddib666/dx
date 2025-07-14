<template>
  <div class="chapter-summary">
    <h3>
      <span class="icon">📊</span> Chapter Summary
    </h3>

    <!-- Characters Section -->
    <div class="summary-section">
      <h4>
        <span class="icon">👤</span> Characters ({{ characters.length }})
      </h4>
      <div v-if="!characters.length" class="empty-section-message">
        No characters involved in this chapter.
      </div>
      <div v-else class="character-grid">
        <div
          v-for="character in characters"
          :key="character.id"
          class="character-card"
          @click="highlightCharacter(character)"
        >
          <div class="character-icon">
            <span class="icon">👤</span>
          </div>
          <div class="character-info">
            <div class="character-name">{{ character.name }}</div>
            <div class="character-id">ID: {{ character.id }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Items Section -->
    <div class="summary-section">
      <h4>
        <span class="icon">📦</span> Items ({{ items.length }})
      </h4>
      <div v-if="!items.length" class="empty-section-message">
        No items involved in this chapter.
      </div>
      <div v-else class="item-grid">
        <div
          v-for="item in items"
          :key="item.id"
          class="item-card"
          @click="highlightItem(item)"
        >
          <div class="item-icon">
            <span class="icon">📦</span>
          </div>
          <div class="item-info">
            <div class="item-name">{{ item.name }}</div>
            <div class="item-id">ID: {{ item.id }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Locations Section -->
    <div class="summary-section">
      <h4>
        <span class="icon">📍</span> Locations ({{ locations.length }})
      </h4>
      <div v-if="!locations.length" class="empty-section-message">
        No locations involved in this chapter.
      </div>
      <div v-else class="location-list">
        <div
          v-for="location in locations"
          :key="location.id"
          class="location-item"
          @click="highlightLocation(location)"
        >
          <div class="location-icon">
            <span class="icon">📍</span>
          </div>
          <span class="location-name">{{ location.name }}</span>
        </div>
      </div>
    </div>

    <!-- Quest Statistics -->
    <div class="summary-section">
      <h4><span class="icon">📊</span> Statistics</h4>
      <div class="stats-grid">
        <div class="stat-item">
          <span class="stat-label">Total Quests:</span>
          <span class="stat-value">{{ chapter.quests?.length || 0 }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Total Experience:</span>
          <span class="stat-value">{{ calculateTotalExperience() }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Avg. Cycle Limit:</span>
          <span class="stat-value">{{ calculateAverageCycleLimit() }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, computed } from 'vue';
import { Chapter } from '@/api/dx-backend';

interface Character {
  id: string;
  name: string;
}

interface Item {
  id: string;
  name: string;
}

interface GameObject {
  id: string;
  name: string;
  type: string;
}

const props = defineProps<{
  chapter: Chapter;
  characters: Character[];
  items: Item[];
  gameObjects?: GameObject[];
}>();

// Computed properties
const locations = computed(() => {
  if (props.gameObjects) {
    return props.gameObjects.filter(obj => obj.type === 'location');
  }
  return [];
});

// Helper functions
const calculateTotalExperience = (): number => {
  let totalXP = 0;

  props.chapter.quests?.forEach(quest => {
    // Sum XP from success rewards
    if (quest.onSuccess?.tokens) {
      const xpToken = quest.onSuccess.tokens.find(token => token.tokenId === 'xp' || token.tokenId === 'experience');
      if (xpToken) {
        totalXP += xpToken.amount || 0;
      }
    }

    // Sum XP from failure rewards (if applicable)
    if (quest.onFailure?.tokens) {
      const xpToken = quest.onFailure.tokens.find(token => token.tokenId === 'xp' || token.tokenId === 'experience');
      if (xpToken) {
        totalXP += xpToken.amount || 0;
      }
    }
  });

  return totalXP;
};

const calculateAverageCycleLimit = (): string => {
  if (!props.chapter.quests?.length) return '0';

  let totalCycles = 0;
  let questsWithCycles = 0;

  props.chapter.quests.forEach(quest => {
    if (quest.cycleLimit) {
      totalCycles += quest.cycleLimit;
      questsWithCycles++;
    }
  });

  if (questsWithCycles === 0) return 'No limit';

  return (totalCycles / questsWithCycles).toFixed(1);
};

// Event handlers
const highlightCharacter = (character: Character) => {
  console.log('Highlight character:', character);
  // This would typically highlight the character in the quest details
};

const highlightItem = (item: Item) => {
  console.log('Highlight item:', item);
  // This would typically highlight the item in the quest details
};

const highlightLocation = (location: GameObject) => {
  console.log('Highlight location:', location);
  // This would typically highlight the location in the quest details
};
</script>

<style scoped>
.chapter-summary {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.chapter-summary h3 {
  font-size: 1.3rem;
  color: var(--cyber-yellow, #ffd700);
  margin-top: 0;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  padding-bottom: 0.75rem;
}

.chapter-summary h3 .icon {
  margin-right: 0.5rem;
}

.summary-section {
  margin-bottom: 1.5rem;
}

.summary-section h4 {
  font-size: 1.1rem;
  color: white;
  margin-top: 0;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.summary-section h4 .icon {
  margin-right: 0.5rem;
}

.empty-section-message {
  text-align: center;
  padding: 1rem;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  font-size: 0.9rem;
}

.character-grid, .item-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.75rem;
}

.character-card, .item-card {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
}

.character-card:hover, .item-card:hover {
  background: rgba(255, 215, 0, 0.1);
  transform: translateY(-2px);
}

.character-icon, .item-icon, .location-icon {
  width: 32px;
  height: 32px;
  min-width: 32px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
}

.character-info, .item-info {
  overflow: hidden;
}

.character-name, .item-name, .location-name {
  font-size: 0.9rem;
  color: white;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.character-id, .item-id {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
}

.location-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.location-item {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.location-item:hover {
  background: rgba(255, 215, 0, 0.1);
  transform: translateX(2px);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
}

.stat-item {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 0.75rem;
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.5rem;
}

.stat-value {
  display: block;
  font-size: 1.2rem;
  color: var(--cyber-yellow, #ffd700);
  font-weight: bold;
}

.icon {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .chapter-summary {
    padding: 1rem;
  }

  .character-grid, .item-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>