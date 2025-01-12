import store from '@/store';
import {
    ActionApi,
    CharacterApi,
    Configuration,
    CoreApi,
    FightApi,
    ModificatorsApi,
    SchoolApi,
    SkillsApi,
    WorldApi,
    ClientApi,
    GalleryApi,
    EffectsApi,
    ItemsApi,
    ShieldsApi,
} from '@/api/dx-backend';

export const GameApiConfig = new Configuration({
    basePath: import.meta.env.VITE_API_BASE_URL,
    accessToken: () => store.getters.getAuthToken,
})

export const ActionGameApi = new ActionApi(GameApiConfig);
export const ClientGameApi = new ClientApi(GameApiConfig);
export const CharacterGameApi = new CharacterApi(GameApiConfig);
export const EffectsGameApi = new EffectsApi(GameApiConfig);
export const SkillsGameApi = new SkillsApi(GameApiConfig);
export const FightGameApi = new FightApi(GameApiConfig);
export const SchoolGameApi = new SchoolApi(GameApiConfig);
export const ModificatorsGameApi = new ModificatorsApi(GameApiConfig);
export const CoreGameApi = new CoreApi(GameApiConfig);
export const WorldGameApi = new WorldApi(GameApiConfig);
export const GalleryGameApi = new GalleryApi(GameApiConfig);
export const ItemsGameApi = new ItemsApi(GameApiConfig);
export const ShieldsGameApi = new ShieldsApi(GameApiConfig);