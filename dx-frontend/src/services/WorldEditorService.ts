import {GameMasterApi, GMWorldGenericSpawnersApi, GMWorldNPCSpawnersApi} from '@/api/backendService';
import {WorldEditorConnection, WorldEditorRoom, WorldEditorState} from '@/models/WorldEditorModels';
import {AxiosResponse} from 'axios';
import {
    WorldPosition,
    PositionConnection,
    PositionConnectionCreateRequest,
    GameObject as ApiGameObject,
    GenericSpawner,
    NPCSpawnerCreateRequest
} from '@/api/dx-backend';

/**
 * Event types for the WorldEditorService
 */
type WorldEditorServiceEventType =
  | 'initialized'
  | 'stateUpdated'
  | 'roomCreated'
  | 'roomDeleted'
  | 'roomUpdated'
  | 'roomMoved'
  | 'connectionCreated'
  | 'connectionDeleted'
  | 'connectionUpdated'
  | 'itemSpawned'
  | 'npcSpawned'
  | 'anomalySpawned'
  | 'spawnerCreated'
  | 'spawnerDeleted'
  | 'spawnerUpdated'
  | 'modeChanged'
  | 'toolChanged'
  | 'layerToggled'
  | 'floorChanged'
  | 'floorChangeFailed'
  | 'selectionChanged'
  | 'refreshed'
  | 'refreshFailed'
  | 'reset';

/**
 * Event callback function type
 */
type EventCallback = (data?: any) => void;

// Using WorldPosition from dx-backend API instead of custom PositionData interface

// Using PositionConnection from dx-backend API instead of custom ConnectionData interface

/**
 * Map data interface from API
 */
interface MapData {
  positions?: WorldPosition[];
  connections?: PositionConnection[];
}

// Using ApiGameObject from dx-backend API instead of custom GameObject interface

/**
 * Room creation data interface
 */
interface RoomCreationData {
  grid_x: number;
  grid_y: number;
  grid_z: number;
  sub_location?: string;
}

/**
 * Room update data interface
 */
interface RoomUpdateData {
  labels?: string[];
  [key: string]: any;
}

// Using PositionConnectionCreateRequest from dx-backend API instead of custom ConnectionCreationRequest interface

/**
 * Entity data interface for spawning
 */
interface EntityData {
  id?: string;
  [key: string]: any;
}

/**
 * Floor change failed event data interface
 */
interface FloorChangeFailedData {
  targetFloor: number;
  currentFloor: number;
  error: Error;
}

/**
 * Room moved event data interface
 */
interface RoomMovedData {
  room: WorldEditorRoom;
  oldPosition: { grid_x: number; grid_y: number; grid_z: number };
  newPosition: { grid_x: number; grid_y: number; grid_z: number };
}

/**
 * Room/Connection deleted event data interface
 */
interface DeletedEventData {
  roomId?: string;
  connectionId?: string;
  room?: WorldEditorRoom;
  connection?: WorldEditorConnection;
}

/**
 * Spawn event data interface
 */
interface SpawnEventData {
  roomId: string;
  itemData?: EntityData;
  npcData?: EntityData;
  anomalyData?: EntityData;
}

/**
 * Layer toggled event data interface
 */
interface LayerToggledData {
  layer: string;
  active: boolean;
}

/**
 * WorldEditor Service
 * Handles world data management, API interactions, and state synchronization
 */
export class WorldEditorService {
    private state: WorldEditorState;
    private eventListeners: Map<WorldEditorServiceEventType, EventCallback[]>;
    private gameObjects: ApiGameObject[];
    private spawners: GenericSpawner[];
    private isInitialized: boolean;

    constructor() {
        this.state = new WorldEditorState();
        this.eventListeners = new Map();
        this.gameObjects = [];
        this.spawners = [];
        this.isInitialized = false;
    }

    /**
     * Initialize the WorldEditor with data from the backend
     */
    async initialize(): Promise<WorldEditorState> {
        try {
            console.log('Initializing WorldEditor...');

            // Load map data, game objects, and spawners in parallel
            // Initially load all floors to get a complete view
            const [mapData, gameObjects, spawners] = await Promise.all([
                this.loadWorldMap(),
                this.loadGameObjects(),
                this.loadSpawners()
            ]);

            console.log(`Initialization data loaded: ${mapData.positions?.length || 0} positions, ${gameObjects.length || 0} game objects, ${spawners.length || 0} spawners`);

            // Sync state with the loaded data
            this.syncStateWithMapData(mapData);

            this.isInitialized = true;
            this.emit('initialized', this.state);
            return this.state;
        } catch (error) {
            console.error('Failed to initialize WorldEditor:', error);
            this.isInitialized = false;
            throw error;
        }
    }

    /**
     * Load game objects from the backend
     */
    async loadGameObjects(): Promise<ApiGameObject[]> {
        try {
            // Fetch all game objects with no filters to get everything
            const response: AxiosResponse<ApiGameObject[] | { results: ApiGameObject[] }> = await GameMasterApi.gamemasterGameObjectsList();
            console.log('Game objects data:', response.data);

            // Handle both response formats: array directly or object with results property
            if (!response.data) {
                console.warn('Game objects API response is empty');
                return [];
            }

            let gameObjects: ApiGameObject[] = [];
            // Check if response.data is an array or has a results property
            if (Array.isArray(response.data)) {
                gameObjects = response.data;
            } else if ((response.data as any).results) {
                gameObjects = (response.data as any).results;
            } else {
                console.warn('Game objects API response has unexpected format:', response.data);
                return [];
            }

            // Only update this.gameObjects if we successfully loaded data
            this.gameObjects = gameObjects;
            console.log(`Loaded ${this.gameObjects.length} game objects`);

            // Log some sample objects to understand their structure
            if (this.gameObjects.length > 0) {
                console.log('Sample game object:', this.gameObjects[0]);

                // Count objects by type for debugging
                const typeCount: Record<string, number> = {};
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
     * Load spawners from the backend
     */
    async loadSpawners(): Promise<GenericSpawner[]> {
        try {
            // Fetch all spawners with no filters to get everything
            const response: AxiosResponse<GenericSpawner[] | { results: GenericSpawner[] }> = await GMWorldGenericSpawnersApi.gamemasterSpawnersAllList();
            console.log('Spawners data:', response.data);

            // Handle both response formats: array directly or object with results property
            if (!response.data) {
                console.warn('Spawners API response is empty');
                return [];
            }

            let spawners: GenericSpawner[] = [];
            // Check if response.data is an array or has a results property
            if (Array.isArray(response.data)) {
                spawners = response.data;
            } else if ((response.data as any).results) {
                spawners = (response.data as any).results;
            } else {
                console.warn('Spawners API response has unexpected format:', response.data);
                return [];
            }

            // Only update this.spawners if we successfully loaded data
            this.spawners = spawners;
            console.log(`Loaded ${this.spawners.length} spawners`);

            // Log some sample spawners to understand their structure
            if (this.spawners.length > 0) {
                console.log('Sample spawner:', this.spawners[0]);

                // Count spawners by type for debugging
                const typeCount: Record<string, number> = {};
                this.spawners.forEach(spawner => {
                    const type = spawner.object_type?.model || 'unknown';
                    typeCount[type] = (typeCount[type] || 0) + 1;
                });
                console.log('Spawners by type:', typeCount);

                // Count spawners with positions
                const spawnersWithPosition = this.spawners.filter(spawner =>
                    spawner.position
                ).length;
                console.log(`Spawners with position: ${spawnersWithPosition}/${this.spawners.length}`);
            }

            return this.spawners;
        } catch (error) {
            console.error('Failed to load spawners:', error);
            throw error;
        }
    }

    /**
     * Load world map data from the backend
     * @param floor - The floor level to load (grid_z value)
     */
    async loadWorldMap(floor: number | null = null): Promise<MapData> {
        try {
            // If floor is provided, use gamemasterWorldMapList with gridZ parameter
            // Otherwise, use gamemasterWorldMapMapRetrieve to get all floors
            let response: AxiosResponse<MapData>;
            if (floor !== null) {
                response = await GameMasterApi.gamemasterWorldMapMapRetrieve(floor);
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
     * @param mapData - The map data from the backend
     * @param floor - The floor level being loaded, used as default for positions without grid_z
     * @param preserveState - Whether to preserve existing state on error
     */
    syncStateWithMapData(mapData: MapData, floor: number | null = null, preserveState: boolean = false): void {
        // Validate mapData before proceeding
        if (!mapData || typeof mapData !== 'object') {
            console.error('Invalid map data provided to syncStateWithMapData:', mapData);
            if (!preserveState) {
                throw new Error('Invalid map data: cannot sync state');
            }
            return;
        }

        // Backup current state in case we need to restore it
        const stateBackup = preserveState ? {
            rooms: new Map(this.state.rooms),
            connections: new Map(this.state.connections),
            currentFloor: this.state.currentFloor
        } : null;

        try {
            // Create new state collections
            const newRooms = new Map<string, WorldEditorRoom>();
            // if flour is not null add newRooms with grid_z != floor to make vertical connections work properly
            if (floor !== null && stateBackup) {
                stateBackup.rooms.forEach((room) => {
                    if (room.position.grid_z !== floor) {
                        newRooms.set(room.id, room);
                    }
                })
            }
            const newConnections = new Map<string, WorldEditorConnection>();

            // Add rooms from map data
            if (mapData.positions && Array.isArray(mapData.positions)) {
                mapData.positions.forEach(positionData => {
                    try {
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
                            anomalies: this.extractEntitiesFromPosition(positionData, 'anomalies'),
                            spawners: this.extractSpawnersFromPosition(positionData)
                        });
                        newRooms.set(room.id, room);
                    } catch (error) {
                        console.error('Error processing position data:', positionData, error);
                    }
                });
            }

            // Add connections from map data
            if (mapData.connections && Array.isArray(mapData.connections)) {
                mapData.connections.forEach(connectionData => {
                    try {
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
                        const direction = connection.isVertical ? 'vertical' : 'horizontal';
                        console.debug(`Creating ${direction} connection: ${connection.id} from ${connection.fromRoomId} to ${connection.toRoomId}`);
                        newConnections.set(connection.id, connection);

                        // Add connection to rooms
                        const fromRoom = newRooms.get(connection.fromRoomId);
                        const toRoom = newRooms.get(connection.toRoomId);

                        if (fromRoom) {
                            if (!fromRoom.connections) fromRoom.connections = [];
                            fromRoom.connections.push(connection);
                        }
                        if (toRoom && toRoom.id !== fromRoom?.id) {
                            if (!toRoom.connections) toRoom.connections = [];
                            toRoom.connections.push(connection);
                        }
                    } catch (error) {
                        console.error('Error processing connection data:', connectionData, error);
                    }
                });
            }

            // Only update state if we have valid data or explicitly allowing empty state
            if (newRooms.size > 0 || mapData.positions?.length === 0) {
                this.state.rooms.clear();
                this.state.connections.clear();

                // Add all new rooms and connections
                newRooms.forEach((room, id) => this.state.rooms.set(id, room));
                newConnections.forEach((connection, id) => this.state.connections.set(id, connection));

                console.log(`State synchronized: ${newRooms.size} rooms, ${newConnections.size} connections`);
            } else {
                console.warn('No valid rooms found in map data, keeping existing state');
                if (stateBackup) {
                    // Restore state if we have a backup
                    this.state.rooms = stateBackup.rooms;
                    this.state.connections = stateBackup.connections;
                    this.state.currentFloor = stateBackup.currentFloor;
                }
                return;
            }

            this.emit('stateUpdated', this.state);
        } catch (error) {
            console.error('Error during state synchronization:', error);

            // Restore state from backup if available
            if (stateBackup) {
                console.log('Restoring state from backup due to sync error');
                this.state.rooms = stateBackup.rooms;
                this.state.connections = stateBackup.connections;
                this.state.currentFloor = stateBackup.currentFloor;
            }

            if (!preserveState) {
                throw error;
            }
        }
    }

    /**
     * Extract entities of a specific type from position data
     */
    extractEntitiesFromPosition(positionData: WorldPosition, entityType: 'players' | 'npcs' | 'objects' | 'anomalies'): any[] {
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
     * Extract spawners from position data
     */
    extractSpawnersFromPosition(positionData: WorldPosition): any[] {
        if (!this.spawners || !this.spawners.length) {
            console.log('No spawners available for extraction');
            return [];
        }

        // Handle different position data formats
        let positionInfo = positionData.position || positionData;

        // Check if essential position data is missing
        if (!positionInfo || !positionInfo.id) {
            console.warn('Invalid position data in extractSpawnersFromPosition:', positionData);
            return [];
        }

        const positionId = positionInfo.id;

        // Log the position ID we're filtering for
        console.log(`Extracting spawners for position: ${positionId}`);

        // Filter spawners by position
        const filteredSpawners = this.spawners
            .filter(spawner => {
                // Check if the spawner has a position property
                if (!spawner.position) {
                    return false;
                }

                // Check if the spawner is in this position
                const spawnerPositionId = typeof spawner.position === 'string' ? spawner.position : (spawner.position?.id || '');
                return spawnerPositionId === positionId;
            })
            .map(spawner => {
                // Return the spawner with additional metadata
                return {
                    ...spawner,
                    spawner_type: spawner.object_type?.model || 'unknown'
                };
            });

        console.log(`Found ${filteredSpawners.length} spawners for position ${positionId}`);

        // Log the first few spawners for debugging
        if (filteredSpawners.length > 0) {
            console.log('Sample spawners:', filteredSpawners.slice(0, 3));
        }

        return filteredSpawners;
    }

    /**
     * Create a new room at the specified coordinates
     */
    async createRoom(gridX: number, gridY: number, gridZ: number = this.state.currentFloor, subLocationId: string | null = null): Promise<WorldEditorRoom> {
        try {
            const roomData: RoomCreationData = {
                grid_x: gridX,
                grid_y: gridY,
                grid_z: gridZ
            };

            // Add sub_location if provided
            if (subLocationId) {
                (roomData as any).sub_location = subLocationId;
            }

            const response: AxiosResponse<any> = await GameMasterApi.gamemasterWorldMapCreate(roomData);

            // Validate response data
            if (!response.data || !response.data.id) {
                console.error('Invalid response data from gamemasterWorldMapCreate:', {response});
                throw new Error('Failed to create room: Invalid response data');
            }

            const newRoom = new WorldEditorRoom({
                id: response.data.id,
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
    async deleteRoom(roomId: string): Promise<boolean> {
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
    async updateRoom(roomId: string, updates: RoomUpdateData): Promise<WorldEditorRoom> {
        try {
            const room = this.state.rooms.get(roomId);
            if (!room) {
                throw new Error(`Room with id ${roomId} not found`);
            }

            // Update room labels if provided
            if (updates.labels) {
                const response: AxiosResponse<any> = await GameMasterApi.gamemasterWorldMapUpdate(roomId, {
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
    async moveRoom(roomId: string, newGridX: number, newGridY: number, newGridZ: number): Promise<WorldEditorRoom> {
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

            const eventData: RoomMovedData = {
                room,
                oldPosition: {
                    grid_x: oldPosition.grid_x,
                    grid_y: oldPosition.grid_y,
                    grid_z: oldPosition.grid_z
                },
                newPosition: {
                    grid_x: room.position.grid_x,
                    grid_y: room.position.grid_y,
                    grid_z: room.position.grid_z
                }
            };
            this.emit('roomMoved', eventData);
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
    async createConnection(fromRoomId: string, toRoomId: string, isVertical: boolean = false): Promise<WorldEditorConnection> {
        try {
            // Get room objects to validate they exist
            const fromRoom = this.state.rooms.get(fromRoomId);
            const toRoom = this.state.rooms.get(toRoomId);

            if (!fromRoom) {
                throw new Error(`Source room with id ${fromRoomId} not found`);
            }
            if (!toRoom) {
                throw new Error(`Target room with id ${toRoomId} not found`);
            }

            // Create connection via backend API
            const connectionRequest: PositionConnectionCreateRequest = {
                position_from: fromRoomId,
                position_to: toRoomId,
                is_active: true,
                is_public: true,
                locked: false
            };

            const response: AxiosResponse<any> = await GameMasterApi.gamemasterWorldMapCreateConnectionCreate(connectionRequest);

            // Validate response data
            if (!response.data || !response.data.id) {
                console.error('Invalid response data from gamemasterWorldMapCreateConnectionCreate:', {response});
                throw new Error('Failed to create connection: Invalid response data');
            }

            // Create local connection object with backend ID
            const connection = new WorldEditorConnection({
                id: response.data.id,
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
    async deleteConnection(connectionId: string): Promise<boolean> {
        try {
            const connection = this.state.connections.get(connectionId);
            if (!connection) {
                throw new Error(`Connection with id ${connectionId} not found`);
            }

            // Delete connection via backend API
            await GameMasterApi.gamemasterWorldMapDeleteConnectionDestroy(connectionId);

            // Remove from local state after successful backend deletion
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
     * Update connection properties
     */
    async updateConnection(connectionId: string, updates: Partial<WorldEditorConnection>): Promise<WorldEditorConnection> {
        try {
            const connection = this.state.connections.get(connectionId);
            if (!connection) {
                throw new Error(`Connection with id ${connectionId} not found`);
            }

            // Apply updates to the connection
            Object.assign(connection, updates);

            // Update the connection in the rooms that reference it
            const sourceRoom = this.state.rooms.get(connection.fromRoomId);
            const targetRoom = this.state.rooms.get(connection.toRoomId);

            if (sourceRoom) {
                const connectionIndex = sourceRoom.connections.findIndex(conn => conn.id === connectionId);
                if (connectionIndex !== -1) {
                    sourceRoom.connections[connectionIndex] = connection;
                }
            }

            if (targetRoom) {
                const connectionIndex = targetRoom.connections.findIndex(conn => conn.id === connectionId);
                if (connectionIndex !== -1) {
                    targetRoom.connections[connectionIndex] = connection;
                }
            }

            this.emit('connectionUpdated', connection);
            this.emit('stateUpdated', this.state);

            return connection;
        } catch (error) {
            console.error('Failed to update connection:', error);
            throw error;
        }
    }

    /**
     * Spawn item in room
     */
    async spawnItem(roomId: string, itemData: EntityData): Promise<EntityData> {
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
    async spawnNPC(roomId: string, npcData: EntityData): Promise<EntityData> {
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
    async spawnAnomaly(roomId: string, anomalyData: EntityData): Promise<EntityData> {
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
     * Create spawner in room
     */
    async createSpawner(roomId: string, characterTemplateId: string, spawnLimit: number = 1, respawnCycles: number = 3): Promise<GenericSpawner> {
        try {
            const room = this.state.rooms.get(roomId);
            if (!room) {
                throw new Error(`Room with id ${roomId} not found`);
            }

            // Create spawner via backend API
            const spawnerRequest: NPCSpawnerCreateRequest = {
                character_template: characterTemplateId,
                campaign: 'current', // This should be dynamically set based on current campaign
                position: roomId,
                spawn_limit: spawnLimit,
                respawn_cycles: respawnCycles,
                dimension: room.position.grid_z
            };

            const response: AxiosResponse<GenericSpawner> = await GMWorldNPCSpawnersApi.gamemasterSpawnersNpcCreate(spawnerRequest);

            // Validate response data
            if (!response.data || !response.data.id) {
                console.error('Invalid response data from gamemasterSpawnersNpcCreate:', {response});
                throw new Error('Failed to create spawner: Invalid response data');
            }

            const newSpawner = response.data;

            // Add spawner to room's spawners array
            room.spawners.push({
                ...newSpawner,
                spawner_type: newSpawner.object_type?.model || 'npcspawner'
            });

            // Add to local spawners array
            this.spawners.push(newSpawner);

            this.emit('spawnerCreated', {roomId, spawnerData: newSpawner});
            this.emit('stateUpdated', this.state);

            return newSpawner;
        } catch (error) {
            console.error('Failed to create spawner:', error);
            throw error;
        }
    }

    /**
     * Toggle editor mode
     */
    toggleMode(): void {
        this.state.toggleMode();
        this.emit('modeChanged', this.state.mode);
        this.emit('stateUpdated', this.state);
    }

    /**
     * Set active tool
     */
    setTool(tool: string): void {
        this.state.setTool(tool);
        this.emit('toolChanged', tool);
        this.emit('stateUpdated', this.state);
    }

    /**
     * Toggle layer visibility
     */
    toggleLayer(layer: string): void {
        this.state.toggleLayer(layer);
        const eventData: LayerToggledData = {layer, active: this.state.isLayerActive(layer)};
        this.emit('layerToggled', eventData);
        this.emit('stateUpdated', this.state);
    }

    /**
     * Change current floor and load floor-specific data
     * @param floor - The floor level to set
     */
    async setFloor(floor: number): Promise<void> {
        if (!this.isInitialized) {
            console.warn('WorldEditor not initialized, calling initialize first');
            await this.initialize();
        }

        const previousFloor = this.state.currentFloor;

        try {
            console.log(`Changing floor from ${previousFloor} to ${floor}`);

            // Update the current floor in state first
            this.state.currentFloor = floor;

            // Load map data specific to this floor
            const mapData = await this.loadWorldMap(floor);

            // Sync state with the floor-specific data, passing the floor parameter
            // Use preserveState=true to avoid breaking state on errors
            this.syncStateWithMapData(mapData, floor, true);

            // Emit events
            console.log(`Floor successfully changed to ${floor}`);
            this.emit('floorChanged', floor);
            this.emit('stateUpdated', this.state);

        } catch (error) {
            console.error(`Failed to load data for floor ${floor}:`, error);

            // Restore previous floor on error
            this.state.currentFloor = previousFloor;

            // Still emit the floor change event to notify UI of the failure
            const eventData: FloorChangeFailedData = {targetFloor: floor, currentFloor: previousFloor, error: error as Error};
            this.emit('floorChangeFailed', eventData);

            throw error;
        }
    }

    /**
     * Select/deselect room
     */
    toggleRoomSelection(roomId: string): void {
        this.state.toggleRoomSelection(roomId);
        this.emit('selectionChanged', Array.from(this.state.selectedRooms));
        this.emit('stateUpdated', this.state);
    }

    /**
     * Clear room selection
     */
    clearSelection(): void {
        this.state.clearSelection();
        this.emit('selectionChanged', []);
        this.emit('stateUpdated', this.state);
    }

    /**
     * Get current state
     */
    getState(): WorldEditorState {
        return this.state;
    }

    /**
     * Event system for components to listen to changes
     */
    on(event: WorldEditorServiceEventType, callback: EventCallback): void {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        this.eventListeners.get(event)!.push(callback);
    }

    /**
     * Remove event listener
     */
    off(event: WorldEditorServiceEventType, callback: EventCallback): void {
        if (this.eventListeners.has(event)) {
            const listeners = this.eventListeners.get(event)!;
            const index = listeners.indexOf(callback);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        }
    }

    /**
     * Emit event to listeners
     */
    private emit(event: WorldEditorServiceEventType, data?: any): void {
        if (this.eventListeners.has(event)) {
            this.eventListeners.get(event)!.forEach(callback => {
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
     * @param forceFullReload - Whether to force a complete reload (like initialize)
     */
    async refresh(forceFullReload: boolean = false): Promise<WorldEditorState> {
        if (!this.isInitialized && !forceFullReload) {
            console.log('WorldEditor not initialized, calling initialize instead of refresh');
            return await this.initialize();
        }

        try {
            console.log('Refreshing world data...');

            const currentFloor = this.state.currentFloor;

            if (forceFullReload) {
                // Force complete reinitialization
                console.log('Force reloading all data...');
                return await this.initialize();
            } else {
                // Smart refresh: reload current floor data, game objects, and spawners
                const [mapData, gameObjects, spawners] = await Promise.all([
                    this.loadWorldMap(currentFloor),
                    this.loadGameObjects(),
                    this.loadSpawners()
                ]);

                console.log(`Refresh complete: ${mapData.positions?.length || 0} positions, ${gameObjects.length || 0} game objects, ${spawners.length || 0} spawners`);

                // Sync state with the new data, preserving state on errors
                this.syncStateWithMapData(mapData, currentFloor, true);

                this.emit('refreshed', this.state);
                return this.state;
            }
        } catch (error) {
            console.error('Failed to refresh world data:', error);
            this.emit('refreshFailed', error);
            throw error;
        }
    }

    /**
     * Reset the service to initial state
     */
    reset(): void {
        this.state = new WorldEditorState();
        this.gameObjects = [];
        this.spawners = [];
        this.isInitialized = false;
        console.log('WorldEditor service reset');
        this.emit('reset');
    }
}

// Export singleton instance
export const worldEditorService = new WorldEditorService();