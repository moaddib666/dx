<script setup lang="ts">
import { defineProps, withDefaults } from 'vue';
import { CharacterActionLog } from '@/api/dx-backend/api';
import RPGActionLogItem from './RPGActionLogItem.vue';

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
  if (index === 0) return true; // Always add a separator for the first item
  return props.actions[index].cycle !== props.actions[index - 1].cycle;
}
</script>

<template>
  <div class="action-log--container">
    <div class="action-log--content">
      <div v-for="(action, index) in actions" :key="action.id">
        <!-- Separator if cycle changes -->
        <div v-if="shouldInsertSeparator(index)" class="cycle-separator">
          Cycle: {{ action.cycle }}
        </div>

        <!-- RPGActionLogItem Component -->
        <RPGActionLogItem
            :initiator="action.initiator"
            :actionType="action.action_type"
            :skill="action.skill"
            :data="action.data"
            :impacts="action.impacts"
        />
      </div>
      <p v-if="actions.length === 0" class="no-actions">No actions logged.</p>
    </div>
  </div>
</template>

<style scoped>
.action-log--container {
  padding: 1rem;
  padding-right: 2rem;
  padding-top: 2rem;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  border-image-source: url("@/assets/rpg/bordertemplate.png");
  border-image-slice: 120 150 120 150 fill;
  border-image-width: 2.5rem 2.5rem 2.5rem 2.5rem;
  border-image-outset: 0 0 0 0;
  border-image-repeat: stretch stretch;
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