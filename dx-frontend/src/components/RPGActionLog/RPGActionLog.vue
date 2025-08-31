<script setup lang="ts">
import {defineProps, withDefaults} from 'vue';
import {CharacterActionLog} from '@/api/dx-backend/api';
import RPGActionLogItem from './RPGActionLogItem.vue';
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";

const props = withDefaults(defineProps<{
  actions: Array<CharacterActionLog>
}>(), {
  actions: () => ([])
});

/**
 * Determines if a separator should be inserted before an action
 * @param index The index of the current action
 * @returns True if a separator should be inserted, false otherwise
 */
function shouldInsertSeparator(index: number): boolean {
  if (!props.actions || index >= props.actions.length || index < 0) return false;
  if (index === 0) return true; // Show separator for first item only if it has cycle info

  // Compare cycle numbers instead of cycle objects
  const currentCycle = props.actions[index].cycle?.number;
  const previousCycle = props.actions[index - 1].cycle?.number;

  return currentCycle !== previousCycle;
}
</script>

<template>
  <RPGContainer
      class="action-log--container"
  >
    <div class="action-log--content">
      <div v-for="(action, index) in actions" :key="action.id">
        <!-- Separator if cycle changes -->
        <div v-if="shouldInsertSeparator(index)" class="cycle-separator">
          Cycle: {{ action.cycle.number }}
        </div>

        <!-- RPGActionLogItem Component -->
        <RPGActionLogItem
            :action="action"
        />
      </div>
      <p v-if="actions.length === 0" class="no-actions">No actions logged.</p>
    </div>
  </RPGContainer>
</template>

<style scoped>
.action-log--container {
  flex-direction: column;
}

.action-log--content {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  padding: 1rem;
  overflow-y: auto;
  max-height: 100%;
}

.cycle-separator {
  font-weight: bold;
  color: yellow;
  margin: 0.5rem 0;
  border-top: 0.2rem solid rgba(255, 255, 255, 0.5);
  padding-top: 0.5rem;
}

.no-actions {
  text-align: center;
  color: #e0e0e0;
  font-style: italic;
  margin-top: 1rem;
}
</style>