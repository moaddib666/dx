<template>
  <g class="world-editor-room">
    <!-- Room base shape -->
    <rect
        :fill="roomFill"
        :height="roomHeight"
        :stroke="roomStroke"
        :width="roomWidth"
        :x="roomLeft"
        :y="roomTop"
        class="room-rect"
        rx="8"
        ry="8"
        stroke-width="2"
    />

    <!-- Room type indicator -->
    <g v-if="showTypeIndicator" class="room-type-indicator">
      <circle
          :cx="roomLeft + 15"
          :cy="roomTop + 15"
          :fill="typeIndicatorColor"
          r="6"
      />
    </g>

    <!-- Entity indicators based on active layers -->
    <g v-if="hasEntities" class="entity-indicators">
      <!-- Players indicator -->
      <g v-if="showPlayers && room.players.length > 0" class="player-indicator">
        <circle
            :cx="roomLeft + roomWidth - 15"
            :cy="roomTop + 15"
            :fill="layerColors.players"
            r="5"
        />
        <text
            :x="roomLeft + roomWidth - 15"
            :y="roomTop + 18"
            fill="#000"
            font-size="8"
            font-weight="bold"
            text-anchor="middle"
        >{{ room.players.length }}
        </text>
      </g>

      <!-- NPCs indicator -->
      <g v-if="showNpcs && room.npcs.length > 0" class="npc-indicator">
        <circle
            :cx="roomLeft + roomWidth - 30"
            :cy="roomTop + 15"
            :fill="layerColors.npcs"
            r="5"
        />
        <text
            :x="roomLeft + roomWidth - 30"
            :y="roomTop + 18"
            fill="#000"
            font-size="8"
            font-weight="bold"
            text-anchor="middle"
        >{{ room.npcs.length }}
        </text>
      </g>

      <!-- Objects indicator -->
      <g v-if="showObjects && room.objects.length > 0" class="object-indicator">
        <circle
            :cx="roomLeft + roomWidth - 15"
            :cy="roomTop + 30"
            :fill="layerColors.objects"
            r="5"
        />
        <text
            :x="roomLeft + roomWidth - 15"
            :y="roomTop + 33"
            fill="#000"
            font-size="8"
            font-weight="bold"
            text-anchor="middle"
        >{{ room.objects.length }}
        </text>
      </g>

      <!-- Anomalies indicator -->
      <g v-if="showAnomalies && room.anomalies.length > 0" class="anomaly-indicator">
        <circle
            :cx="roomLeft + roomWidth - 30"
            :cy="roomTop + 30"
            :fill="layerColors.anomalies"
            r="5"
        />
        <text
            :x="roomLeft + roomWidth - 30"
            :y="roomTop + 33"
            fill="#000"
            font-size="8"
            font-weight="bold"
            text-anchor="middle"
        >{{ room.anomalies.length }}
        </text>
      </g>
    </g>
  </g>
</template>

<script>
import {WorldEditorLayer} from '@/models/WorldEditorModels.js';

export default {
  name: 'WorldEditorRoom',
  props: {
    room: {
      type: Object,
      required: true
    },
    cellSize: {
      type: Number,
      default: 80
    },
    cellPadding: {
      type: Number,
      default: 35
    },
    selected: {
      type: Boolean,
      default: false
    },
    editorState: {
      type: Object,
      default: () => ({})
    },
    activeLayers: {
      type: Set,
      default: () => new Set()
    }
  },
  computed: {
    // Room positioning
    roomLeft() {
      return this.room.position.grid_x * this.cellSize + this.cellPadding / 2;
    },
    roomTop() {
      return this.room.position.grid_y * this.cellSize + this.cellPadding / 2;
    },
    roomWidth() {
      return this.cellSize - this.cellPadding;
    },
    roomHeight() {
      return this.cellSize - this.cellPadding;
    },

    // Room styling
    roomFill() {
      if (this.selected) {
        return '#1E90FF'; // Selected color
      }

      // Different colors based on room type
      switch (this.room.type) {
        case 'special':
          return '#8A2BE2'; // BlueViolet
        case 'secret':
          return '#9932CC'; // DarkOrchid
        case 'dangerous':
          return '#B22222'; // FireBrick
        default:
          return '#444'; // Default dark gray
      }
    },
    roomStroke() {
      return this.selected ? '#FFA500' : '#666'; // Orange when selected, dark gray otherwise
    },

    // Type indicator
    showTypeIndicator() {
      return this.room.type !== 'default';
    },
    typeIndicatorColor() {
      switch (this.room.type) {
        case 'special':
          return '#E6E6FA'; // Lavender
        case 'secret':
          return '#FFD700'; // Gold
        case 'dangerous':
          return '#FF4500'; // OrangeRed
        default:
          return '#FFFFFF'; // White
      }
    },

    // Layer visibility
    showPlayers() {
      return this.activeLayers.has(WorldEditorLayer.PLAYERS);
    },
    showNpcs() {
      return this.activeLayers.has(WorldEditorLayer.NPCS);
    },
    showObjects() {
      return this.activeLayers.has(WorldEditorLayer.OBJECTS);
    },
    showAnomalies() {
      return this.activeLayers.has(WorldEditorLayer.ANOMALIES);
    },

    // Entity presence
    hasEntities() {
      return this.room.players.length > 0 ||
          this.room.npcs.length > 0 ||
          this.room.objects.length > 0 ||
          this.room.anomalies.length > 0;
    },

    // Layer colors
    layerColors() {
      return {
        players: '#00ff00',   // Green
        npcs: '#ffff00',      // Yellow
        objects: '#ff8800',   // Orange
        anomalies: '#ff0088'  // Pink
      };
    }
  }
};
</script>

<style scoped>
.world-editor-room {
  transition: all 0.2s ease;
}

.world-editor-room:hover .room-rect {
  filter: brightness(1.2);
}

.room-type-indicator {
  pointer-events: none;
}

.entity-indicators {
  pointer-events: none;
}

/* Ensure text is readable */
text {
  font-family: 'Roboto', sans-serif;
  user-select: none;
}
</style>