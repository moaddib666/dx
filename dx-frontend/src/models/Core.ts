
export enum ImpactType {
    PHYSICAL = "Physical",
    MENTAL = "Mental",
    ENERGY = "Energy",
    HEAT = "Heat",
    COLD = "Cold",
    LIGHT = "Light",
    DARKNESS = "Darkness"
}

export enum LifePath {
    PATH_OF_TECH = "Tech",
    PATH_OF_MAGIC = "Magic"
}

export enum PlayerStat {
    PHYSICAL_STRENGTH = "Physical Strength",
    MENTAL_STRENGTH = "Mental Strength",
    LUCK = "Luck",
    SPEED = "Speed",
    CONCENTRATION = "Concentration",
    FLOW_MANIPULATION = "Flow Manipulation",
    FLOW_CONNECTION = "Flow Connection",
    KNOWLEDGE = "Knowledge",
    FLOW_RESONANCE = "Flow Resonance"
}

export enum AttributeType {
    HEALTH = "Health",
    ENERGY = "Energy",
    ACTION_POINTS = "Action Points"
}

interface Attribute {
    name: AttributeType;
    current: number;
    max: number;
}

interface attributes {
    health: number;
    max_health: number;
    energy: number;
    max_energy: number;
    ap: number;
    max_ap: number;
}

interface Location {
    id: string;
    name: string;
}

interface Dimension {
    number: number;
    speed: number;
    energy: number;
}

interface Rank {
    name: string;
    experience: number;
    grade: number;
    next_rank_experience: number;
}