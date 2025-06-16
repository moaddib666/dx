import {GameMasterApi} from '@/api/backendService.js';

/**
 * GameMasterCharacter Service
 * Handles fetching, caching, and managing character information for the WorldEditor
 * Maximum opened characters is limited to 2
 */
export class GameMasterCharacterService {
    constructor() {
        this.characters = new Map(); // Map of character IDs to character data
        this.openedCharacters = []; // Array of opened character IDs (max 2)
        this.isLoading = false;
        this.lastLoaded = null;
        this.eventListeners = new Map();
    }

    /**
     * Initialize the service
     */
    async initialize() {
        try {
            console.log('Initializing GameMasterCharacterService...');
            return true;
        } catch (error) {
            console.error('Failed to initialize GameMasterCharacterService:', error);
            throw error;
        }
    }

    /**
     * Load character information by ID
     * @param {string} characterId - The ID of the character to load
     * @param {boolean} forceRefresh - Whether to force a refresh from the server
     */
    async loadCharacter(characterId, forceRefresh = false) {
        if (!characterId) {
            console.error('Character ID is required');
            return null;
        }

        // Check if character is already loaded and not forcing refresh
        if (!forceRefresh && this.characters.has(characterId)) {
            console.log(`Character ${characterId} already loaded, using cached data`);
            return this.characters.get(characterId);
        }

        if (this.isLoading) {
            console.log('Character already loading, waiting for completion...');
            return null;
        }

        try {
            this.isLoading = true;
            this.emit('loadingStarted', characterId);

            console.log(`Loading character ${characterId} from server...`);
            const response = await GameMasterApi.gamemasterCharactersCharacterCardRetrieve(characterId);

            if (!response.data) {
                console.warn('Character API response is empty');
                return null;
            }

            const character = response.data;
            this.characters.set(characterId, character);
            this.lastLoaded = new Date();

            // Add to opened characters, maintaining max of 2
            this.addToOpenedCharacters(characterId);

            console.log(`Loaded character ${characterId}`);
            this.emit('characterLoaded', character);
            return character;
        } catch (error) {
            console.error(`Failed to load character ${characterId}:`, error);
            this.emit('loadingFailed', {characterId, error});
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Add a character ID to the opened characters list, maintaining max of 2
     * @param {string} characterId - The ID of the character to add
     */
    addToOpenedCharacters(characterId) {
        // Remove if already in the list
        const index = this.openedCharacters.indexOf(characterId);
        if (index > -1) {
            this.openedCharacters.splice(index, 1);
        }

        // Add to the beginning of the list
        this.openedCharacters.unshift(characterId);

        // Maintain max of 2 opened characters
        if (this.openedCharacters.length > 2) {
            this.openedCharacters.pop();
        }

        this.emit('openedCharactersChanged', this.openedCharacters);
    }

    /**
     * Get character by ID
     * @param {string} characterId - The ID of the character to get
     * @param {boolean} autoLoad - Whether to automatically load the character if not cached
     */
    async getCharacter(characterId, autoLoad = true) {
        if (this.characters.has(characterId)) {
            return this.characters.get(characterId);
        }

        if (autoLoad) {
            return this.loadCharacter(characterId);
        }

        return null;
    }

    /**
     * Get all opened characters
     */
    getOpenedCharacters() {
        return this.openedCharacters.map(id => this.characters.get(id)).filter(Boolean);
    }

    /**
     * Close a character (remove from opened characters)
     * @param {string} characterId - The ID of the character to close
     */
    closeCharacter(characterId) {
        const index = this.openedCharacters.indexOf(characterId);
        if (index > -1) {
            this.openedCharacters.splice(index, 1);
            this.emit('openedCharactersChanged', this.openedCharacters);
        }
    }

    /**
     * Refresh character information
     * @param {string} characterId - The ID of the character to refresh
     */
    async refreshCharacter(characterId) {
        try {
            console.log(`Refreshing character ${characterId}...`);
            const character = await this.loadCharacter(characterId, true);
            this.emit('characterRefreshed', character);
            return character;
        } catch (error) {
            console.error(`Failed to refresh character ${characterId}:`, error);
            this.emit('refreshFailed', {characterId, error});
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
        this.characters.clear();
        this.openedCharacters = [];
        this.isLoading = false;
        this.lastLoaded = null;
        console.log('GameMasterCharacterService reset');
        this.emit('reset');
    }
}

// Export singleton instance
export const gameMasterCharacterService = new GameMasterCharacterService();