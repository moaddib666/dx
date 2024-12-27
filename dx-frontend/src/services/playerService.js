class PlayerService {
    /**
     * Create an instance of PlayerService.
     * @param {Object} playerData - The data representing the player.
     */
    constructor(playerData) {
        if (!playerData || typeof playerData !== "object") {
            throw new Error("Invalid player data.");
        }
        this.player = playerData;
    }

    /**
     * Get the value of a specific attribute by name.
     * @param {string} attributeName - The name of the attribute to retrieve.
     * @returns {Object|null} The attribute object, or null if not found.
     */
    getAttribute(attributeName) {
        const attribute = this.player.attributes.find(attr => attr.name === attributeName);
        return attribute || null;
    }

    /**
     * Check if the player has action points remaining.
     * @returns {boolean} True if the player has action points, false otherwise.
     */
    hasActionPoints() {
        const actionPoints = this.getAttribute("Action Points");
        return actionPoints ? actionPoints.current > 0 : false;
    }

    /**
     * Get the current position of the player.
     * @returns {string} The player's position.
     */
    getPosition() {
        return this.player.position;
    }

    /**
     * Get the player's name.
     * @returns {string} The player's name.
     */
    getName() {
        return this.player.name;
    }

    /**
     * Get the player's rank grade.
     * @returns {number} The player's rank grade.
     */
    getRankGrade() {
        return this.player.rank_grade;
    }

    /**
     * Check if the player is engaged in a fight.
     * @returns {boolean} True if the player is in a fight, false otherwise.
     */
    isInFight() {
        return this.player.fight !== null;
    }

    /**
     * Check if the player has duel invitations.
     * @returns {boolean} True if there are duel invitations, false otherwise.
     */
    hasDuelInvitations() {
        return Array.isArray(this.player.duel_invitations) && this.player.duel_invitations.length > 0;
    }

    /**
     * Get the current value of an attribute by name.
     * @param {string} attributeName - The name of the attribute to retrieve.
     * @returns {number|null} The current value of the attribute, or null if not found.
     */
    getCurrentAttributeValue(attributeName) {
        const attribute = this.getAttribute(attributeName);
        return attribute ? attribute.current : null;
    }

    /**
     * Get the max value of an attribute by name.
     * @param {string} attributeName - The name of the attribute to retrieve.
     * @returns {number|null} The max value of the attribute, or null if not found.
     */
    getMaxAttributeValue(attributeName) {
        const attribute = this.getAttribute(attributeName);
        return attribute ? attribute.max : null;
    }
}

export default PlayerService;
