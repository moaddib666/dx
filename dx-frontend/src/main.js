import { createApp} from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './assets/styles/global.css';
import './assets/styles/colors.css';
import './assets/styles/typography.css';
import './assets/styles/layout.css';
import './assets/styles/buttons.css';
import WebSocketPlugin from "@/plugins/websocket-bus.js";


createApp(App).use(store).use(router).use(WebSocketPlugin, {url: import.meta.env.VITE_WS_BASE_URL}).mount('#app');
