import {createApp} from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './assets/styles/global.css';
import './assets/styles/colors.css';
import './assets/styles/typography.css';
import './assets/styles/layout.css';
import './assets/styles/buttons.css';
import skillService from '@/services/skillService';

async function bootstrap() {
    try {
        // Display a loading screen (optional)
        document.getElementById("app").innerHTML = "Loading, please wait...";

        // Ensure the skill cache is updated before app initialization
        try {
            await skillService.updateCache();
        } catch (error) {
            console.error("Failed to update skill service cache:", error);
        }
        // Create and mount the app
        createApp(App)
            .use(store)
            .use(router)
            // .use(WebSocketPlugin, {url: import.meta.env.VITE_WS_BASE_URL})
            .mount('#app');
    } catch (error) {
        console.error("Failed to initialize the app:", error);
        document.getElementById("app").innerHTML = "Failed to load application.";
    }
}

// Run the bootstrap function
bootstrap();
