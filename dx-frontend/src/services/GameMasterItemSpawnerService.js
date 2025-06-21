import { GameMasterApi } from '@/api/backendService.js';

/**
 * GameMasterItemSpawner Service
 * Handles spawning items to characters or positions in the game world
 */
export class GameMasterItemSpawnerService {
    constructor() {
        this.isSpawning = false;
        this.eventListeners = new Map();
    }

    /**
     * Initialize the service
     */
    async initialize() {
        try {
            console.log('Initializing GameMasterItemSpawnerService...');
            return true;
        } catch (error) {
            console.error('Failed to initialize GameMasterItemSpawnerService:', error);
            throw error;
        }
    }

    /**
     * Spawn an item to a character's inventory
     * @param {string} itemId - The ID of the item to spawn
     * @param {string} characterId - The ID of the character to give the item to
     */
    async spawnItemToCharacter(itemId, characterId) {
        console.log('GameMasterItemSpawnerService.spawnItemToCharacter called with:', { itemId, characterId });

        if (!itemId || !characterId) {
            console.error('Item ID and Character ID are required');
            return null;
        }

        if (this.isSpawning) {
            console.log('Item already spawning, waiting for completion...');
            return null;
        }

        try {
            this.isSpawning = true;
            this.emit('spawnStarted', { itemId, characterId });

            console.log(`Spawning item ${itemId} to character ${characterId}...`);
            console.log('Calling GameMasterApi.spawnItem with:', {
                itemId,
                request: { to_character_id: characterId }
            });

            const response = await GameMasterApi.spawnItem(itemId, {
                to_character_id: characterId
            });

            if (!response.data) {
                console.warn('Spawn item API response is empty');
                return null;
            }

            const result = response.data;
            console.log(`Spawned item ${itemId} to character ${characterId}`);
            this.emit('itemSpawnedToCharacter', { itemId, characterId, result });
            return result;
        } catch (error) {
            console.error(`Failed to spawn item ${itemId} to character ${characterId}:`, error);
            this.emit('spawnFailed', { itemId, characterId, error });
            throw error;
        } finally {
            this.isSpawning = false;
        }
    }

    /**
     * Spawn an item to a position in the game world
     * @param {string} itemId - The ID of the item to spawn
     * @param {string} positionId - The ID of the position to place the item at
     */
    async spawnItemToPosition(itemId, positionId) {
        console.log('GameMasterItemSpawnerService.spawnItemToPosition called with:', { itemId, positionId });

        if (!itemId || !positionId) {
            console.error('Item ID and Position ID are required');
            return null;
        }

        if (this.isSpawning) {
            console.log('Item already spawning, waiting for completion...');
            return null;
        }

        try {
            this.isSpawning = true;
            this.emit('spawnStarted', { itemId, positionId });

            console.log(`Spawning item ${itemId} to position ${positionId}...`);
            console.log('Calling GameMasterApi.spawnItem with:', {
                itemId,
                request: { to_position_id: positionId }
            });

            const response = await GameMasterApi.spawnItem(itemId, {
                to_position_id: positionId
            });

            if (!response.data) {
                console.warn('Spawn item API response is empty');
                return null;
            }

            const result = response.data;
            console.log(`Spawned item ${itemId} to position ${positionId}`);
            this.emit('itemSpawnedToPosition', { itemId, positionId, result });
            return result;
        } catch (error) {
            console.error(`Failed to spawn item ${itemId} to position ${positionId}:`, error);
            this.emit('spawnFailed', { itemId, positionId, error });
            throw error;
        } finally {
            this.isSpawning = false;
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
        this.isSpawning = false;
        console.log('GameMasterItemSpawnerService reset');
        this.emit('reset');
    }
}

// Export singleton instance
export const gameMasterItemSpawnerService = new GameMasterItemSpawnerService();
