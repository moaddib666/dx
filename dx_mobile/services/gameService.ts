// import api from './api';

const fetchCharacters = async () => {
    try {
        // const response = await api.get('/characters');
        // return response.data;
    } catch (error) {
        throw new Error('Failed to fetch characters');
    }
};

const createCharacter = async (characterData: any) => {
    try {
        // const response = await api.post('/characters', characterData);
        // return response.data;
    } catch (error) {
        throw new Error('Failed to create character');
    }
};

const startFight = async (characterId: string) => {
    try {
        // const response = await api.post(`/fight/start`, { characterId });
        // return response.data;
    } catch (error) {
        throw new Error('Failed to start fight');
    }
};

export default { fetchCharacters, createCharacter, startFight };
