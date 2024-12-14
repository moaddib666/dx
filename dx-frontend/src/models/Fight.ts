import {CurrentFight} from "../api/dx-backend";
import {PlayerFightParticipant} from "./Player";

export class Fight {
    data: CurrentFight;
    enemies: PlayerFightParticipant[];
    allies: PlayerFightParticipant[];

    constructor(data: CurrentFight) {
        this.data = data;
        this.enemies = this.getEnemies();
        this.allies = this.getAllies();
    }

    getFightId(): string {
        return this.data.fight.id;
    }

    private getAllies(): PlayerFightParticipant[] {
        return this.data.allies.map((participant) => new PlayerFightParticipant(participant));
    }

    private getEnemies(): PlayerFightParticipant[] {
        return this.data.enemies.map((participant) => new PlayerFightParticipant(participant));
    }
}

