import {createRouter, createWebHistory} from 'vue-router';
import Home from '@/views/Home.vue';
import Story from '@/views/Story.vue';
import Characters from '@/views/Characters.vue';
import Gameplay from '@/views/Gameplay.vue';
import Community from '@/views/Community.vue';
import Shop from '@/views/Shop.vue';
import Support from '@/views/Support.vue';
import FAQ from '@/views/FAQ.vue';
import ArtGallery from "@/views/ArtGallery.vue";
import NewcomersGuide from "@/views/NewcomersGuide.vue";
import PlayerCheatSheet from "@/views/PlayerCheatSheet.vue";
import WatIsIt from "@/views/WatIsIt.vue";
import NotFound from "@/views/NotFound.vue";
import store from "@/store/index.js";
import Login from "@/views/Login.vue";
import CharacterSubmit from "@/views/Player/CharacterSubmit.vue";
import CharacterView from "@/views/Cartograph/Map.vue";
import DiceTest from "@/views/DiceTest.vue";
import LocationView from "@/views/Game/Location.vue";
import Register from "@/views/Register.vue";
import GameMasterMain from "@/views/GameMaster/GameMasterMain.vue";
import GameMasterLogin from "@/views/GameMaster/GameMasterLogin.vue"; // Component handles impersonation now
import CharacterSkills from "@/views/CharacterSkills.vue";
import CharacterInfo from "@/views/CharacterInfo.vue";
import MiniMap from "@/views/Cartograph/MiniMap.vue";
import UserMap from "@/views/Cartograph/UserMap.vue";
import WorldEditor from "@/views/WorldEditor/WorldEditor.vue";
import PlayerHomeDashboard from "@/views/PlyerHomeDashboard/PlayerHomeDashboard.vue";

const routes = [
    // Public pages
    {path: '/', name: 'Home', component: Home, meta: {requiresAuth: false}},
    {path: '/story', name: 'Story', component: Story, meta: {requiresAuth: false}},
    {path: '/gameplay', name: 'Gameplay', component: Gameplay, meta: {requiresAuth: false}},
    {path: '/community', name: 'Community', component: Community, meta: {requiresAuth: false}},
    {path: '/shop', name: 'Shop', component: Shop, meta: {requiresAuth: false}},
    {path: '/support', name: 'Support', component: Support, meta: {requiresAuth: false}},
    {path: '/faq', name: 'FAQ', component: FAQ, meta: {requiresAuth: false}},
    {path: '/art-gallery', name: 'ArtGallery', component: ArtGallery, meta: {requiresAuth: false}},
    {path: '/faq/newcomers-guide', name: 'NewcomersGuide', component: NewcomersGuide, meta: {requiresAuth: false}},
    {path: '/faq/player-cheatsheet', name: 'PlayerCheatSheet', component: PlayerCheatSheet, meta: {requiresAuth: false}},
    {path: '/faq/what-is-it', name: 'WhatIsIt', component: WatIsIt, meta: {requiresAuth: false}},

    // Authentication routes
    {path: '/login', name: 'Login', component: Login, meta: {requiresAuth: false}},
    {path: '/register', name: 'Register', component: Register, meta: {requiresAuth: false}},

    // Player dashboard and character management
    {path: '/player/dashboard', name: 'PlayerHomeDashboard', component: PlayerHomeDashboard, meta: {requiresAuth: true}},
    {path: '/player/characters', name: 'Characters', component: Characters, meta: {requiresAuth: false}},
    {path: '/player/characters/submit', name: 'CharacterSubmit', component: CharacterSubmit, meta: {requiresAuth: false}},
    {path: '/player/characters/info', name: 'CharacterInfo', component: CharacterInfo, meta: {requiresAuth: true}},
    {path: '/player/characters/skills', name: 'CharacterSkills', component: CharacterSkills, meta: {requiresAuth: false}},

    // Map and cartography routes
    {path: '/map', name: 'UserMap', component: UserMap, meta: {requiresAuth: true}},
    {path: '/map/mini', name: 'MiniMap', component: MiniMap, meta: {requiresAuth: true}},

    // Game and tools routes
    {path: '/dice', name: 'Dice', component: DiceTest, meta: {requiresAuth: false}},
    {path: '/game', name: 'Game', component: LocationView, meta: {requiresAuth: true}},
    // {path: '/game/fight', name: 'GameFight', component: FightView, meta: {requiresAuth: true}},

    // Game Master routes
    {path: '/game-master', name: 'GameMaster', component: GameMasterMain, meta: {requiresAuth: true, requiresGameMaster: true}},
    {path: '/game-master/impersonate', name: 'GameMasterImpersonate', component: GameMasterLogin, meta: {requiresAuth: false}},
    {path: '/game-master/cartograph', name: 'Cartograph', component: CharacterView, meta: {requiresAuth: false, requiresGameMaster: true}},
    {path: '/game-master/world-editor', name: 'WorldEditor', component: WorldEditor, meta: {requiresAuth: true, requiresGameMaster: true}},

    // 404 page - catch all route
    {path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound, meta: {requiresAuth: false}},
];

// access vue environment variables

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!store.getters.isAuthenticated) {
            next({path: '/login'});
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;
