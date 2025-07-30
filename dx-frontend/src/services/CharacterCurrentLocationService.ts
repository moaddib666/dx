import {WorldGameApi} from "@/api/backendService.js";
import {ensureConnection} from "@/api/dx-websocket/index.ts";
import type {CharacterOnPosition, WorldPosition} from "@/api/dx-backend";

/**
 * Service for managing character location data
 * Provides methods to get current position information and character details
 */
export class characterCurrentLocationService {
    private position: WorldPosition | null = null;
    private characters: CharacterOnPosition[] = [];
    private npcCharacters: CharacterOnPosition[] = [];
    private bus: any;

    /**
     * Creates a new instance of the characterCurrentLocationService
     */
    constructor() {
        // Initialize the websocket connection
        this.bus = ensureConnection();

        // Listen for events related to character movements
        this.bus.on("world::character_arrived", this.handleCharacterArrived.bind(this));
        this.bus.on("world::character_left", this.handleCharacterLeft.bind(this));
        this.bus.on("world::new_cycle", this.refreshData.bind(this));
    }

    /**
     * Initializes the service by fetching the current position data
     * @returns Promise that resolves when the data is fetched
     */
    public async initialize(): Promise<void> {
        await this.refreshData();
    }

    /**
     * Refreshes all data by fetching the current position and character information
     * @returns Promise that resolves when the data is refreshed
     */
    public async refreshData(): Promise<void> {
        await this.getCurrentPositionInfo();
    }

    /**
     * Gets the current position information
     * @returns Promise that resolves to the current position
     */
    private async getCurrentPositionInfo(): Promise<WorldPosition | null> {
        try {
            this.position = (await WorldGameApi.worldPositionCurrentRetrieve()).data;

            // Reset character arrays
            this.characters = [];
            this.npcCharacters = [];

            // Process characters on position
            if (this.position && this.position.characters_on_position) {
                for (const char of this.position.characters_on_position) {
                    if (char.npc) {
                        this.npcCharacters.push(char);
                    } else {
                        this.characters.push(char);
                    }
                }
            }

            return this.position;
        } catch (error) {
            console.error("Error getting current position info:", error);
            this.position = null;
            this.characters = [];
            this.npcCharacters = [];
            return null;
        }
    }

    /**
     * Handles the character arrived event
     * @param data The event data
     */
    private async handleCharacterArrived(data: CharacterOnPosition): Promise<void> {
        console.debug("Character arrived event received:", data);
        if (!this.position) {
            console.warn("Position is not set, cannot handle character arrival.");
            return;
        }
        if (data.npc) {
            // If the character is an NPC, add it to the NPC characters list
            this.npcCharacters.push(data);
        } else {
            // If the character is a player, add it to the player characters list
            this.characters.push(data);
        }
    }

    /**
     * Handles the character left event
     * @param data The event data
     */
    private async handleCharacterLeft(data: CharacterOnPosition): Promise<void> {
        console.debug("Character left event received:", data);
        if (!this.position) {
            console.warn("Position is not set, cannot handle character departure.");
            return;
        }
        // Remove the character from the appropriate list
        if (data.npc) {
            this.npcCharacters = this.npcCharacters.filter(char => char.id !== data.id);
        } else {
            this.characters = this.characters.filter(char => char.id !== data.id);
        }
    }

    /**
     * Gets the current position
     * @returns The current position
     */
    public getPosition(): WorldPosition | null {
        return this.position;
    }

    /**
     * Gets all characters at the current position
     * @returns Array of characters
     */
    public getAllCharacters(): CharacterOnPosition[] {
        return [...this.characters, ...this.npcCharacters];
    }

    /**
     * Gets player characters at the current position
     * @returns Array of player characters
     */
    public getPlayerCharacters(): CharacterOnPosition[] {
        return this.characters;
    }

    /**
     * Gets NPC characters at the current position
     * @returns Array of NPC characters
     */
    public getNpcCharacters(): CharacterOnPosition[] {
        return this.npcCharacters;
    }

}

// Create a singleton instance of the service
const CharacterCurrentLocationService = new characterCurrentLocationService();

// Export the singleton instance
export default CharacterCurrentLocationService;