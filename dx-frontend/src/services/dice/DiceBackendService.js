import { ActionGameApi } from "@/api/backendService.js";

/**
 * Service for handling dice rolling operations via backend API
 */
export class DiceBackendService {
  /**
   * @constructor
   */
  constructor() {
    /**
     * The API client instance
     * @type {import('@/api/dx-backend').ActionApi}
     * @private
     */
    this.actionApi = ActionGameApi;
  }

  /**
   * Rolls a D20 dice using the backend API
   * @returns {Promise<{
   *   number: number,
   *   rollTime: number,
   *   targetNumber: number,
   *   outcome: string,
   *   isDeterministic: boolean
   * }>} Promise resolving to the dice roll result
   */
  async rollD20Dice() {
    try {
      const response = await this.actionApi.actionRollD20DiceCreate();

      // Get the dice roll value from the API response
      const diceValue = response.data.dice_side || 1;

      // Map API outcome to UI-compatible outcome
      let mappedOutcome;
      if (response.data.outcome) {
        mappedOutcome = this.mapApiOutcomeToUiOutcome(response.data.outcome, diceValue);
      } else {
        mappedOutcome = this.determineOutcome(diceValue);
      }

      // Create result with mapped outcome
      const result = {
        number: diceValue,
        rollTime: 0, // Not provided by API, using 0 as default
        targetNumber: 11, // Default target for D20 rolls
        outcome: mappedOutcome,
        isDeterministic: true // API rolls are deterministic
      };

      return result;
    } catch (error) {
      console.error('Error rolling D20 dice via API:', error);
      throw error;
    }
  }

  /**
   * Maps API outcome values to UI-compatible outcome values
   * @param {string} apiOutcome - The outcome from the API
   * @param {number} diceValue - The dice value (used as fallback)
   * @returns {string} UI-compatible outcome
   */
  mapApiOutcomeToUiOutcome(apiOutcome, diceValue) {
    switch (apiOutcome) {
      case 'Critical Fail':
        return 'Critical Fail';
      case 'Critical Success':
        return 'Critical Success';
      case 'Bad Luck':
        return 'Fail';
      case 'Good Luck':
        return 'Success';
      case 'Base Value':
        // For Base Value, determine outcome based on dice value
        return this.determineOutcome(diceValue);
      default:
        // For any other unexpected values, determine based on dice value
        return this.determineOutcome(diceValue);
    }
  }

  /**
   * Determines the outcome based on the dice roll value
   * @param {number} rollValue - The value rolled on the dice
   * @returns {string} The outcome of the roll
   */
  determineOutcome(rollValue) {
    if (rollValue === 1) {
      return 'Critical Fail';
    } else if (rollValue < 15) {
      return 'Fail';
    } else if (rollValue === 20) {
      return 'Critical Success';
    } else {
      return 'Success';
    }
  }
}

// Export default instance for backward compatibility
export default DiceBackendService;