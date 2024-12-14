
interface Cost {
    kind: string;
    value: number;
}

interface Target {
    id: string;
    name: string;
}


class Action {
    id: string;
    name: string;
    cost: Cost[];
    target: Target;
    actionType: string;
    constructor(id: string, name: string, cost: Cost[], target: Target, actionType: string)
    {
        this.id = id;
        this.name = name;
        this.cost = cost;
        this.target = target;
        this.actionType = actionType;
    }

    toString() {
        return `Action: ${this.name}\nCost: ${this.cost.map(c => `${c.value} ${c.kind}`).join(', ')}\nTarget: ${this.target.name}`;
    }

    getName(): string {
        return this.name;
    }

    getActionPointsCost(): number {
        const apCost = this.cost.find(c => c.kind === 'Action Points');
        return apCost ? apCost.value : 0;
    }

    getEnergyCost(): number {
        const energyCost = this.cost.find(c => c.kind === 'Energy');
        return energyCost ? energyCost.value : 0;
    }

    getTargetName(): string {
        return this.target.name;
    }

    getTargetId(): string {
        return this.target.id;
    }

    getActionId(): string {
        return this.id;
    }
}

export default Action;