import {ClientGameApi, CharacterGameApi} from "@/api/backendService.js";

class ClientManagerService {
    /**
     * Create an instance of ClientManagerService.
     * @param {import('@/api/dx-backend').ClientApi} clientApi - The API client instance for client management.
     * @param {import('@/api/dx-backend').CharacterApi} characterApi - The API client instance for character management.
     */
    constructor(clientApi, characterApi) {
        this.clientApi = clientApi;
        this.characterApi = characterApi;
        this.clientInfo = null; // Cache for client info
    }

    /**
     * Get current client information.
     * @returns {import('@/api/dx-backend').CurrentClientInfo} The client information object.
     */
    async getCurrentClientInfo() {
        // If we don't have the client info cached, fetch it
        if (!this.clientInfo) {
            try {
                const response = await this.clientApi.clientCurrentInfoRetrieve();
                this.clientInfo = response.data;
            } catch (error) {
                console.error("Error fetching client info:", error);
                throw error;
            }
        }
        return this.clientInfo;
    }

    /**
     * Clear the cached client information.
     */
    clearClientInfoCache() {
        this.clientInfo = null;
    }

    /**
     * Use a character by selecting it.
     * @param {string} id - The id of the character to select.
     * @returns {import('@/api/dx-backend').OpenaiCharacter} The selected character.
     */
    async useCharacter(id) {
        try {
            // The API requires an empty request object as the second parameter
            const emptyRequest = {};
            const response = await this.characterApi.characterOwnedSelectCharacterCreate(id, emptyRequest);
            // Clear the client info cache as it might have changed
            this.clearClientInfoCache();
            return response.data;
        } catch (error) {
            console.error(`Error selecting character with id ${id}:`, error);
            throw error;
        }
    }

    /**
     * Set the current campaign for the client.
     * @param {string} campaignId - The id of the campaign to set as current.
     * @returns {Promise<any>} The response data from the API.
     */
    async setCurrentCampaign(campaignId) {
        try {
            const response = await this.clientApi.clientCampaignsSetCurrentCampaignCreate(campaignId);
            // Clear the client info cache as it might have changed
            this.clearClientInfoCache();
            console.log('Campaign successfully set on backend:', campaignId);
            return response.data;
        } catch (error) {
            console.error(`Error setting current campaign with id ${campaignId}:`, error);
            throw error;
        }
    }
}

// Create a singleton instance with the API instances
const ClientManagerServiceInstance = new ClientManagerService(ClientGameApi, CharacterGameApi);
export default ClientManagerServiceInstance;