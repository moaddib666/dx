import {GameMasterApi} from '@/api/backendService.js';

/**
 * Character Templates Service
 * Handles fetching, caching, and managing character templates for the WorldEditor
 */
export class CharacterTemplatesService {
    constructor() {
        this.templates = [];
        this.isLoading = false;
        this.lastLoaded = null;
        this.eventListeners = new Map();
    }

    /**
     * Initialize the service and load character templates
     */
    async initialize() {
        try {
            console.log('Initializing CharacterTemplatesService...');
            await this.loadTemplates();
            return this.templates;
        } catch (error) {
            console.error('Failed to initialize CharacterTemplatesService:', error);
            throw error;
        }
    }

    /**
     * Load character templates from the backend
     */
    async loadTemplates() {
        if (this.isLoading) {
            console.log('Character templates already loading, waiting for completion...');
            return this.templates;
        }

        try {
            this.isLoading = true;
            this.emit('loadingStarted');

            console.log('Loading character templates from server...');
            const response = await GameMasterApi.gamemasterCharacterTemplatesList();

            if (!response.data) {
                console.warn('Character Templates API response is empty');
                this.templates = [];
                return this.templates;
            }

            // Handle response format (array or object with results)
            let templates = [];
            if (Array.isArray(response.data)) {
                templates = response.data;
            } else if (response.data.results) {
                templates = response.data.results;
            } else {
                console.warn('Character Templates API response has unexpected format:', response.data);
                this.templates = [];
                return this.templates;
            }

            this.templates = templates;
            this.lastLoaded = new Date();
            console.log(`Loaded ${this.templates.length} character templates`);

            // Log sample templates for debugging
            if (this.templates.length > 0) {
                console.log('Sample template:', this.templates[0]);
            }

            this.emit('templatesLoaded', this.templates);
            return this.templates;
        } catch (error) {
            console.error('Failed to load character templates:', error);
            this.emit('loadingFailed', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Get all character templates
     */
    getTemplates() {
        return this.templates;
    }

    /**
     * Get character template by ID
     */
    getTemplateById(id) {
        return this.templates.find(template => template.id === id);
    }

    /**
     * Get character templates by behavior type
     */
    getTemplatesByBehavior(behavior) {
        return this.templates.filter(template => template.behavior === behavior);
    }

    /**
     * Search character templates by name
     */
    searchTemplates(query) {
        if (!query) return this.templates;

        const lowerQuery = query.toLowerCase();
        return this.templates.filter(template =>
            template.name.toLowerCase().includes(lowerQuery) ||
            (template.description && template.description.toLowerCase().includes(lowerQuery))
        );
    }

    /**
     * Create a new NPC from a template at a specific position
     */
    async createNpcFromTemplate(templateId, position) {
        try {
            console.log(`Creating NPC from template ${templateId} at position ${JSON.stringify(position)}`);
            const createNPCFromTemplateRequest = {
                template_id: templateId,
                position_id: position.id.toString() // Ensure position_id is a string UUID
            };

            const response = await GameMasterApi.gamemasterCharacterTemplatesCreateNpcCreate(
                createNPCFromTemplateRequest
            );

            console.log('NPC created successfully:', response.data);
            this.emit('npcCreated', response.data);
            return response.data;
        } catch (error) {
            console.error('Failed to create NPC from template:', error);
            this.emit('npcCreationFailed', error);
            throw error;
        }
    }

    /**
     * Refresh character templates from the server
     */
    async refresh() {
        try {
            console.log('Refreshing character templates...');
            await this.loadTemplates();
            this.emit('refreshed', this.templates);
            return this.templates;
        } catch (error) {
            console.error('Failed to refresh character templates:', error);
            this.emit('refreshFailed', error);
            throw error;
        }
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
     * Reset the service to initial state
     */
    reset() {
        this.templates = [];
        this.isLoading = false;
        this.lastLoaded = null;
        console.log('CharacterTemplatesService reset');
        this.emit('reset');
    }
}

// Export singleton instance
export const characterTemplatesService = new CharacterTemplatesService();
