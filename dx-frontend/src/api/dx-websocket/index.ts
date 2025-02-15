import {Centrifuge} from "centrifuge";
import {EventCategory, GameEvent} from "./events";
import {SubscriptionResolver} from "./router";
import {v4 as uuidv4} from "uuid";
import {EventBus} from "./emmiter";
import mitt from "mitt";

export const eventbus = mitt()

class DxSocketClient {
    protected centrifuge: Centrifuge | null = null;
    private eventBus: EventBus;
    private router: SubscriptionResolver;
    private connected: boolean;

    constructor(eventBus: EventBus) {
        this.eventBus = eventBus;
        this.router = new SubscriptionResolver();
        this.connected = false
    }

    connect(url: string): void {
        if (this.connected) {
            console.warn('Already connected to WebSocket');
            return;
        }
        this.centrifuge = new Centrifuge(url, {});

        this.centrifuge.on('connected', this.OnSocketConnected.bind(this));
        this.centrifuge.on('disconnected', this.OnSocketClose.bind(this));
        this.centrifuge.on('error', this.OnSocketError.bind(this));
        this.centrifuge.on('subscribed', this.OnSubscribed.bind(this));
        this.centrifuge.on('subscribing', this.OnSubscribing.bind(this));
        this.centrifuge.on('unsubscribed', this.OnUnsubscribed.bind(this));
        this.centrifuge.on('publication', this.OnPublication.bind(this));
        this.centrifuge.connect();
        this.connected = true;
    }

    sendMessage(message: GameEvent): void {
        const channel = this.router.getSubscriptionForEvent(message);
        const serializedMessage = JSON.stringify(message);
        this.centrifuge.publish(channel, serializedMessage)
            .then(() => {
                console.log(`Message sent to channel: ${channel}`, serializedMessage);
            })
            .catch((error) => {
                console.error(`Failed to send message to channel: ${channel}`, error);
            });
    }

    OnSocketConnected(): void {
        console.debug('WebSocket connection established');
        this.eventBus.emit('ws-connected');
    }

    OnSocketClose(): void {
        console.debug('WebSocket connection closed');
        this.eventBus.emit('ws-disconnected');
    }

    OnSocketError(error: Event): void {
        console.error('WebSocket error:', error);
        this.eventBus.emit('ws-error', {});
    }

    OnSubscribed(ctx: any): void {
        console.debug('Subscribed to server-side channel:', ctx.channel);
        this.router.addSubscription(ctx.channel);
        if (ctx.channel.startsWith("player_actions")) {
            // Request Refresh Player Info
            const event: GameEvent = {
                name: "refresh",
                timestamp: Date.now(),
                id: uuidv4(),
                category: EventCategory.PLAYER,
            };
            this.sendMessage(event);
        }
    }

    OnSubscribing(ctx: any): void {
        console.debug('Subscribing to server-side channel:', ctx.channel);
    }

    OnUnsubscribed(ctx: any): void {
        console.debug('Unsubscribed from server-side channel:', ctx.channel);
        this.router.removeSubscription(ctx.channel);
    }

    OnPublication(ctx: any): void {
        console.debug('Publication received from server-side channel:', ctx.channel, ctx.data, typeof ctx.data);
        const event: GamepadEvent = JSON.parse(ctx.data);
        console.debug("Emitting event:", event.category + "::" + event.name, event.data);
        this.eventBus.emit(event.category + "::" + event.name, event.data);
    }
}


export const GameEventsClient = new DxSocketClient(eventbus);
export const ensureConnection = () => {
    GameEventsClient.connect(import.meta.env.VITE_WS_BASE_URL as string)
    return eventbus
}