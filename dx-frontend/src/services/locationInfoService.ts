import {WorldGameApi} from "@/api/backendService.js";
import {CacheService} from "@/services/cacheService.js";
import {WorldPosition, TeleportPositionRequest, TeleportCoordinatesRequest} from "@/api/dx-backend";
import {AxiosResponse} from "axios";

class LocationInfoService {
    private cache: CacheService;

    /**
     * Creates a new instance of the LocationInfoService.
     * @param cacheService - The cache service to use for storing data.
     */
    constructor(cacheService: CacheService) {
        this.cache = cacheService;
    }

    /**
     * Fetches the infography for a Location by ID.
     * @param id - The ID of the location
     * @returns Promise resolving to the location information
     */
    async getLocationInfo(id: string): Promise<WorldPosition> {
        let info = await this.cache.acquire(id);
        console.debug(`Got info for ${id} from cache: ${info}`);
        if (!info) {
            info = (await WorldGameApi.worldPositionInfoRetrieve(id)).data;
            await this.cache.set(id, info);
        }
        await this.cache.release(id);
        return info;
    }

    /**
     * Resolve Background url
     * @param id - The ID of the location
     * @returns Promise resolving to the background URL
     */
    async getBackgroundUrl(id: string): Promise<string | null> {
        let info = await this.getLocationInfo(id);
        console.debug(`Got info for ${id}: ${info}`);
        const image = info.image;
        console.debug(`Got background for ${id} from info: ${image}`);
        return image;
    }

    /**
     * Teleport a character to a position
     * @param characterId - The ID of the character to teleport
     * @param positionId - The ID of the position to teleport to
     * @returns Promise resolving when teleport is complete
     */
    async teleportToPosition(characterId: string, positionId: string): Promise<void> {
        const teleportRequest: TeleportPositionRequest = {id: positionId};
        await WorldGameApi.worldPositionTeleportToPositionCreate(characterId, teleportRequest);
    }

    /**
     * Teleport a character to coordinates
     * @param characterId - The ID of the character to teleport
     * @param x - The x coordinate
     * @param y - The y coordinate
     * @param z - The z coordinate
     * @returns Promise resolving when teleport is complete
     */
    async teleportToCoordinates(characterId: string, x: number, y: number, z: number): Promise<void> {
        const teleportRequest: TeleportCoordinatesRequest = {
            grid_x: x,
            grid_y: y,
            grid_z: z,
        };
        await WorldGameApi.worldPositionTeleportToCoordinatesCreate(characterId, teleportRequest);
    }
}

const LocationInfoGameService = new LocationInfoService(
    new CacheService("LocationInfo"),
);

export {LocationInfoGameService};