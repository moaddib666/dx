import { FightGameApi } from '@/api/backendService';
import type { FightGeneric, Fighter, OpenaiCharacter } from '@/api/dx-backend';

/**
 * Fight Service for managing character fights
 * This service provides methods to:
 * - Check if a character is in a fight
 * - Get information about a fight
 * - Check if a character is pending to join a fight
 * - Get other participants in a fight
 */
export class FightService {
  private currentFight: FightGeneric | null = null;
  private pendingJoinUsers: Fighter[] = [];
  private joinedUsers: Fighter[] = [];

  /**
   * Determines if a character is in a fight by checking the fight property
   * @param character The OpenaiCharacter to check
   * @returns Promise<boolean> indicating if the character is in a fight
   */
  public async isInFight(character: OpenaiCharacter): Promise<boolean> {
    // Check if the character has a fight UUID
    const hasFight = !!character.fight;

    // If the character doesn't have a fight UUID, clean the current fight data
    if (!hasFight) {
      this.currentFight = null;
      this.pendingJoinUsers = [];
      this.joinedUsers = [];
    }

    return hasFight;
  }

  /**
   * Determines if a character is pending to join a fight
   * @param character The OpenaiCharacter to check
   * @returns Promise<boolean> indicating if the character is pending to join a fight
   */
  public async isPendingJoin(character: OpenaiCharacter): Promise<boolean> {
    // Use cached fight data if available
    if (!character.fight) {
      return false;
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return false;
    }

    return this.currentFight.pending_join?.some(fighter => fighter.id === character.id) || false;
  }

  /**
   * Gets the current fight for a character
   * Uses cached fight data if available, otherwise initializes it
   * @param character The OpenaiCharacter to get the fight for
   * @returns Promise<FightGeneric | null> The fight or null if not in a fight
   */
  public async getFight(character: OpenaiCharacter): Promise<FightGeneric | null> {
    // Clean fight data if character doesn't have a fight UUID
    if (!character.fight) {
      this.currentFight = null;
      this.pendingJoinUsers = [];
      this.joinedUsers = [];
      return null;
    }

    // If we already have fight data and it matches the character's fight UUID, use the cached data
    if (this.currentFight && this.currentFight.id === character.fight) {
      return this.currentFight;
    }

    // If we don't have fight data or it doesn't match, fetch it
    return this.refreshFight(character);
  }

  /**
   * Refreshes the fight data from the API
   * @param character The OpenaiCharacter to refresh the fight for
   * @returns Promise<FightGeneric | null> The refreshed fight or null if not in a fight or error
   */
  public async refreshFight(character: OpenaiCharacter): Promise<FightGeneric | null> {
    // Clean fight data if character doesn't have a fight UUID
    if (!character.fight) {
      this.currentFight = null;
      this.pendingJoinUsers = [];
      this.joinedUsers = [];
      return null;
    }

    // Fetch the latest fight data from the API
    try {
      const response = await FightGameApi.fightFightRetrieve(character.fight);
      this.currentFight = response.data;
      this.pendingJoinUsers = this.currentFight.pending_join || [];
      this.joinedUsers = this.currentFight.joined || [];
      return this.currentFight;
    } catch (error) {
      console.error('Error fetching fight:', error);
      // Clean fight data if there was an error fetching the fight
      this.currentFight = null;
      this.pendingJoinUsers = [];
      this.joinedUsers = [];
      return null;
    }
  }

  /**
   * Gets the participants in a fight
   * @param character The OpenaiCharacter to get the fight participants for
   * @returns Promise<Fighter[]> Array of fight participants
   */
  public async getFightParticipants(character: OpenaiCharacter): Promise<Fighter[]> {
    // Use cached fight data if available
    if (!character.fight) {
      return [];
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return [];
    }

    return this.joinedUsers;
  }

  /**
   * Gets the pending join users in a fight
   * @param character The OpenaiCharacter to get the pending join users for
   * @returns Promise<Fighter[]> Array of pending join fighters
   */
  public async getPendingJoinUsers(character: OpenaiCharacter): Promise<Fighter[]> {
    // Use cached fight data if available
    if (!character.fight) {
      return [];
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return [];
    }

    return this.pendingJoinUsers;
  }

  /**
   * Gets the attacker in a fight
   * @param character The OpenaiCharacter to get the attacker for
   * @returns Promise<Fighter | null> The attacker or null if not in a fight
   */
  public async getAttacker(character: OpenaiCharacter): Promise<Fighter | null> {
    // Use cached fight data if available
    if (!character.fight) {
      return null;
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return null;
    }

    return this.currentFight.attacker;
  }

  /**
   * Gets the defender in a fight
   * @param character The OpenaiCharacter to get the defender for
   * @returns Promise<Fighter | null> The defender or null if not in a fight
   */
  public async getDefender(character: OpenaiCharacter): Promise<Fighter | null> {
    // Use cached fight data if available
    if (!character.fight) {
      return null;
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return null;
    }

    return this.currentFight.defender;
  }

  /**
   * Checks if the fight is a duel
   * @param character The OpenaiCharacter to check
   * @returns Promise<boolean | null> indicating if the fight is a duel or null if not in a fight
   */
  public async isDuel(character: OpenaiCharacter): Promise<boolean | null> {
    // Use cached fight data if available
    if (!character.fight) {
      return null;
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return null;
    }

    return this.currentFight.duel || false;
  }

  /**
   * Checks if the fight is open for others to join
   * @param character The OpenaiCharacter to check
   * @returns Promise<boolean | null> indicating if the fight is open or null if not in a fight
   */
  public async isOpen(character: OpenaiCharacter): Promise<boolean | null> {
    // Use cached fight data if available
    if (!character.fight) {
      return null;
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return null;
    }

    return this.currentFight.open || false;
  }

  /**
   * Gets the current round of the fight
   * @param character The OpenaiCharacter to get the current round for
   * @returns Promise<number | null> The current round or null if not in a fight
   */
  public async getCurrentRound(character: OpenaiCharacter): Promise<number | null> {
    // Use cached fight data if available
    if (!character.fight) {
      return null;
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return null;
    }

    return this.currentFight.current_round || 0;
  }

  /**
   * Gets the position ID where the fight is taking place
   * @param character The OpenaiCharacter to get the position for
   * @returns Promise<string | null> The position ID or null if not in a fight
   */
  public async getPosition(character: OpenaiCharacter): Promise<string | null> {
    // Use cached fight data if available
    if (!character.fight) {
      return null;
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return null;
    }

    return this.currentFight.position;
  }

  /**
   * Gets the campaign ID the fight belongs to
   * @param character The OpenaiCharacter to get the campaign for
   * @returns Promise<string | null> The campaign ID or null if not in a fight
   */
  public async getCampaign(character: OpenaiCharacter): Promise<string | null> {
    // Use cached fight data if available
    if (!character.fight) {
      return null;
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return null;
    }

    return this.currentFight.campaign;
  }

  /**
   * Gets the timestamp when the fight was created
   * @param character The OpenaiCharacter to get the created timestamp for
   * @returns Promise<number | null> The created timestamp or null if not in a fight or not available
   */
  public async getCreatedTimestamp(character: OpenaiCharacter): Promise<number | null> {
    // Use cached fight data if available
    if (!character.fight) {
      return null;
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return null;
    }

    return this.currentFight.created || null;
  }

  /**
   * Gets the timestamp when the fight ended
   * @param character The OpenaiCharacter to get the ended timestamp for
   * @returns Promise<number | null> The ended timestamp or null if not in a fight or not ended
   */
  public async getEndedTimestamp(character: OpenaiCharacter): Promise<number | null> {
    // Use cached fight data if available
    if (!character.fight) {
      return null;
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return null;
    }

    return this.currentFight.ended_at || null;
  }

  /**
   * Checks if the fight has ended
   * @param character The OpenaiCharacter to check
   * @returns Promise<boolean> indicating if the fight has ended
   */
  public async hasEnded(character: OpenaiCharacter): Promise<boolean> {
    // Use cached fight data if available
    if (!character.fight) {
      return false;
    }

    // Get fight data (uses cache if available)
    await this.getFight(character);

    if (!this.currentFight) {
      return false;
    }

    return !!this.currentFight.ended_at;
  }
}

// Export a singleton instance of the FightService
export const fightService = new FightService();