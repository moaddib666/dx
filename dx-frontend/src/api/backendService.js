import store from '@/store';
import {
    ActionApi,
    BargainApi,
    CharacterApi,
    ClientApi,
    Configuration,
    CoreApi,
    EffectsApi,
    GalleryApi,
    GamemasterApi,
    GMWorldEditiorPositionConnectionsApi,
    GMWorldEditiorPositionsApi,
    GMWorldEditorSubLocationsApi,
    GMWorldEditorAllSpawnersApi,
    GMWorldEditorNPCSpawnersApi,
    ItemsApi,
    ModificatorsApi,
    SchoolApi,
    ShieldsApi,
    SkillsApi,
    StoryApi,
    WorldApi,
    FightApi,
    DiceApi,
    KnowledgeBaseDocumentsApi,
    KnowledgeBaseTimelineEventsApi,
    CharactersPublishedApi
} from '@/api/dx-backend';

export const GameApiConfig = new Configuration({
    basePath: import.meta.env.VITE_API_BASE_URL,
    accessToken: () => store.getters.getAuthToken,
})
export const PublicApiConfig = new Configuration({
    basePath: import.meta.env.VITE_API_BASE_URL,
})
export const BargainGameApi = new BargainApi(GameApiConfig);
export const ActionGameApi = new ActionApi(GameApiConfig);
export const ClientGameApi = new ClientApi(GameApiConfig);
export const CharacterGameApi = new CharacterApi(GameApiConfig);
export const EffectsGameApi = new EffectsApi(GameApiConfig);
export const SkillsGameApi = new SkillsApi(GameApiConfig);
export const SchoolGameApi = new SchoolApi(GameApiConfig);
export const ModificatorsGameApi = new ModificatorsApi(GameApiConfig);
export const CoreGameApi = new CoreApi(GameApiConfig);
export const WorldGameApi = new WorldApi(GameApiConfig);
export const GalleryGameApi = new GalleryApi(GameApiConfig);
export const ItemsGameApi = new ItemsApi(GameApiConfig);
export const ShieldsGameApi = new ShieldsApi(GameApiConfig);
export const GameMasterApi = new GamemasterApi(GameApiConfig);
export const GMWorldPositionConnectionsApi = new GMWorldEditiorPositionConnectionsApi(GameApiConfig);
export const GMWorldPositionsApi = new GMWorldEditiorPositionsApi(GameApiConfig);
export const GMWorldSubLocationsApi = new GMWorldEditorSubLocationsApi(GameApiConfig);
export const GMWorldGenericSpawnersApi = new GMWorldEditorAllSpawnersApi(GameApiConfig);
export const GMWorldNPCSpawnersApi = new GMWorldEditorNPCSpawnersApi(GameApiConfig);
export const StoryGameApi = new StoryApi(GameApiConfig);
export const FightGameApi = new FightApi(GameApiConfig);
export const DiceGameApi = new DiceApi(GameApiConfig);
export const KnowledgeBaseDocumentsGameApi = new KnowledgeBaseDocumentsApi(GameApiConfig);
export const KnowledgeBaseTimelineEventsGameApi = new KnowledgeBaseTimelineEventsApi(GameApiConfig);
export const PublishedCharactersPublicApi = new CharactersPublishedApi(PublicApiConfig);