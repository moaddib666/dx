import {GameMasterApi} from '@/api/backendService.js';
import {EventEmitter} from 'events';

// Enums for God Intervention
export const GodInterventionType = {
    BLESSING: 'Blessing',
    CURSE: 'Curse'
};

export const GodInterventionSize = {
    SMALL: 'Small',
    MEDIUM: 'Medium',
    LARGE: 'Large',
    GOD: 'God'
};

export const GodInterventionAttribute = {
    HEALTH: 'Health',
    ENERGY: 'Energy',
    ACTION_POINTS: 'Action Points'
};

class GameMasterInterventionalService extends EventEmitter {
    constructor() {
        super();
        this.isLoading = false;
    }

    /**
     * Apply an instant kill intervention to a character
     * @param {string} characterId - The ID of the character to kill
     * @returns {Promise<any>} - The response from the API
     */
    async instantKill(characterId) {
        try {
            this.isLoading = true;
            this.emit('loadingStarted', characterId);

            const godInterventionRequest = {
                type: GodInterventionType.CURSE,
                size: GodInterventionSize.GOD,
                attributes: [GodInterventionAttribute.HEALTH]
            };

            const response = await GameMasterApi.gamemasterCharactersGodInterventionCreate(
                characterId,
                godInterventionRequest
            );

            this.emit('interventionSuccess', {characterId, type: 'kill', response});
            return response;
        } catch (error) {
            console.error('Error applying instant kill intervention:', error);
            this.emit('interventionFailed', {characterId, type: 'kill', error});
            throw error;
        } finally {
            this.isLoading = false;
            this.emit('loadingFinished', characterId);
        }
    }

    /**
     * Apply an instant heal intervention to a character
     * @param {string} characterId - The ID of the character to heal
     * @returns {Promise<any>} - The response from the API
     */
    async instantHeal(characterId) {
        try {
            this.isLoading = true;
            this.emit('loadingStarted', characterId);

            const godInterventionRequest = {
                type: GodInterventionType.BLESSING,
                size: GodInterventionSize.GOD,
                attributes: [GodInterventionAttribute.HEALTH]
            };

            const response = await GameMasterApi.gamemasterCharactersGodInterventionCreate(
                characterId,
                godInterventionRequest
            );

            this.emit('interventionSuccess', {characterId, type: 'heal', response});
            return response;
        } catch (error) {
            console.error('Error applying instant heal intervention:', error);
            this.emit('interventionFailed', {characterId, type: 'heal', error});
            throw error;
        } finally {
            this.isLoading = false;
            this.emit('loadingFinished', characterId);
        }
    }

    /**
     * Apply a custom intervention to a character
     * @param {string} characterId - The ID of the character
     * @param {object} interventionDetails - The details of the intervention
     * @param {string} interventionDetails.type - The type of intervention (Blessing or Curse)
     * @param {string} interventionDetails.size - The size of intervention (Small, Medium, Large, God)
     * @param {Array<string>} interventionDetails.attributes - The attributes to affect
     * @returns {Promise<any>} - The response from the API
     */
    async customIntervention(characterId, interventionDetails) {
        try {
            this.isLoading = true;
            this.emit('loadingStarted', characterId);

            const godInterventionRequest = {
                type: interventionDetails.type,
                size: interventionDetails.size,
                attributes: interventionDetails.attributes
            };

            const response = await GameMasterApi.gamemasterCharactersGodInterventionCreate(
                characterId,
                godInterventionRequest
            );

            this.emit('interventionSuccess', {characterId, type: 'custom', response});
            return response;
        } catch (error) {
            console.error('Error applying custom intervention:', error);
            this.emit('interventionFailed', {characterId, type: 'custom', error});
            throw error;
        } finally {
            this.isLoading = false;
            this.emit('loadingFinished', characterId);
        }
    }
}

// Create and export a singleton instance
export const gameMasterInterventionalService = new GameMasterInterventionalService();