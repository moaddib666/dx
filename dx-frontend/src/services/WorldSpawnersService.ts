import {GMWorldGenericSpawnersApi, GMWorldNPCSpawnersApi} from '@/api/backendService';
import {AxiosResponse} from 'axios';
import type {
    GenericSpawner,
    NPCGenericSpawnerRequest,
    PatchedNPCGenericSpawnerRequest,
    GameObjectType,
    OneOf,
    NPCSpawnerMinimalPreview
} from '@/api/dx-backend';

/**
 * Event types for the WorldSpawnersService
 */
type WorldSpawnersServiceEventType =
  | 'loadingStarted'
  | 'spawnersLoaded'
  | 'loadingFailed'
  | 'refreshed'
  | 'refreshFailed'
  | 'reset'
  | 'spawnerCreated'
  | 'spawnerCreationFailed'
  | 'spawnerUpdated'
  | 'spawnerUpdateFailed';

/**
 * Event callback function type
 */
type EventCallback = (data?: any) => void;


/**
 * World Spawners Service
 * Handles fetching, caching, and managing spawners for the WorldEditor
 */
export class WorldSpawnersService {
    private genericSpawners: GenericSpawner[];
    private isLoading: boolean;
    private lastLoaded: Date | null;
    private eventListeners: Map<WorldSpawnersServiceEventType, EventCallback[]>;

    constructor() {
        this.genericSpawners = [];
        this.isLoading = false;
        this.lastLoaded = null;
        this.eventListeners = new Map();
    }

    /**
     * Initialize the service and load all spawners
     */
    async initialize(): Promise<GenericSpawner[]> {
        try {
            console.log('Initializing WorldSpawnersService...');
            await this.loadSpawners();
            return this.genericSpawners;
        } catch (error) {
            console.error('Failed to initialize WorldSpawnersService:', error);
            throw error;
        }
    }

    /**
     * Load all spawners from the backend
     */
    async loadSpawners(): Promise<GenericSpawner[]> {
        if (this.isLoading) {
            console.log('Spawners already loading, waiting for completion...');
            return this.genericSpawners;
        }

        try {
            this.isLoading = true;
            this.emit('loadingStarted');

            console.log('Loading spawners from server...');

            // Load generic spawners (includes NPC spawners)
            await this.loadGenericSpawners();

            this.lastLoaded = new Date();
            console.log(`Loaded ${this.genericSpawners.length} generic spawners`);

            this.emit('spawnersLoaded', this.genericSpawners);

            return this.genericSpawners;
        } catch (error) {
            console.error('Failed to load spawners:', error);
            this.emit('loadingFailed', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Load generic spawners from the backend
     */
    private async loadGenericSpawners(): Promise<void> {
        try {
            console.log('Loading generic spawners...');
            const response = await GMWorldGenericSpawnersApi.gamemasterSpawnersAllList();

            if (!response.data) {
                console.warn('Generic Spawners API response is empty');
                this.genericSpawners = [];
                return;
            }

            // Handle response format (array or object with results)
            let spawners: GenericSpawner[] = [];
            if (Array.isArray(response.data)) {
                spawners = response.data;
            } else if (response.data.results) {
                spawners = response.data.results;
            } else {
                console.warn('Generic Spawners API response has unexpected format:', response.data);
                this.genericSpawners = [];
                return;
            }

            this.genericSpawners = spawners;
            console.log(`Loaded ${this.genericSpawners.length} generic spawners`);

            // Log sample spawner for debugging
            if (this.genericSpawners.length > 0) {
                console.log('Sample generic spawner:', this.genericSpawners[0]);
            }
        } catch (error) {
            console.error('Failed to load generic spawners:', error);
            this.genericSpawners = [];
            throw error;
        }
    }


    /**
     * Get all spawners
     */
    getAllSpawners(): GenericSpawner[] {
        return this.genericSpawners;
    }

    /**
     * Get spawner by ID
     */
    getSpawnerById(id: string): GenericSpawner | undefined {
        return this.genericSpawners.find(spawner => spawner.id === id);
    }

    /**
     * Get spawners by position ID
     */
    getSpawnersByPosition(positionId: string): GenericSpawner[] {
        return this.genericSpawners.filter(spawner => spawner.position === positionId);
    }


    /**
     * Get active spawners only
     */
    getActiveSpawners(): GenericSpawner[] {
        return this.genericSpawners.filter(spawner => spawner.is_active);
    }

    /**
     * Create a new NPC spawner
     */
    async createNPCSpawner(spawnerData: {
        position: string;
        character_template: string;
        dimension?: number;
        is_active?: boolean;
        spawn_limit?: number;
        respawn_cycles?: number;
    }): Promise<GenericSpawner> {
        try {
            console.log('Creating NPC spawner:', spawnerData);

            const request: NPCGenericSpawnerRequest = {
                position: spawnerData.position,
                character_template: spawnerData.character_template,
                dimension: spawnerData.dimension,
                is_active: spawnerData.is_active ?? true,
                spawn_limit: spawnerData.spawn_limit ?? 1,
                respawn_cycles: spawnerData.respawn_cycles ?? 1
            };

            const response: AxiosResponse = await GMWorldNPCSpawnersApi.gamemasterSpawnersNpcCreate(request);
            const createdSpawner = response.data;

            console.log('NPC spawner created successfully:', createdSpawner);

            // Now fetch the generic spawner representation by ID
            const genericSpawnerResponse = await GMWorldGenericSpawnersApi.gamemasterSpawnersAllRetrieve(createdSpawner.id);
            const genericSpawner = genericSpawnerResponse.data as GenericSpawner;

            // Add to cache
            this.genericSpawners.push(genericSpawner);

            this.emit('spawnerCreated', genericSpawner);
            return genericSpawner;
        } catch (error) {
            console.error('Failed to create NPC spawner:', error);
            this.emit('spawnerCreationFailed', error);
            throw error;
        }
    }

    /**
     * Update an existing NPC spawner
     */
    async updateNPCSpawner(spawnerId: string, spawnerData: PatchedNPCGenericSpawnerRequest): Promise<GenericSpawner> {
        try {
            console.log(`Updating NPC spawner ${spawnerId}:`, spawnerData);

            const response: AxiosResponse = await GMWorldNPCSpawnersApi.gamemasterSpawnersNpcPartialUpdate(
                spawnerId,
                spawnerData
            );

            console.log('NPC spawner updated successfully');

            // Now fetch the generic spawner representation by ID
            const genericSpawnerResponse = await GMWorldGenericSpawnersApi.gamemasterSpawnersAllRetrieve(spawnerId);
            const genericSpawner = genericSpawnerResponse.data as GenericSpawner;

            // Update in cache
            const index = this.genericSpawners.findIndex(spawner => spawner.id === spawnerId);
            if (index !== -1) {
                this.genericSpawners[index] = genericSpawner;
            }

            this.emit('spawnerUpdated', genericSpawner);
            return genericSpawner;
        } catch (error) {
            console.error('Failed to update NPC spawner:', error);
            this.emit('spawnerUpdateFailed', error);
            throw error;
        }
    }

    /**
     * Refresh spawners from the server
     */
    async refresh(): Promise<GenericSpawner[]> {
        try {
            console.log('Refreshing spawners...');
            const result = await this.loadSpawners();
            this.emit('refreshed', result);
            return result;
        } catch (error) {
            console.error('Failed to refresh spawners:', error);
            this.emit('refreshFailed', error);
            throw error;
        }
    }

    /**
     * Event system for components to listen to changes
     */
    on(event: WorldSpawnersServiceEventType, callback: EventCallback): void {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event)?.push(callback);
    }

    /**
     * Remove event listener
     */
    off(event: WorldSpawnersServiceEventType, callback: EventCallback): void {
        if (this.eventListeners.has(event)) {
            const listeners = this.eventListeners.get(event);
            if (listeners) {
                const index = listeners.indexOf(callback);
                if (index > -1) {
                    listeners.splice(index, 1);
                }
            }
        }
    }

    /**
     * Emit event to listeners
     */
    private emit(event: WorldSpawnersServiceEventType, data?: any): void {
        if (this.eventListeners.has(event)) {
            this.eventListeners.get(event)?.forEach(callback => {
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
    reset(): void {
        this.genericSpawners = [];
        this.isLoading = false;
        this.lastLoaded = null;
        console.log('WorldSpawnersService reset');
        this.emit('reset');
    }
}

// Export singleton instance
export const worldSpawnersService = new WorldSpawnersService();
export default worldSpawnersService;