<template>
  <div class="quest-details">
    <div class="quest-header">
      <h3 v-if="!editMode">{{ quest.title }}</h3>
      <input
        v-else
        v-model="localQuest.title"
        class="quest-title-input"
        placeholder="Quest Title"
      />
    </div>

    <!-- Quest Description -->
    <div class="quest-section">
      <h4>Description</h4>
      <p v-if="!editMode" class="quest-description">{{ quest.description }}</p>
      <textarea
        v-else
        v-model="localQuest.description"
        class="quest-description-input"
        placeholder="Quest description..."
      />
    </div>

    <!-- Starter Conditions -->
    <div class="quest-section">
      <h4>
        <span class="icon">🚀</span> Starter Conditions
        <button v-if="editMode" @click="addCondition('starters')" class="btn-add-condition">
          <span class="icon">+</span>
        </button>
      </h4>

      <div v-if="!quest.starters?.length" class="empty-section-message">
        No starter conditions defined.
      </div>

      <div v-else class="conditions-list">
        <div
          v-for="condition in quest.starters"
          :key="condition.id"
          class="condition-item"
        >
          <div class="condition-header">
            <span class="condition-type">{{ formatConditionType(condition.type) }}</span>
            <div v-if="editMode" class="condition-actions">
              <button @click="editCondition(condition)" class="action-button">
                <span class="icon">✏️</span>
              </button>
              <button @click="deleteCondition(condition.id)" class="action-button">
                <span class="icon">🗑️</span>
              </button>
            </div>
          </div>

          <div class="condition-triggers">
            <div v-for="trigger in condition.triggers" :key="trigger.id" class="trigger-item">
              <span class="trigger-type">{{ formatTriggerType(trigger.type) }}</span>
              <span v-if="trigger.gameObject" class="trigger-object">{{ trigger.gameObject }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Objectives -->
    <div class="quest-section">
      <h4>
        <span class="icon">🎯</span> Objectives
        <button v-if="editMode" @click="addCondition('objectives')" class="btn-add-condition">
          <span class="icon">+</span>
        </button>
      </h4>

      <div v-if="!quest.objectives?.length" class="empty-section-message">
        No objectives defined.
      </div>

      <div v-else class="conditions-list">
        <div
          v-for="condition in quest.objectives"
          :key="condition.id"
          class="condition-item"
        >
          <div class="condition-header">
            <span class="condition-type">{{ formatConditionType(condition.type) }}</span>
            <div v-if="editMode" class="condition-actions">
              <button @click="editCondition(condition)" class="action-button">
                <span class="icon">✏️</span>
              </button>
              <button @click="deleteCondition(condition.id)" class="action-button">
                <span class="icon">🗑️</span>
              </button>
            </div>
          </div>

          <div class="condition-triggers">
            <div v-for="trigger in condition.triggers" :key="trigger.id" class="trigger-item">
              <span class="trigger-type">{{ formatTriggerType(trigger.type) }}</span>
              <span v-if="trigger.gameObject" class="trigger-object">{{ trigger.gameObject }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Rewards -->
    <div class="quest-section">
      <h4><span class="icon">🏆</span> Rewards</h4>

      <div class="rewards-container">
        <div class="reward-box">
          <h5>Success Reward</h5>
          <div v-if="!editMode" class="reward-content">
            <div v-if="quest.onSuccess?.items?.length" class="reward-items">
              <div v-for="item in quest.onSuccess.items" :key="item.itemId" class="reward-item">
                <span class="icon">📦</span> {{ item.itemId }} (x{{ item.quantity || 1 }})
              </div>
            </div>

            <div v-if="quest.onSuccess?.tokens?.length" class="reward-tokens">
              <div v-for="token in quest.onSuccess.tokens" :key="token.tokenId" class="reward-token">
                <span class="icon">💰</span> {{ token.tokenId }}: {{ token.amount }}
              </div>
            </div>

            <div v-if="quest.onSuccess?.effects?.length" class="reward-effects">
              <div v-for="effect in quest.onSuccess.effects" :key="effect.effectId" class="reward-effect">
                <span class="icon">✨</span> {{ effect.effectId }}
              </div>
            </div>

            <div v-if="!hasSuccessRewards" class="empty-reward-message">
              No success rewards defined.
            </div>
          </div>

          <div v-else class="reward-edit">
            <button @click="editSuccessReward" class="btn-edit-reward">
              Edit Success Reward
            </button>
          </div>
        </div>

        <div class="reward-box">
          <h5>Failure Reward</h5>
          <div v-if="!editMode" class="reward-content">
            <div v-if="quest.onFailure?.items?.length" class="reward-items">
              <div v-for="item in quest.onFailure.items" :key="item.itemId" class="reward-item">
                <span class="icon">📦</span> {{ item.itemId }} (x{{ item.quantity || 1 }})
              </div>
            </div>

            <div v-if="quest.onFailure?.tokens?.length" class="reward-tokens">
              <div v-for="token in quest.onFailure.tokens" :key="token.tokenId" class="reward-token">
                <span class="icon">💰</span> {{ token.tokenId }}: {{ token.amount }}
              </div>
            </div>

            <div v-if="quest.onFailure?.effects?.length" class="reward-effects">
              <div v-for="effect in quest.onFailure.effects" :key="effect.effectId" class="reward-effect">
                <span class="icon">✨</span> {{ effect.effectId }}
              </div>
            </div>

            <div v-if="!hasFailureRewards" class="empty-reward-message">
              No failure rewards defined.
            </div>
          </div>

          <div v-else class="reward-edit">
            <button @click="editFailureReward" class="btn-edit-reward">
              Edit Failure Reward
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Cycle Limit -->
    <div class="quest-section">
      <h4><span class="icon">⏱️</span> Time Limit</h4>
      <div class="cycle-limit">
        <span v-if="!editMode">{{ quest.cycleLimit || 'No limit' }} cycles</span>
        <input
          v-else
          v-model.number="localQuest.cycleLimit"
          type="number"
          min="0"
          class="cycle-limit-input"
          placeholder="Cycle limit (0 for no limit)"
        />
      </div>
    </div>

    <!-- Save Button (Edit Mode) -->
    <div v-if="editMode" class="quest-actions">
      <button @click="saveChanges" class="btn-save" :disabled="!isValid">
        Save Changes
      </button>
      <button @click="cancelChanges" class="btn-cancel">
        Cancel
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import {
  Quest,
  Condition,
  Reward
} from '@/api/dx-backend';

const props = defineProps<{
  quest: Quest;
  editMode: boolean;
}>();

const emit = defineEmits<{
  (e: 'update', quest: Quest): void;
}>();

// Local state for editing
const localQuest = ref<Quest>({ ...props.quest });

// Reset local quest when props change
watch(() => props.quest, (newQuest) => {
  localQuest.value = { ...newQuest };
}, { deep: true });

// Computed properties
const hasSuccessRewards = computed(() => {
  const reward = props.quest.onSuccess;
  return !!(
    reward?.items?.length ||
    reward?.tokens?.length ||
    reward?.effects?.length
  );
});

const hasFailureRewards = computed(() => {
  const reward = props.quest.onFailure;
  return !!(
    reward?.items?.length ||
    reward?.tokens?.length ||
    reward?.effects?.length
  );
});

const isValid = computed(() => {
  return !!localQuest.value.title?.trim() && !!localQuest.value.description?.trim();
});

// Helper functions
const formatConditionType = (type: string | undefined): string => {
  if (!type) return 'Unknown';

  // Convert camelCase or snake_case to Title Case with spaces
  return type
    .replace(/([A-Z])/g, ' $1') // Insert space before capital letters
    .replace(/_/g, ' ') // Replace underscores with spaces
    .replace(/^\w/, c => c.toUpperCase()); // Capitalize first letter
};

const formatTriggerType = (type: string | undefined): string => {
  if (!type) return 'Unknown';

  const triggerTypeMap = {
    'interaction': '💬 Talk to',
    'location': '📍 Visit',
    'useItem': '🔧 Use item',
    'combat': '⚔️ Combat',
    'skill': '🎯 Skill check'
  };

  return triggerTypeMap[type] || type;
};

// Event handlers
const addCondition = (type: 'starters' | 'objectives') => {
  // This would typically open a modal or form to add a new condition
  console.log(`Add ${type} condition`);

  // For demonstration, we'll just add a placeholder condition
  const newCondition: Condition = {
    id: `temp-${Date.now()}`,
    type: 'custom',
    triggers: []
  };

  if (!localQuest.value[type]) {
    localQuest.value[type] = [];
  }

  localQuest.value[type].push(newCondition);
};

const editCondition = (condition: Condition) => {
  // This would typically open a modal or form to edit the condition
  console.log('Edit condition', condition);
};

const deleteCondition = (conditionId: string) => {
  // Remove the condition from starters or objectives
  if (localQuest.value.starters) {
    localQuest.value.starters = localQuest.value.starters.filter(c => c.id !== conditionId);
  }

  if (localQuest.value.objectives) {
    localQuest.value.objectives = localQuest.value.objectives.filter(c => c.id !== conditionId);
  }
};

const editSuccessReward = () => {
  // This would typically open a modal or form to edit the success reward
  console.log('Edit success reward');

  // For demonstration, we'll just add a placeholder reward if none exists
  if (!localQuest.value.onSuccess) {
    localQuest.value.onSuccess = {
      items: [],
      tokens: [],
      effects: []
    };
  }
};

const editFailureReward = () => {
  // This would typically open a modal or form to edit the failure reward
  console.log('Edit failure reward');

  // For demonstration, we'll just add a placeholder reward if none exists
  if (!localQuest.value.onFailure) {
    localQuest.value.onFailure = {
      items: [],
      tokens: [],
      effects: []
    };
  }
};

const saveChanges = () => {
  if (isValid.value) {
    emit('update', localQuest.value);
  }
};

const cancelChanges = () => {
  localQuest.value = { ...props.quest };
};
</script>

<style scoped>
.quest-details {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
}

.quest-header {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  padding-bottom: 1rem;
}

.quest-header h3 {
  font-size: 1.5rem;
  color: var(--cyber-yellow, #ffd700);
  margin: 0;
}

.quest-title-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.75rem;
  color: white;
  font-size: 1.2rem;
}

.quest-section {
  margin-bottom: 2rem;
}

.quest-section h4 {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  color: var(--cyber-yellow, #ffd700);
  margin-top: 0;
  margin-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.quest-section h4 .icon {
  margin-right: 0.5rem;
}

.quest-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
  white-space: pre-line;
}

.quest-description-input {
  width: 100%;
  min-height: 100px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.75rem;
  color: white;
  resize: vertical;
}

.btn-add-condition {
  margin-left: auto;
  background: rgba(255, 215, 0, 0.2);
  color: var(--cyber-yellow, #ffd700);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-add-condition:hover {
  background: rgba(255, 215, 0, 0.3);
}

.empty-section-message {
  text-align: center;
  padding: 1rem;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.conditions-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.condition-item {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 0.75rem;
}

.condition-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.condition-type {
  font-weight: bold;
  color: white;
}

.condition-actions {
  display: flex;
  gap: 5px;
}

.condition-triggers {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.trigger-item {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  padding: 0.5rem;
  font-size: 0.9rem;
}

.trigger-type {
  color: rgba(255, 255, 255, 0.8);
}

.trigger-object {
  margin-left: 0.5rem;
  color: var(--cyber-yellow, #ffd700);
  background: rgba(255, 215, 0, 0.1);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.rewards-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.reward-box {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 0.75rem;
}

.reward-box h5 {
  margin-top: 0;
  margin-bottom: 0.75rem;
  color: white;
  font-size: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.reward-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.reward-items, .reward-tokens, .reward-effects {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.reward-item, .reward-token, .reward-effect {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
}

.empty-reward-message {
  text-align: center;
  padding: 0.5rem;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
  font-size: 0.9rem;
}

.btn-edit-reward {
  width: 100%;
  background: rgba(255, 215, 0, 0.2);
  color: var(--cyber-yellow, #ffd700);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit-reward:hover {
  background: rgba(255, 215, 0, 0.3);
}

.cycle-limit {
  color: white;
}

.cycle-limit-input {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.5rem;
  color: white;
  width: 100px;
}

.quest-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  justify-content: flex-end;
}

.btn-save {
  background: var(--cyber-yellow, #ffd700);
  color: black;
  border: none;
  border-radius: 4px;
  padding: 0.75rem 1.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-save:hover:not(:disabled) {
  background: #ffdf33;
  transform: translateY(-2px);
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.2);
}

.action-button {
  background: rgba(0, 0, 0, 0.3);
  border: none;
  border-radius: 4px;
  width: 24px;
  height: 24px;
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
  margin-right: 0.25rem;
}

@media (max-width: 768px) {
  .rewards-container {
    grid-template-columns: 1fr;
  }

  .quest-details {
    padding: 1rem;
  }

  .quest-header h3 {
    font-size: 1.3rem;
  }

  .quest-section h4 {
    font-size: 1rem;
  }
}
</style>