<template>
  <div class="story-selector">
    <div class="story-selector__dropdown">
      <div
        class="selected-story"
        @click="toggleDropdown"
      >
        <span v-if="selectedStory" class="story-title">{{ selectedStory.title }}</span>
        <span v-else class="no-story">No story selected</span>
        <span class="dropdown-icon">▼</span>
      </div>

      <div v-if="isDropdownOpen" class="story-dropdown">
        <div class="dropdown-header">
          <h4>Select a Story</h4>
          <button @click="toggleDropdown" class="btn-close">
            <span class="icon">✖</span>
          </button>
        </div>

        <div v-if="!stories.length" class="no-stories-message">
          No stories available. Create your first story!
        </div>

        <div v-else class="story-list">
          <div
            v-for="story in stories"
            :key="story.id"
            class="story-item"
            :class="{ 'story-item--selected': selectedStory?.id === story.id }"
            @click="selectStory(story)"
          >
            <div class="story-info">
              <div class="story-item-title">{{ story.title }}</div>
              <div class="story-meta">
                <span v-if="story.isCanonical" class="story-canonical">Canonical</span>
                <span class="story-chapters">{{ story.chapters?.length || 0 }} chapters</span>
              </div>
            </div>

            <div class="story-actions">
              <button @click.stop="confirmDeleteStory(story)" class="action-button">
                <span class="icon">🗑️</span>
              </button>
            </div>
          </div>
        </div>

        <div class="dropdown-footer">
          <button @click="createNewStory" class="btn-create-story">
            <span class="icon">+</span> Create New Story
          </button>
        </div>
      </div>
    </div>

    <!-- Create Story Modal -->
    <div v-if="showCreateModal" class="create-story-modal" @click="cancelCreateStory">
      <div class="modal-content" @click.stop>
        <h4>Create New Story</h4>

        <div class="form-group">
          <label for="story-title">Title</label>
          <input
            id="story-title"
            v-model="storyForm.title"
            type="text"
            class="story-title-input"
            placeholder="Story title"
          />
        </div>

        <div class="form-group">
          <label for="story-description">Description</label>
          <textarea
            id="story-description"
            v-model="storyForm.description"
            class="story-description-input"
            placeholder="Story description"
            rows="4"
          ></textarea>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="storyForm.isCanonical"
            />
            Set as canonical story
          </label>
        </div>

        <div class="form-actions">
          <button @click="submitCreateStory" class="btn-save" :disabled="!isFormValid">
            Create
          </button>
          <button @click="cancelCreateStory" class="btn-cancel">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, defineEmits } from 'vue';
import { Story } from '@/api/dx-backend';

const props = defineProps<{
  stories: Story[];
  selectedStory: Story | null;
}>();

const emit = defineEmits<{
  (e: 'update:selectedStory', story: Story): void;
  (e: 'create', storyData: { title: string; description: string; isCanonical: boolean }): void;
  (e: 'delete', storyId: string): void;
}>();

// State
const isDropdownOpen = ref(false);
const showCreateModal = ref(false);
const storyForm = ref({
  title: '',
  description: '',
  isCanonical: false
});

// Computed
const isFormValid = computed(() => {
  return !!storyForm.value.title.trim() && !!storyForm.value.description.trim();
});

// Event handlers
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const selectStory = (story: Story) => {
  emit('update:selectedStory', story);
  isDropdownOpen.value = false;
};

const createNewStory = () => {
  storyForm.value = {
    title: '',
    description: '',
    isCanonical: false
  };
  showCreateModal.value = true;
  isDropdownOpen.value = false;
};

const submitCreateStory = () => {
  if (isFormValid.value) {
    emit('create', { ...storyForm.value });
    showCreateModal.value = false;
  }
};

const cancelCreateStory = () => {
  showCreateModal.value = false;
};

const confirmDeleteStory = (story: Story) => {
  if (confirm(`Are you sure you want to delete the story "${story.title}"? This action cannot be undone.`)) {
    emit('delete', story.id);
  }
};
</script>

<style scoped>
.story-selector {
  position: relative;
  min-width: 250px;
}

.story-selector__dropdown {
  position: relative;
}

.selected-story {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 6px;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.selected-story:hover {
  background: rgba(255, 215, 0, 0.1);
}

.story-title {
  font-weight: bold;
  color: white;
}

.no-story {
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
}

.dropdown-icon {
  margin-left: 0.5rem;
  color: var(--cyber-yellow, #ffd700);
  font-size: 0.8rem;
}

.story-dropdown {
  position: absolute;
  top: calc(100% + 5px);
  left: 0;
  width: 100%;
  min-width: 300px;
  background: rgba(30, 30, 30, 0.95);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  z-index: 100;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  animation: fadeIn 0.2s ease;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.dropdown-header h4 {
  margin: 0;
  color: var(--cyber-yellow, #ffd700);
  font-size: 1.1rem;
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

.no-stories-message {
  padding: 1.5rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
}

.story-list {
  max-height: 300px;
  overflow-y: auto;
  padding: 0.5rem;
}

.story-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 0.5rem;
}

.story-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.story-item--selected {
  background: rgba(255, 215, 0, 0.1);
  border-left: 3px solid var(--cyber-yellow, #ffd700);
}

.story-info {
  flex: 1;
  overflow: hidden;
}

.story-item-title {
  font-weight: bold;
  color: white;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.story-meta {
  display: flex;
  gap: 0.75rem;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
}

.story-canonical {
  background: rgba(255, 215, 0, 0.2);
  color: var(--cyber-yellow, #ffd700);
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.story-actions {
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
  background: rgba(255, 0, 0, 0.3);
}

.dropdown-footer {
  padding: 0.75rem 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: center;
}

.btn-create-story {
  background: rgba(255, 215, 0, 0.2);
  color: var(--cyber-yellow, #ffd700);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  width: 100%;
  justify-content: center;
}

.btn-create-story:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: translateY(-2px);
}

/* Create Story Modal */
.create-story-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: rgba(30, 30, 30, 0.95);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  padding: 2rem;
  width: 90%;
  max-width: 500px;
}

.modal-content h4 {
  color: var(--cyber-yellow, #ffd700);
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  padding-bottom: 0.75rem;
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

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  cursor: pointer;
}

.story-title-input, .story-description-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.75rem;
  color: white;
  font-size: 1rem;
}

.story-description-input {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
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
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .story-dropdown {
    min-width: 250px;
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