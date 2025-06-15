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

    <!-- Clipped circular image -->
    <clipPath :id="clipId">
      <circle
          :cx="roomLeft + roomWidth / 2"
          :cy="roomTop + roomHeight / 2"
          :r="Math.min(roomWidth, roomHeight) / 2 - 8"
      />
    </clipPath>
    <image
        v-if="backgroundImage"
        :clip-path="`url(#${clipId})`"
        :height="roomHeight"
        :href="backgroundImageSrc"
        :width="roomWidth"
        :x="roomLeft"
        :y="roomTop"
        preserveAspectRatio="xMidYMid slice"
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
      <!-- Players indicator (top-left corner) - GREEN CIRCLE -->
      <g v-if="showPlayers && room.players.length > 0" class="player-indicator entity-group"
         @click="showEntityDetails('players')">
        <title>{{ getPlayerTooltip() }}</title>
        <circle
            :cx="roomLeft"
            :cy="roomTop"
            :fill="layerColors.players"
            class="entity-circle"
            r="8"
            stroke="#000"
            stroke-width="1"
        >
        </circle>
        <text
            :x="roomLeft"
            :y="roomTop + 2"
            fill="#000"
            font-size="8"
            font-weight="bold"
            text-anchor="middle"
        >{{ room.players.length }}
        </text>
      </g>

      <!-- NPCs indicator (top-right corner) - YELLOW SQUARE -->
      <g v-if="showNpcs && room.npcs.length > 0" class="npc-indicator entity-group" @click="showEntityDetails('npcs')">
        <title>{{ getNpcTooltip() }}</title>
        <rect
            :x="roomLeft + roomWidth - 8"
            :y="roomTop - 8"
            class="entity-square"
            height="16"
            :fill="layerColors.npcs"
            rx="2"
            ry="2"
            stroke="#000"
            stroke-width="1"
            width="16"
        />
        <text
            :x="roomLeft + roomWidth"
            :y="roomTop + 3"
            fill="#000"
            font-size="8"
            font-weight="bold"
            text-anchor="middle"
        >{{ room.npcs.length }}
        </text>
      </g>

      <!-- Anomalies indicator (top middle) - RED CIRCLE -->
      <g v-if="showAnomalies && room.anomalies.length > 0" class="anomaly-indicator entity-group"
         @click="showEntityDetails('anomalies')">
        <title>{{ getAnomalyTooltip() }}</title>
        <circle
            :cx="roomLeft + roomWidth/2"
            :cy="roomTop"
            :fill="layerColors.anomalies"
            class="entity-circle"
            r="8"
            stroke="#000"
            stroke-width="1"
        />
        <text
            :x="roomLeft + roomWidth/2"
            :y="roomTop + 3"
            fill="#000"
            font-size="8"
            font-weight="bold"
            text-anchor="middle"
        >{{ room.anomalies.length }}
        </text>
      </g>

      <!-- Objects indicator (top-left middle) - BLUE SQUARE -->
      <g v-if="showObjects && room.objects.length > 0" class="object-indicator entity-group"
         @click="showEntityDetails('objects')">
        <title>{{ getObjectTooltip() }}</title>
        <rect
            :fill="layerColors.objects"
            :x="roomLeft + roomWidth/4 - 8"
            :y="roomTop - 16"
            class="entity-square"
            height="16"
            rx="2"
            ry="2"
            stroke="#000"
            stroke-width="1"
            width="16"
        />
        <text
            :x="roomLeft + roomWidth/4"
            :y="roomTop - 8"
            fill="#000"
            font-size="8"
            font-weight="bold"
            text-anchor="middle"
        >{{ room.objects.length }}
        </text>
      </g>
    </g>
  </g>
</template>

<script>
import {WorldEditorLayer} from '@/models/WorldEditorModels.js';
import {RoomLabel} from "@/utils/mapData.js";

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
  data() {
    return {
      roomType: null,
      roomLabel: null,
      backgroundImage: null,
    };
  },
  created() {
    this.extractLabels();
    this.loadIcon();
  },
  methods: {
    extractLabels() {
      const labels = this.room.labels || [];
      this.roomType = labels[0] || null;
      this.roomLabel = labels[1] || null;
    },
    loadIcon() {
      const icon = RoomLabel.getIcon(this.roomLabel);
      if (icon instanceof HTMLImageElement) {
        this.backgroundImage = icon;
      } else {
        this.backgroundImage = null;
      }
    },
    showEntityDetails(entityType) {
      // Emit an event to show detailed information about the entities
      this.$emit('show-entity-details', {
        roomId: this.room.id,
        entityType: entityType,
        entities: this.room[entityType]
      });
    },
    getPlayerTooltip() {
      if (!this.room.players.length) return 'No players';

      let tooltip = `Players (${this.room.players.length}):\n`;
      const playerNames = this.room.players
          .map(player => player.name || 'Unnamed Player')
          .slice(0, 5);

      tooltip += playerNames.join('\n');

      if (this.room.players.length > 5) {
        tooltip += `\n...and ${this.room.players.length - 5} more`;
      }

      return tooltip;
    },
    getNpcTooltip() {
      if (!this.room.npcs.length) return 'No NPCs';

      let tooltip = `NPCs (${this.room.npcs.length}):\n`;
      const npcNames = this.room.npcs
          .map(npc => npc.name || 'Unnamed NPC')
          .slice(0, 5);

      tooltip += npcNames.join('\n');

      if (this.room.npcs.length > 5) {
        tooltip += `\n...and ${this.room.npcs.length - 5} more`;
      }

      return tooltip;
    },
    getObjectTooltip() {
      if (!this.room.objects.length) return 'No objects';

      let tooltip = `Objects (${this.room.objects.length}):\n`;
      const objectNames = this.room.objects
          .map(obj => obj.name || 'Unnamed Object')
          .slice(0, 5);

      tooltip += objectNames.join('\n');

      if (this.room.objects.length > 5) {
        tooltip += `\n...and ${this.room.objects.length - 5} more`;
      }

      return tooltip;
    },
    getAnomalyTooltip() {
      if (!this.room.anomalies.length) return 'No anomalies';

      let tooltip = `Anomalies (${this.room.anomalies.length}):\n`;
      const anomalyNames = this.room.anomalies
          .map(anomaly => anomaly.name || 'Unnamed Anomaly')
          .slice(0, 5);

      tooltip += anomalyNames.join('\n');

      if (this.room.anomalies.length > 5) {
        tooltip += `\n...and ${this.room.anomalies.length - 5} more`;
      }

      return tooltip;
    }
  },
  computed: {
    // Background image source
    backgroundImageSrc() {
      return this.backgroundImage ? this.backgroundImage.src : null;
    },
    // Unique ID for the clipPath to avoid conflicts
    clipId() {
      return `clip-${this.room.id}`;
    },
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
        objects: '#0088ff',   // Blue
        anomalies: '#ff0000'  // Red
      };
    }
  },
  watch: {
    room: {
      immediate: true,
      handler() {
        this.extractLabels();
        this.loadIcon();
      },
    },
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

.entity-circle {
  filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.5));
}

.entity-square {
  filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.5));
}

.entity-group {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.entity-group:hover {
  transform: scale(1.2);
}

.entity-group:hover .entity-circle,
.entity-group:hover .entity-square {
  stroke: rgba(255, 255, 255, 0.8);
  stroke-width: 1.5;
}

/* Ensure text is readable */
text {
  font-family: 'Roboto', sans-serif;
  user-select: none;
  filter: drop-shadow(0px 1px 1px rgba(0, 0, 0, 0.5));
}
</style>
