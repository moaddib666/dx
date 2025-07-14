<template>
  <div
    class="item-card"
    :class="{ 'item-card--interactive': interactive }"
    @click="handleClick"
  >
    <div class="item-icon">
      <GameObjectIcon
        type="item"
        :object="item"
        :tooltipEnabled="false"
      />
    </div>

    <div class="item-info">
      <div class="item-name">{{ item.name }}</div>

      <div v-if="item.type" class="item-type">
        {{ formatItemType(item.type) }}
      </div>

      <div v-if="showDetails" class="item-details">
        <div v-if="item.rarity" class="item-rarity" :class="`rarity-${item.rarity.toLowerCase()}`">
          {{ item.rarity }}
        </div>

        <div v-if="item.value" class="item-value">
          {{ item.value }} coins
        </div>
      </div>
    </div>

    <div v-if="interactive" class="item-actions">
      <button @click.stop="$emit('view', item)" class="action-button">
        <span class="icon">👁️</span>
      </button>
      <button v-if="editable" @click.stop="$emit('edit', item)" class="action-button">
        <span class="icon">✏️</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import GameObjectIcon from './GameObjectIcon.vue';

interface Item {
  id: string;
  name: string;
  type?: string;
  rarity?: string;
  value?: number;
  description?: string;
  [key: string]: any;
}

const props = defineProps<{
  item: Item;
  showDetails?: boolean;
  interactive?: boolean;
  editable?: boolean;
}>();

const emit = defineEmits<{
  (e: 'click', item: Item): void;
  (e: 'view', item: Item): void;
  (e: 'edit', item: Item): void;
}>();

// Helper functions
const formatItemType = (type: string): string => {
  // Convert camelCase or snake_case to Title Case with spaces
  return type
    .replace(/([A-Z])/g, ' $1') // Insert space before capital letters
    .replace(/_/g, ' ') // Replace underscores with spaces
    .replace(/^\w/, c => c.toUpperCase()); // Capitalize first letter
};

// Event handlers
const handleClick = () => {
  if (props.interactive) {
    emit('click', props.item);
  }
};
</script>

<style scoped>
.item-card {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(50, 205, 50, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.2s ease;
}

.item-card--interactive {
  cursor: pointer;
}

.item-card--interactive:hover {
  background: rgba(50, 205, 50, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.item-icon {
  margin-right: 0.75rem;
}

.item-info {
  flex: 1;
  overflow: hidden;
}

.item-name {
  font-weight: bold;
  color: white;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-type {
  font-size: 0.8rem;
  color: rgba(50, 205, 50, 1);
  margin-bottom: 0.25rem;
}

.item-details {
  display: flex;
  gap: 0.75rem;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
}

.item-rarity {
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.rarity-common {
  background: rgba(200, 200, 200, 0.2);
  color: #c8c8c8;
}

.rarity-uncommon {
  background: rgba(30, 255, 0, 0.2);
  color: #1eff00;
}

.rarity-rare {
  background: rgba(0, 112, 221, 0.2);
  color: #0070dd;
}

.rarity-epic {
  background: rgba(163, 53, 238, 0.2);
  color: #a335ee;
}

.rarity-legendary {
  background: rgba(255, 128, 0, 0.2);
  color: #ff8000;
}

.item-value {
  background: rgba(255, 215, 0, 0.2);
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  color: var(--cyber-yellow, #ffd700);
}

.item-actions {
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
  .item-card {
    padding: 0.5rem;
  }

  .item-icon {
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