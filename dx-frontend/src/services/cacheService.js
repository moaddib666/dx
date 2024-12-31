class CacheService {
    constructor(name) {
        this.cache = localStorage;
        this.chains = {};        // Stores the chain of promises per key
        this.releaseFns = {};    // Stores release functions per key
        this.name = name;
    }

    formatKey(key) {
        return `dx:${this.name}:${key}`;
    }

    createChainLink(key) {
        let releaseFn;
        const newLink = new Promise((resolve) => {
            releaseFn = resolve;
        });
        // If there's no existing chain, start with a resolved promise
        if (!this.chains[key]) {
            this.chains[key] = Promise.resolve();
        }
        // Link this new promise after the existing chain
        const prevLink = this.chains[key];
        this.chains[key] = prevLink.then(() => newLink);
        // Return the release function and the previous link for waiting
        return {releaseFn, prevLink};
    }

    async acquire(key) {
        console.debug(`Acquiring lock for ${key}...`);
        const {releaseFn, prevLink} = this.createChainLink(key);
        // Wait for all previous operations on this key to finish
        await prevLink;

        // We now "hold" the lock until release is called
        this.releaseFns[key] = releaseFn;

        const data = this.getInternally(key);
        console.debug(`Data for ${key}: ${data}`);
        return data;
    }

    async release(key) {
        if (!this.releaseFns[key]) {
            throw new Error(`Key ${key} is not locked.`);
        }
        console.debug(`Releasing lock on ${key}`);
        // Resolve the promise to let the next request proceed
        this.releaseFns[key]();
        delete this.releaseFns[key];
    }

    set(key, data) {
        if (!this.releaseFns[key]) {
            throw new Error(`Trying to set ${key} without acquiring it first.`);
        }
        this.setInternally(key, data);
    }

    setInternally(key, data) {
        console.debug(`Setting ${JSON.stringify(data)} for ${this.formatKey(key)} in cache`);
        this.cache.setItem(this.formatKey(key), JSON.stringify(data));
    }

    getInternally(key) {
        const dataString = this.cache.getItem(this.formatKey(key));
        return dataString ? JSON.parse(dataString) : null;
    }
}

export {CacheService};
