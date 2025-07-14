<template>
  <div class="page-container">
    <div class="hero-background"></div>
    <div class="story-builder">
      <!-- Loading overlay -->
      <Loader
        v-if="loading"
        text="Loading Story Builder"
        message="Preparing your storytelling tools..."
      />

      <!-- Header -->
      <div class="story-builder__header">
        <StorySelector
          v-model:selectedStory="currentStory"
          :stories="stories"
          @create="handleCreateStory"
          @delete="handleDeleteStory"
        />
        <ModeToggle v-model="editMode" />
      </div>

      <!-- Main Content -->
      <div class="story-builder__content">
        <!-- Left Panel: Quest Management -->
        <div class="story-builder__left-panel">
          <ChapterTimeline
            :chapters="currentStory?.chapters || []"
            :selectedChapter="selectedChapter"
            @select="handleChapterSelect"
            @create="handleCreateChapter"
            @edit="handleEditChapter"
            @delete="handleDeleteChapter"
            @moveUp="handleMoveChapterUp"
            @moveDown="handleMoveChapterDown"
            :editMode="editMode"
          />

          <ChapterEditor
            v-if="isChapterEditorVisible && chapterBeingEdited"
            :chapter="chapterBeingEdited"
            :editMode="true"
            @update="handleChapterUpdate"
            @cancel="closeChapterEditor"
          />

          <QuestList
            v-if="selectedChapter"
            :quests="selectedChapter.quests || []"
            :selectedQuest="selectedQuest"
            @select="handleQuestSelect"
            @create="handleCreateQuest"
            @edit="handleEditQuest"
            @delete="handleDeleteQuest"
            :editMode="editMode"
          />

          <QuestDetails
            v-if="selectedQuest"
            :quest="selectedQuest"
            @update="handleQuestUpdate"
            :editMode="editMode"
          />
        </div>

        <!-- Right Panel: Summary & Media -->
        <div class="story-builder__right-panel">
          <ChapterSummary
            v-if="selectedChapter"
            :chapter="selectedChapter"
            :characters="extractCharacters(selectedChapter)"
            :items="extractItems(selectedChapter)"
            :gameObjects="extractGameObjects(selectedChapter)"
          />

          <ImageGallery
            :images="currentImages"
            @upload="handleImageUpload"
            @delete="handleImageDelete"
            :editMode="editMode"
          />

          <NotesPanel
            :notes="currentNotes"
            @create="handleCreateNote"
            @update="handleUpdateNote"
            @delete="handleDeleteNote"
            :editMode="editMode"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { storyService } from '@/services/Story';
import {
  Story,
  Chapter,
  Quest,
  Note
} from '@/api/dx-backend';

// Import components
import Loader from '@/components/Loader.vue';
import StorySelector from './components/StorySelector.vue';
import ModeToggle from './components/ModeToggle.vue';
import ChapterTimeline from './components/LeftPanel/ChapterTimeline.vue';
import ChapterEditor from './components/LeftPanel/ChapterEditor.vue';
import QuestList from './components/LeftPanel/QuestList.vue';
import QuestDetails from './components/LeftPanel/QuestDetails.vue';
import ChapterSummary from './components/RightPanel/ChapterSummary.vue';
import ImageGallery from './components/RightPanel/ImageGallery.vue';
import NotesPanel from './components/RightPanel/NotesPanel.vue';

// State
const loading = ref(true);
const editMode = ref(false);
const stories = ref<Story[]>([]);
const currentStory = ref<Story | null>(null);
const selectedChapter = ref<Chapter | null>(null);
const selectedQuest = ref<Quest | null>(null);
const currentNotes = ref<Note[]>([]);
const currentImages = ref<string[]>([]);
const isChapterEditorVisible = ref(false);
const chapterBeingEdited = ref<Chapter | null>(null);

// Computed properties
const extractCharacters = (chapter: Chapter) => {
  const characters: Set<string> = new Set();

  chapter.quests?.forEach(quest => {
    // Extract from starters
    quest.starters?.forEach(condition => {
      condition.triggers?.forEach(trigger => {
        if (trigger.type === 'interaction' && trigger.gameObject) {
          characters.add(trigger.gameObject);
        }
      });
    });

    // Extract from objectives
    quest.objectives?.forEach(condition => {
      condition.triggers?.forEach(trigger => {
        if (trigger.type === 'interaction' && trigger.gameObject) {
          characters.add(trigger.gameObject);
        }
      });
    });
  });

  // Convert to character objects
  return Array.from(characters).map(id => ({ id, name: id }));
};

const extractItems = (chapter: Chapter) => {
  const items: Set<string> = new Set();

  chapter.quests?.forEach(quest => {
    // Extract from rewards
    quest.onSuccess?.items?.forEach(item => items.add(item.itemId));
    quest.onFailure?.items?.forEach(item => items.add(item.itemId));

    // Extract from triggers
    quest.starters?.forEach(condition => {
      condition.triggers?.forEach(trigger => {
        if (trigger.type === 'useItem' && trigger.gameObject) {
          items.add(trigger.gameObject);
        }
      });
    });
  });

  return Array.from(items).map(id => ({ id, name: id }));
};

const extractGameObjects = (chapter: Chapter) => {
  // Combine characters and items
  const characters = extractCharacters(chapter);
  const items = extractItems(chapter);

  // Extract locations
  const locations: Set<string> = new Set();
  chapter.quests?.forEach(quest => {
    quest.starters?.forEach(condition => {
      condition.triggers?.forEach(trigger => {
        if (trigger.type === 'location' && trigger.gameObject) {
          locations.add(trigger.gameObject);
        }
      });
    });
  });

  const locationObjects = Array.from(locations).map(id => ({ id, name: id, type: 'location' }));

  return [
    ...characters.map(c => ({ ...c, type: 'character' })),
    ...items.map(i => ({ ...i, type: 'item' })),
    ...locationObjects
  ];
};

// Event handlers
const handleCreateStory = async (storyData) => {
  try {
    loading.value = true;
    const story = await storyService.createStory(storyData);
    stories.value.push(story);
    currentStory.value = story;
  } catch (error) {
    console.error('Failed to create story:', error);
  } finally {
    loading.value = false;
  }
};

const handleDeleteStory = async (storyId) => {
  try {
    loading.value = true;
    await storyService.deleteStory(storyId);
    stories.value = stories.value.filter(story => story.id !== storyId);
    if (currentStory.value?.id === storyId) {
      currentStory.value = stories.value.length > 0 ? stories.value[0] : null;
    }
  } catch (error) {
    console.error('Failed to delete story:', error);
  } finally {
    loading.value = false;
  }
};

const handleChapterSelect = (chapter) => {
  selectedChapter.value = chapter;
  selectedQuest.value = null;

  // Load notes for this chapter
  loadChapterNotes(chapter.id);

  // Load images for this chapter
  loadChapterImages(chapter.id);
};

const handleCreateChapter = async () => {
  try {
    loading.value = true;

    // Find the maximum order value from existing chapters
    let maxOrder = 0;
    if (currentStory.value?.chapters && currentStory.value.chapters.length > 0) {
      maxOrder = Math.max(...currentStory.value.chapters.map(c => c.order || 0));
    }

    // Create a new chapter with required fields and incremented order
    const chapterData = {
      title: "New Chapter",
      description: "Chapter description",
      story: currentStory.value?.id,
      order: maxOrder + 1
    };

    const chapter = await storyService.createChapter({
      ...chapterData,
      storyId: currentStory.value?.id
    });

    // Refresh the current story to get updated chapters
    if (currentStory.value) {
      const updatedStory = await storyService.loadStory(currentStory.value.id);
      if (updatedStory) {
        currentStory.value = updatedStory;
      }
    }

    selectedChapter.value = chapter;
  } catch (error) {
    console.error('Failed to create chapter:', error);
  } finally {
    loading.value = false;
  }
};

const handleEditChapter = (chapter) => {
  // Set the chapter being edited and show the editor
  chapterBeingEdited.value = { ...chapter };
  isChapterEditorVisible.value = true;
};

const handleChapterUpdate = async (updatedChapter) => {
  try {
    loading.value = true;
    const chapter = await storyService.updateChapter(updatedChapter.id, updatedChapter);

    // Update the chapter in the current story
    if (currentStory.value && currentStory.value.chapters) {
      const index = currentStory.value.chapters.findIndex(c => c.id === chapter.id);
      if (index >= 0) {
        currentStory.value.chapters[index] = chapter;
      }
    }

    if (selectedChapter.value?.id === chapter.id) {
      selectedChapter.value = chapter;
    }

    // Close the editor
    closeChapterEditor();
  } catch (error) {
    console.error('Failed to update chapter:', error);
  } finally {
    loading.value = false;
  }
};

const closeChapterEditor = () => {
  isChapterEditorVisible.value = false;
  chapterBeingEdited.value = null;
};

const handleMoveChapterUp = async (chapter) => {
  try {
    loading.value = true;

    if (!currentStory.value?.chapters || currentStory.value.chapters.length <= 1) {
      return;
    }

    // Find the chapter's current index
    const chapters = currentStory.value.chapters;
    const currentIndex = chapters.findIndex(c => c.id === chapter.id);

    if (currentIndex <= 0) {
      return; // Already at the top
    }

    // Get the chapter above
    const prevChapter = chapters[currentIndex - 1];

    // Swap orders
    const tempOrder = chapter.order;
    chapter.order = prevChapter.order;
    prevChapter.order = tempOrder;

    // Update both chapters in the backend
    await Promise.all([
      storyService.updateChapter(chapter.id, chapter),
      storyService.updateChapter(prevChapter.id, prevChapter)
    ]);

    // Refresh the current story to get updated chapters
    if (currentStory.value) {
      const updatedStory = await storyService.loadStory(currentStory.value.id);
      if (updatedStory) {
        currentStory.value = updatedStory;
      }
    }
  } catch (error) {
    console.error('Failed to move chapter up:', error);
  } finally {
    loading.value = false;
  }
};

const handleMoveChapterDown = async (chapter) => {
  try {
    loading.value = true;

    if (!currentStory.value?.chapters || currentStory.value.chapters.length <= 1) {
      return;
    }

    // Find the chapter's current index
    const chapters = currentStory.value.chapters;
    const currentIndex = chapters.findIndex(c => c.id === chapter.id);

    if (currentIndex >= chapters.length - 1 || currentIndex < 0) {
      return; // Already at the bottom or not found
    }

    // Get the chapter below
    const nextChapter = chapters[currentIndex + 1];

    // Swap orders
    const tempOrder = chapter.order;
    chapter.order = nextChapter.order;
    nextChapter.order = tempOrder;

    // Update both chapters in the backend
    await Promise.all([
      storyService.updateChapter(chapter.id, chapter),
      storyService.updateChapter(nextChapter.id, nextChapter)
    ]);

    // Refresh the current story to get updated chapters
    if (currentStory.value) {
      const updatedStory = await storyService.loadStory(currentStory.value.id);
      if (updatedStory) {
        currentStory.value = updatedStory;
      }
    }
  } catch (error) {
    console.error('Failed to move chapter down:', error);
  } finally {
    loading.value = false;
  }
};

const handleDeleteChapter = async (chapterId) => {
  try {
    loading.value = true;
    await storyService.deleteChapter(chapterId);

    // Refresh the current story to get updated chapters
    if (currentStory.value) {
      const updatedStory = await storyService.loadStory(currentStory.value.id);
      if (updatedStory) {
        currentStory.value = updatedStory;
      }
    }

    if (selectedChapter.value?.id === chapterId) {
      selectedChapter.value = null;
      selectedQuest.value = null;
    }
  } catch (error) {
    console.error('Failed to delete chapter:', error);
  } finally {
    loading.value = false;
  }
};

const handleQuestSelect = (quest) => {
  selectedQuest.value = quest;
};

const handleCreateQuest = async (questData) => {
  try {
    loading.value = true;
    const quest = await storyService.createQuest({
      ...questData,
      chapterId: selectedChapter.value?.id
    });

    // Refresh the selected chapter to get updated quests
    if (selectedChapter.value) {
      const updatedChapter = await storyService.loadChapters(currentStory.value?.id || '');
      const chapter = updatedChapter.find(c => c.id === selectedChapter.value?.id);
      if (chapter) {
        selectedChapter.value = chapter;
      }
    }

    selectedQuest.value = quest;
  } catch (error) {
    console.error('Failed to create quest:', error);
  } finally {
    loading.value = false;
  }
};

const handleEditQuest = async (questData) => {
  try {
    loading.value = true;
    const quest = await storyService.updateQuest(questData.id, questData);

    // Update the quest in the selected chapter
    if (selectedChapter.value && selectedChapter.value.quests) {
      const index = selectedChapter.value.quests.findIndex(q => q.id === quest.id);
      if (index >= 0) {
        selectedChapter.value.quests[index] = quest;
      }
    }

    if (selectedQuest.value?.id === quest.id) {
      selectedQuest.value = quest;
    }
  } catch (error) {
    console.error('Failed to update quest:', error);
  } finally {
    loading.value = false;
  }
};

const handleDeleteQuest = async (questId) => {
  try {
    loading.value = true;
    await storyService.deleteQuest(questId);

    // Refresh the selected chapter to get updated quests
    if (selectedChapter.value) {
      const updatedChapter = await storyService.loadChapters(currentStory.value?.id || '');
      const chapter = updatedChapter.find(c => c.id === selectedChapter.value?.id);
      if (chapter) {
        selectedChapter.value = chapter;
      }
    }

    if (selectedQuest.value?.id === questId) {
      selectedQuest.value = null;
    }
  } catch (error) {
    console.error('Failed to delete quest:', error);
  } finally {
    loading.value = false;
  }
};

const handleQuestUpdate = async (questData) => {
  try {
    loading.value = true;
    const quest = await storyService.updateQuest(questData.id, questData);

    // Update the quest in the selected chapter
    if (selectedChapter.value && selectedChapter.value.quests) {
      const index = selectedChapter.value.quests.findIndex(q => q.id === quest.id);
      if (index >= 0) {
        selectedChapter.value.quests[index] = quest;
      }
    }

    selectedQuest.value = quest;
  } catch (error) {
    console.error('Failed to update quest:', error);
  } finally {
    loading.value = false;
  }
};

const handleCreateNote = async (noteData) => {
  try {
    loading.value = true;
    const note = await storyService.createNote({
      ...noteData,
      chapterId: selectedChapter.value?.id
    });

    currentNotes.value.push(note);
  } catch (error) {
    console.error('Failed to create note:', error);
  } finally {
    loading.value = false;
  }
};

const handleUpdateNote = async (noteData) => {
  try {
    loading.value = true;
    const note = await storyService.updateNote(noteData.id, noteData);

    const index = currentNotes.value.findIndex(n => n.id === note.id);
    if (index >= 0) {
      currentNotes.value[index] = note;
    }
  } catch (error) {
    console.error('Failed to update note:', error);
  } finally {
    loading.value = false;
  }
};

const handleDeleteNote = async (noteId) => {
  try {
    loading.value = true;
    await storyService.deleteNote(noteId);

    currentNotes.value = currentNotes.value.filter(note => note.id !== noteId);
  } catch (error) {
    console.error('Failed to delete note:', error);
  } finally {
    loading.value = false;
  }
};

const handleImageUpload = (imageUrl) => {
  currentImages.value.push(imageUrl);
};

const handleImageDelete = (imageUrl) => {
  currentImages.value = currentImages.value.filter(url => url !== imageUrl);
};

// Helper functions
const loadChapterNotes = async (chapterId) => {
  // This would be implemented with a real API call
  // For now, we'll use placeholder data
  currentNotes.value = [];
};

const loadChapterImages = async (chapterId) => {
  // This would be implemented with a real API call
  // For now, we'll use placeholder data
  currentImages.value = [];
};

// Lifecycle hooks
onMounted(async () => {
  try {
    // Initialize the story service if not already initialized
    if (!storyService.isInitialized) {
      await storyService.initialize();
    }

    // Load stories
    const loadedStories = await storyService.loadStories();
    stories.value = loadedStories;

    // Set the first story as current if available
    if (loadedStories.length > 0) {
      currentStory.value = loadedStories[0];
    }
  } catch (error) {
    console.error('Failed to initialize Story Builder:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* Page Container and Background */
.page-container {
  position: relative;
  min-height: 100vh;
}

.hero-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/images/dashbaord/dashboard-2.png');
  background-size: cover;
  background-position: center 10%;
  background-attachment: fixed;
  z-index: -1;
}

.hero-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7));
}

.story-builder {
  height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 90vw;
  margin: 0 auto;
  padding: 20px;
  position: relative;
  color: white;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(1px);
}

.story-builder__header {
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid var(--border-color, rgba(255, 215, 0, 0.2));
  margin-bottom: 20px;
}

.story-builder__content {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 20px;
  padding: 20px;
  overflow: hidden;
}

.story-builder__left-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.2);
  padding: 20px;
}

.story-builder__right-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.2);
  padding: 20px;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .story-builder__content {
    grid-template-columns: 1fr 350px;
  }
}

@media (max-width: 900px) {
  .story-builder__content {
    grid-template-columns: 1fr;
  }

  .story-builder__right-panel {
    display: none;
  }
}

@media (max-width: 768px) {
  .story-builder {
    padding: 10px;
    max-width: 100vw;
  }

  .story-builder__header {
    height: auto;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
  }

  .story-builder__content {
    padding: 10px;
  }
}
</style>