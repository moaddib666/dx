import {EventCategory, GameEvent} from "./events";

export class SubscriptionResolver {
    private subscriptions: Set<string>;
    constructor() {
        this.subscriptions = new Set();
    }

    public addSubscription(channel: string): void {
        if (!this.subscriptions.has(channel)) {
            this.subscriptions.add(channel);
            console.log(`Subscribed to channel: ${channel}`);
        }
    }

    public removeSubscription(channel: string): void {
        if (this.subscriptions.has(channel)) {
            this.subscriptions.delete(channel);
            console.log(`Unsubscribed from channel: ${channel}`);
        }
    }

    public getSubscriptionForEvent(event: GameEvent): string | null {
        switch (event.category) {
            default:
                // player_actions::{player_id}
                console.debug("Current subscriptions: ", this.subscriptions);
                for (const subscription of this.subscriptions) {
                    console.debug(`Checking subscription: ${subscription}`);
                    if (subscription.startsWith("player_actions")) {
                        console.debug(`Found subscription: ${subscription}`);
                        return subscription;
                    }
                }
                return null; // Return null if no matching subscription is found
        }
    }
}
