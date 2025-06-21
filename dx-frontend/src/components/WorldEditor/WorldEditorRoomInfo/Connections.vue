<template>
  <div class="info-section">
    <div class="section-header">
      <h4>Connections</h4>
      <EditInDjangoAdmin
          :id="room.id"
          app="world"
          model="position"
      />
    </div>
    <div class="connections-container">
      <div v-if="roomConnections.length > 0" class="connection-list">
        <div
            v-for="connection in roomConnections"
            :key="connection.id"
            class="connection-item"
            @click="openConnectionInfo(connection)"
        >
          <div class="connection-info">
            <div class="connection-header">
              <span class="connection-direction">{{ getConnectionDirection(connection) }}</span>
              <span class="connection-id">ID: {{
                  typeof connection.id === 'string' ? connection.id.substring(0, 8) + '...' : connection.id
                }}</span>
            </div>
            <div class="connection-details">
              <span class="connection-type">{{ connection.isVertical ? 'Vertical' : 'Horizontal' }}</span>
              <span :class="{ 'locked': connection.type === 'locked' }" class="connection-status">
                {{ connection.type === 'locked' ? 'Locked' : 'Open' }}
              </span>
            </div>
          </div>
          <div class="connection-actions">
            <button
                class="view-connection-btn"
                title="View connection details"
                @click.stop="openConnectionInfo(connection)"
            >
              <i class="icon-info-circle"></i>
            </button>
            <button
                v-if="editable"
                class="remove-connection-btn"
                title="Remove connection"
                @click.stop="removeConnection(connection)"
            >
              <i class="icon-unlink"></i>
            </button>
          </div>
        </div>
      </div>
      <div v-else class="empty-connections">
        <p>No connections from this room</p>
      </div>
    </div>
  </div>
</template>

<script>
import EditInDjangoAdmin from '@/components/EditInDjangoAdmin.vue';

export default {
  name: 'Connections',
  components: {
    EditInDjangoAdmin
  },
  props: {
    room: {
      type: Object,
      required: true
    },
    roomConnections: {
      type: Array,
      default: () => []
    },
    editable: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    openConnectionInfo(connection) {
      this.$emit('open-connection-info', connection);
    },

    removeConnection(connection) {
      this.$emit('remove-connection', connection);
    },

    getConnectionDirection(connection) {
      if (!connection) {
        console.error('Cannot get connection direction: connection is undefined');
        return 'Unknown';
      }

      // For simple display in the component, we can use a simplified version
      // that just shows the direction based on the connection properties

      // If it's a vertical connection
      if (connection.isVertical) {
        return connection.direction === 'up' ? 'Up' : 'Down';
      }

      // For horizontal connections, use the direction property if available
      if (connection.direction) {
        switch (connection.direction.toLowerCase()) {
          case 'north':
            return 'North';
          case 'east':
            return 'East';
          case 'south':
            return 'South';
          case 'west':
            return 'West';
          default:
            return connection.direction;
        }
      }

      return 'Unknown';
    }
  }
};
</script>

<style scoped>
.info-section {
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.connections-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.connection-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.connection-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #2a2a2a;
  border-radius: 6px;
  padding: 0.75rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.connection-item:hover {
  background: #3a3a3a;
}

.connection-info {
  flex: 1;
}

.connection-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
}

.connection-direction {
  font-weight: bold;
  color: #fff;
}

.connection-id {
  color: #aaa;
  font-size: 0.8rem;
}

.connection-details {
  display: flex;
  gap: 1rem;
}

.connection-type {
  color: #ccc;
  font-size: 0.9rem;
}

.connection-status {
  color: #66cc66;
  font-size: 0.9rem;
}

.connection-status.locked {
  color: #ff6666;
}

.connection-actions {
  display: flex;
  gap: 0.5rem;
}

.view-connection-btn,
.remove-connection-btn {
  width: 28px;
  height: 28px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-connection-btn {
  background: rgba(0, 128, 255, 0.2);
  border: 1px solid rgba(0, 128, 255, 0.3);
  color: #66aaff;
}

.view-connection-btn:hover {
  background: rgba(0, 128, 255, 0.3);
  border-color: rgba(0, 128, 255, 0.4);
}

.remove-connection-btn {
  background: rgba(255, 0, 0, 0.2);
  border: 1px solid rgba(255, 0, 0, 0.3);
  color: #ff6666;
}

.remove-connection-btn:hover {
  background: rgba(255, 0, 0, 0.3);
  border-color: rgba(255, 0, 0, 0.4);
}

.empty-connections {
  text-align: center;
  color: #aaa;
  font-style: italic;
  padding: 1rem;
}
</style>
