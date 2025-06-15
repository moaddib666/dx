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
            console.log('Initializing WorldEditor...');

            // Load both map data and game objects in parallel
            // Initially load all floors to get a complete view
            const [mapData, gameObjects] = await Promise.all([
                this.loadWorldMap(),
                this.loadGameObjects()
            ]);

            console.log(`Initialization data loaded: ${mapData.positions?.length || 0} positions, ${gameObjects.length || 0} game objects`);

            // Sync state with the loaded data
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
            // Fetch all game objects with no filters to get everything
            const response = await GameMasterApi.gamemasterGameObjectsList();
            console.log('Game objects data:', response.data);

            // Handle both response formats: array directly or object with results property
            if (!response.data) {
                console.warn('Game objects API response is empty');
                this.gameObjects = [];
                return [];
            }

            // Check if response.data is an array or has a results property
            if (Array.isArray(response.data)) {
                this.gameObjects = response.data;
            } else if (response.data.results) {
                this.gameObjects = response.data.results;
            } else {
                console.warn('Game objects API response has unexpected format:', response.data);
                this.gameObjects = [];
                return [];
            }

            console.log(`Loaded ${this.gameObjects.length} game objects`);

            // Log some sample objects to understand their structure
            if (this.gameObjects.length > 0) {
                console.log('Sample game object:', this.gameObjects[0]);

                // Count objects by type for debugging
                const typeCount = {};
                this.gameObjects.forEach(obj => {
                    const type = obj.object_type?.model || 'unknown';
                    typeCount[type] = (typeCount[type] || 0) + 1;
                });
                console.log('Game objects by type:', typeCount);

                // Count objects with positions
                const objectsWithPosition = this.gameObjects.filter(obj =>
                    obj.position || obj.real_instance?.position
                ).length;
                console.log(`Objects with position: ${objectsWithPosition}/${this.gameObjects.length}`);
            }

            return this.gameObjects;
        } catch (error) {
            console.error('Failed to load game objects:', error);
            throw error;
        }
    }

    /**
     * Load world map data from the backend
     * @param {Number} floor - The floor level to load (grid_z value)
     */
    async loadWorldMap(floor = null) {
        try {
            // If floor is provided, use gamemasterWorldMapList with gridZ parameter
            // Otherwise, use gamemasterWorldMapMapRetrieve to get all floors
            let response;
            if (floor !== null) {
                response = await GameMasterApi.gamemasterWorldMapList(floor);
                console.log(`World map data for floor ${floor}:`, response.data);
            } else {
                response = await GameMasterApi.gamemasterWorldMapMapRetrieve();
                console.log('World map data (all floors):', response.data);
            }
            return response.data;
        } catch (error) {
            console.error('Failed to load world map:', error);
            throw error;
        }
    }

    /**
     * Sync internal state with map data from backend
     * @param {Object} mapData - The map data from the backend
     * @param {Number} [floor] - The floor level being loaded, used as default for positions without grid_z
     */
    syncStateWithMapData(mapData, floor = null) {
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

                // Determine the correct grid_z value
                // If we're loading a specific floor and grid_z is missing, use the floor parameter
                // Otherwise, use the grid_z from the position data or the current floor from state
                const defaultGridZ = floor !== null ? floor : this.state.currentFloor;
                const grid_z = positionInfo.grid_z !== undefined ? positionInfo.grid_z : defaultGridZ;

                const room = new WorldEditorRoom({
                    id: positionInfo.id,
                    position: {
                        x: positionInfo.x || 0,
                        y: positionInfo.y || 0,
                        z: positionInfo.z || 0,
                        grid_x: positionInfo.grid_x || 0,
                        grid_y: positionInfo.grid_y || 0,
                        grid_z: grid_z
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
            // First, clear existing connections from rooms
            for (const room of this.state.rooms.values()) {
                room.connections = [];
            }

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
            console.log(`No game objects available for extraction (${entityType})`);
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

        // Log the position ID we're filtering for
        console.log(`Extracting ${entityType} for position: ${positionId}`);

        // Filter and map game objects by position and type
        const filteredObjects = this.gameObjects
            .filter(obj => {
                // Check if the object has a real_instance property
                if (!obj.real_instance) {
                    return false;
                }

                // Get the real instance data
                const realInstance = obj.real_instance;

                // Check if the object has a position property
                if (!realInstance.position && !obj.position) {
                    return false;
                }

                // Check if the object is in this position
                // The position might be in the real_instance or in the main object
                const objPosition = realInstance.position || obj.position;
                const objPositionId = typeof objPosition === 'string' ? objPosition : (objPosition?.id || '');
                if (objPositionId !== positionId) {
                    return false;
                }

                // Get the object type from object_type.model
                const objTypeModel = obj.object_type?.model || '';

                // Categorize the object based on its type
                switch (entityType) {
                    case 'players':
                        return objTypeModel === 'character' && !realInstance.npc;
                    case 'npcs':
                        return objTypeModel === 'character' && realInstance.npc;
                    case 'objects':
                        return objTypeModel === 'worlditem' || objTypeModel === 'item';
                    case 'anomalies':
                        return objTypeModel === 'dimensionanomaly';
                    default:
                        return false;
                }
            })
            .map(obj => {
                // Return the real_instance with additional metadata
                return {
                    ...obj.real_instance,
                    object_type: obj.object_type,
                    original_object: obj
                };
            });

        console.log(`Found ${filteredObjects.length} ${entityType} for position ${positionId}`);

        // Log the first few objects for debugging
        if (filteredObjects.length > 0) {
            console.log(`Sample ${entityType} objects:`, filteredObjects.slice(0, 3));
        }

        return filteredObjects;
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
     * Change current floor and load floor-specific data
     * @param {Number} floor - The floor level to set
     */
    async setFloor(floor) {
        // Update the current floor in state
        this.state.currentFloor = floor;

        try {
            // Load map data specific to this floor
            const mapData = await this.loadWorldMap(floor);

            // Sync state with the floor-specific data, passing the floor parameter
            this.syncStateWithMapData(mapData, floor);

            // Emit events
            console.log(`Floor changed to ${floor}`);
            this.emit('floorChanged', floor);
            this.emit('stateUpdated', this.state);
            // Ugly hack to ensure the map is re-rendered
            // FIXME: it's not a good practice to re initialize as we lose all current state totally and why we develop feature semitransparent upper or down flours room it could become the problem
            await this.initialize();
        } catch (error) {
            console.error(`Failed to load data for floor ${floor}:`, error);
            // Still emit the floor change event even if data loading fails
            this.emit('floorChanged', floor);
            this.emit('stateUpdated', this.state);
        }
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
     * @param {Boolean} loadAllFloors - Whether to load all floors or just the current floor
     */
    async refresh(loadAllFloors = false) {
        try {
            console.log('Refreshing world data...');

            // Load both map data and game objects in parallel
            // If loadAllFloors is true, load all floors, otherwise load only the current floor
            const currentFloor = this.state.currentFloor;
            const [mapData, gameObjects] = await Promise.all([
                loadAllFloors ? this.loadWorldMap() : this.loadWorldMap(currentFloor),
                this.loadGameObjects()
            ]);

            console.log(`Refresh complete: ${mapData.positions?.length || 0} positions, ${gameObjects.length || 0} game objects`);

            // Sync state with the new data, passing the current floor if we're loading floor-specific data
            this.syncStateWithMapData(mapData, loadAllFloors ? null : currentFloor);

            return this.state;
        } catch (error) {
            console.error('Failed to refresh world data:', error);
            throw error;
        }
    }
}

// Export singleton instance
export const worldEditorService = new WorldEditorService();
