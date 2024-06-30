import {PlayerGameApi} from "../../api";

export const fetchPlayer = () => {
    return async (dispatch: any) => {
        try {
            const player = await PlayerGameApi.playerPlayerInfoRetrieve();
            dispatch({ type: 'FETCH_PLAYER_SUCCESS', payload: player });
        } catch (error) {
            console.error('Failed to fetch player', error);
        }
    };
};
