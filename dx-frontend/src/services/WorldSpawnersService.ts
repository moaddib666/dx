import {GMWorldGenericSpawnersApi, GMWorldNPCSpawnersApi} from '@/api/backendService';
import {AxiosResponse} from 'axios';
import type {
    GenericSpawner,
    NPCGenericSpawner,
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
    private npcSpawners: NPCGenericSpawner[];
    private isLoading: boolean;
    private lastLoaded: Date | null;
    private eventListeners: Map<WorldSpawnersServiceEventType, EventCallback[]>;

    constructor() {
        this.genericSpawners = [];
        this.npcSpawners = [];
        this.isLoading = false;
        this.lastLoaded = null;
        this.eventListeners = new Map();
    }

    /**
     * Initialize the service and load all spawners
     */
    async initialize(): Promise<{generic: GenericSpawner[], npc: NPCGenericSpawner[]}> {
        try {
            console.log('Initializing WorldSpawnersService...');
            await this.loadSpawners();
            return {
                generic: this.genericSpawners,
                npc: this.npcSpawners
            };
        } catch (error) {
            console.error('Failed to initialize WorldSpawnersService:', error);
            throw error;
        }
    }

    /**
     * Load all spawners from the backend
     */
    async loadSpawners(): Promise<{generic: GenericSpawner[], npc: NPCGenericSpawner[]}> {
        if (this.isLoading) {
            console.log('Spawners already loading, waiting for completion...');
            return {
                generic: this.genericSpawners,
                npc: this.npcSpawners
            };
        }

        try {
            this.isLoading = true;
            this.emit('loadingStarted');

            console.log('Loading spawners from server...');

            // Load generic spawners
            await this.loadGenericSpawners();

            // Load NPC spawners
            await this.loadNPCSpawners();

            this.lastLoaded = new Date();
            console.log(`Loaded ${this.genericSpawners.length} generic spawners and ${this.npcSpawners.length} NPC spawners`);

            this.emit('spawnersLoaded', {
                generic: this.genericSpawners,
                npc: this.npcSpawners
            });

            return {
                generic: this.genericSpawners,
                npc: this.npcSpawners
            };
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
     * Load NPC spawners from the backend
     */
    private async loadNPCSpawners(): Promise<void> {
        try {
            console.log('Loading NPC spawners...');
            const response = await GMWorldNPCSpawnersApi.gamemasterSpawnersNpcList();

            if (!response.data) {
                console.warn('NPC Spawners API response is empty');
                this.npcSpawners = [];
                return;
            }

            // Handle response format (array or object with results)
            let spawners: NPCGenericSpawner[] = [];
            if (Array.isArray(response.data)) {
                spawners = response.data;
            } else if (response.data.results) {
                spawners = response.data.results;
            } else {
                console.warn('NPC Spawners API response has unexpected format:', response.data);
                this.npcSpawners = [];
                return;
            }

            this.npcSpawners = spawners;
            console.log(`Loaded ${this.npcSpawners.length} NPC spawners`);

            // Log sample spawner for debugging
            if (this.npcSpawners.length > 0) {
                console.log('Sample NPC spawner:', this.npcSpawners[0]);
            }
        } catch (error) {
            console.error('Failed to load NPC spawners:', error);
            this.npcSpawners = [];
            throw error;
        }
    }

    /**
     * Get all generic spawners
     */
    getGenericSpawners(): GenericSpawner[] {
        return this.genericSpawners;
    }

    /**
     * Get all NPC spawners
     */
    getNPCSpawners(): NPCGenericSpawner[] {
        return this.npcSpawners;
    }

    /**
     * Get all spawners (both generic and NPC)
     */
    getAllSpawners(): (GenericSpawner | NPCGenericSpawner)[] {
        return [...this.genericSpawners, ...this.npcSpawners];
    }

    /**
     * Get spawner by ID (searches both generic and NPC spawners)
     */
    getSpawnerById(id: string): GenericSpawner | NPCGenericSpawner | undefined {
        // First check NPC spawners
        const npcSpawner = this.npcSpawners.find(spawner => spawner.id === id);
        if (npcSpawner) {
            return npcSpawner;
        }

        // Then check generic spawners
        return this.genericSpawners.find(spawner => spawner.id === id);
    }

    /**
     * Get NPC spawner by ID with character template details
     */
    getNPCSpawnerById(id: string): NPCGenericSpawner | undefined {
        return this.npcSpawners.find(spawner => spawner.id === id);
    }

    /**
     * Get spawners by position ID
     */
    getSpawnersByPosition(positionId: string): (GenericSpawner | NPCGenericSpawner)[] {
        const genericByPosition = this.genericSpawners.filter(spawner => spawner.position === positionId);
        const npcByPosition = this.npcSpawners.filter(spawner => spawner.position === positionId);
        return [...genericByPosition, ...npcByPosition];
    }

    /**
     * Get spawners by campaign ID
     */
    getSpawnersByCampaign(campaignId: string): (GenericSpawner | NPCGenericSpawner)[] {
        const genericByCampaign = this.genericSpawners.filter(spawner => spawner.campaign === campaignId);
        const npcByCampaign = this.npcSpawners.filter(spawner => spawner.campaign === campaignId);
        return [...genericByCampaign, ...npcByCampaign];
    }

    /**
     * Get active spawners only
     */
    getActiveSpawners(): (GenericSpawner | NPCGenericSpawner)[] {
        const activeGeneric = this.genericSpawners.filter(spawner => spawner.is_active);
        const activeNPC = this.npcSpawners.filter(spawner => spawner.is_active);
        return [...activeGeneric, ...activeNPC];
    }

    /**
     * Create a new NPC spawner
     */
    async createNPCSpawner(spawnerData: {
        position: string;
        character_template: string;
        campaign: string;
        dimension?: number;
        is_active?: boolean;
        spawn_limit?: number;
        respawn_cycles?: number;
    }): Promise<NPCGenericSpawner> {
        try {
            console.log('Creating NPC spawner:', spawnerData);

            const request: NPCGenericSpawnerRequest = {
                position: spawnerData.position,
                character_template: spawnerData.character_template,
                campaign: spawnerData.campaign,
                dimension: spawnerData.dimension,
                is_active: spawnerData.is_active ?? true,
                spawn_limit: spawnerData.spawn_limit ?? 1,
                respawn_cycles: spawnerData.respawn_cycles ?? 1
            };

            const response: AxiosResponse = await GMWorldNPCSpawnersApi.gamemasterSpawnersNpcCreate(request);

            const newSpawner = response.data as NPCGenericSpawner;

            // Add to cache
            this.npcSpawners.push(newSpawner);

            console.log('NPC spawner created successfully:', newSpawner);
            this.emit('spawnerCreated', newSpawner);
            return newSpawner;
        } catch (error) {
            console.error('Failed to create NPC spawner:', error);
            this.emit('spawnerCreationFailed', error);
            throw error;
        }
    }

    /**
     * Update an existing NPC spawner
     */
    async updateNPCSpawner(spawnerId: string, spawnerData: PatchedNPCGenericSpawnerRequest): Promise<NPCGenericSpawner> {
        try {
            console.log(`Updating NPC spawner ${spawnerId}:`, spawnerData);

            const response: AxiosResponse = await GMWorldNPCSpawnersApi.gamemasterSpawnersNpcPartialUpdate(
                spawnerId,
                spawnerData
            );

            const updatedSpawner = response.data as NPCGenericSpawner;

            // Update in cache
            const index = this.npcSpawners.findIndex(spawner => spawner.id === spawnerId);
            if (index !== -1) {
                this.npcSpawners[index] = updatedSpawner;
            }

            console.log('NPC spawner updated successfully:', updatedSpawner);
            this.emit('spawnerUpdated', updatedSpawner);
            return updatedSpawner;
        } catch (error) {
            console.error('Failed to update NPC spawner:', error);
            this.emit('spawnerUpdateFailed', error);
            throw error;
        }
    }

    /**
     * Refresh spawners from the server
     */
    async refresh(): Promise<{generic: GenericSpawner[], npc: NPCGenericSpawner[]}> {
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
        this.npcSpawners = [];
        this.isLoading = false;
        this.lastLoaded = null;
        console.log('WorldSpawnersService reset');
        this.emit('reset');
    }
}

// Export singleton instance
export const worldSpawnersService = new WorldSpawnersService();
export default worldSpawnersService;