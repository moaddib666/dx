// EventTypes.ts
export enum EventCategory {
    PLAYER = "player",
    LOCATION = "location",
    FIGHT = "fight",
    GAME = "game",
}

export interface GameEventData {}

export interface GameEvent {
    name: string;
    timestamp: number;
    id: string;
    category: EventCategory;
    data?: GameEventData;
}

// {"name":"player_turn_init","timestamp":1719570982.9488451,"id":"996cf57b-9c08-4723-bf5d-220b73e7346b","category":"fight","data":{"current_turn":{"id":"6e33a19a-7afa-4d6a-be51-0cf4bc33aeae","started_at":"2024-06-28T10:36:22.937810Z","duration":60},"player_info":{"id":"8f7b9e38-e568-4a8a-8008-3717d6e53b82","name":"Zena","rank_grade":1,"attributes":[{"name":"Health","current":50,"max":38},{"name":"Energy","current":15,"max":128},{"name":"Action Points","current":4,"max":4}],"dimension":2,"location":"2ffbc3ef-48ad-4fcc-80f2-0935a71d1760","fight":"6aaa7b4f-45f5-45b3-97d1-46888ad8f8e3","duel_invitations":["820aeced-1714-4e10-a01b-e8e29917e38a"]}}}
export interface PlayerEventData extends GameEventData {
    current_turn: {
        id: string;
        started_at: string;
        duration: number;
    };
    player_info: {
        id: string;
        name: string;
        rank_grade: number;
        attributes: {
            name: string;
            current: number;
            max: number;
        }[];
        dimension: number;
        location: string;
        fight: string;
        duel_invitations: string[];
    };
}

export interface RequestRefreshPlayerInfo extends GameEventData {}

export interface Events extends Record<string, GameEventData>{
    'fight::player_turn_init': GameEventData;
}
