// src/services/bargainService.js
import {BargainGameApi} from '@/api/backendService';

/**
 * BargainService wraps the auto-generated API client to provide methods
 * for interacting with the bargain and gift endpoints.
 */
class BargainService {
    /**
     * Create an instance of BargainService.
     * @param {BargainApi} api The API client generated from the backend service.
     */
    constructor(api = BargainGameApi) {
        this.api = api;
    }

    /**
     * Retrieve a list of all open bargains.
     *
     * Endpoint: GET /bargain/open_bargains/
     *
     * @returns {Promise<Array>} A promise that resolves to an array of bargain objects.
     */
    async getOpenBargains() {
        return (await this.api.bargainOpenBargainsList()).data;
    }

    /**
     * Retrieve the items for a specific bargain.
     *
     * Endpoint: GET /bargain/open_bargains/{bargain_pk}/items/
     *
     * @param {string} bargainPk - The primary key of the bargain.
     * @returns {Promise<Object>} A promise that resolves to the bargain details (including items).
     */
    async getBargainItems(bargainPk) {
        return (await this.api.bargainOpenBargainsRetrieve(bargainPk)).data;
    }

    /**
     * Add an item to a bargain.
     *
     * Endpoint: POST /bargain/open_bargains/{bargain_pk}/items/
     *
     * @param {string} bargainPk - The primary key of the bargain.
     * @param {string} itemId - The ID of the item to add.
     * @returns {Promise<Object>} A promise that resolves to the created bargain item.
     */
    async addItemToBargain(bargainPk, itemId) {
        return (await this.api.bargainOpenBargainsItemsCreate(bargainPk, {item: itemId})).data;
    }

    /**
     * Remove an item from a bargain.
     *
     * Endpoint: DELETE /bargain/open_bargains/{bargain_pk}/items/{id}/
     *
     * @param {string} bargainPk - The primary key of the bargain.
     * @param {string} id - The ID of the item to remove.
     * @returns {Promise<void>} A promise that resolves when the item is removed.
     */
    async removeItemFromBargain(bargainPk, id) {
        return (await this.api.bargainOpenBargainsItemsDestroy(bargainPk, id)).data;
    }

    /**
     * Retrieve detailed information for a specific bargain.
     *
     * Endpoint: GET /bargain/open_bargains/{id}/
     *
     * @param {string} bargainId - The primary key of the bargain.
     * @returns {Promise<Object>} A promise that resolves to the bargain details.
     */
    async getBargainDetails(bargainId) {
        return (await this.api.bargainOpenBargainsRetrieve(bargainId)).data;
    }

    /**
     * Initiate a gift bargain by specifying the hasTarget character's ID.
     *
     * Endpoint: POST /bargain/open_bargains/gift/
     *
     * @param {string} targetCharacterId - The hasTarget character's ID.
     * @returns {Promise<Object>} A promise that resolves to the created gift bargain object.
     */
    async sendGift(targetCharacterId) {
        return (await this.api.bargainOpenBargainsGiftCreate({target_character_id: targetCharacterId})).data;
    }

    /**
     * Accept a bargain.
     *
     * Endpoint: POST /bargain/open_bargains/{bargain_pk}/accept/
     *
     * @param {string} bargainPk - The primary key of the bargain.
     * @returns {Promise<Object>} A promise that resolves to the accepted bargain object.
     */
    async acceptBargain(bargainPk) {
        return (await this.api.bargainOpenBargainsAcceptCreate(bargainPk)).data;
    }

    /**
     * Reject a bargain.
     *
     * Endpoint: POST /bargain/open_bargains/{bargain_pk}/reject/
     *
     * @param {string} bargainPk - The primary key of the bargain.
     * @returns {Promise<Object>} A promise that resolves to the rejected bargain object.
     */
    async rejectBargain(bargainPk) {
        return (await this.api.bargainOpenBargainsRejectCreate(bargainPk)).data;
    }
}

export default new BargainService(BargainGameApi);
