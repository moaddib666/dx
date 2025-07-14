<template>
  <div class="condition-editor">
    <div class="condition-header">
      <h4>{{ isNew ? 'Create Condition' : 'Edit Condition' }}</h4>
      <button @click="$emit('cancel')" class="btn-close">
        <span class="icon">✖</span>
      </button>
    </div>

    <div class="form-group">
      <label for="condition-type">Condition Type</label>
      <select
        id="condition-type"
        v-model="localCondition.type"
        class="condition-type-select"
      >
        <option value="custom">Custom</option>
        <option value="interaction">Interaction</option>
        <option value="location">Location</option>
        <option value="item">Item</option>
        <option value="combat">Combat</option>
        <option value="skill">Skill Check</option>
      </select>
    </div>

    <!-- Triggers Section -->
    <div class="triggers-section">
      <div class="section-header">
        <h5>Triggers</h5>
        <button @click="addTrigger" class="btn-add-trigger">
          <span class="icon">+</span> Add Trigger
        </button>
      </div>

      <div v-if="!localCondition.triggers?.length" class="empty-section-message">
        No triggers defined. Add a trigger to specify how this condition is met.
      </div>

      <div v-else class="triggers-list">
        <div
          v-for="(trigger, index) in localCondition.triggers"
          :key="trigger.id || index"
          class="trigger-item"
        >
          <div class="trigger-header">
            <select
              v-model="trigger.type"
              class="trigger-type-select"
            >
              <option value="interaction">Talk to Character</option>
              <option value="location">Visit Location</option>
              <option value="useItem">Use Item</option>
              <option value="combat">Combat</option>
              <option value="skill">Skill Check</option>
            </select>
            <button @click="removeTrigger(index)" class="btn-remove-trigger">
              <span class="icon">🗑️</span>
            </button>
          </div>

          <div class="trigger-details">
            <div class="form-group">
              <label for="game-object">{{ getTriggerObjectLabel(trigger.type) }}</label>
              <input
                :id="`game-object-${index}`"
                v-model="trigger.gameObject"
                type="text"
                class="game-object-input"
                :placeholder="getTriggerObjectPlaceholder(trigger.type)"
              />
            </div>

            <div v-if="trigger.type === 'skill'" class="form-group">
              <label for="skill-value">Skill Value</label>
              <input
                :id="`skill-value-${index}`"
                v-model.number="trigger.value"
                type="number"
                min="1"
                class="skill-value-input"
                placeholder="Minimum skill value required"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="form-actions">
      <button @click="saveCondition" class="btn-save" :disabled="!isValid">
        Save Condition
      </button>
      <button @click="$emit('cancel')" class="btn-cancel">
        Cancel
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { Condition, Trigger } from '@/api/dx-backend';

const props = defineProps<{
  condition?: Condition;
  questId?: string;
  type?: 'starters' | 'objectives';
}>();

const emit = defineEmits<{
  (e: 'save', condition: Condition): void;
  (e: 'cancel'): void;
}>();

// Determine if this is a new condition or editing an existing one
const isNew = computed(() => !props.condition);

// Create a local copy of the condition for editing
const localCondition = ref<Condition>(props.condition ? { ...props.condition } : {
  id: '',
  type: 'custom',
  triggers: []
});

// Reset local condition when props change
watch(() => props.condition, (newCondition) => {
  if (newCondition) {
    localCondition.value = { ...newCondition };
  }
}, { deep: true });

// Computed properties
const isValid = computed(() => {
  return !!localCondition.value.type &&
         localCondition.value.triggers &&
         localCondition.value.triggers.length > 0 &&
         localCondition.value.triggers.every(trigger =>
           !!trigger.type &&
           (trigger.type !== 'interaction' || !!trigger.gameObject) &&
           (trigger.type !== 'location' || !!trigger.gameObject) &&
           (trigger.type !== 'useItem' || !!trigger.gameObject) &&
           (trigger.type !== 'skill' || (!!trigger.gameObject && !!trigger.value))
         );
});

// Helper functions
const getTriggerObjectLabel = (triggerType: string): string => {
  const labels = {
    'interaction': 'Character ID',
    'location': 'Location ID',
    'useItem': 'Item ID',
    'combat': 'Enemy ID',
    'skill': 'Skill ID'
  };
  return labels[triggerType] || 'Object ID';
};

const getTriggerObjectPlaceholder = (triggerType: string): string => {
  const placeholders = {
    'interaction': 'Enter character ID',
    'location': 'Enter location ID',
    'useItem': 'Enter item ID',
    'combat': 'Enter enemy ID',
    'skill': 'Enter skill ID'
  };
  return placeholders[triggerType] || 'Enter object ID';
};

// Event handlers
const addTrigger = () => {
  if (!localCondition.value.triggers) {
    localCondition.value.triggers = [];
  }

  const newTrigger: Trigger = {
    id: `temp-${Date.now()}`,
    type: 'interaction',
    gameObject: '',
    value: 0
  };

  localCondition.value.triggers.push(newTrigger);
};

const removeTrigger = (index: number) => {
  if (localCondition.value.triggers) {
    localCondition.value.triggers.splice(index, 1);
  }
};

const saveCondition = async () => {
  if (isValid.value) {
    emit('save', localCondition.value);
  }
};
</script>

<style scoped>
.condition-editor {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.condition-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  padding-bottom: 0.75rem;
}

.condition-header h4 {
  font-size: 1.2rem;
  color: var(--cyber-yellow, #ffd700);
  margin: 0;
}

.btn-close {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-close:hover {
  color: white;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: white;
  font-weight: bold;
}

.condition-type-select, .trigger-type-select, .game-object-input, .skill-value-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.75rem;
  color: white;
  font-size: 1rem;
}

.triggers-section {
  margin-bottom: 1.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h5 {
  font-size: 1rem;
  color: white;
  margin: 0;
}

.btn-add-trigger {
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

.btn-add-trigger:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: translateY(-2px);
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

.triggers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.trigger-item {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 1rem;
}

.trigger-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.btn-remove-trigger {
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

.btn-remove-trigger:hover {
  background: rgba(255, 0, 0, 0.3);
}

.trigger-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
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

.icon {
  font-size: 1rem;
  margin-right: 0.25rem;
}

@media (max-width: 768px) {
  .condition-editor {
    padding: 1rem;
  }

  .form-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .btn-save, .btn-cancel {
    width: 100%;
  }
}
</style>