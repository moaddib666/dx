import Action from './Action';
import {AttributeType, LifePath} from "./Core";

import {FightParticipant, PlayerInfo} from "../api/dx-backend";

interface GenericComputedAttributes {
    health: number;
    max_health: number;
    energy: number;
    max_energy: number;
}

interface ComputedAttributes extends GenericComputedAttributes{
    ap: number;
    max_ap: number;
}

export class Player {
    data: PlayerInfo;
    attributes: ComputedAttributes;
    name: string
    dimension: number
    id: string
    constructor(data: PlayerInfo) {
        this.data = data;
        this.attributes = {
            health: 0,
            max_health: 0,
            energy: 0,
            max_energy: 0,
            ap: 0,
            max_ap: 0

        };
        this.name = data.name
        this.dimension = data.dimension
        this.id = data.id
        this.calculateAttributes()
    }

    private calculateAttributes(): void {
        this.data.attributes.forEach((attr) => {
            switch (attr.name) {
                case AttributeType.HEALTH:
                    this.attributes.health = attr.current;
                    this.attributes.max_health = attr.max;
                    break;
                case AttributeType.ENERGY:
                    this.attributes.energy = attr.current;
                    this.attributes.max_energy = attr.max;
                    break;
                case AttributeType.ACTION_POINTS:
                    this.attributes.ap = attr.current;
                    this.attributes.max_ap = attr.max;
                    break;
            }
        });
    }

    validateAction(action: Action): boolean {
        const apCost = action.getActionPointsCost();
        const energyCost = action.getEnergyCost();

        return this.attributes.ap >= apCost && this.attributes.energy >= energyCost;
    }

    makeAction(action: Action): boolean {
        if (!this.validateAction(action)) {
            return false;
        }

        this.attributes.ap -= action.getActionPointsCost();
        this.attributes.energy -= action.getEnergyCost();
        return true;
    }

    discardAction(action: Action): void {
        this.attributes.ap += action.getActionPointsCost();
        this.attributes.energy += action.getEnergyCost();
    }

    hasUnusedActionPoints(): boolean {
        return this.attributes.ap > 0;
    }
}

export class PlayerFightParticipant {
    data: FightParticipant
    attributes: GenericComputedAttributes;
    id: string
    name: string

    constructor(data: FightParticipant) {
        this.data = data;
        this.id = data.id
        this.name = data.name
        this.attributes = {
            health: 0,
            max_health: 0,
            energy: 0,
            max_energy: 0
        };
        this.calculateAttributes();
    }

    private calculateAttributes(): void {
        this.data.attributes.forEach((attr) => {
            switch (attr.name) {
                case AttributeType.HEALTH:
                    this.attributes.health = attr.current;
                    this.attributes.max_health = attr.max;
                    break;
                case AttributeType.ENERGY:
                    this.attributes.energy = attr.current;
                    this.attributes.max_energy = attr.max;
                    break;
            }
        });
    }
}

export default Player;