import store from '@/store';
import { Configuration, PlayerApi, SkillsApi, FightApi } from '@/api/dx-backend';

export const GameApiConfig = new Configuration({
    basePath: import.meta.env.VITE_API_BASE_URL,
    accessToken: store.state.token,
})

export const PlayerGameApi = new PlayerApi(GameApiConfig);
export const SkillsGameApi = new SkillsApi(GameApiConfig);
export const FightGameApi = new FightApi(GameApiConfig);


