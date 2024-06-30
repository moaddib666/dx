interface FightState {
    allies: any[];
    enemies: any[];
    scheduledActions: any[];
    actionHistory: any[];
}

const initialState: FightState = {
    allies: [],
    enemies: [],
    scheduledActions: [],
    actionHistory: [],
};

const fightReducer = (state = initialState, action: any): FightState => {
    switch (action.type) {
        case 'SET_ALLIES':
            return {
                ...state,
                allies: action.payload,
            };
        case 'SET_ENEMIES':
            return {
                ...state,
                enemies: action.payload,
            };
        case 'SCHEDULE_ACTION':
            return {
                ...state,
                scheduledActions: [...state.scheduledActions, action.payload],
            };
        case 'ADD_ACTION_HISTORY':
            return {
                ...state,
                actionHistory: [...state.actionHistory, action.payload],
            };
        default:
            return state;
    }
};

export default fightReducer;
