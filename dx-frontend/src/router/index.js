import {createRouter, createWebHistory} from 'vue-router';
import Home from '@/views/Home.vue';
import Story from '@/views/Story.vue';
import Characters from '@/views/Characters.vue';
import Gameplay from '@/views/Gameplay.vue';
import Community from '@/views/Community.vue';
import Shop from '@/views/Shop.vue';
import Support from '@/views/Support.vue';
import FAQ from '@/views/FAQ.vue';
import RegisterPlay from '@/views/RegisterPlay.vue';
import ArtGallery from "@/views/ArtGallery.vue";
import store from "@/store/index.js";
import Login from "@/views/Login.vue";
import FightView from "@/views/Game/Fight.vue";
import CharacterSubmit from "@/views/Player/CharacterSubmit.vue";
import CharacterView from "@/views/Cartograph/Map.vue";

const routes = [
    {path: '/', name: 'Home', component: Home, meta: {requiresAuth: false}},
    {path: '/story', name: 'Story', component: Story, meta: {requiresAuth: false}},
    {path: '/cartograph', name: 'Cartograph', component: CharacterView, meta: {requiresAuth: false}},
    {path: '/characters', name: 'Characters', component: Characters, meta: {requiresAuth: false}},
    {path: '/characters/submit', name: 'CharacterSubmit', component: CharacterSubmit, meta: {requiresAuth: false}},
    {path: '/gameplay', name: 'Gameplay', component: Gameplay, meta: {requiresAuth: false}},
    {path: '/community', name: 'Community', component: Community, meta: {requiresAuth: false}},
    {path: '/shop', name: 'Shop', component: Shop, meta: {requiresAuth: false}},
    {path: '/support', name: 'Support', component: Support, meta: {requiresAuth: false}},
    {path: '/faq', name: 'FAQ', component: FAQ, meta: {requiresAuth: false}},
    {path: '/register', name: 'RegisterPlay', component: RegisterPlay, meta: {requiresAuth: false}},
    {path: '/art', name: 'ArtGallery', component: ArtGallery, meta: {requiresAuth: false}},
    // TODO: Add route group here /game/* for game routes that require authentication
    {path: '/game', name: 'Game', component: FightView, meta: {requiresAuth: true}},
    {path: '/login', name: 'Login', component: Login, meta: {requiresAuth: false}}
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
