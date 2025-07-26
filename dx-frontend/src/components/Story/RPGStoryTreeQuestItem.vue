<script setup lang="ts">
import {defineProps, computed} from 'vue';
import {Quest} from '@/api/dx-backend';

interface Props {
  quest: Quest;
  selected: boolean;
  selectedItem: string;
  collapsed: boolean;
}

const props = defineProps<Props>();

// Determine if this quest is active
const isActive = computed(() => {
  return props.selectedItem === props.quest.id;
});
</script>

<template>
  <div class="quest-item" :class="{ 'active': isActive }">
    <div class="quest-header">
      <div class="quest-content">
        <h4 class="quest-title">{{ props.quest.title }}</h4>
        <div class="quest-subtext" v-if="props.quest.description">
          {{ props.quest.description }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quest-item {
  margin-bottom: 0.75rem;
  border-radius: 4px;
  background-color: rgba(0, 0, 0, 0.2);
  padding: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: border-color 0.3s ease, transform 0.2s ease;
}

.quest-item:hover {
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateX(2px);
}

.quest-item.active {
  border-color: var(--color-active);
  box-shadow: 0 0 8px rgba(79, 209, 255, 0.3);
}

.quest-header {
  display: flex;
  align-items: center;
}

.quest-content {
  flex: 1;
}

.quest-title {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
  color: #ffffff;
}

.quest-subtext {
  font-family: var(--font-body);
  font-size: 0.75rem;
  color: #aaa;
}

/* Responsive design for smaller containers (30% width) */
@media (max-width: 480px), (max-width: 30vw) {
  .quest-item {
    margin-bottom: 0.5rem;
    padding: 0.5rem;
  }

  .quest-item:hover {
    transform: translateX(1px);
  }

  .quest-title {
    font-size: 0.85rem;
    margin: 0 0 0.15rem 0;
  }

  .quest-subtext {
    font-size: 0.65rem;
  }
}
</style>