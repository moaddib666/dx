import {GameMasterApi} from '@/api/backendService.js';
import {GameMasterItem} from "@/api/dx-backend";
import {AxiosResponse} from 'axios';

/**
 * Event types for the ItemsService
 */
type ItemsServiceEventType = 'loadingStarted' | 'itemsLoaded' | 'loadingFailed' | 'refreshed' | 'refreshFailed' | 'reset';

/**
 * Event callback function type
 */
type EventCallback = (data?: any) => void;

/**
 * Items Service
 * Handles fetching, caching, and managing items for the WorldEditor
 */
export class ItemsService {
    private items: GameMasterItem[];
    private isLoading: boolean;
    private lastLoaded: Date | null;
    private eventListeners: Map<ItemsServiceEventType, EventCallback[]>;

    constructor() {
        this.items = [];
        this.isLoading = false;
        this.lastLoaded = null;
        this.eventListeners = new Map();
    }

    /**
     * Initialize the service and load items
     */
    async initialize(): Promise<GameMasterItem[]> {
        try {
            console.log('Initializing ItemsService...');
            await this.loadItems();
            return this.items;
        } catch (error) {
            console.error('Failed to initialize ItemsService:', error);
            throw error;
        }
    }

    /**
     * Load items from the backend
     */
    async loadItems(): Promise<GameMasterItem[]> {
        if (this.isLoading) {
            console.log('Items already loading, waiting for completion...');
            return this.items;
        }

        try {
            this.isLoading = true;
            this.emit('loadingStarted');

            console.log('Loading items from server...');
            const response: AxiosResponse = await GameMasterApi.gamemasterItemsList();

            if (!response.data) {
                console.warn('Items API response is empty');
                this.items = [];
                return this.items;
            }

            // Handle response format (array or object with results)
            let items: GameMasterItem[] = [];
            if (Array.isArray(response.data)) {
                items = response.data;
            } else if (response.data.results) {
                items = response.data.results;
            } else {
                console.warn('Items API response has unexpected format:', response.data);
                this.items = [];
                return this.items;
            }

            this.items = items;
            this.lastLoaded = new Date();
            console.log(`Loaded ${this.items.length} items`);

            // Log sample items for debugging
            if (this.items.length > 0) {
                console.log('Sample item:', this.items[0]);
            }

            this.emit('itemsLoaded', this.items);
            return this.items;
        } catch (error) {
            console.error('Failed to load items:', error);
            this.emit('loadingFailed', error);
            throw error;
        } finally {
            this.isLoading = false;
        }
    }

    /**
     * Get all items
     */
    getItems(): GameMasterItem[] {
        return this.items;
    }

    /**
     * Get item by ID
     */
    getItemById(id: string): GameMasterItem | undefined {
        return this.items.find(item => item.id === id);
    }

    /**
     * Get items by type
     */
    getItemsByType(type: string): GameMasterItem[] {
        return this.items.filter(item => item.type === type);
    }

    /**
     * Search items by name
     */
    searchItems(query: string): GameMasterItem[] {
        if (!query) return this.items;

        const lowerQuery = query.toLowerCase();
        return this.items.filter(item =>
            item.name.toLowerCase().includes(lowerQuery) ||
            (item.description && item.description.toLowerCase().includes(lowerQuery))
        );
    }

    /**
     * Refresh items from the server
     */
    async refresh(): Promise<GameMasterItem[]> {
        try {
            console.log('Refreshing items...');
            await this.loadItems();
            this.emit('refreshed', this.items);
            return this.items;
        } catch (error) {
            console.error('Failed to refresh items:', error);
            this.emit('refreshFailed', error);
            throw error;
        }
    }

    /**
     * Event system for components to listen to changes
     */
    on(event: ItemsServiceEventType, callback: EventCallback): void {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event)?.push(callback);
    }

    /**
     * Remove event listener
     */
    off(event: ItemsServiceEventType, callback: EventCallback): void {
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
    private emit(event: ItemsServiceEventType, data?: any): void {
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
        this.items = [];
        this.isLoading = false;
        this.lastLoaded = null;
        console.log('ItemsService reset');
        this.emit('reset');
    }
}

// Export singleton instance
export const itemsService = new ItemsService();