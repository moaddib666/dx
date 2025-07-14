import { StoryGameApi, ItemsGameApi, CharacterGameApi, EffectsGameApi } from '@/api/backendService';
import {
    Story,
    StoryDetail,
    StoryRequest,
    Chapter,
    ChapterRequest,
    Quest,
    QuestRequest,
    Condition,
    ConditionRequest,
    Trigger,
    TriggerRequest,
    Reward,
    RewardRequest,
    ItemReward,
    TokenReward,
    EffectReward,
    Note,
    NoteRequest
} from '@/api/dx-backend';

/**
 * StoryState class to manage the state of the Story service
 */
class StoryState {
    stories: Map<string, Story> = new Map();
    currentStory: Story | null = null;
    selectedChapter: Chapter | null = null;
    selectedQuest: Quest | null = null;

    constructor() {}

    /**
     * Add or update a story in the state
     */
    addStory(story: Story) {
        this.stories.set(story.id, story);
    }

    /**
     * Remove a story from the state
     */
    removeStory(storyId: string) {
        this.stories.delete(storyId);
        if (this.currentStory && this.currentStory.id === storyId) {
            this.currentStory = null;
        }
    }

    /**
     * Set the current story
     */
    setCurrentStory(story: Story) {
        this.currentStory = story;
    }

    /**
     * Set the selected chapter
     */
    setSelectedChapter(chapter: Chapter) {
        this.selectedChapter = chapter;
    }

    /**
     * Set the selected quest
     */
    setSelectedQuest(quest: Quest) {
        this.selectedQuest = quest;
    }

    /**
     * Clear selections
     */
    clearSelections() {
        this.selectedChapter = null;
        this.selectedQuest = null;
    }
}

/**
 * Story Service
 * Handles story data management, API interactions, and state synchronization
 */
export class StoryService {
    constructor() {
        this.state = new StoryState();
        this.eventListeners = new Map();
        this.isInitialized = false;
    }

    /**
     * Initialize the Story service with data from the backend
     */
    async initialize() {
        try {
            console.log('Initializing Story service...');

            // Load stories from the backend
            const stories = await this.loadStories();

            console.log(`Loaded ${stories.length} stories`);

            // Add stories to the state
            stories.forEach(story => {
                this.state.addStory(story);
            });

            this.isInitialized = true;
            this.emit('initialized', this.state);
            return this.state;
        } catch (error) {
            console.error('Failed to initialize Story service:', error);
            this.isInitialized = false;
            throw error;
        }
    }

    /**
     * Load stories from the backend
     */
    async loadStories() {
        try {
            const response = await StoryGameApi.storyStoriesList();

            if (!response.data) {
                console.warn('Stories API response is empty');
                return [];
            }

            let stories = [];
            if (Array.isArray(response.data)) {
                stories = response.data;
            } else if (response.data.results) {
                stories = response.data.results;
            } else {
                console.warn('Stories API response has unexpected format:', response.data);
                return [];
            }

            return stories;
        } catch (error) {
            console.error('Failed to load stories:', error);
            throw error;
        }
    }

    /**
     * Load a story by ID
     */
    async loadStory(storyId: string) {
        try {
            const response = await StoryGameApi.storyStoriesRetrieve(storyId);

            if (!response.data) {
                console.warn(`Story API response for ID ${storyId} is empty`);
                return null;
            }

            const story = response.data;
            this.state.addStory(story);

            return story;
        } catch (error) {
            console.error(`Failed to load story with ID ${storyId}:`, error);
            throw error;
        }
    }

    /**
     * Create a new story
     */
    async createStory(storyData: StoryRequest) {
        try {
            const response = await StoryGameApi.storyStoriesCreate(storyData);

            if (!response.data) {
                console.warn('Story creation API response is empty');
                return null;
            }

            const story = response.data;
            this.state.addStory(story);
            this.emit('storyCreated', story);

            return story;
        } catch (error) {
            console.error('Failed to create story:', error);
            throw error;
        }
    }

    /**
     * Update a story
     */
    async updateStory(storyId: string, storyData: StoryRequest) {
        try {
            const response = await StoryGameApi.storyStoriesUpdate(storyId, storyData);

            if (!response.data) {
                console.warn(`Story update API response for ID ${storyId} is empty`);
                return null;
            }

            const story = response.data;
            this.state.addStory(story);
            this.emit('storyUpdated', story);

            return story;
        } catch (error) {
            console.error(`Failed to update story with ID ${storyId}:`, error);
            throw error;
        }
    }

    /**
     * Delete a story
     */
    async deleteStory(storyId: string) {
        try {
            await StoryGameApi.storyStoriesDestroy(storyId);

            this.state.removeStory(storyId);
            this.emit('storyDeleted', { storyId });

            return true;
        } catch (error) {
            console.error(`Failed to delete story with ID ${storyId}:`, error);
            throw error;
        }
    }

    /**
     * Set a story as canonical
     */
    async setStoryCanonical(storyId: string) {
        try {
            const story = this.state.stories.get(storyId);
            if (!story) {
                throw new Error(`Story with ID ${storyId} not found in state`);
            }

            const response = await StoryGameApi.storyStoriesSetCanonicalCreate(storyId, {
                title: story.title,
                description: story.description
            });

            if (!response.data) {
                console.warn(`Set canonical API response for ID ${storyId} is empty`);
                return null;
            }

            const updatedStory = response.data;
            this.state.addStory(updatedStory);
            this.emit('storyUpdated', updatedStory);

            return updatedStory;
        } catch (error) {
            console.error(`Failed to set story with ID ${storyId} as canonical:`, error);
            throw error;
        }
    }

    /**
     * Unset a story as canonical
     */
    async unsetStoryCanonical(storyId: string) {
        try {
            const story = this.state.stories.get(storyId);
            if (!story) {
                throw new Error(`Story with ID ${storyId} not found in state`);
            }

            const response = await StoryGameApi.storyStoriesUnsetCanonicalCreate(storyId, {
                title: story.title,
                description: story.description
            });

            if (!response.data) {
                console.warn(`Unset canonical API response for ID ${storyId} is empty`);
                return null;
            }

            const updatedStory = response.data;
            this.state.addStory(updatedStory);
            this.emit('storyUpdated', updatedStory);

            return updatedStory;
        } catch (error) {
            console.error(`Failed to unset story with ID ${storyId} as canonical:`, error);
            throw error;
        }
    }

    /**
     * Load chapters for a story
     */
    async loadChapters(storyId: string) {
        try {
            const response = await StoryGameApi.storyChaptersList(null, storyId);

            if (!response.data) {
                console.warn(`Chapters API response for story ID ${storyId} is empty`);
                return [];
            }

            let chapters = [];
            if (Array.isArray(response.data)) {
                chapters = response.data;
            } else if (response.data.results) {
                chapters = response.data.results;
            } else {
                console.warn('Chapters API response has unexpected format:', response.data);
                return [];
            }

            return chapters;
        } catch (error) {
            console.error(`Failed to load chapters for story with ID ${storyId}:`, error);
            throw error;
        }
    }

    /**
     * Create a new chapter
     */
    async createChapter(chapterData: ChapterRequest) {
        try {
            const response = await StoryGameApi.storyChaptersCreate(chapterData);

            if (!response.data) {
                console.warn('Chapter creation API response is empty');
                return null;
            }

            const chapter = response.data;
            this.emit('chapterCreated', chapter);

            return chapter;
        } catch (error) {
            console.error('Failed to create chapter:', error);
            throw error;
        }
    }

    /**
     * Update a chapter
     */
    async updateChapter(chapterId: string, chapterData: ChapterRequest) {
        try {
            const response = await StoryGameApi.storyChaptersUpdate(chapterId, chapterData);

            if (!response.data) {
                console.warn(`Chapter update API response for ID ${chapterId} is empty`);
                return null;
            }

            const chapter = response.data;
            this.emit('chapterUpdated', chapter);

            return chapter;
        } catch (error) {
            console.error(`Failed to update chapter with ID ${chapterId}:`, error);
            throw error;
        }
    }

    /**
     * Delete a chapter
     */
    async deleteChapter(chapterId: string) {
        try {
            await StoryGameApi.storyChaptersDestroy(chapterId);

            this.emit('chapterDeleted', { chapterId });

            return true;
        } catch (error) {
            console.error(`Failed to delete chapter with ID ${chapterId}:`, error);
            throw error;
        }
    }

    /**
     * Load quests for a chapter
     */
    async loadQuests(chapterId: string) {
        try {
            const response = await StoryGameApi.storyQuestsList(chapterId, null);

            if (!response.data) {
                console.warn(`Quests API response for chapter ID ${chapterId} is empty`);
                return [];
            }

            let quests = [];
            if (Array.isArray(response.data)) {
                quests = response.data;
            } else if (response.data.results) {
                quests = response.data.results;
            } else {
                console.warn('Quests API response has unexpected format:', response.data);
                return [];
            }

            return quests;
        } catch (error) {
            console.error(`Failed to load quests for chapter with ID ${chapterId}:`, error);
            throw error;
        }
    }

    /**
     * Create a new quest
     */
    async createQuest(questData: QuestRequest) {
        try {
            const response = await StoryGameApi.storyQuestsCreate(questData);

            if (!response.data) {
                console.warn('Quest creation API response is empty');
                return null;
            }

            const quest = response.data;
            this.emit('questCreated', quest);

            return quest;
        } catch (error) {
            console.error('Failed to create quest:', error);
            throw error;
        }
    }

    /**
     * Update a quest
     */
    async updateQuest(questId: string, questData: QuestRequest) {
        try {
            const response = await StoryGameApi.storyQuestsUpdate(questId, questData);

            if (!response.data) {
                console.warn(`Quest update API response for ID ${questId} is empty`);
                return null;
            }

            const quest = response.data;
            this.emit('questUpdated', quest);

            return quest;
        } catch (error) {
            console.error(`Failed to update quest with ID ${questId}:`, error);
            throw error;
        }
    }

    /**
     * Delete a quest
     */
    async deleteQuest(questId: string) {
        try {
            await StoryGameApi.storyQuestsDestroy(questId);

            this.emit('questDeleted', { questId });

            return true;
        } catch (error) {
            console.error(`Failed to delete quest with ID ${questId}:`, error);
            throw error;
        }
    }

    /**
     * Create a new condition
     */
    async createCondition(conditionData: ConditionRequest) {
        try {
            const response = await StoryGameApi.storyConditionsCreate(conditionData);

            if (!response.data) {
                console.warn('Condition creation API response is empty');
                return null;
            }

            const condition = response.data;
            this.emit('conditionCreated', condition);

            return condition;
        } catch (error) {
            console.error('Failed to create condition:', error);
            throw error;
        }
    }

    /**
     * Update a condition
     */
    async updateCondition(conditionId: string, conditionData: ConditionRequest) {
        try {
            const response = await StoryGameApi.storyConditionsUpdate(conditionId, conditionData);

            if (!response.data) {
                console.warn(`Condition update API response for ID ${conditionId} is empty`);
                return null;
            }

            const condition = response.data;
            this.emit('conditionUpdated', condition);

            return condition;
        } catch (error) {
            console.error(`Failed to update condition with ID ${conditionId}:`, error);
            throw error;
        }
    }

    /**
     * Delete a condition
     */
    async deleteCondition(conditionId: string) {
        try {
            await StoryGameApi.storyConditionsDestroy(conditionId);

            this.emit('conditionDeleted', { conditionId });

            return true;
        } catch (error) {
            console.error(`Failed to delete condition with ID ${conditionId}:`, error);
            throw error;
        }
    }

    /**
     * Create a new trigger
     */
    async createTrigger(triggerData: TriggerRequest) {
        try {
            const response = await StoryGameApi.storyTriggersCreate(triggerData);

            if (!response.data) {
                console.warn('Trigger creation API response is empty');
                return null;
            }

            const trigger = response.data;
            this.emit('triggerCreated', trigger);

            return trigger;
        } catch (error) {
            console.error('Failed to create trigger:', error);
            throw error;
        }
    }

    /**
     * Update a trigger
     */
    async updateTrigger(triggerId: string, triggerData: TriggerRequest) {
        try {
            const response = await StoryGameApi.storyTriggersUpdate(triggerId, triggerData);

            if (!response.data) {
                console.warn(`Trigger update API response for ID ${triggerId} is empty`);
                return null;
            }

            const trigger = response.data;
            this.emit('triggerUpdated', trigger);

            return trigger;
        } catch (error) {
            console.error(`Failed to update trigger with ID ${triggerId}:`, error);
            throw error;
        }
    }

    /**
     * Delete a trigger
     */
    async deleteTrigger(triggerId: string) {
        try {
            await StoryGameApi.storyTriggersDestroy(triggerId);

            this.emit('triggerDeleted', { triggerId });

            return true;
        } catch (error) {
            console.error(`Failed to delete trigger with ID ${triggerId}:`, error);
            throw error;
        }
    }

    /**
     * Create a new reward
     */
    async createReward(rewardData: RewardRequest) {
        try {
            const response = await StoryGameApi.storyRewardsCreate(rewardData);

            if (!response.data) {
                console.warn('Reward creation API response is empty');
                return null;
            }

            const reward = response.data;
            this.emit('rewardCreated', reward);

            return reward;
        } catch (error) {
            console.error('Failed to create reward:', error);
            throw error;
        }
    }

    /**
     * Update a reward
     */
    async updateReward(rewardId: string, rewardData: RewardRequest) {
        try {
            const response = await StoryGameApi.storyRewardsUpdate(rewardId, rewardData);

            if (!response.data) {
                console.warn(`Reward update API response for ID ${rewardId} is empty`);
                return null;
            }

            const reward = response.data;
            this.emit('rewardUpdated', reward);

            return reward;
        } catch (error) {
            console.error(`Failed to update reward with ID ${rewardId}:`, error);
            throw error;
        }
    }

    /**
     * Delete a reward
     */
    async deleteReward(rewardId: string) {
        try {
            await StoryGameApi.storyRewardsDestroy(rewardId);

            this.emit('rewardDeleted', { rewardId });

            return true;
        } catch (error) {
            console.error(`Failed to delete reward with ID ${rewardId}:`, error);
            throw error;
        }
    }

    /**
     * Create a new note
     */
    async createNote(noteData: NoteRequest) {
        try {
            const response = await StoryGameApi.storyNotesCreate(noteData);

            if (!response.data) {
                console.warn('Note creation API response is empty');
                return null;
            }

            const note = response.data;
            this.emit('noteCreated', note);

            return note;
        } catch (error) {
            console.error('Failed to create note:', error);
            throw error;
        }
    }

    /**
     * Update a note
     */
    async updateNote(noteId: string, noteData: NoteRequest) {
        try {
            const response = await StoryGameApi.storyNotesUpdate(noteId, noteData);

            if (!response.data) {
                console.warn(`Note update API response for ID ${noteId} is empty`);
                return null;
            }

            const note = response.data;
            this.emit('noteUpdated', note);

            return note;
        } catch (error) {
            console.error(`Failed to update note with ID ${noteId}:`, error);
            throw error;
        }
    }

    /**
     * Delete a note
     */
    async deleteNote(noteId: string) {
        try {
            await StoryGameApi.storyNotesDestroy(noteId);

            this.emit('noteDeleted', { noteId });

            return true;
        } catch (error) {
            console.error(`Failed to delete note with ID ${noteId}:`, error);
            throw error;
        }
    }

    /**
     * Set the current story
     */
    setCurrentStory(storyId: string) {
        const story = this.state.stories.get(storyId);
        if (!story) {
            throw new Error(`Story with ID ${storyId} not found in state`);
        }

        this.state.setCurrentStory(story);
        this.state.clearSelections();
        this.emit('currentStoryChanged', story);
    }

    /**
     * Set the selected chapter
     */
    setSelectedChapter(chapter: Chapter) {
        this.state.setSelectedChapter(chapter);
        this.emit('selectedChapterChanged', chapter);
    }

    /**
     * Set the selected quest
     */
    setSelectedQuest(quest: Quest) {
        this.state.setSelectedQuest(quest);
        this.emit('selectedQuestChanged', quest);
    }

    /**
     * Clear selections
     */
    clearSelections() {
        this.state.clearSelections();
        this.emit('selectionsCleared');
    }

    /**
     * Get current state
     */
    getState() {
        return this.state;
    }

    /**
     * Event system for components to listen to changes
     */
    on(event, callback) {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event).push(callback);
    }

    /**
     * Remove event listener
     */
    off(event, callback) {
        if (this.eventListeners.has(event)) {
            const listeners = this.eventListeners.get(event);
            const index = listeners.indexOf(callback);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        }
    }

    /**
     * Emit event to listeners
     */
    emit(event, data) {
        if (this.eventListeners.has(event)) {
            this.eventListeners.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in event listener for ${event}:`, error);
                }
            });
        }
    }

    /**
     * Refresh data from backend
     */
    async refresh() {
        if (!this.isInitialized) {
            console.log('Story service not initialized, calling initialize instead of refresh');
            return await this.initialize();
        }

        try {
            console.log('Refreshing story data...');

            // Load stories from the backend
            const stories = await this.loadStories();

            console.log(`Refreshed ${stories.length} stories`);

            // Clear existing stories and add the refreshed ones
            this.state.stories.clear();
            stories.forEach(story => {
                this.state.addStory(story);
            });

            // If there was a current story, try to find it in the refreshed data
            if (this.state.currentStory) {
                const currentStoryId = this.state.currentStory.id;
                const refreshedCurrentStory = stories.find(story => story.id === currentStoryId);
                if (refreshedCurrentStory) {
                    this.state.setCurrentStory(refreshedCurrentStory);
                } else {
                    this.state.currentStory = null;
                }
            }

            this.emit('refreshed', this.state);
            return this.state;
        } catch (error) {
            console.error('Failed to refresh story data:', error);
            this.emit('refreshFailed', error);
            throw error;
        }
    }

    /**
     * Reset the service to initial state
     */
    reset() {
        this.state = new StoryState();
        this.isInitialized = false;
        console.log('Story service reset');
        this.emit('reset');
    }
}

// Export singleton instance
export const storyService = new StoryService();