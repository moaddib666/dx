export class Turn {
    id: string;
    started_at: string;
    duration: number;

    constructor(data: any) {
        this.id = data.id;
        this.started_at = data.started_at;
        this.duration = data.duration;
    }

    timeLeft(): number {
        const startedAt = new Date(this.started_at).getTime();
        const now = new Date().getTime();
        const timePassed = now - startedAt;
        const timePassedSeconds = timePassed / 1000;
        return this.duration - timePassedSeconds;
    }
}