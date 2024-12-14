// services/apiConfig.ts
import {Configuration, PlayerApi, SkillsApi, FightApi, AuthApi} from './dx-backend';
import {API_BASE_URL} from "@env";
import { DxSocketClient } from './dx-websocket';
console.debug('PROCESS_ENV', API_BASE_URL);

const createApiConfig = (token: string) => {
    return new Configuration({
        basePath: API_BASE_URL,
        accessToken: token,
    });
};

let GameApiConfig = createApiConfig('');
export const PlayerGameApi = new PlayerApi(GameApiConfig);
export const SkillsGameApi = new SkillsApi(GameApiConfig);
export const FightGameApi = new FightApi(GameApiConfig);
export const AuthGameApi = new AuthApi(GameApiConfig);
export const DefaultGameBus = new DxSocketClient();
