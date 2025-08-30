// WorldEditor Data Models
// Based on requirements from WorldEditor.MD

import { Position as ApiPosition } from '@/api/dx-backend';

/**
 * Enum for WorldEditor modes
 */
export const WorldEditorMode = {
    VIEW: 'view',
    EDIT: 'edit'
} as const;

export type WorldEditorModeType = typeof WorldEditorMode[keyof typeof WorldEditorMode];

/**
 * Enum for WorldEditor tools (used in edit mode)
 */
export const WorldEditorTool = {
    SELECT: 'select',
    CREATE_ROOM: 'create_room',
    DELETE_ROOM: 'delete_room',
    MOVE_ROOM: 'move_room',
    CONNECT_ROOMS: 'connect_rooms',
    DISCONNECT_ROOMS: 'disconnect_rooms',
    SPAWN_ITEM: 'spawn_item',
    EDIT_ITEM: 'edit_item',
    SPAWN_NPC: 'spawn_npc',
    EDIT_NPC: 'edit_npc',
    SPAWN_ANOMALY: 'spawn_anomaly',
    EDIT_ANOMALY: 'edit_anomaly'
} as const;

export type WorldEditorToolType = typeof WorldEditorTool[keyof typeof WorldEditorTool];

/**
 * Enum for WorldEditor layers
 */
export const WorldEditorLayer = {
    PLAYERS: 'players',
    NPCS: 'npcs',
    OBJECTS: 'objects',
    ANOMALIES: 'anomalies',
    TBD: 'tbd'
} as const;

export type WorldEditorLayerType = typeof WorldEditorLayer[keyof typeof WorldEditorLayer];

/**
 * Position interface for room coordinates
 * Extends API Position with additional WorldEditor-specific properties
 */
export interface Position extends Omit<ApiPosition, 'id' | 'sub_location' | 'sub_location_details' | 'labels' | 'is_safe' | 'image' | 'coordinates'> {
    x?: number;
    y?: number;
    z?: number;
    grid_x: number;
    grid_y: number;
    grid_z: number;
}

/**
 * Entity interface for room entities (players, NPCs, objects, anomalies)
 */
export interface Entity {
    id: string;
    [key: string]: any;
}

/**
 * Room data interface for constructor
 */
export interface WorldEditorRoomData {
    id?: string | null;
    position?: Partial<Position>;
    type?: string;
    labels?: string[];
    icons?: string[];
    players?: Entity[];
    npcs?: Entity[];
    objects?: Entity[];
    anomalies?: Entity[];
    connections?: WorldEditorConnection[];
    metadata?: Record<string, any>;
}

/**
 * Connection data interface for constructor
 */
export interface WorldEditorConnectionData {
    id?: string | null;
    fromRoomId?: string | null;
    toRoomId?: string | null;
    position_from?: string | null;
    position_to?: string | null;
    isVertical?: boolean;
    is_vertical?: boolean;
    type?: string;
    metadata?: Record<string, any>;
}

/**
 * Room data structure for WorldEditor
 */
export class WorldEditorRoom {
    public id: string | null;
    public position: Position;
    public type: string;
    public labels: string[];
    public icons: string[];
    public players: Entity[];
    public npcs: Entity[];
    public objects: Entity[];
    public anomalies: Entity[];
    public connections: WorldEditorConnection[];
    public metadata: Record<string, any>;

    constructor(data: WorldEditorRoomData = {}) {
        this.id = data.id || null;
        this.position = {
            x: data.position?.x || 0,
            y: data.position?.y || 0,
            z: data.position?.z || 0,
            grid_x: data.position?.grid_x || 0,
            grid_y: data.position?.grid_y || 0,
            grid_z: data.position?.grid_z || 0
        };
        this.type = data.type || 'default';
        this.labels = data.labels || [];
        this.icons = data.icons || [];
        this.players = data.players || [];
        this.npcs = data.npcs || [];
        this.objects = data.objects || [];
        this.anomalies = data.anomalies || [];
        this.connections = data.connections || [];
        this.metadata = data.metadata || {};
    }

    /**
     * Get room display name
     */
    getDisplayName(): string {
        if (this.labels && this.labels.length > 0) {
            return this.labels[this.labels.length - 1];
        }
        return `Room (${this.position.grid_x}, ${this.position.grid_y})`;
    }

    /**
     * Check if room has entities of a specific layer type
     */
    hasLayerEntities(layer: WorldEditorLayerType): boolean {
        switch (layer) {
            case WorldEditorLayer.PLAYERS:
                return this.players.length > 0;
            case WorldEditorLayer.NPCS:
                return this.npcs.length > 0;
            case WorldEditorLayer.OBJECTS:
                return this.objects.length > 0;
            case WorldEditorLayer.ANOMALIES:
                return this.anomalies.length > 0;
            default:
                return false;
        }
    }
}

/**
 * Connection data structure for WorldEditor
 */
export class WorldEditorConnection {
    public id: string | null;
    public fromRoomId: string | null;
    public toRoomId: string | null;
    public isVertical: boolean;
    public type: string;
    public metadata: Record<string, any>;

    constructor(data: WorldEditorConnectionData = {}) {
        this.id = data.id || null;
        this.fromRoomId = data.fromRoomId || data.position_from || null;
        this.toRoomId = data.toRoomId || data.position_to || null;
        this.isVertical = data.isVertical || data.is_vertical || false;
        this.type = data.type || 'normal';
        this.metadata = data.metadata || {};
    }
}

/**
 * History entry interface for undo/redo functionality
 */
export interface HistoryEntry {
    action: string;
    data: any;
    timestamp: number;
}

/**
 * WorldEditor state management class
 */
export class WorldEditorState {
    public mode: WorldEditorModeType;
    public selectedTool: WorldEditorToolType;
    public activeLayers: Set<WorldEditorLayerType>;
    public selectedRooms: Set<string>;
    public currentFloor: number;
    public rooms: Map<string, WorldEditorRoom>;
    public connections: Map<string, WorldEditorConnection>;
    public clipboard: any;
    public history: HistoryEntry[];
    public historyIndex: number;

    constructor() {
        this.mode = WorldEditorMode.VIEW;
        this.selectedTool = WorldEditorTool.SELECT;
        this.activeLayers = new Set([
            WorldEditorLayer.PLAYERS,
            WorldEditorLayer.NPCS,
            WorldEditorLayer.OBJECTS,
            WorldEditorLayer.ANOMALIES
        ]);
        this.selectedRooms = new Set();
        this.currentFloor = 1;
        this.rooms = new Map(); // roomId -> WorldEditorRoom
        this.connections = new Map(); // connectionId -> WorldEditorConnection
        this.clipboard = null;
        this.history = [];
        this.historyIndex = -1;
    }

    /**
     * Toggle editor mode
     */
    toggleMode(): void {
        this.mode = this.mode === WorldEditorMode.VIEW ? WorldEditorMode.EDIT : WorldEditorMode.VIEW;
        if (this.mode === WorldEditorMode.VIEW) {
            this.selectedTool = WorldEditorTool.SELECT;
            this.selectedRooms.clear();
        }
    }

    /**
     * Set active tool
     */
    setTool(tool: WorldEditorToolType): void {
        if (this.mode === WorldEditorMode.EDIT) {
            this.selectedTool = tool;
        }
    }

    /**
     * Toggle layer visibility
     */
    toggleLayer(layer: WorldEditorLayerType): void {
        if (this.activeLayers.has(layer)) {
            this.activeLayers.delete(layer);
        } else {
            this.activeLayers.add(layer);
        }
    }

    /**
     * Check if layer is active
     */
    isLayerActive(layer: WorldEditorLayerType): boolean {
        return this.activeLayers.has(layer);
    }

    /**
     * Select/deselect room
     */
    toggleRoomSelection(roomId: string): void {
        if (this.selectedRooms.has(roomId)) {
            this.selectedRooms.delete(roomId);
        } else {
            this.selectedRooms.add(roomId);
        }
    }

    /**
     * Clear room selection
     */
    clearSelection(): void {
        this.selectedRooms.clear();
    }

    /**
     * Get rooms for current floor
     */
    getRoomsForFloor(floor: number = this.currentFloor): WorldEditorRoom[] {
        return Array.from(this.rooms.values()).filter(room => room.position.grid_z === floor);
    }

    /**
     * Get connections for current floor
     */
    getConnectionsForFloor(floor: number = this.currentFloor): WorldEditorConnection[] {
        return Array.from(this.connections.values()).filter(connection => {
            const fromRoom = this.rooms.get(connection.fromRoomId!);
            const toRoom = this.rooms.get(connection.toRoomId!);
            return fromRoom && toRoom &&
                fromRoom.position.grid_z === floor &&
                toRoom.position.grid_z === floor &&
                !connection.isVertical;
        });
    }

    /**
     * Add room to state
     */
    addRoom(room: WorldEditorRoom | WorldEditorRoomData): void {
        if (!(room instanceof WorldEditorRoom)) {
            room = new WorldEditorRoom(room);
        }
        this.rooms.set(room.id!, room);
    }

    /**
     * Remove room from state
     */
    removeRoom(roomId: string): void {
        this.rooms.delete(roomId);
        this.selectedRooms.delete(roomId);
        // Remove connections involving this room
        for (const [connId, connection] of this.connections.entries()) {
            if (connection.fromRoomId === roomId || connection.toRoomId === roomId) {
                this.connections.delete(connId);
            }
        }
    }

    /**
     * Add connection to state
     */
    addConnection(connection: WorldEditorConnection | WorldEditorConnectionData): void {
        if (!(connection instanceof WorldEditorConnection)) {
            connection = new WorldEditorConnection(connection);
        }
        this.connections.set(connection.id!, connection);

        // Add connection to the source and target rooms' connections arrays
        const sourceRoom = this.rooms.get(connection.fromRoomId!);
        const targetRoom = this.rooms.get(connection.toRoomId!);

        if (sourceRoom) {
            // Check if connection already exists in the array
            if (!sourceRoom.connections.some(conn => conn.id === connection.id)) {
                sourceRoom.connections.push(connection);
            }
        }

        if (targetRoom) {
            // Check if connection already exists in the array
            if (!targetRoom.connections.some(conn => conn.id === connection.id)) {
                targetRoom.connections.push(connection);
            }
        }
    }

    /**
     * Remove connection from state
     */
    removeConnection(connectionId: string): void {
        const connection = this.connections.get(connectionId);
        if (connection) {
            // Remove connection from the source and target rooms' connections arrays
            const sourceRoom = this.rooms.get(connection.fromRoomId!);
            const targetRoom = this.rooms.get(connection.toRoomId!);

            if (sourceRoom) {
                sourceRoom.connections = sourceRoom.connections.filter(conn => conn.id !== connectionId);
            }

            if (targetRoom) {
                targetRoom.connections = targetRoom.connections.filter(conn => conn.id !== connectionId);
            }
        }

        this.connections.delete(connectionId);
    }
}

/**
 * Room colors configuration interface
 */
export interface RoomColorsConfig {
    default: string;
    selected: string;
    current: string;
}

/**
 * Connection colors configuration interface
 */
export interface ConnectionColorsConfig {
    normal: string;
    vertical: string;
}

/**
 * Layer colors configuration interface
 */
export interface LayerColorsConfig {
    [WorldEditorLayer.PLAYERS]: string;
    [WorldEditorLayer.NPCS]: string;
    [WorldEditorLayer.OBJECTS]: string;
    [WorldEditorLayer.ANOMALIES]: string;
    [WorldEditorLayer.TBD]: string;
}

/**
 * WorldEditor configuration interface
 */
export interface WorldEditorConfigType {
    cellSize: number;
    cellPadding: number;
    gridColor: string;
    roomColors: RoomColorsConfig;
    connectionColors: ConnectionColorsConfig;
    layerColors: LayerColorsConfig;
}

/**
 * WorldEditor configuration
 */
export const WorldEditorConfig: WorldEditorConfigType = {
    cellSize: 80,
    cellPadding: 35,
    gridColor: '#aaa',
    roomColors: {
        default: '#444',
        selected: '#1E90FF',
        current: '#1E90FF'
    },
    connectionColors: {
        normal: 'red',
        vertical: 'blue'
    },
    layerColors: {
        [WorldEditorLayer.PLAYERS]: '#00ff00',
        [WorldEditorLayer.NPCS]: '#ffff00',
        [WorldEditorLayer.OBJECTS]: '#ff8800',
        [WorldEditorLayer.ANOMALIES]: '#ff0088',
        [WorldEditorLayer.TBD]: '#888888'
    }
};