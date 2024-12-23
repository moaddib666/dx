import store from '@/store';
import {Configuration, CoreApi, FightApi, ModificatorsApi, PlayerApi, SchoolApi, SkillsApi} from '@/api/dx-backend';

export const GameApiConfig = new Configuration({
    basePath: import.meta.env.VITE_API_BASE_URL,
    accessToken: store.state.token,
})

export const PlayerGameApi = new PlayerApi(GameApiConfig);
export const SkillsGameApi = new SkillsApi(GameApiConfig);
export const FightGameApi = new FightApi(GameApiConfig);
export const SchoolGameApi = new SchoolApi(GameApiConfig);
export const ModificatorsGameApi = new ModificatorsApi(GameApiConfig);
export const CoreGameApi = new CoreApi(GameApiConfig);