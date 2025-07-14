<template>
  <div
    class="character-card"
    :class="{ 'character-card--interactive': interactive }"
    @click="handleClick"
  >
    <div class="character-avatar">
      <GameObjectIcon
        type="character"
        :object="character"
        :tooltipEnabled="false"
      />
    </div>

    <div class="character-info">
      <div class="character-name">{{ character.name }}</div>

      <div v-if="character.role" class="character-role">
        {{ formatRole(character.role) }}
      </div>

      <div v-if="showDetails" class="character-details">
        <div v-if="character.level" class="character-level">
          Level {{ character.level }}
        </div>

        <div v-if="character.faction" class="character-faction">
          {{ character.faction }}
        </div>
      </div>
    </div>

    <div v-if="interactive" class="character-actions">
      <button @click.stop="$emit('view', character)" class="action-button">
        <span class="icon">👁️</span>
      </button>
      <button v-if="editable" @click.stop="$emit('edit', character)" class="action-button">
        <span class="icon">✏️</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import GameObjectIcon from './GameObjectIcon.vue';

interface Character {
  id: string;
  name: string;
  role?: string;
  level?: number;
  faction?: string;
  description?: string;
  [key: string]: any;
}

const props = defineProps<{
  character: Character;
  showDetails?: boolean;
  interactive?: boolean;
  editable?: boolean;
}>();

const emit = defineEmits<{
  (e: 'click', character: Character): void;
  (e: 'view', character: Character): void;
  (e: 'edit', character: Character): void;
}>();

// Helper functions
const formatRole = (role: string): string => {
  // Convert camelCase or snake_case to Title Case with spaces
  return role
    .replace(/([A-Z])/g, ' $1') // Insert space before capital letters
    .replace(/_/g, ' ') // Replace underscores with spaces
    .replace(/^\w/, c => c.toUpperCase()); // Capitalize first letter
};

// Event handlers
const handleClick = () => {
  if (props.interactive) {
    emit('click', props.character);
  }
};
</script>

<style scoped>
.character-card {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(65, 105, 225, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.2s ease;
}

.character-card--interactive {
  cursor: pointer;
}

.character-card--interactive:hover {
  background: rgba(65, 105, 225, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.character-avatar {
  margin-right: 0.75rem;
}

.character-info {
  flex: 1;
  overflow: hidden;
}

.character-name {
  font-weight: bold;
  color: white;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.character-role {
  font-size: 0.8rem;
  color: rgba(65, 105, 225, 1);
  margin-bottom: 0.25rem;
}

.character-details {
  display: flex;
  gap: 0.75rem;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
}

.character-level {
  background: rgba(65, 105, 225, 0.2);
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.character-faction {
  background: rgba(255, 215, 0, 0.2);
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  color: var(--cyber-yellow, #ffd700);
}

.character-actions {
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

.icon {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .character-card {
    padding: 0.5rem;
  }

  .character-avatar {
    margin-right: 0.5rem;
  }

  .action-button {
    width: 24px;
    height: 24px;
  }

  .icon {
    font-size: 0.9rem;
  }
}
</style>