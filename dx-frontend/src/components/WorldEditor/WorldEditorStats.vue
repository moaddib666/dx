<template>
  <div class="world-editor-stats">
    <div class="stats-header">
      <h3>World Statistics</h3>
      <button class="refresh-btn" title="Refresh Statistics" @click="refreshStats">
        <i class="icon-refresh"></i>
      </button>
    </div>

    <div class="stats-content">
      <!-- Overview Stats -->
      <div class="stats-section">
        <h4>Overview</h4>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-value">{{ stats.totalRooms || 0 }}</div>
            <div class="stat-label">Total Rooms</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.totalConnections || 0 }}</div>
            <div class="stat-label">Connections</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.floorsUsed || 0 }}</div>
            <div class="stat-label">Floors Used</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ totalEntities }}</div>
            <div class="stat-label">Total Entities</div>
          </div>
        </div>
      </div>

      <!-- Entity Breakdown -->
      <div class="stats-section">
        <h4>Entities by Type</h4>
        <div class="entity-stats">
          <div v-for="(count, type) in entityStats" :key="type" class="entity-item">
            <div class="entity-info">
              <i :class="getEntityIcon(type)" :style="{ color: getEntityColor(type) }"></i>
              <span class="entity-name">{{ formatEntityType(type) }}</span>
            </div>
            <div class="entity-count">{{ count }}</div>
            <div class="entity-bar">
              <div
                  :style="{
                  width: getEntityPercentage(count) + '%',
                  backgroundColor: getEntityColor(type)
                }"
                  class="entity-bar-fill"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Floor Distribution -->
      <div v-if="floorStats.length > 0" class="stats-section">
        <h4>Floor Distribution</h4>
        <div class="floor-stats">
          <div v-for="floor in floorStats" :key="floor.floor" class="floor-item">
            <div class="floor-info">
              <span class="floor-name">Floor {{ floor.floor }}</span>
              <span class="floor-count">{{ floor.roomCount }} rooms</span>
            </div>
            <div class="floor-bar">
              <div
                  :style="{ width: getFloorPercentage(floor.roomCount) + '%' }"
                  class="floor-bar-fill"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Connection Types -->
      <div v-if="connectionStats" class="stats-section">
        <h4>Connection Types</h4>
        <div class="connection-stats">
          <div class="connection-item">
            <span class="connection-label">Horizontal</span>
            <span class="connection-count">{{ connectionStats.horizontal || 0 }}</span>
          </div>
          <div class="connection-item">
            <span class="connection-label">Vertical</span>
            <span class="connection-count">{{ connectionStats.vertical || 0 }}</span>
          </div>
        </div>
      </div>

      <!-- Performance Metrics -->
      <div class="stats-section">
        <h4>Performance</h4>
        <div class="performance-stats">
          <div class="performance-item">
            <span class="performance-label">Avg. Entities per Room</span>
            <span class="performance-value">{{ averageEntitiesPerRoom }}</span>
          </div>
          <div class="performance-item">
            <span class="performance-label">Avg. Connections per Room</span>
            <span class="performance-value">{{ averageConnectionsPerRoom }}</span>
          </div>
          <div class="performance-item">
            <span class="performance-label">World Density</span>
            <span class="performance-value">{{ worldDensity }}%</span>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div v-if="recentActivity.length > 0" class="stats-section">
        <h4>Recent Activity</h4>
        <div class="activity-list">
          <div
              v-for="(activity, index) in recentActivity"
              :key="index"
              class="activity-item"
          >
            <div class="activity-icon">
              <i :class="getActivityIcon(activity.type)"></i>
            </div>
            <div class="activity-content">
              <div class="activity-description">{{ activity.description }}</div>
              <div class="activity-time">{{ formatTime(activity.timestamp) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'WorldEditorStats',
  props: {
    stats: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      recentActivity: [
        {
          type: 'room_created',
          description: 'Created room at (5, 3)',
          timestamp: Date.now() - 300000 // 5 minutes ago
        },
        {
          type: 'connection_created',
          description: 'Connected rooms (5, 3) and (6, 3)',
          timestamp: Date.now() - 600000 // 10 minutes ago
        },
        {
          type: 'entity_spawned',
          description: 'Spawned NPC in room (4, 2)',
          timestamp: Date.now() - 900000 // 15 minutes ago
        }
      ]
    };
  },
  computed: {
    entityStats() {
      return this.stats.entitiesByType || {};
    },

    totalEntities() {
      return Object.values(this.entityStats).reduce((sum, count) => sum + count, 0);
    },

    floorStats() {
      // This would be calculated from the actual room data
      // For now, return mock data
      return [
        {floor: 1, roomCount: 15},
        {floor: 2, roomCount: 8},
        {floor: 3, roomCount: 3}
      ];
    },

    connectionStats() {
      // This would be calculated from actual connection data
      return {
        horizontal: (this.stats.totalConnections || 0) - 2,
        vertical: 2
      };
    },

    averageEntitiesPerRoom() {
      const totalRooms = this.stats.totalRooms || 1;
      return (this.totalEntities / totalRooms).toFixed(1);
    },

    averageConnectionsPerRoom() {
      const totalRooms = this.stats.totalRooms || 1;
      const totalConnections = this.stats.totalConnections || 0;
      return (totalConnections / totalRooms).toFixed(1);
    },

    worldDensity() {
      // Calculate based on some metric of world utilization
      const totalRooms = this.stats.totalRooms || 0;
      const maxExpectedRooms = 100; // This could be configurable
      return Math.min(100, Math.round((totalRooms / maxExpectedRooms) * 100));
    }
  },
  methods: {
    refreshStats() {
      this.$emit('refresh-stats');
    },

    getEntityIcon(type) {
      const icons = {
        players: 'icon-users',
        npcs: 'icon-user-friends',
        objects: 'icon-cube',
        anomalies: 'icon-exclamation-triangle'
      };
      return icons[type] || 'icon-question';
    },

    getEntityColor(type) {
      const colors = {
        players: '#00ff00',
        npcs: '#ffff00',
        objects: '#ff8800',
        anomalies: '#ff0088'
      };
      return colors[type] || '#888888';
    },

    formatEntityType(type) {
      return type.charAt(0).toUpperCase() + type.slice(1);
    },

    getEntityPercentage(count) {
      if (this.totalEntities === 0) return 0;
      return Math.round((count / this.totalEntities) * 100);
    },

    getFloorPercentage(roomCount) {
      const maxRooms = Math.max(...this.floorStats.map(f => f.roomCount));
      if (maxRooms === 0) return 0;
      return Math.round((roomCount / maxRooms) * 100);
    },

    getActivityIcon(type) {
      const icons = {
        room_created: 'icon-plus-square',
        room_deleted: 'icon-trash',
        connection_created: 'icon-link',
        connection_deleted: 'icon-unlink',
        entity_spawned: 'icon-plus',
        entity_removed: 'icon-minus'
      };
      return icons[type] || 'icon-info';
    },

    formatTime(timestamp) {
      const now = Date.now();
      const diff = now - timestamp;
      const minutes = Math.floor(diff / 60000);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);

      if (days > 0) return `${days}d ago`;
      if (hours > 0) return `${hours}h ago`;
      if (minutes > 0) return `${minutes}m ago`;
      return 'Just now';
    }
  }
};
</script>

<style scoped>
.world-editor-stats {
  background: #2d2d2d;
  padding: 1rem;
  height: 100%;
  overflow-y: auto;
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.stats-header h3 {
  margin: 0;
  color: #1E90FF;
  font-size: 1.1rem;
  font-weight: 600;
}

.refresh-btn {
  padding: 0.25rem;
  background: #444;
  color: #ccc;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  background: #555;
  color: #fff;
}

.stats-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Stats Sections */
.stats-section {
  background: #333;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 1rem;
}

.stats-section h4 {
  margin: 0 0 0.75rem 0;
  color: #fff;
  font-size: 0.9rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Overview Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.stat-item {
  text-align: center;
  padding: 0.75rem;
  background: #444;
  border-radius: 4px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1E90FF;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.8rem;
  color: #ccc;
}

/* Entity Stats */
.entity-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.entity-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #444;
  border-radius: 4px;
}

.entity-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.entity-name {
  color: #fff;
  font-size: 0.9rem;
}

.entity-count {
  color: #ccc;
  font-weight: bold;
  min-width: 30px;
  text-align: right;
}

.entity-bar {
  width: 60px;
  height: 8px;
  background: #555;
  border-radius: 4px;
  overflow: hidden;
}

.entity-bar-fill {
  height: 100%;
  transition: width 0.3s ease;
}

/* Floor Stats */
.floor-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.floor-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #444;
  border-radius: 4px;
}

.floor-info {
  display: flex;
  justify-content: space-between;
  flex: 1;
}

.floor-name {
  color: #fff;
  font-weight: 500;
}

.floor-count {
  color: #ccc;
  font-size: 0.9rem;
}

.floor-bar {
  width: 60px;
  height: 8px;
  background: #555;
  border-radius: 4px;
  overflow: hidden;
}

.floor-bar-fill {
  height: 100%;
  background: #1E90FF;
  transition: width 0.3s ease;
}

/* Connection Stats */
.connection-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.connection-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: #444;
  border-radius: 4px;
}

.connection-label {
  color: #fff;
  font-size: 0.9rem;
}

.connection-count {
  color: #1E90FF;
  font-weight: bold;
}

/* Performance Stats */
.performance-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.performance-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: #444;
  border-radius: 4px;
}

.performance-label {
  color: #fff;
  font-size: 0.9rem;
}

.performance-value {
  color: #1E90FF;
  font-weight: bold;
}

/* Activity List */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #444;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: #4a4a4a;
}

.activity-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #555;
  border-radius: 50%;
  color: #1E90FF;
  font-size: 12px;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.activity-description {
  color: #fff;
  font-size: 0.9rem;
  line-height: 1.3;
}

.activity-time {
  color: #aaa;
  font-size: 0.8rem;
}

/* Scrollbar Styling */
.world-editor-stats::-webkit-scrollbar,
.activity-list::-webkit-scrollbar {
  width: 6px;
}

.world-editor-stats::-webkit-scrollbar-track,
.activity-list::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.world-editor-stats::-webkit-scrollbar-thumb,
.activity-list::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}

.world-editor-stats::-webkit-scrollbar-thumb:hover,
.activity-list::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* Responsive Design */
@media (max-width: 768px) {
  .world-editor-stats {
    padding: 0.5rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .stat-item {
    padding: 0.5rem;
  }

  .stat-value {
    font-size: 1.2rem;
  }

  .entity-bar,
  .floor-bar {
    width: 40px;
  }

  .activity-item {
    padding: 0.5rem;
  }

  .activity-icon {
    width: 20px;
    height: 20px;
    font-size: 10px;
  }
}

/* Icon placeholders */
.icon-refresh::before {
  content: '🔄';
}

.icon-users::before {
  content: '👥';
}

.icon-user-friends::before {
  content: '👫';
}

.icon-cube::before {
  content: '📦';
}

.icon-exclamation-triangle::before {
  content: '⚠️';
}

.icon-question::before {
  content: '❓';
}

.icon-plus-square::before {
  content: '⊞';
}

.icon-trash::before {
  content: '🗑';
}

.icon-link::before {
  content: '🔗';
}

.icon-unlink::before {
  content: '⛓';
}

.icon-plus::before {
  content: '➕';
}

.icon-minus::before {
  content: '➖';
}

.icon-info::before {
  content: 'ℹ️';
}
</style>
