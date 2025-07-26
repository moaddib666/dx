// Service that loads stories, chapters, and quests from the GM API
// Provides methods to get stories, chapters, and quests
// Provides mapping between stories, chapters, and quests in both directions
import {StoryGameApi} from '@/api/backendService';
import {
    Story,
    Chapter,
    Quest,
    StoryApi,
} from '@/api/dx-backend';

export class GMStories {
    private stories: Story[] = [];
    private chapters: Chapter[] = [];
    private quests: Quest[] = [];
    private storyMap: Map<string, Story> = new Map();
    private chapterMap: Map<string, Chapter> = new Map();
    private questMap: Map<string, Quest> = new Map();
    private chapterToStoryMap: Map<string, string> = new Map();
    private questToChapterMap: Map<string, string> = new Map();

    constructor(private api: StoryApi) {
    }

    async ensureInitialized(): Promise<void> {
        // Ensure the service is initialized by loading stories
        if (this.stories.length === 0) {
            await this.refresh();
        }
    }

    /**
     * Loads all stories, chapters, and quests from the API
     */
    async refresh(): Promise<void> {
        await this.loadStories();
    }

    /**
     * Loads all stories from the API
     */
    async loadStories(): Promise<Story[]> {
        try {
            const response = await this.api.storyStoriesList();
            this.stories = response.data;

            // Update the story map
            this.storyMap.clear();
            this.chapterMap.clear();
            this.questMap.clear();
            for (const story of this.stories) {
                this.storyMap.set(story.id, story);
                for (const chapter of story.chapters || []) {
                    this.chapterMap.set(chapter.id, chapter);
                    this.chapterToStoryMap.set(chapter.id, story.id);
                    this.chapters.push(chapter);
                    for (const quest of chapter.quests || []) {
                        this.questMap.set(quest.id, quest);
                        this.questToChapterMap.set(quest.id, chapter.id);
                        this.quests.push(quest);
                    }
                }
            }
            return this.stories;
        } catch (error) {
            console.error('Error loading stories:', error);
            throw error;
        }
    }

    /**
     * Gets all stories
     */
    getStories(): Story[] {
        return this.stories;
    }

    /**
     * Gets a story by ID
     */
    getStoryById(storyId: string): Story | undefined {
        return this.storyMap.get(storyId);
    }

    /**
     * Gets all chapters
     */
    getChapters(): Chapter[] {
        return this.chapters;
    }

    /**
     * Gets a chapter by ID
     */
    getChapterById(chapterId: string): Chapter | undefined {
        return this.chapterMap.get(chapterId);
    }

    /**
     * Gets all quests
     */
    getQuests(): Quest[] {
        return this.quests;
    }

    /**
     * Gets a quest by ID
     */
    getQuestById(questId: string): Quest | undefined {
        return this.questMap.get(questId);
    }

    /**
     * Gets chapters for a specific story
     */
    getChaptersForStory(storyId: string): Chapter[] {
        return this.chapters.filter(chapter => chapter.story === storyId);
    }

    /**
     * Gets quests for a specific chapter
     */
    getQuestsForChapter(chapterId: string): Quest[] {
        return this.quests.filter(quest => quest.chapter === chapterId);
    }

    /**
     * Gets the parent story for a chapter
     */
    getStoryForChapter(chapterId: string): Story | undefined {
        const storyId = this.chapterToStoryMap.get(chapterId);
        if (storyId) {
            return this.storyMap.get(storyId);
        }
        return undefined;
    }

    /**
     * Gets the parent chapter for a quest
     */
    getChapterForQuest(questId: string): Chapter | undefined {
        const chapterId = this.questToChapterMap.get(questId);
        if (chapterId) {
            return this.chapterMap.get(chapterId);
        }
        return undefined;
    }

    /**
     * Gets the parent story for a quest
     */
    getStoryForQuest(questId: string): Story | undefined {
        const chapter = this.getChapterForQuest(questId);
        if (chapter) {
            return this.getStoryForChapter(chapter.id);
        }
        return undefined;
    }
}

export const gmStories = new GMStories(StoryGameApi);