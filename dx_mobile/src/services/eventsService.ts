import {DefaultGameBus} from "../api";
import {WEBSOCKET_BASE_URL} from "@env";

const connectBus = async () => {
    return DefaultGameBus.connect(WEBSOCKET_BASE_URL);
}

export default connectBus;

