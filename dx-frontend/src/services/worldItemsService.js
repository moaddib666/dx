import {ItemsGameApi} from "@/api/backendService.js";

class WorldItemsService {
    /**
     * Create an instance of WorldItemsService.
     * @param {ItemsApi} api - The API client instance for world items.
     */
    constructor(api) {
        this.api = api;
        this.mapping = {}; // Cache for world items
    }

    /**
     * Get WorldItem by id.
     * @param {string} id - The id of the item to retrieve.
     * @returns {CharacterItem|None} The item object, or null if not found.
     */
    async getWorldItem(id) {
        // Check if the id in the cache if not fetch it
        if (!this.mapping[id]) {
            this.mapping[id] = (await this.api.itemsWorldRetrieve(id)).data;
        }
        return this.mapping[id] || null;
    }

    /**
     * GetCachedWorldItem by id.
     * @param {string} id - The id of the item to retrieve.
     * @returns {CharacterItem|None} The item object, or null if not found.
     */
    getCachedWorldItem(id) {
        return this.mapping[id] || null;
    }
}

const WorldItemsGameMasterService = new WorldItemsService(ItemsGameApi);
export default WorldItemsGameMasterService;
