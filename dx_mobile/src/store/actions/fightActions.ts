import gameService from '../../services/gameService';

export const setAllies = (allies: any[]) => ({
    type: 'SET_ALLIES',
    payload: allies,
});

export const setEnemies = (enemies: any[]) => ({
    type: 'SET_ENEMIES',
    payload: enemies,
});

export const scheduleAction = (action: any) => ({
    type: 'SCHEDULE_ACTION',
    payload: action,
});

export const addActionHistory = (action: any) => ({
    type: 'ADD_ACTION_HISTORY',
    payload: action,
});

export const startFight = (characterId: string) => {
    return async (dispatch: any) => {
        try {
            const fightData = await gameService.startFight(characterId);
            // Dispatch actions to update the state with fight data
        } catch (error) {
            console.error('Failed to start fight', error);
        }
    };
};
