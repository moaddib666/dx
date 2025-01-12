import {CoreGameApi} from "@/api/backendService.js";

class ViolationsService {
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
    async refreshViolations() {
        const attributes = (await this.api.coreViolationsList()).data;
        attributes.forEach(attr => this.mapping[attr.id] = attr);
    }

    /**
     * Get the value of a specific attribute by name.
     * @param {string} attributeName - The name of the attribute to retrieve.
     * @returns {Object|null} The attribute object, or null if not found.
     */
    async getViolation(attributeName) {
        // Check if the mapping is empty
        if (Object.keys(this.mapping).length === 0) {
            await this.refreshViolations();
        }
        return this.mapping[attributeName] || null;
    }

    /**
     * Get the icon of a specific attribute by name.
     * @param {string} attributeName - The name of the attribute to retrieve.
     * @returns {Object|null} The attribute object, or null if not found.
     */
    async getViolationImage(attributeName) {
        const attribute = await this.getViolation(attributeName);
        return attribute ? attribute.icon : null;
    }

    /**
     * List all the stats.
     * @returns {ViolationObject[]} The list of stats.
     */
    async listViolation() {
        if (Object.keys(this.mapping).length === 0) {
            await this.refreshViolations();
        }
        return Object.values(this.mapping);
    }

    /**
     * Get the cached violation image
     * @param attributeName
     * @returns {*|null}
     */
    getCachedViolationImage(attributeName) {
        return this.mapping[attributeName] ? this.mapping[attributeName].icon : null;
    }

    /**
     * List all the cached violations
     * @returns {ViolationObject[]}
     */
    listCachedViolations() {
        return Object.values(this.mapping);
    }
}

const ViolationsGameService = new ViolationsService(CoreGameApi);
export default ViolationsGameService