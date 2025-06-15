import {GameMasterApi} from '@/api/backendService.js';
import {WorldEditorConnection, WorldEditorRoom, WorldEditorState} from '@/models/WorldEditorModels.js';

/**
 * WorldEditor Service
 * Handles world data management, API interactions, and state synchronization
 */
export class WorldEditorService {
    constructor() {
        this.state = new WorldEditorState();
        this.eventListeners = new Map();
        this.gameObjects = [];
    }

    /**
     * Initialize the WorldEditor with data from the backend
     */
    async initialize() {
        try {
            const [mapData] = await Promise.all([
                this.loadWorldMap(),
                this.loadGameObjects()
            ]);
            this.syncStateWithMapData(mapData);
            this.emit('initialized', this.state);
            return this.state;
        } catch (error) {
            console.error('Failed to initialize WorldEditor:', error);
            throw error;
        }
    }

    /**
     * Load game objects from the backend
     */
    async loadGameObjects() {
        try {
            const response = await GameMasterApi.gamemasterGameObjectsList();
            console.log('Game objects data:', response.data);
            this.gameObjects = response.data.results || [];
            return this.gameObjects;
        } catch (error) {
            console.error('Failed to load game objects:', error);
            throw error;
        }
    }

    /**
     * Load world map data from the backend
     */
    async loadWorldMap() {
        try {
            const response = await GameMasterApi.gamemasterWorldMapMapRetrieve();
            console.log('World map data:', response.data);
            return response.data;
        } catch (error) {
            console.error('Failed to load world map:', error);
            throw error;
        }
    }

    /**
     * Sync internal state with map data from backend
     */
    syncStateWithMapData(mapData) {
        // Clear existing state
        this.state.rooms.clear();
        this.state.connections.clear();

        // Add rooms from map data
        if (mapData.positions) {
            mapData.positions.forEach(positionData => {
                // Handle different position data formats
                // Some APIs return position data directly, others nested under a "position" property
                let positionInfo = positionData.position || positionData;

                // Skip if essential position data is missing
                if (!positionInfo || !positionInfo.id) {
                    console.warn('Invalid position data found:', positionData);
                    return;
                }

                // Parse coordinates string if it exists
                if (positionInfo.coordinates && typeof positionInfo.coordinates === 'string') {
                    const coords = positionInfo.coordinates.split('x').map(Number);
                    if (coords.length === 3) {
                        positionInfo.grid_x = coords[0];
                        positionInfo.grid_y = coords[1];
                        positionInfo.grid_z = coords[2];
                    }
                }

                const room = new WorldEditorRoom({
                    id: positionInfo.id,
                    position: {
                        x: positionInfo.x || 0,
                        y: positionInfo.y || 0,
                        z: positionInfo.z || 1,
                        grid_x: positionInfo.grid_x || 0,
                        grid_y: positionInfo.grid_y || 0,
                        grid_z: positionInfo.grid_z || 1
                    },
                    labels: positionData.labels || [],
                    // Extract entities from position data
                    players: this.extractEntitiesFromPosition(positionData, 'players'),
                    npcs: this.extractEntitiesFromPosition(positionData, 'npcs'),
                    objects: this.extractEntitiesFromPosition(positionData, 'objects'),
                    anomalies: this.extractEntitiesFromPosition(positionData, 'anomalies')
                });
                this.state.addRoom(room);
            });
        }

        // Add connections from map data
        if (mapData.connections) {
            mapData.connections.forEach(connectionData => {
                // Skip if connectionData is invalid
                if (!connectionData || !connectionData.id || !connectionData.position_from || !connectionData.position_to) {
                    console.warn('Invalid connection data found:', connectionData);
                    return;
                }

                const connection = new WorldEditorConnection({
                    id: connectionData.id,
                    fromRoomId: connectionData.position_from,
                    toRoomId: connectionData.position_to,
                    isVertical: connectionData.is_vertical || false,
                    type: connectionData.type || 'normal'
                });
                this.state.addConnection(connection);
            });
        }

        this.emit('stateUpdated', this.state);
    }

    /**
     * Extract entities of a specific type from position data
     */
    extractEntitiesFromPosition(positionData, entityType) {
        if (!this.gameObjects || !this.gameObjects.length) {
            return [];
        }

        // Handle different position data formats
        let positionInfo = positionData.position || positionData;

        // Check if essential position data is missing
        if (!positionInfo || !positionInfo.id) {
            console.warn('Invalid position data in extractEntitiesFromPosition:', positionData);
            return [];
        }

        const positionId = positionInfo.id;

        // Filter game objects by position and type
        return this.gameObjects.filter(obj => {
            // Check if the object is in this position
            if (obj.position !== positionId) {
                return false;
            }

            // Categorize the object based on its type
            switch (entityType) {
                case 'players':
                    return obj.type === 'player' || obj.type === 'character';
                case 'npcs':
                    return obj.type === 'npc';
                case 'objects':
                    return obj.type === 'item' || obj.type === 'object';
                case 'anomalies':
                    return obj.type === 'anomaly';
                default:
                    return false;
            }
        });
    }

    /**
     * Create a new room at the specified coordinates
     */
    async createRoom(gridX, gridY, gridZ = this.state.currentFloor) {
        try {
            const response = await GameMasterApi.gamemasterWorldMapCreate({
                grid_x: gridX,
                grid_y: gridY,
                grid_z: gridZ
            });

            // Validate response data
            if (!response.data || !response.data.position || !response.data.position.id) {
                console.error('Invalid response data from gamemasterWorldMapCreate:', response.data);
                throw new Error('Failed to create room: Invalid response data');
            }

            const newRoom = new WorldEditorRoom({
                id: response.data.position.id,
                position: {
                    grid_x: gridX,
                    grid_y: gridY,
                    grid_z: gridZ
                }
            });

            this.state.addRoom(newRoom);
            this.emit('roomCreated', newRoom);
            this.emit('stateUpdated', this.state);

            return newRoom;
        } catch (error) {
            console.error('Failed to create room:', error);
            throw error;
        }
    }

    /**
     * Delete a room
     */
    async deleteRoom(roomId) {
        try {
            await GameMasterApi.gamemasterWorldMapDestroy(roomId);

            const room = this.state.rooms.get(roomId);
            this.state.removeRoom(roomId);

            this.emit('roomDeleted', {roomId, room});
            this.emit('stateUpdated', this.state);

            return true;
        } catch (error) {
            console.error('Failed to delete room:', error);
            throw error;
        }
    }

    /**
     * Update room properties
     */
    async updateRoom(roomId, updates) {
        try {
            const room = this.state.rooms.get(roomId);
            if (!room) {
                throw new Error(`Room with id ${roomId} not found`);
            }

            // Update room labels if provided
            if (updates.labels) {
                const response = await GameMasterApi.gamemasterWorldMapUpdate(roomId, {
                    labels: updates.labels
                });

                // Validate response data
                if (!response || !response.data) {
                    console.warn('Invalid response from gamemasterWorldMapUpdate:', response);
                    // Continue anyway, using the provided labels
                }

                room.labels = updates.labels;
            }

            // Apply other updates to the room object
            Object.assign(room, updates);

            this.emit('roomUpdated', room);
            this.emit('stateUpdated', this.state);

            return room;
        } catch (error) {
            console.error('Failed to update room:', error);
            throw error;
        }
    }

    /**
     * Move room to new coordinates
     */
    async moveRoom(roomId, newGridX, newGridY, newGridZ) {
        try {
            // This would need a backend API endpoint for moving rooms
            // For now, we'll update the local state
            const room = this.state.rooms.get(roomId);
            if (!room) {
                throw new Error(`Room with id ${roomId} not found`);
            }

            const oldPosition = {...room.position};
            room.position.grid_x = newGridX;
            room.position.grid_y = newGridY;
            room.position.grid_z = newGridZ;

            this.emit('roomMoved', {room, oldPosition, newPosition: room.position});
            this.emit('stateUpdated', this.state);

            return room;
        } catch (error) {
            console.error('Failed to move room:', error);
            throw error;
        }
    }

    /**
     * Create connection between two rooms
     */
    async createConnection(fromRoomId, toRoomId, isVertical = false) {
        try {
            // This would need a backend API endpoint for creating connections
            // For now, we'll create a local connection
            const connectionId = `conn_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

            const connection = new WorldEditorConnection({
                id: connectionId,
                fromRoomId,
                toRoomId,
                isVertical
            });

            this.state.addConnection(connection);

            this.emit('connectionCreated', connection);
            this.emit('stateUpdated', this.state);

            return connection;
        } catch (error) {
            console.error('Failed to create connection:', error);
            throw error;
        }
    }

    /**
     * Delete connection
     */
    async deleteConnection(connectionId) {
        try {
            const connection = this.state.connections.get(connectionId);
            this.state.removeConnection(connectionId);

            this.emit('connectionDeleted', {connectionId, connection});
            this.emit('stateUpdated', this.state);

            return true;
        } catch (error) {
            console.error('Failed to delete connection:', error);
            throw error;
        }
    }

    /**
     * Spawn item in room
     */
    async spawnItem(roomId, itemData) {
        try {
            // This would integrate with ItemsApi
            const room = this.state.rooms.get(roomId);
            if (!room) {
                throw new Error(`Room with id ${roomId} not found`);
            }

            // Add item to room's objects array
            room.objects.push(itemData);

            this.emit('itemSpawned', {roomId, itemData});
            this.emit('stateUpdated', this.state);

            return itemData;
        } catch (error) {
            console.error('Failed to spawn item:', error);
            throw error;
        }
    }

    /**
     * Spawn NPC in room
     */
    async spawnNPC(roomId, npcData) {
        try {
            // This would integrate with CharacterApi for NPCs
            const room = this.state.rooms.get(roomId);
            if (!room) {
                throw new Error(`Room with id ${roomId} not found`);
            }

            // Add NPC to room's npcs array
            room.npcs.push(npcData);

            this.emit('npcSpawned', {roomId, npcData});
            this.emit('stateUpdated', this.state);

            return npcData;
        } catch (error) {
            console.error('Failed to spawn NPC:', error);
            throw error;
        }
    }

    /**
     * Spawn anomaly in room
     */
    async spawnAnomaly(roomId, anomalyData) {
        try {
            const room = this.state.rooms.get(roomId);
            if (!room) {
                throw new Error(`Room with id ${roomId} not found`);
            }

            // Add anomaly to room's anomalies array
            room.anomalies.push(anomalyData);

            this.emit('anomalySpawned', {roomId, anomalyData});
            this.emit('stateUpdated', this.state);

            return anomalyData;
        } catch (error) {
            console.error('Failed to spawn anomaly:', error);
            throw error;
        }
    }

    /**
     * Toggle editor mode
     */
    toggleMode() {
        this.state.toggleMode();
        this.emit('modeChanged', this.state.mode);
        this.emit('stateUpdated', this.state);
    }

    /**
     * Set active tool
     */
    setTool(tool) {
        this.state.setTool(tool);
        this.emit('toolChanged', tool);
        this.emit('stateUpdated', this.state);
    }

    /**
     * Toggle layer visibility
     */
    toggleLayer(layer) {
        this.state.toggleLayer(layer);
        this.emit('layerToggled', {layer, active: this.state.isLayerActive(layer)});
        this.emit('stateUpdated', this.state);
    }

    /**
     * Change current floor
     */
    setFloor(floor) {
        this.state.currentFloor = floor;
        this.emit('floorChanged', floor);
        this.emit('stateUpdated', this.state);
    }

    /**
     * Select/deselect room
     */
    toggleRoomSelection(roomId) {
        this.state.toggleRoomSelection(roomId);
        this.emit('selectionChanged', Array.from(this.state.selectedRooms));
        this.emit('stateUpdated', this.state);
    }

    /**
     * Clear room selection
     */
    clearSelection() {
        this.state.clearSelection();
        this.emit('selectionChanged', []);
        this.emit('stateUpdated', this.state);
    }

    /**
     * Get current state
     */
    getState() {
        return this.state;
    }

    /**
     * Event system for components to listen to changes
     */
    on(event, callback) {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event).push(callback);
    }

    /**
     * Remove event listener
     */
    off(event, callback) {
        if (this.eventListeners.has(event)) {
            const listeners = this.eventListeners.get(event);
            const index = listeners.indexOf(callback);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        }
    }

    /**
     * Emit event to listeners
     */
    emit(event, data) {
        if (this.eventListeners.has(event)) {
            this.eventListeners.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in event listener for ${event}:`, error);
                }
            });
        }
    }

    /**
     * Refresh data from backend
     */
    async refresh() {
        try {
            const [mapData] = await Promise.all([
                this.loadWorldMap(),
                this.loadGameObjects()
            ]);
            this.syncStateWithMapData(mapData);
            return this.state;
        } catch (error) {
            console.error('Failed to refresh world data:', error);
            throw error;
        }
    }
}

// Export singleton instance
export const worldEditorService = new WorldEditorService();
