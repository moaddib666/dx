<template>
  <div class="notes-panel">
    <h3>
      <span class="icon">📝</span> Notes
      <button
        v-if="editMode"
        @click="createNewNote"
        class="btn-create-note"
      >
        <span class="icon">+</span> Add Note
      </button>
    </h3>

    <div v-if="!notes.length" class="empty-notes-message">
      No notes available for this chapter.
    </div>

    <div v-else class="notes-list">
      <div
        v-for="note in notes"
        :key="note.id"
        class="note-item"
      >
        <div class="note-header">
          <div class="note-title">{{ note.title }}</div>
          <div v-if="editMode" class="note-actions">
            <button @click="editNote(note)" class="action-button">
              <span class="icon">✏️</span>
            </button>
            <button @click="deleteNote(note.id)" class="action-button">
              <span class="icon">🗑️</span>
            </button>
          </div>
        </div>
        <div class="note-content">{{ note.content }}</div>
        <div class="note-meta">
          <div class="note-date">{{ formatDate(note.createdAt) }}</div>
          <div v-if="note.tags?.length" class="note-tags">
            <span
              v-for="tag in note.tags"
              :key="tag"
              class="note-tag"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Note Editor Modal -->
    <div v-if="showNoteEditor" class="note-editor-modal" @click="cancelNoteEdit">
      <div class="modal-content" @click.stop>
        <h4>{{ editingNote ? 'Edit Note' : 'Create Note' }}</h4>

        <div class="form-group">
          <label for="note-title">Title</label>
          <input
            id="note-title"
            v-model="noteForm.title"
            type="text"
            class="note-title-input"
            placeholder="Note title"
          />
        </div>

        <div class="form-group">
          <label for="note-content">Content</label>
          <textarea
            id="note-content"
            v-model="noteForm.content"
            class="note-content-input"
            placeholder="Note content"
            rows="5"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="note-tags">Tags (comma separated)</label>
          <input
            id="note-tags"
            v-model="tagsInput"
            type="text"
            class="note-tags-input"
            placeholder="tag1, tag2, tag3"
          />
        </div>

        <div class="form-actions">
          <button @click="saveNote" class="btn-save" :disabled="!isFormValid">
            Save
          </button>
          <button @click="cancelNoteEdit" class="btn-cancel">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, defineEmits } from 'vue';
import { Note } from '@/api/dx-backend';

const props = defineProps<{
  notes: Note[];
  editMode: boolean;
}>();

const emit = defineEmits<{
  (e: 'create', note: Note): void;
  (e: 'update', note: Note): void;
  (e: 'delete', noteId: string): void;
}>();

// State
const showNoteEditor = ref(false);
const editingNote = ref<Note | null>(null);
const noteForm = ref({
  title: '',
  content: '',
  tags: [] as string[]
});
const tagsInput = ref('');

// Computed
const isFormValid = computed(() => {
  return !!noteForm.value.title.trim() && !!noteForm.value.content.trim();
});

// Helper functions
const formatDate = (dateString: string | undefined): string => {
  if (!dateString) return 'Unknown date';

  try {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  } catch (error) {
    return 'Invalid date';
  }
};

const resetForm = () => {
  noteForm.value = {
    title: '',
    content: '',
    tags: []
  };
  tagsInput.value = '';
  editingNote.value = null;
};

// Event handlers
const createNewNote = () => {
  resetForm();
  showNoteEditor.value = true;
};

const editNote = (note: Note) => {
  editingNote.value = note;
  noteForm.value = {
    title: note.title || '',
    content: note.content || '',
    tags: note.tags || []
  };
  tagsInput.value = note.tags?.join(', ') || '';
  showNoteEditor.value = true;
};

const deleteNote = (noteId: string) => {
  if (confirm('Are you sure you want to delete this note?')) {
    emit('delete', noteId);
  }
};

const saveNote = () => {
  // Parse tags from comma-separated input
  const tags = tagsInput.value
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag.length > 0);

  if (editingNote.value) {
    // Update existing note
    const updatedNote: Note = {
      ...editingNote.value,
      title: noteForm.value.title,
      content: noteForm.value.content,
      tags,
      updatedAt: new Date().toISOString()
    };
    emit('update', updatedNote);
  } else {
    // Create new note
    const newNote: Note = {
      id: `note-${Date.now()}`,
      title: noteForm.value.title,
      content: noteForm.value.content,
      tags,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    emit('create', newNote);
  }

  // Close the editor
  showNoteEditor.value = false;
  resetForm();
};

const cancelNoteEdit = () => {
  showNoteEditor.value = false;
  resetForm();
};
</script>

<style scoped>
.notes-panel {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1.5rem;
  position: relative;
}

.notes-panel h3 {
  font-size: 1.3rem;
  color: var(--cyber-yellow, #ffd700);
  margin-top: 0;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  padding-bottom: 0.75rem;
}

.notes-panel h3 .icon {
  margin-right: 0.5rem;
}

.btn-create-note {
  margin-left: auto;
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

.btn-create-note:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: translateY(-2px);
}

.empty-notes-message {
  text-align: center;
  padding: 2rem;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.notes-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 400px;
  overflow-y: auto;
}

.note-item {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 1rem;
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.note-title {
  font-weight: bold;
  color: white;
  font-size: 1.1rem;
}

.note-actions {
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

.note-content {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 1rem;
  white-space: pre-line;
  line-height: 1.5;
}

.note-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
}

.note-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.note-tag {
  background: rgba(255, 215, 0, 0.1);
  color: var(--cyber-yellow, #ffd700);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

/* Note Editor Modal */
.note-editor-modal {
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
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
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

.note-title-input, .note-tags-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.75rem;
  color: white;
  font-size: 1rem;
}

.note-content-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.75rem;
  color: white;
  font-size: 1rem;
  resize: vertical;
  min-height: 120px;
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

@media (max-width: 768px) {
  .notes-panel {
    padding: 1rem;
  }

  .modal-content {
    padding: 1.5rem;
    width: 95%;
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