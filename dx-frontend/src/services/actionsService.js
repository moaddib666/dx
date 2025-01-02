import {ActionGameApi} from "@/api/backendService.js";

class ActionService {
    /**
     * Create an instance of ActionService.
     * @param {Object} api - The API instance (e.g., Axios or Fetch).
     */
    constructor(api = ActionGameApi) {
        this.api = api;
    }

    /**
     * Perform an action.
     * @param {Object} params - Parameters for the action.
     * @param {string} params.actionType - The type of action to perform (e.g., "MOVE", "USE_SKILL").
     * @param {Object} [params.actionData] - Additional data associated with the action (optional).
     * @param {string} [params.position] - The position of the player (optional).
     * @param {string} [params.skill] - The skill to use (optional).
     * @param {Array<string>} [params.targets] - The targets of the action (optional).
     * @returns {Promise<Object>} The response from the server.
     * @throws Will throw an error if the request fails.
     */
    async performAction({actionType, actionData = {}, position = null, skill = null, targets = [], item = null}) {
        if (!actionType) {
            throw new Error("Action type is required.");
        }

        const payload = {
            action_type: actionType,
            data: actionData,
            position,
            skill,
            targets,
            item
        };

        try {
            const response = await this.api.actionCreate(payload);
            return response.data;
        } catch (error) {
            console.error("Failed to perform action:", error);
            throw error;
        }
    }

    async performActionForCharacter({
                                        actionType,
                                        actionData = {},
                                        position = null,
                                        skill = null,
                                        targets = [],
                                        characterId
                                    }) {
        if (!actionType) {
            throw new Error("Action type is required.");
        }

        const payload = {
            initiator: characterId,
            action_type: actionType,
            data: actionData,
            position,
            skill,
            targets,
        };

        try {
            const response = await this.api.actionGmRegisterCharacterActionCreate(payload);
            return response.data;
        } catch (error) {
            console.error("Failed to perform action:", error);
            throw error;
        }
    }

    /**
     * Perform a "MOVE" action.
     * @param {string} position - The position to move to.
     * @returns {Promise<Object>} The response from the server.
     */
    async move(position) {
        if (!position) {
            throw new Error("Position is required for MOVE action.");
        }
        return await this.performAction({actionType: "MOVE", position});
    }

    /**
     * Perform a "USE_SKILL" action.
     * @param {string} skill - The skill to use.
     * @param {Array<string>} targets - The targets of the skill.
     * @param {Object} [actionData] - Additional data for the skill action (optional).
     * @returns {Promise<Object>} The response from the server.
     */
    async useSkill(skill, targets, actionData = {}) {
        if (!skill) {
            throw new Error("Skill is required for USE_SKILL action.");
        }
        if (!Array.isArray(targets) || targets.length === 0) {
            throw new Error("At least one target is required for USE_SKILL action.");
        }
        return await this.performAction({
            actionType: "USE_SKILL",
            skill,
            targets,
            actionData,
        });
    }

    /**
     * perform dice roll action
     * @param sides
     * @returns {Promise<Number>}
     */
    async diceRoll(sides) {
        const result = await this.performAction({
            actionType: "DICE_ROLL",
            actionData: {
                sides: sides
            }
        });

        return result?.data.dice_result;
    }

    /**
     * Perform a generic action with custom parameters.
     * @param {Object} params - Parameters for the action.
     * @returns {Promise<Object>} The response from the server.
     */
    async customAction(params) {
        return await this.performAction(params);
    }
}

export default ActionService;
