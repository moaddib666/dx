<template>
  <div class="player-component">
    <!-- Player Image Section -->
    <div :style="{ backgroundImage: `url(${playerImage})` }" class="player-image"></div>

    <!-- Player Info Section -->
    <div class="player-info">
      <div class="player-name">{{ player?.name || 'Unknown' }}</div>
      <div class="player-meta">
        <span>Rank: {{ player?.rank_grade || 0 }}</span>
        <span>Dimension: {{ player?.dimension || 0 }}</span>
      </div>

      <!-- Attributes Section -->
      <div class="player-attributes">
        <div
            v-for="attribute in sortedAttributes"
            :key="attribute.name"
            class="attribute-row"
        >
          <span class="attribute-name">{{ attribute.name }}</span>
          <AttributeBar
              :current="attribute.current"
              :max="attribute.max"
              :type="attribute.name"
          />
        </div>
      </div>
      <!-- System Info Section -->
      <div v-if="extended" class="player-system-info">
        <div class="player-system-info-item">
          <span class="player-system-info-label">ID:</span>
          <span class="player-system-info-value" @click="copyToClipboard(player?.id || '')" title="Click to copy">
            {{ player?.id || '' }}
          </span>
        </div>
        <div class="player-system-info-item">
          <span class="player-system-info-label">Position:</span>
          <span class="player-system-info-value" @click="copyToClipboard(player?.position || '')" title="Click to copy">
            {{ player?.position || '' }}
          </span>
        </div>
        <!-- System Tags -->
        <div class="player-system-info-item">
          <span class="player-system-info-label">Tags:</span>
          <span v-for="tag in player?.tags || []" :key="tag" class="player-system-info-value">{{ tag }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AttributeBar from "./AttributeBar.vue";
import CoordinatesDisplay from "@/components/Map/Coordinates.vue";

export default {
  name: "PlayerComponent",
  components: {
    CoordinatesDisplay,
    AttributeBar,
  },
  props: {
    player: {
      type: Object,
      required: false,
      default: () => ({
        name: 'Unknown',
        rank_grade: 0,
        dimension: 0,
        attributes: [],
        tags: [],
        id: '',
        position: ''
      }),
    },
    playerImage: {
      type: String,
      required: false,
      default: '',
    },
    extended: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    sortedAttributes() {
      const order = ["Health", "Energy", "Action Points"];
      if (!this.player || !this.player.attributes || !this.player.attributes.length) {
        return [];
      }
      return this.player.attributes.sort(
          (a, b) => order.indexOf(a.name) - order.indexOf(b.name)
      );
    },
  },
  methods: {
    copyToClipboard(value) {
      navigator.clipboard.writeText(value);
    },
  },
};
</script>

<style scoped>
/* Player Component Container */
.player-component {
  display: flex;
  align-items: center;
  width: 18rem;
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  padding: 0.75rem;
  box-sizing: border-box;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  gap: 0.75rem;
}

/* Player Image */
.player-image {
  width: 5rem;
  height: 5rem;
  border-radius: 0.5rem;
  background-size: cover;
  background-position: center;
}

/* Player Info */
.player-info {
  display: flex;
  flex-direction: column;
  flex: 1;
  font-size: 0.85rem;
}

/* Player Name */
.player-name {
  font-size: 1rem;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.25rem;
}

/* Player Metadata */
.player-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.5rem;
}

/* Player Attributes */
.player-attributes {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.attribute-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Attribute Name */
.attribute-name {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
  flex: 0 0 4rem;
}

/* System Info Section */
.player-system-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-top: 0.5rem;
}

.player-system-info-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
}

.player-system-info-value {
  cursor: pointer;
  color: #ffcc00;
  text-decoration: underline;
}

.player-system-info-value:hover {
  color: #ffaa00;
}
</style>
