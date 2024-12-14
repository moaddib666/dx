import {DxSocketClient} from "@/api/dx-websocket/index";
import mitt from "mitt";

const WebSocketPlugin = {
    install(app, options) {
        console.debug('WebSocketPlugin.install', options);

        const eventbus = mitt()
        const webSocketService = new DxSocketClient(eventbus);
        app.config.globalProperties.$dxBus = eventbus;
        webSocketService.connect(options.url);
        console.debug('WebSocketPlugin.install', app.config.globalProperties.$dxBus)
    }
};

export default WebSocketPlugin;