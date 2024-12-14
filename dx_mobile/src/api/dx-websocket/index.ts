import {Centrifuge} from "centrifuge";
import {SubscriptionResolver} from "./router";


export class DxSocketClient {
    protected centrifuge: Centrifuge | null = null;
    private router: SubscriptionResolver;

    constructor() {
        this.router = new SubscriptionResolver();
    }

    connect(url: string): void {
        console.debug("Connecting to WebSocket server:", url)
        this.centrifuge = new Centrifuge(url, {});

        this.centrifuge.on('connected', this.OnSocketConnected.bind(this));
        this.centrifuge.on('disconnected', this.OnSocketClose.bind(this));
        this.centrifuge.on('error', this.OnSocketError.bind(this));
        this.centrifuge.on('subscribed', this.OnSubscribed.bind(this));
        this.centrifuge.on('subscribing', this.OnSubscribing.bind(this));
        this.centrifuge.on('unsubscribed', this.OnUnsubscribed.bind(this));
        this.centrifuge.on('publication', this.OnPublication.bind(this));

        this.centrifuge.connect();
    }

    sendMessage(message: any): void {
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
    }

    OnSocketClose(): void {
        console.debug('WebSocket connection closed');
    }

    OnSocketError(error: Event): void {
        console.error('WebSocket error:', error);
    }

    OnSubscribed(ctx: any): void {
        console.debug('Subscribed to server-side channel:', ctx.channel);
        this.router.addSubscription(ctx.channel);
        // if (ctx.channel.startsWith("player_actions")) {
            // Request Refresh Player Info
            // const event: GameEvent = {
            //     name: "refresh",
            //     timestamp: Date.now(),
            //     id: uuidv4(),
            //     category: EventCategory.PLAYER,
            // };
            // this.sendMessage(event);
        // }
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
        const event = JSON.parse(ctx.data);
        console.debug("Emitting event:", {event});
    }
}

