import { OpenaiCharacter } from '@/api/dx-backend';
import { KindDeeEnum } from '@/api/dx-backend';

/**
 * Interface representing an attribute with current and max values
 */
interface Attribute {
  name: string;
  current: number;
  max: number;
}

/**
 * Extended OpenaiCharacter interface that includes the attributes array
 */
interface PlayerData extends Partial<OpenaiCharacter> {
  attributes?: Attribute[];
  position?: string | null;
  duel_invitations?: any[];
  rank_grade?: number;
}

/**
 * Service for managing player data and operations
 */
class PlayerService {
  private player: PlayerData;

  /**
   * Create an instance of PlayerService.
   * @param playerData - The data representing the player.
   */
  constructor(playerData: PlayerData) {
    if (!playerData || typeof playerData !== "object") {
      throw new Error("Invalid player data.");
    }
    this.player = playerData;
  }

  /**
   * Get the value of a specific attribute by name.
   * @param attributeName - The name of the attribute to retrieve.
   * @returns The attribute object, or null if not found.
   */
  getAttribute(attributeName: string): Attribute | null {
    if (!this.player.attributes || !Array.isArray(this.player.attributes)) {
      return null;
    }
    const attribute = this.player.attributes.find(attr => attr.name === attributeName);
    return attribute || null;
  }

  /**
   * Check if the player has action points remaining.
   * @returns True if the player has action points, false otherwise.
   */
  hasActionPoints(): boolean {
    const actionPoints = this.getAttribute("Action Points");
    return actionPoints ? actionPoints.current > 0 : false;
  }

  /**
   * Get the current position of the player.
   * @returns The player's position.
   */
  getPosition(): string | null {
    return this.player.position || null;
  }

  /**
   * Get the player's name.
   * @returns The player's name.
   */
  getName(): string {
    return this.player.name || '';
  }

  /**
   * Get the player's rank grade.
   * @returns The player's rank grade.
   */
  getRankGrade(): number {
    return this.player.rank_grade || 0;
  }

  /**
   * Check if the player is engaged in a fight.
   * @returns True if the player is in a fight, false otherwise.
   */
  isInFight(): boolean {
    return this.player.fight !== null && this.player.fight !== undefined;
  }

  /**
   * Check if the player has duel invitations.
   * @returns True if there are duel invitations, false otherwise.
   */
  hasDuelInvitations(): boolean {
    return Array.isArray(this.player.duel_invitations) && this.player.duel_invitations.length > 0;
  }

  /**
   * Get the current value of an attribute by name.
   * @param attributeName - The name of the attribute to retrieve.
   * @returns The current value of the attribute, or null if not found.
   */
  getCurrentAttributeValue(attributeName: string): number | null {
    const attribute = this.getAttribute(attributeName);
    return attribute ? attribute.current : null;
  }

  /**
   * Get the max value of an attribute by name.
   * @param attributeName - The name of the attribute to retrieve.
   * @returns The max value of the attribute, or null if not found.
   */
  getMaxAttributeValue(attributeName: string): number | null {
    const attribute = this.getAttribute(attributeName);
    return attribute ? attribute.max : null;
  }
}

export default PlayerService;