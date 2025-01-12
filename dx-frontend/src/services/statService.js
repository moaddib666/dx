import {CoreGameApi} from "@/api/backendService.js";

class StatsService {
    /**
     * Create an instance of StatsService.
     * @param {CoreApi} api - The data representing the player.
     */
    constructor(api) {
        this.api = api;
        this.mapping = {};
    }

    /**
     * Fill the mapping with the attributes from the API.
     *
     */
    async refreshStats() {
        const attributes = (await this.api.coreStatsList()).data;
        attributes.forEach(attr => this.mapping[attr.id] = attr);
    }

    /**
     * Get the value of a specific attribute by name.
     * @param {string} attributeName - The name of the attribute to retrieve.
     * @returns {Object|null} The attribute object, or null if not found.
     */
    async getStat(attributeName) {
        // Check if the mapping is empty
        if (Object.keys(this.mapping).length === 0) {
            await this.refreshStats();
        }
        return this.mapping[attributeName] || null;
    }

    /**
     * Get the icon of a specific attribute by name.
     * @param {string} attributeName - The name of the attribute to retrieve.
     * @returns {Object|null} The attribute object, or null if not found.
     */
    async getStatImage(attributeName) {
        const attribute = await this.getStat(attributeName);
        return attribute ? attribute.icon : null;
    }

    /**
     * List all the stats.
     * @returns {StatObject[]} The list of stats.
     */
    async listStats() {
        if (Object.keys(this.mapping).length === 0) {
            await this.refreshStats();
        }
        return Object.values(this.mapping);
    }

    getCachedStatImage(attributeName) {
        return this.mapping[attributeName] ? this.mapping[attributeName].icon : null;
    }

    /**
     * List all the cached stats.
     * @returns {StatObject[]} The list of stats.
     */
    listCachedStats() {
        return Object.values(this.mapping);
    }
}

const StatsGameService = new StatsService(CoreGameApi);
export default StatsGameService