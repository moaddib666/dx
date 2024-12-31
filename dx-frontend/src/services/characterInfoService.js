// import {CharacterGameApi} from "@/api/backendService.js";

import {CharacterGameApi} from "@/api/backendService.js";
import {CacheService} from "@/services/cacheService.js";


class CharacterInfoService {
    /**
     * Creates a new instance of the CharacterInfoService.
     * @param {Object} cacheService - The cache service to use for storing data.
     */
    constructor(cacheService) {
        this.cache = cacheService;
    }

    /**
     * Fetches the infography for a character by ID.
     * @param id
     * @param {Boolean} gmMode - Whether to fetch the GM infography or the player infography.
     * @returns {Promise<OpenaiCharacter>}
     */
    async getCharacterInfo(id, gmMode) {
        let info = await this.cache.acquire(id);
        console.debug(`Got info for ${id} from cache: ${info}`);
        if (!info) {
            if (gmMode) {
                info = await this.getCharacterInfoGm(id);
            } else {
                info = await this.getCharacterInfoPlayer(id);
            }
            await this.cache.set(id, info);
        }
        await this.cache.release(id);
        return info;
    }

    /**
     * Fetches the infography for a character by ID as a GM.
     * @param id
     * @returns {Promise<OpenaiCharacter>}
     */
    async getCharacterInfoGm(id) {
        return (await CharacterGameApi.characterGmRetrieve(id)).data;
    }

    /**
     * Fetches the infography for a character by ID as a player.
     * @param id
     * @returns {Promise<OpenaiCharacter>}
     */
    async getCharacterInfoPlayer(id) {
        return (await CharacterGameApi.characterPlayerRetrieve(id)).data;
    }

    /** Resolve Avatar url
     * @param {string} id
     * @param {boolean} gmMode
     * @returns {Promise<string>}
     */
    async getAvatarUrl(id, gmMode) {
        let info = await this.getCharacterInfo(id, gmMode);
        const avatar = info.biography.avatar;
        console.debug(`Got avatar for ${id} from info: ${avatar}`);
        return avatar;
    }


}

const CharacterInfoGameService = new CharacterInfoService(
    new CacheService("characterInfo"),
);

export {CharacterInfoGameService};
