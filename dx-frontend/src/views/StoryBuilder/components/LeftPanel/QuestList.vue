<template>
  <div class="quest-list">
    <div class="quest-list-header">
      <h3>Quests</h3>
      <button
        v-if="editMode"
        @click="$emit('create')"
        class="btn-create-quest"
      >
        <span class="icon">+</span> Add Quest
      </button>
    </div>

    <div v-if="quests.length === 0" class="no-quests-message">
      No quests available for this chapter.
      <div v-if="editMode" class="create-first-quest">
        <button @click="$emit('create')" class="btn-create-first">
          Create your first quest
        </button>
      </div>
    </div>

    <div v-else class="quests-container">
      <div
        v-for="quest in quests"
        :key="quest.id"
        :class="[
          'quest-item',
          { 'quest-item--selected': selectedQuest?.id === quest.id }
        ]"
        @click="$emit('select', quest)"
      >
        <div class="quest-icon">
          <span class="quest-icon-symbol">📜</span>
        </div>

        <div class="quest-content">
          <h4 class="quest-title">{{ quest.title }}</h4>
          <p class="quest-description">{{ truncateDescription(quest.description) }}</p>

          <div class="quest-meta">
            <div class="quest-objectives">
              <span class="icon">🎯</span>
              {{ quest.objectives?.length || 0 }} objectives
            </div>

            <div class="quest-cycle-limit" v-if="quest.cycleLimit">
              <span class="icon">⏱️</span>
              {{ quest.cycleLimit }} cycles
            </div>
          </div>
        </div>

        <div v-if="editMode" class="quest-actions">
          <button @click.stop="$emit('edit', quest)" class="action-button">
            <span class="icon">✏️</span>
          </button>
          <button @click.stop="$emit('delete', quest.id)" class="action-button">
            <span class="icon">🗑️</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import { Quest } from '@/api/dx-backend';

const props = defineProps<{
  quests: Quest[];
  selectedQuest: Quest | null;
  editMode: boolean;
}>();

defineEmits<{
  (e: 'select', quest: Quest): void;
  (e: 'create'): void;
  (e: 'edit', quest: Quest): void;
  (e: 'delete', questId: string): void;
}>();

// Helper function to truncate long descriptions
const truncateDescription = (description: string | undefined): string => {
  if (!description) return '';
  return description.length > 100 ? `${description.substring(0, 100)}...` : description;
};
</script>

<style scoped>
.quest-list {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.quest-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.quest-list-header h3 {
  font-size: 1.2rem;
  color: var(--cyber-yellow, #ffd700);
  margin: 0;
}

.btn-create-quest {
  background: rgba(255, 215, 0, 0.2);
  color: var(--cyber-yellow, #ffd700);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

.btn-create-quest:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: translateY(-2px);
}

.no-quests-message {
  text-align: center;
  padding: 2rem;
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
}

.create-first-quest {
  margin-top: 1rem;
}

.btn-create-first {
  background: rgba(255, 215, 0, 0.2);
  color: var(--cyber-yellow, #ffd700);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-create-first:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: translateY(-2px);
}

.quests-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 400px;
  overflow-y: auto;
}

.quest-item {
  display: flex;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.quest-item:hover {
  background: rgba(255, 215, 0, 0.1);
  transform: translateY(-2px);
}

.quest-item--selected {
  background: rgba(255, 215, 0, 0.15);
  border-left: 3px solid var(--cyber-yellow, #ffd700);
}

.quest-icon {
  width: 40px;
  height: 40px;
  min-width: 40px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
}

.quest-icon-symbol {
  font-size: 1.2rem;
}

.quest-content {
  flex: 1;
}

.quest-title {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: white;
}

.quest-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.75rem;
}

.quest-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
}

.quest-objectives, .quest-cycle-limit {
  display: flex;
  align-items: center;
}

.icon {
  margin-right: 5px;
}

.quest-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
}

.action-button {
  background: rgba(0, 0, 0, 0.3);
  border: none;
  border-radius: 4px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover {
  background: rgba(0, 0, 0, 0.5);
}

@media (max-width: 768px) {
  .quest-item {
    padding: 0.75rem;
  }

  .quest-icon {
    width: 30px;
    height: 30px;
    min-width: 30px;
    margin-right: 0.75rem;
  }

  .quest-icon-symbol {
    font-size: 1rem;
  }

  .quest-title {
    font-size: 1rem;
  }

  .quest-description {
    font-size: 0.8rem;
  }
}
</style>