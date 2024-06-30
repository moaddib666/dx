import gameService from '../../services/gameService';

export const addCharacter = (character: any) => ({
    type: 'ADD_CHARACTER',
    payload: character,
});

export const selectCharacter = (character: any) => ({
    type: 'SELECT_CHARACTER',
    payload: character,
});

export const fetchCharacters = () => {
    return async (dispatch: any) => {
        try {
            const characters = await gameService.fetchCharacters();
            // Dispatch actions to update the state with fetched characters
        } catch (error) {
            console.error('Failed to fetch characters', error);
        }
    };
};

export const createCharacter = (characterData: any) => {
    return async (dispatch: any) => {
        try {
            const newCharacter = await gameService.createCharacter(characterData);
            dispatch(addCharacter(newCharacter));
        } catch (error) {
            console.error('Failed to create character', error);
        }
    };
};
