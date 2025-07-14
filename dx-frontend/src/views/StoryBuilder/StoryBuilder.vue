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

      <!-- Header (3.75rem) -->
      <header class="story-builder__header">
        <div class="header-left">
          <StorySelector
            v-model:selectedStory="currentStory"
            :stories="stories"
            @create="handleCreateStory"
            @delete="handleDeleteStory"
          />
          <div class="header-actions">
            <button class="header-btn" @click="handleNewStory">New</button>
            <button class="header-btn" @click="handleSaveStory">Save</button>
            <button class="header-btn" @click="handleExportStory">Export</button>
          </div>
        </div>
        <div class="header-right">
          <ModeToggle v-model="editMode" />
        </div>
      </header>

      <!-- Main Content Area -->
      <div class="story-builder__content">
        <!-- Left Column: Timeline Navigation (25rem) -->
        <aside class="story-builder__left-column">
          <TreeNavigation
            :story="currentStory"
            :selectedItem="selectedItem"
            :editMode="editMode"
            @select="handleItemSelect"
            @create="handleCreateItem"
            @edit="handleEditItem"
            @delete="handleDeleteItem"
            @reorder="handleReorderItem"
          />
        </aside>

        <!-- Right Column: Main Content/Editor (flexible) -->
        <main class="story-builder__right-column">
          <ContentEditor
            :selectedItem="selectedItem"
            :editMode="editMode"
            :entityMap="entityMap"
            @update="handleItemUpdate"
            @toggle-edit="handleToggleEdit"
            @entity-highlight="handleEntityHighlight"
          />
        </main>
      </div>

      <!-- Footer: Quick Reference Panel (7.5rem) -->
      <footer class="story-builder__footer">
        <QuickReference
          :entities="allEntities"
          :highlightedEntity="highlightedEntity"
          @search="handleEntitySearch"
          @highlight="handleEntityHighlight"
          @clear="handleClearHighlight"
        />
      </footer>
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
import TreeNavigation from './components/TreeNavigation.vue';
import ContentEditor from './components/ContentEditor.vue';
import QuickReference from './components/QuickReference.vue';

// State
const loading = ref(true);
const editMode = ref(false);
const stories = ref<Story[]>([]);
const currentStory = ref<Story | null>(null);
const selectedItem = ref<any>(null); // Can be Story, Chapter, or Quest
const highlightedEntity = ref<string | null>(null);
const entityMap = ref<Map<string, any>>(new Map());
const allEntities = ref<any[]>([]);

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
  // This is now handled by handleItemSelect
  handleItemSelect('chapter', chapter);
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

    selectedItem.value = { ...chapter, type: 'chapter' };
  } catch (error) {
    console.error('Failed to create chapter:', error);
  } finally {
    loading.value = false;
  }
};

const handleEditChapter = (chapter) => {
  // Enable edit mode for the selected chapter
  selectedItem.value = { ...chapter, type: 'chapter' };
  editMode.value = true;
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

    if (selectedItem.value?.id === chapter.id) {
      selectedItem.value = { ...chapter, type: 'chapter' };
    }

    // Exit edit mode
    editMode.value = false;
  } catch (error) {
    console.error('Failed to update chapter:', error);
  } finally {
    loading.value = false;
  }
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

    if (selectedItem.value?.id === chapterId) {
      selectedItem.value = null;
    }
  } catch (error) {
    console.error('Failed to delete chapter:', error);
  } finally {
    loading.value = false;
  }
};

const handleQuestSelect = (quest) => {
  handleItemSelect('quest', quest);
};

const handleCreateQuest = async () => {
  try {
    loading.value = true;

    // Find the maximum order value from existing quests
    let maxOrder = 0;
    if (selectedItem.value?.type === 'chapter' && selectedItem.value?.quests && selectedItem.value.quests.length > 0) {
      maxOrder = Math.max(...selectedItem.value.quests.map(q => q.order || 0));
    }

    // Create a new quest with required fields
    const questData = {
      title: "New Quest",
      description: "Quest description",
      chapter: selectedItem.value?.id,
      order: maxOrder + 1
    };

    const quest = await storyService.createQuest(questData);

    // Refresh the current story to get updated data
    if (currentStory.value) {
      const updatedStory = await storyService.loadStory(currentStory.value.id);
      if (updatedStory) {
        currentStory.value = updatedStory;
      }
    }

    selectedItem.value = { ...quest, type: 'quest' };
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

    // Update the quest in the current story
    if (currentStory.value?.chapters) {
      currentStory.value.chapters.forEach(chapter => {
        if (chapter.quests) {
          const index = chapter.quests.findIndex(q => q.id === quest.id);
          if (index >= 0) {
            chapter.quests[index] = quest;
          }
        }
      });
    }

    if (selectedItem.value?.id === quest.id) {
      selectedItem.value = { ...quest, type: 'quest' };
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

    // Refresh the current story to get updated data
    if (currentStory.value) {
      const updatedStory = await storyService.loadStory(currentStory.value.id);
      if (updatedStory) {
        currentStory.value = updatedStory;
      }
    }

    if (selectedItem.value?.id === questId) {
      selectedItem.value = null;
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

    // Update the quest in the current story
    if (currentStory.value?.chapters) {
      currentStory.value.chapters.forEach(chapter => {
        if (chapter.quests) {
          const index = chapter.quests.findIndex(q => q.id === quest.id);
          if (index >= 0) {
            chapter.quests[index] = quest;
          }
        }
      });
    }

    selectedItem.value = { ...quest, type: 'quest' };
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
      chapterId: selectedItem.value?.type === 'chapter' ? selectedItem.value.id : null
    });

    // Notes functionality would be implemented here
    console.log('Note created:', note);
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

    // Notes functionality would be implemented here
    console.log('Note updated:', note);
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

    // Notes functionality would be implemented here
    console.log('Note deleted:', noteId);
  } catch (error) {
    console.error('Failed to delete note:', error);
  } finally {
    loading.value = false;
  }
};

const handleImageUpload = (imageUrl) => {
  // Image functionality would be implemented here
  console.log('Image uploaded:', imageUrl);
};

const handleImageDelete = (imageUrl) => {
  // Image functionality would be implemented here
  console.log('Image deleted:', imageUrl);
};

// New event handlers for the restructured components
const handleItemSelect = (type: string, item: any) => {
  selectedItem.value = { ...item, type };
  updateEntityMap();
};

const handleCreateItem = async (type: string, parentId?: string) => {
  try {
    loading.value = true;
    
    if (type === 'chapter') {
      await handleCreateChapter();
    } else if (type === 'quest') {
      await handleCreateQuest();
    }
  } catch (error) {
    console.error(`Failed to create ${type}:`, error);
  } finally {
    loading.value = false;
  }
};

const handleEditItem = (type: string, item: any) => {
  // Enable edit mode for the selected item
  selectedItem.value = { ...item, type };
  editMode.value = true;
};

const handleDeleteItem = async (type: string, item: any) => {
  try {
    loading.value = true;
    
    if (type === 'chapter') {
      await handleDeleteChapter(item.id);
    } else if (type === 'quest') {
      await handleDeleteQuest(item.id);
    }
  } catch (error) {
    console.error(`Failed to delete ${type}:`, error);
  } finally {
    loading.value = false;
  }
};

const handleReorderItem = (type: string, item: any, direction: 'up' | 'down') => {
  if (type === 'chapter') {
    if (direction === 'up') {
      handleMoveChapterUp(item);
    } else {
      handleMoveChapterDown(item);
    }
  }
};

const handleItemUpdate = async (updatedItem: any) => {
  try {
    loading.value = true;
    
    if (updatedItem.type === 'story') {
      // Update story logic would go here
      currentStory.value = { ...currentStory.value, ...updatedItem };
    } else if (updatedItem.type === 'chapter') {
      await handleChapterUpdate(updatedItem);
    } else if (updatedItem.type === 'quest') {
      await handleQuestUpdate(updatedItem);
    }
    
    // Update the selected item
    selectedItem.value = updatedItem;
    editMode.value = false;
  } catch (error) {
    console.error('Failed to update item:', error);
  } finally {
    loading.value = false;
  }
};

const handleToggleEdit = () => {
  editMode.value = !editMode.value;
};

const handleEntityHighlight = (entityId: string) => {
  highlightedEntity.value = entityId;
};

const handleEntitySearch = (query: string) => {
  // Filter entities based on search query
  // This would be implemented with more sophisticated search logic
  console.log('Searching for:', query);
};

const handleClearHighlight = () => {
  highlightedEntity.value = null;
};

const handleNewStory = async () => {
  const storyData = {
    title: 'New Story',
    description: 'A new story description'
  };
  await handleCreateStory(storyData);
};

const handleSaveStory = async () => {
  if (currentStory.value) {
    try {
      loading.value = true;
      await storyService.updateStory(currentStory.value.id, currentStory.value);
      console.log('Story saved successfully');
    } catch (error) {
      console.error('Failed to save story:', error);
    } finally {
      loading.value = false;
    }
  }
};

const handleExportStory = () => {
  if (currentStory.value) {
    const dataStr = JSON.stringify(currentStory.value, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `${currentStory.value.title || 'story'}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  }
};

const updateEntityMap = () => {
  // Extract entities from the current story for the quick reference
  const entities: any[] = [];
  
  if (currentStory.value?.chapters) {
    currentStory.value.chapters.forEach(chapter => {
      chapter.quests?.forEach(quest => {
        // Extract NPCs from interactions
        quest.starters?.forEach(condition => {
          condition.triggers?.forEach(trigger => {
            if (trigger.type === 'interaction' && trigger.gameObject) {
              entities.push({
                id: trigger.gameObject,
                name: trigger.gameObject,
                type: 'npc',
                description: trigger.description
              });
            }
          });
        });
        
        quest.objectives?.forEach(condition => {
          condition.triggers?.forEach(trigger => {
            if (trigger.type === 'interaction' && trigger.gameObject) {
              entities.push({
                id: trigger.gameObject,
                name: trigger.gameObject,
                type: 'npc',
                description: trigger.description
              });
            }
          });
        });
        
        // Extract items from rewards
        quest.onSuccess?.items?.forEach(item => {
          entities.push({
            id: item.itemId,
            name: item.itemId,
            type: 'item',
            description: item.description
          });
        });
      });
    });
  }
  
  // Remove duplicates
  const uniqueEntities = entities.filter((entity, index, self) => 
    index === self.findIndex(e => e.id === entity.id && e.type === entity.type)
  );
  
  allEntities.value = uniqueEntities;
};

// Helper functions
const loadChapterNotes = async (chapterId) => {
  // This would be implemented with a real API call
  // For now, we'll use placeholder data
  console.log('Loading notes for chapter:', chapterId);
};

const loadChapterImages = async (chapterId) => {
  // This would be implemented with a real API call
  // For now, we'll use placeholder data
  console.log('Loading images for chapter:', chapterId);
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
/* CSS Units Strategy based on StoryScreen.MD */
html {
  font-size: 16px;
}

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

/* Main Story Builder Container */
.story-builder {
  height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 100vw;
  margin: 0 auto;
  position: relative;
  color: white;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(1px);
}

/* Header (3.75rem) */
.story-builder__header {
  height: 3.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1.5rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.header-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 215, 0, 0.1);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 6px;
  color: #ffd700;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.header-btn:hover {
  background: rgba(255, 215, 0, 0.2);
  border-color: rgba(255, 215, 0, 0.5);
}

.header-right {
  display: flex;
  align-items: center;
}

/* Main Content Area */
.story-builder__content {
  flex: 1;
  display: flex;
  overflow: hidden;
  min-height: 0;
}

/* Left Column: Timeline Navigation (25rem) */
.story-builder__left-column {
  width: 25rem;
  min-width: 20rem;
  background: rgba(255, 255, 255, 0.05);
  border-right: 1px solid rgba(255, 215, 0, 0.2);
  overflow-y: auto;
  padding: 1.5rem;
}

/* Right Column: Main Content/Editor (flexible) */
.story-builder__right-column {
  flex: 1;
  background: rgba(255, 255, 255, 0.03);
  overflow-y: auto;
  padding: 1.5rem;
}

/* Footer: Quick Reference Panel (7.5rem) */
.story-builder__footer {
  height: 7.5rem;
  min-height: 6rem;
  background: rgba(0, 0, 0, 0.4);
  border-top: 1px solid rgba(255, 215, 0, 0.2);
  padding: 1rem 1.5rem;
  backdrop-filter: blur(8px);
}

/* Typography */
.quest-title {
  font-size: 1.5rem;
  line-height: 1.4;
  font-weight: 600;
  color: #ffd700;
}

.description {
  font-size: 1rem;
  line-height: 1.6;
  color: #e0e0e0;
}

.metadata {
  font-size: 0.875rem;
  color: #b0b0b0;
}

/* Spacing utilities */
.section-gap {
  margin-bottom: 1.5rem;
}

.trigger-padding {
  padding: 1rem;
}

.form-field-spacing {
  margin-bottom: 0.75rem;
}

/* Responsive Breakpoints */
/* Large (>75rem): Full layout as shown */
@media (min-width: 75rem) {
  .story-builder__left-column {
    width: 25rem;
  }
}

/* Medium (48-75rem): Reduce left panel to 20rem */
@media (min-width: 48rem) and (max-width: 75rem) {
  .story-builder__left-column {
    width: 20rem;
    min-width: 18rem;
  }
}

/* Small (<48rem): Collapsible left panel, full-width right panel */
@media (max-width: 48rem) {
  .story-builder__content {
    flex-direction: column;
  }
  
  .story-builder__left-column {
    width: 100%;
    height: auto;
    min-width: unset;
    max-height: 40vh;
  }
  
  .story-builder__right-column {
    flex: 1;
    min-height: 0;
  }
  
  .story-builder__footer {
    height: auto;
    min-height: 5rem;
  }
  
  .story-builder__header {
    height: auto;
    flex-direction: column;
    gap: 0.75rem;
    padding: 1rem;
  }
  
  .header-left {
    flex-direction: column;
    gap: 1rem;
    width: 100%;
  }
  
  .header-actions {
    justify-content: center;
  }
}

/* Mobile adjustments */
@media (max-width: 768px) {
  .story-builder {
    padding: 0;
  }
  
  .story-builder__header {
    padding: 0.75rem;
  }
  
  .story-builder__left-column,
  .story-builder__right-column {
    padding: 1rem;
  }
  
  .story-builder__footer {
    padding: 0.75rem;
  }
  
  .header-btn {
    padding: 0.375rem 0.75rem;
    font-size: 0.8rem;
  }
}
</style>