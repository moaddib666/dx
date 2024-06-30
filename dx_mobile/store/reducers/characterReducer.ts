interface CharacterState {
    characters: any[];
    selectedCharacter: any | null;
}

const initialState: CharacterState = {
    characters: [],
    selectedCharacter: null,
};

const characterReducer = (state = initialState, action: any): CharacterState => {
    switch (action.type) {
        case 'ADD_CHARACTER':
            return {
                ...state,
                characters: [...state.characters, action.payload],
            };
        case 'SELECT_CHARACTER':
            return {
                ...state,
                selectedCharacter: action.payload,
            };
        default:
            return state;
    }
};

export default characterReducer;
