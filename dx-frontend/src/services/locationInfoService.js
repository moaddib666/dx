import {WorldGameApi} from "@/api/backendService.js";
import {CacheService} from "@/services/cacheService.js";


class LocationInfoService {
    /**
     * Creates a new instance of the LocationInfoService.
     * @param {Object} cacheService - The cache service to use for storing data.
     */
    constructor(cacheService) {
        this.cache = cacheService;
    }

    /**
     * Fetches the infography for a Location by ID.
     * @param id
     * @returns {Promise<Position>}
     */
    async getLocationInfo(id) {
        let info = await this.cache.acquire(id);
        console.debug(`Got info for ${id} from cache: ${info}`);
        if (!info) {
            info = (await WorldGameApi.worldPositionInfoRetrieve(id)).data;
            await this.cache.set(id, info);
        }
        await this.cache.release(id);
        return info;
    }

    /** Resolve Background url
     * @param {string} id
     * @returns {Promise<string>}
     */
    async getBackgroundUrl(id) {
        let info = await this.getLocationInfo(id);
        console.debug(`Got info for ${id}: ${info}`);
        const image = info.image;
        console.debug(`Got background for ${id} from info: ${image}`);
        return image;
    }

    /** teleportToPosition
     * @param {string} characterId
     * @param {string} positionId
     * @returns {Promise<void>}
     */
    async teleportToPosition(characterId, positionId) {
        await WorldGameApi.worldPositionTeleportToPositionCreate(characterId, {id: positionId});
    }

    /** teleportToCoordinates
     * @param {string} characterId
     * @param {number} x
     * @param {number} y
     * @param {number} z
     * @returns {Promise<void>}
     */
    async teleportToCoordinates(characterId, x, y, z) {
        await WorldGameApi.worldPositionTeleportToCoordinatesCreate(characterId, {
            grid_x: x,
            grid_y: y,
            grid_z: z,
        });
    }


}

const LocationInfoGameService = new LocationInfoService(
    new CacheService("LocationInfo"),
);

export {LocationInfoGameService};
