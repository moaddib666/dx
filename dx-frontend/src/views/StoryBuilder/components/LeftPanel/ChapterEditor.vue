<template>
  <div class="chapter-editor">
    <div class="chapter-header">
      <h3 v-if="!editMode">{{ chapter.title }}</h3>
      <input
        v-else
        v-model="localChapter.title"
        class="chapter-title-input"
        placeholder="Chapter Title"
      />
    </div>

    <!-- Chapter Description -->
    <div class="chapter-section">
      <h4>Description</h4>
      <p v-if="!editMode" class="chapter-description">{{ chapter.description }}</p>
      <textarea
        v-else
        v-model="localChapter.description"
        class="chapter-description-input"
        placeholder="Chapter description..."
      />
    </div>

    <!-- Chapter Order -->
    <div v-if="editMode" class="chapter-section">
      <h4><span class="icon">🔢</span> Order</h4>
      <div class="order-control">
        <input
          v-model.number="localChapter.order"
          type="number"
          min="1"
          class="order-input"
          placeholder="Chapter order"
        />
        <p class="order-help">Set the order of this chapter in the story timeline.</p>
      </div>
    </div>

    <!-- Save Button (Edit Mode) -->
    <div v-if="editMode" class="chapter-actions">
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
import { Chapter } from '@/api/dx-backend';

const props = defineProps<{
  chapter: Chapter;
  editMode: boolean;
}>();

const emit = defineEmits<{
  (e: 'update', chapter: Chapter): void;
  (e: 'cancel'): void;
}>();

// Local state for editing
const localChapter = ref<Chapter>({ ...props.chapter });

// Reset local chapter when props change
watch(() => props.chapter, (newChapter) => {
  localChapter.value = { ...newChapter };
}, { deep: true });

// Computed properties
const isValid = computed(() => {
  return !!localChapter.value.title?.trim() && !!localChapter.value.description?.trim();
});

// Event handlers
const saveChanges = () => {
  if (isValid.value) {
    emit('update', localChapter.value);
  }
};

const cancelChanges = () => {
  localChapter.value = { ...props.chapter };
  emit('cancel');
};
</script>

<style scoped>
.chapter-editor {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
}

.chapter-header {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  padding-bottom: 1rem;
}

.chapter-header h3 {
  font-size: 1.5rem;
  color: var(--cyber-yellow, #ffd700);
  margin: 0;
}

.chapter-title-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.75rem;
  color: white;
  font-size: 1.2rem;
}

.chapter-section {
  margin-bottom: 2rem;
}

.chapter-section h4 {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  color: var(--cyber-yellow, #ffd700);
  margin-top: 0;
  margin-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.chapter-section h4 .icon {
  margin-right: 0.5rem;
}

.chapter-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
  white-space: pre-line;
}

.chapter-description-input {
  width: 100%;
  min-height: 100px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.75rem;
  color: white;
  resize: vertical;
}

.order-control {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.order-input {
  width: 100px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.5rem;
  color: white;
}

.order-help {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
}

.chapter-actions {
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

.icon {
  font-size: 1rem;
  margin-right: 0.25rem;
}

@media (max-width: 768px) {
  .chapter-editor {
    padding: 1rem;
  }

  .chapter-header h3 {
    font-size: 1.3rem;
  }

  .chapter-section h4 {
    font-size: 1rem;
  }
}
</style>