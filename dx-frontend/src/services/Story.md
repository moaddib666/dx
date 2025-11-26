# Story Service Documentation

The Story Service provides a comprehensive interface for managing stories, chapters, quests, and related components in the game. It handles all interactions with the backend API and maintains a local state for efficient access to story data.

## Installation

The Story Service is already included in the project. To use it, simply import the singleton instance:

```javascript
import { storyService } from '@/services/Story';
```

## Initialization

Before using the service, you should initialize it to load data from the backend:

```javascript
// In your component's mounted or created hook
async mounted() {
  try {
    await storyService.initialize();
    // Service is now ready to use
  } catch (error) {
    console.error('Failed to initialize Story service:', error);
  }
}
```

## Event System

The Story Service uses an event system to notify components of changes. You can subscribe to events using the `on` method:

```javascript
// Subscribe to events
storyService.on('storyCreated', (story) => {
  console.log('A new story was created:', story);
});

// Unsubscribe when component is destroyed
beforeDestroy() {
  storyService.off('storyCreated', this.myCallback);
}
```

### Available Events

- `initialized`: Fired when the service is initialized
- `storyCreated`: Fired when a new story is created
- `storyUpdated`: Fired when a story is updated
- `storyDeleted`: Fired when a story is deleted
- `chapterCreated`: Fired when a new chapter is created
- `chapterUpdated`: Fired when a chapter is updated
- `chapterDeleted`: Fired when a chapter is deleted
- `questCreated`: Fired when a new quest is created
- `questUpdated`: Fired when a quest is updated
- `questDeleted`: Fired when a quest is deleted
- `conditionCreated`: Fired when a new condition is created
- `conditionUpdated`: Fired when a condition is updated
- `conditionDeleted`: Fired when a condition is deleted
- `triggerCreated`: Fired when a new trigger is created
- `triggerUpdated`: Fired when a trigger is updated
- `triggerDeleted`: Fired when a trigger is deleted
- `rewardCreated`: Fired when a new reward is created
- `rewardUpdated`: Fired when a reward is updated
- `rewardDeleted`: Fired when a reward is deleted
- `noteCreated`: Fired when a new note is created
- `noteUpdated`: Fired when a note is updated
- `noteDeleted`: Fired when a note is deleted
- `currentStoryChanged`: Fired when the current story is changed
- `selectedChapterChanged`: Fired when the selected chapter is changed
- `selectedQuestChanged`: Fired when the selected quest is changed
- `selectionsCleared`: Fired when selections are cleared
- `refreshed`: Fired when the service data is refreshed
- `refreshFailed`: Fired when the service refresh fails
- `reset`: Fired when the service is reset

## Managing Stories

### Loading Stories

```javascript
// Load all stories
const stories = await storyService.loadStories();

// Load a specific story by ID
const story = await storyService.loadStory('story-id');
```

### Creating a Story

```javascript
const newStory = await storyService.createStory({
  title: 'My New Story',
  description: 'A description of my new story'
});
```

### Updating a Story

```javascript
const updatedStory = await storyService.updateStory('story-id', {
  title: 'Updated Story Title',
  description: 'Updated description'
});
```

### Deleting a Story

```javascript
const success = await storyService.deleteStory('story-id');
```

### Setting a Story as Canonical

```javascript
const canonicalStory = await storyService.setStoryCanonical('story-id');
```

### Unsetting a Story as Canonical

```javascript
const nonCanonicalStory = await storyService.unsetStoryCanonical('story-id');
```

## Managing Chapters

### Loading Chapters

```javascript
const chapters = await storyService.loadChapters('story-id');
```

### Creating a Chapter

```javascript
const newChapter = await storyService.createChapter({
  title: 'My New Chapter',
  description: 'A description of my new chapter',
  story: 'story-id'
});
```

### Updating a Chapter

```javascript
const updatedChapter = await storyService.updateChapter('chapter-id', {
  title: 'Updated Chapter Title',
  description: 'Updated description'
});
```

### Deleting a Chapter

```javascript
const success = await storyService.deleteChapter('chapter-id');
```

## Managing Quests

### Loading Quests

```javascript
const quests = await storyService.loadQuests('chapter-id');
```

### Creating a Quest

```javascript
const newQuest = await storyService.createQuest({
  title: 'My New Quest',
  description: 'A description of my new quest',
  chapter: 'chapter-id'
});
```

### Updating a Quest

```javascript
const updatedQuest = await storyService.updateQuest('quest-id', {
  title: 'Updated Quest Title',
  description: 'Updated description'
});
```

### Deleting a Quest

```javascript
const success = await storyService.deleteQuest('quest-id');
```

## Managing Conditions, Triggers, and Rewards

The service provides similar methods for managing conditions, triggers, and rewards. See the service implementation for details.

## State Management

### Getting the Current State

```javascript
const state = storyService.getState();
console.log('Current stories:', state.stories);
console.log('Current story:', state.currentStory);
```

### Setting the Current Story

```javascript
storyService.setCurrentStory('story-id');
```

### Setting the Selected Chapter

```javascript
storyService.setSelectedChapter(chapterObject);
```

### Setting the Selected Quest

```javascript
storyService.setSelectedQuest(questObject);
```

### Clearing Selections

```javascript
storyService.clearSelections();
```

## Refreshing and Resetting

### Refreshing Data

```javascript
await storyService.refresh();
```

### Resetting the Service

```javascript
storyService.reset();
```

## Integration with Other Services

The Story Service is designed to work with other services like ItemsGameApi, CharacterGameApi, and EffectsGameApi. These integrations allow for comprehensive story management that includes items, characters, and effects.

## Error Handling

All methods in the Story Service include error handling. Errors are logged to the console and thrown to the caller. You should wrap calls to the service in try-catch blocks to handle errors appropriately.

```javascript
try {
  const story = await storyService.createStory({
    title: 'My Story',
    description: 'My description'
  });
} catch (error) {
  console.error('Failed to create story:', error);
  // Handle the error appropriately
}
```

## Example Usage

Here's a complete example of using the Story Service in a Vue component:

```vue
<template>
  <div>
    <h1>Story Manager</h1>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <h2>Stories</h2>
      <ul>
        <li v-for="story in stories" :key="story.id">
          {{ story.title }}
          <button @click="selectStory(story.id)">Select</button>
          <button @click="deleteStory(story.id)">Delete</button>
        </li>
      </ul>
      <button @click="createNewStory">Create New Story</button>
      
      <div v-if="currentStory">
        <h2>Current Story: {{ currentStory.title }}</h2>
        <h3>Chapters</h3>
        <ul>
          <li v-for="chapter in chapters" :key="chapter.id">
            {{ chapter.title }}
            <button @click="selectChapter(chapter)">Select</button>
          </li>
        </ul>
        <button @click="createNewChapter">Create New Chapter</button>
      </div>
    </div>
  </div>
</template>

<script>
import { storyService } from '@/services/Story';

export default {
  data() {
    return {
      loading: true,
      stories: [],
      currentStory: null,
      chapters: []
    };
  },
  
  async mounted() {
    try {
      // Initialize the service
      await storyService.initialize();
      
      // Get the initial state
      const state = storyService.getState();
      this.stories = Array.from(state.stories.values());
      this.currentStory = state.currentStory;
      
      // Load chapters if there's a current story
      if (this.currentStory) {
        this.chapters = await storyService.loadChapters(this.currentStory.id);
      }
      
      // Subscribe to events
      storyService.on('storyCreated', this.handleStoryCreated);
      storyService.on('storyDeleted', this.handleStoryDeleted);
      storyService.on('currentStoryChanged', this.handleCurrentStoryChanged);
      storyService.on('chapterCreated', this.handleChapterCreated);
      
      this.loading = false;
    } catch (error) {
      console.error('Failed to initialize Story Manager:', error);
      this.loading = false;
    }
  },
  
  beforeDestroy() {
    // Unsubscribe from events
    storyService.off('storyCreated', this.handleStoryCreated);
    storyService.off('storyDeleted', this.handleStoryDeleted);
    storyService.off('currentStoryChanged', this.handleCurrentStoryChanged);
    storyService.off('chapterCreated', this.handleChapterCreated);
  },
  
  methods: {
    async createNewStory() {
      try {
        await storyService.createStory({
          title: 'New Story',
          description: 'A new story created from the Story Manager'
        });
      } catch (error) {
        console.error('Failed to create story:', error);
      }
    },
    
    async selectStory(storyId) {
      try {
        storyService.setCurrentStory(storyId);
        this.chapters = await storyService.loadChapters(storyId);
      } catch (error) {
        console.error('Failed to select story:', error);
      }
    },
    
    async deleteStory(storyId) {
      try {
        await storyService.deleteStory(storyId);
      } catch (error) {
        console.error('Failed to delete story:', error);
      }
    },
    
    async createNewChapter() {
      if (!this.currentStory) return;
      
      try {
        await storyService.createChapter({
          title: 'New Chapter',
          description: 'A new chapter created from the Story Manager',
          story: this.currentStory.id
        });
      } catch (error) {
        console.error('Failed to create chapter:', error);
      }
    },
    
    selectChapter(chapter) {
      storyService.setSelectedChapter(chapter);
    },
    
    // Event handlers
    handleStoryCreated(story) {
      this.stories.push(story);
    },
    
    handleStoryDeleted(data) {
      const index = this.stories.findIndex(story => story.id === data.storyId);
      if (index !== -1) {
        this.stories.splice(index, 1);
      }
      
      if (this.currentStory && this.currentStory.id === data.storyId) {
        this.currentStory = null;
        this.chapters = [];
      }
    },
    
    handleCurrentStoryChanged(story) {
      this.currentStory = story;
    },
    
    handleChapterCreated(chapter) {
      if (this.currentStory && chapter.story === this.currentStory.id) {
        this.chapters.push(chapter);
      }
    }
  }
};
</script>
```

This example demonstrates how to use the Story Service to manage stories and chapters in a Vue component. It includes initialization, event handling, and basic CRUD operations.