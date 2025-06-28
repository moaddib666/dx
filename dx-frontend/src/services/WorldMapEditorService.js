import { GameMasterApi, GMWorldPositionConnectionsApi, GMWorldPositionsApi } from '@/api/backendService.js';

/**
 * WorldMapEditor Service
 * Handles world positions and position connections management, API interactions, and state synchronization
 */
export class WorldMapEditorService {
    constructor() {
        this.positions = new Map();
        this.connections = new Map();
    }

    // ==================== Position Methods ====================

    /**
     * Get all world positions
     * @returns {Promise<Array>} Array of position objects
     */
    async getWorldPositions() {
        try {
            const response = await GMWorldPositionsApi.gamemasterWorldPositionsList();
            const positions = response.data.results || response.data;

            // Update the positions cache
            positions.forEach(position => {
                this.positions.set(position.id, position);
            });

            return positions;
        } catch (error) {
            console.error('Failed to get world positions:', error);
            throw error;
        }
    }

    /**
     * Get a world position by ID
     * @param {string} id - Position ID
     * @returns {Promise<Object>} Position object
     */
    async getWorldPosition(id) {
        try {
            // Check if we have it cached
            if (this.positions.has(id)) {
                return this.positions.get(id);
            }

            const response = await GMWorldPositionsApi.gamemasterWorldPositionsRetrieve(id);
            const position = response.data;

            // Update the cache
            this.positions.set(id, position);

            return position;
        } catch (error) {
            console.error(`Failed to get world position ${id}:`, error);
            throw error;
        }
    }

    /**
     * Create a new world position
     * @param {Object} positionData - Position data
     * @returns {Promise<Object>} Created position object
     */
    async createWorldPosition(positionData) {
        try {
            const response = await GMWorldPositionsApi.gamemasterWorldPositionsCreate(positionData);
            const position = response.data;

            // Update the cache
            this.positions.set(position.id, position);

            return position;
        } catch (error) {
            console.error('Failed to create world position:', error);
            throw error;
        }
    }

    /**
     * Update a world position
     * @param {string} id - Position ID
     * @param {Object} positionData - Updated position data
     * @returns {Promise<Object>} Updated position object
     */
    async updateWorldPosition(id, positionData) {
        try {
            const response = await GMWorldPositionsApi.gamemasterWorldPositionsUpdate(id, positionData);
            const position = response.data;

            // Update the cache
            this.positions.set(id, position);

            return position;
        } catch (error) {
            console.error(`Failed to update world position ${id}:`, error);
            throw error;
        }
    }

    /**
     * Partially update a world position
     * @param {string} id - Position ID
     * @param {Object} positionData - Partial position data
     * @returns {Promise<Object>} Updated position object
     */
    async patchWorldPosition(id, positionData) {
        try {
            const response = await GMWorldPositionsApi.gamemasterWorldPositionsPartialUpdate(id, positionData);
            const position = response.data;

            // Update the cache
            if (this.positions.has(id)) {
                this.positions.set(id, { ...this.positions.get(id), ...position });
            } else {
                this.positions.set(id, position);
            }

            return position;
        } catch (error) {
            console.error(`Failed to patch world position ${id}:`, error);
            throw error;
        }
    }

    /**
     * Delete a world position
     * @param {string} id - Position ID
     * @returns {Promise<void>}
     */
    async deleteWorldPosition(id) {
        try {
            await GMWorldPositionsApi.gamemasterWorldPositionsDestroy(id);

            // Remove from cache
            this.positions.delete(id);
        } catch (error) {
            console.error(`Failed to delete world position ${id}:`, error);
            throw error;
        }
    }

    /**
     * Mark a position as dangerous
     * @param {string} id - Position ID
     * @param {Object} positionData - Position data
     * @returns {Promise<Object>} Updated position object
     */
    async markPositionDangerous(id, positionData = {}) {
        try {
            const response = await GMWorldPositionsApi.gamemasterWorldPositionsMarkDangerousCreate(id, positionData);
            const position = response.data;

            // Update the cache
            if (this.positions.has(id)) {
                this.positions.set(id, { ...this.positions.get(id), ...position });
            } else {
                this.positions.set(id, position);
            }

            return position;
        } catch (error) {
            console.error(`Failed to mark position ${id} as dangerous:`, error);
            throw error;
        }
    }

    /**
     * Mark a position as safe
     * @param {string} id - Position ID
     * @param {Object} positionData - Position data
     * @returns {Promise<Object>} Updated position object
     */
    async markPositionSafe(id, positionData = {}) {
        try {
            const response = await GMWorldPositionsApi.gamemasterWorldPositionsMarkSafeCreate(id, positionData);
            const position = response.data;

            // Update the cache
            if (this.positions.has(id)) {
                this.positions.set(id, { ...this.positions.get(id), ...position });
            } else {
                this.positions.set(id, position);
            }

            return position;
        } catch (error) {
            console.error(`Failed to mark position ${id} as safe:`, error);
            throw error;
        }
    }

    /**
     * Move a position
     * @param {string} id - Position ID
     * @param {Object} moveData - Move data (new coordinates)
     * @returns {Promise<Object>} Updated position object
     */
    async movePosition(id, moveData) {
        try {
            const response = await GMWorldPositionsApi.gamemasterWorldPositionsMoveCreate(id, moveData);
            const position = response.data;

            // Update the cache
            if (this.positions.has(id)) {
                this.positions.set(id, { ...this.positions.get(id), ...position });
            } else {
                this.positions.set(id, position);
            }

            return position;
        } catch (error) {
            console.error(`Failed to move position ${id}:`, error);
            throw error;
        }
    }

    // ==================== Position Connection Methods ====================

    /**
     * Get all position connections
     * @returns {Promise<Array>} Array of connection objects
     */
    async getPositionConnections() {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsList();
            const connections = response.data.results || response.data;

            // Update the connections cache
            connections.forEach(connection => {
                this.connections.set(connection.id, connection);
            });

            return connections;
        } catch (error) {
            console.error('Failed to get position connections:', error);
            throw error;
        }
    }

    /**
     * Get a position connection by ID
     * @param {number} id - Connection ID
     * @returns {Promise<Object>} Connection object
     */
    async getPositionConnection(id) {
        try {
            // Check if we have it cached
            if (this.connections.has(id)) {
                return this.connections.get(id);
            }

            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsRetrieve(id);
            const connection = response.data;

            // Update the cache
            this.connections.set(id, connection);

            return connection;
        } catch (error) {
            console.error(`Failed to get position connection ${id}:`, error);
            throw error;
        }
    }

    /**
     * Create a new position connection
     * @param {Object} connectionData - Connection data
     * @returns {Promise<Object>} Created connection object
     */
    async createPositionConnection(connectionData) {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsCreate(connectionData);
            const connection = response.data;

            // Update the cache
            this.connections.set(connection.id, connection);

            return connection;
        } catch (error) {
            console.error('Failed to create position connection:', error);
            throw error;
        }
    }

    /**
     * Connect two positions
     * @param {Object} connectionData - Connection data with position_from and position_to
     * @returns {Promise<Object>} Created connection object
     */
    async connectPositions(connectionData) {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsConnectCreate(connectionData);
            const connection = response.data;

            // Update the cache
            this.connections.set(connection.id, connection);

            return connection;
        } catch (error) {
            console.error('Failed to connect positions:', error);
            throw error;
        }
    }

    /**
     * Update a position connection
     * @param {number} id - Connection ID
     * @param {Object} connectionData - Updated connection data
     * @returns {Promise<Object>} Updated connection object
     */
    async updatePositionConnection(id, connectionData) {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsUpdate(id, connectionData);
            const connection = response.data;

            // Update the cache
            this.connections.set(id, connection);

            return connection;
        } catch (error) {
            console.error(`Failed to update position connection ${id}:`, error);
            throw error;
        }
    }

    /**
     * Partially update a position connection
     * @param {number} id - Connection ID
     * @param {Object} connectionData - Partial connection data
     * @returns {Promise<Object>} Updated connection object
     */
    async patchPositionConnection(id, connectionData) {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsPartialUpdate(id, connectionData);
            const connection = response.data;

            // Update the cache
            if (this.connections.has(id)) {
                this.connections.set(id, { ...this.connections.get(id), ...connection });
            } else {
                this.connections.set(id, connection);
            }

            return connection;
        } catch (error) {
            console.error(`Failed to patch position connection ${id}:`, error);
            throw error;
        }
    }

    /**
     * Delete a position connection
     * @param {number} id - Connection ID
     * @returns {Promise<void>}
     */
    async deletePositionConnection(id) {
        try {
            await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsDestroy(id);

            // Remove from cache
            this.connections.delete(id);
        } catch (error) {
            console.error(`Failed to delete position connection ${id}:`, error);
            throw error;
        }
    }

    /**
     * Activate a position connection
     * @param {number} id - Connection ID
     * @param {Object} connectionData - Connection data
     * @returns {Promise<Object>} Updated connection object
     */
    async activatePositionConnection(id, connectionData = {}) {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsActivateCreate(id, connectionData);
            const connection = response.data;

            // Update the cache
            if (this.connections.has(id)) {
                this.connections.set(id, { ...this.connections.get(id), is_active: true });
            } else {
                this.connections.set(id, connection);
            }

            return connection;
        } catch (error) {
            console.error(`Failed to activate position connection ${id}:`, error);
            throw error;
        }
    }

    /**
     * Deactivate a position connection
     * @param {number} id - Connection ID
     * @param {Object} connectionData - Connection data
     * @returns {Promise<Object>} Updated connection object
     */
    async deactivatePositionConnection(id, connectionData = {}) {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsDeactivateCreate(id, connectionData);
            const connection = response.data;

            // Update the cache
            if (this.connections.has(id)) {
                this.connections.set(id, { ...this.connections.get(id), is_active: false });
            } else {
                this.connections.set(id, connection);
            }

            return connection;
        } catch (error) {
            console.error(`Failed to deactivate position connection ${id}:`, error);
            throw error;
        }
    }

    /**
     * Configure a position connection
     * @param {number} id - Connection ID
     * @param {Object} configData - Configuration data
     * @returns {Promise<Object>} Updated connection object
     */
    async configurePositionConnection(id, configData) {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsConfigureCreate(id, configData);
            const connection = response.data;

            // Update the cache
            if (this.connections.has(id)) {
                this.connections.set(id, { ...this.connections.get(id), config: configData });
            } else {
                this.connections.set(id, connection);
            }

            return connection;
        } catch (error) {
            console.error(`Failed to configure position connection ${id}:`, error);
            throw error;
        }
    }

    /**
     * Lock a position connection
     * @param {number} id - Connection ID
     * @param {Object} connectionData - Connection data
     * @returns {Promise<Object>} Updated connection object
     */
    async lockPositionConnection(id, connectionData = {}) {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsLockCreate(id, connectionData);
            const connection = response.data;

            // Update the cache
            if (this.connections.has(id)) {
                this.connections.set(id, { ...this.connections.get(id), locked: true });
            } else {
                this.connections.set(id, connection);
            }

            return connection;
        } catch (error) {
            console.error(`Failed to lock position connection ${id}:`, error);
            throw error;
        }
    }

    /**
     * Unlock a position connection
     * @param {number} id - Connection ID
     * @param {Object} connectionData - Connection data
     * @returns {Promise<Object>} Updated connection object
     */
    async unlockPositionConnection(id, connectionData = {}) {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsUnlockCreate(id, connectionData);
            const connection = response.data;

            // Update the cache
            if (this.connections.has(id)) {
                this.connections.set(id, { ...this.connections.get(id), locked: false });
            } else {
                this.connections.set(id, connection);
            }

            return connection;
        } catch (error) {
            console.error(`Failed to unlock position connection ${id}:`, error);
            throw error;
        }
    }

    /**
     * Set a position connection as public
     * @param {number} id - Connection ID
     * @param {Object} connectionData - Connection data
     * @returns {Promise<Object>} Updated connection object
     */
    async setPositionConnectionPublic(id, connectionData = {}) {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsSetPublicCreate(id, connectionData);
            const connection = response.data;

            // Update the cache
            if (this.connections.has(id)) {
                this.connections.set(id, { ...this.connections.get(id), is_public: true });
            } else {
                this.connections.set(id, connection);
            }

            return connection;
        } catch (error) {
            console.error(`Failed to set position connection ${id} as public:`, error);
            throw error;
        }
    }

    /**
     * Set a position connection as private
     * @param {number} id - Connection ID
     * @param {Object} connectionData - Connection data
     * @returns {Promise<Object>} Updated connection object
     */
    async setPositionConnectionPrivate(id, connectionData = {}) {
        try {
            const response = await GMWorldPositionConnectionsApi.gamemasterWorldPositionConnectionsSetPrivateCreate(id, connectionData);
            const connection = response.data;

            // Update the cache
            if (this.connections.has(id)) {
                this.connections.set(id, { ...this.connections.get(id), is_public: false });
            } else {
                this.connections.set(id, connection);
            }

            return connection;
        } catch (error) {
            console.error(`Failed to set position connection ${id} as private:`, error);
            throw error;
        }
    }
}

// Create and export an instance of the service
export const worldMapEditorService = new WorldMapEditorService();