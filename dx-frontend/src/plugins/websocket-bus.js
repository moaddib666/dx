import {eventbus} from "@/api/dx-websocket/index";


const WebSocketPlugin = {
    install(app, options) {
        console.debug('WebSocketPlugin.install', options);
        app.config.globalProperties.$dxBus = eventbus;
        console.debug('WebSocketPlugin.install', app.config.globalProperties.$dxBus)
    }
};

export default WebSocketPlugin;