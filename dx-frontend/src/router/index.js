import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Story from '@/views/Story.vue';
import Characters from '@/views/Characters.vue';
import Gameplay from '@/views/Gameplay.vue';
import Community from '@/views/Community.vue';
import Shop from '@/views/Shop.vue';
import Support from '@/views/Support.vue';
import FAQ from '@/views/FAQ.vue';
import RegisterPlay from '@/views/RegisterPlay.vue';
const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/story', name: 'Story', component: Story },
  { path: '/characters', name: 'Characters', component: Characters },
  { path: '/gameplay', name: 'Gameplay', component: Gameplay },
  { path: '/community', name: 'Community', component: Community },
  { path: '/shop', name: 'Shop', component: Shop },
  { path: '/support', name: 'Support', component: Support },
  { path: '/faq', name: 'FAQ', component: FAQ },
  { path: '/register', name: 'RegisterPlay', component: RegisterPlay }
];

// access vue environment variables

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
