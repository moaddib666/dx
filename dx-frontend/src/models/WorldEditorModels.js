// WorldEditor Data Models
// Based on requirements from WorldEditor.MD

/**
 * Enum for WorldEditor modes
 */
export const WorldEditorMode = {
    VIEW: 'view',
    EDIT: 'edit'
};

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
};

/**
 * Enum for WorldEditor layers
 */
export const WorldEditorLayer = {
    PLAYERS: 'players',
    NPCS: 'npcs',
    OBJECTS: 'objects',
    ANOMALIES: 'anomalies',
    TBD: 'tbd'
};

/**
 * Room data structure for WorldEditor
 */
export class WorldEditorRoom {
    constructor(data = {}) {
        this.id = data.id || null;
        this.position = {
            x: data.position?.x || 0,
            y: data.position?.y || 0,
            z: data.position?.z || 1,
            grid_x: data.position?.grid_x || 0,
            grid_y: data.position?.grid_y || 0,
            grid_z: data.position?.grid_z || 1
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
    getDisplayName() {
        if (this.labels && this.labels.length > 0) {
            return this.labels[this.labels.length - 1];
        }
        return `Room (${this.position.grid_x}, ${this.position.grid_y})`;
    }

    /**
     * Check if room has entities of a specific layer type
     */
    hasLayerEntities(layer) {
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
    constructor(data = {}) {
        this.id = data.id || null;
        this.fromRoomId = data.fromRoomId || data.position_from || null;
        this.toRoomId = data.toRoomId || data.position_to || null;
        this.isVertical = data.isVertical || data.is_vertical || false;
        this.type = data.type || 'normal';
        this.metadata = data.metadata || {};
    }
}

/**
 * WorldEditor state management class
 */
export class WorldEditorState {
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
    toggleMode() {
        this.mode = this.mode === WorldEditorMode.VIEW ? WorldEditorMode.EDIT : WorldEditorMode.VIEW;
        if (this.mode === WorldEditorMode.VIEW) {
            this.selectedTool = WorldEditorTool.SELECT;
            this.selectedRooms.clear();
        }
    }

    /**
     * Set active tool
     */
    setTool(tool) {
        if (this.mode === WorldEditorMode.EDIT) {
            this.selectedTool = tool;
        }
    }

    /**
     * Toggle layer visibility
     */
    toggleLayer(layer) {
        if (this.activeLayers.has(layer)) {
            this.activeLayers.delete(layer);
        } else {
            this.activeLayers.add(layer);
        }
    }

    /**
     * Check if layer is active
     */
    isLayerActive(layer) {
        return this.activeLayers.has(layer);
    }

    /**
     * Select/deselect room
     */
    toggleRoomSelection(roomId) {
        if (this.selectedRooms.has(roomId)) {
            this.selectedRooms.delete(roomId);
        } else {
            this.selectedRooms.add(roomId);
        }
    }

    /**
     * Clear room selection
     */
    clearSelection() {
        this.selectedRooms.clear();
    }

    /**
     * Get rooms for current floor
     */
    getRoomsForFloor(floor = this.currentFloor) {
        return Array.from(this.rooms.values()).filter(room => room.position.grid_z === floor);
    }

    /**
     * Get connections for current floor
     */
    getConnectionsForFloor(floor = this.currentFloor) {
        return Array.from(this.connections.values()).filter(connection => {
            const fromRoom = this.rooms.get(connection.fromRoomId);
            const toRoom = this.rooms.get(connection.toRoomId);
            return fromRoom && toRoom &&
                fromRoom.position.grid_z === floor &&
                toRoom.position.grid_z === floor &&
                !connection.isVertical;
        });
    }

    /**
     * Add room to state
     */
    addRoom(room) {
        if (!(room instanceof WorldEditorRoom)) {
            room = new WorldEditorRoom(room);
        }
        this.rooms.set(room.id, room);
    }

    /**
     * Remove room from state
     */
    removeRoom(roomId) {
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
    addConnection(connection) {
        if (!(connection instanceof WorldEditorConnection)) {
            connection = new WorldEditorConnection(connection);
        }
        this.connections.set(connection.id, connection);
    }

    /**
     * Remove connection from state
     */
    removeConnection(connectionId) {
        this.connections.delete(connectionId);
    }
}

/**
 * WorldEditor configuration
 */
export const WorldEditorConfig = {
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