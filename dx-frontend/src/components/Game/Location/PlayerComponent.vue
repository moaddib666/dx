<template>
  <div class="player-component">
    <!-- Player Image Section -->
    <div :style="{ backgroundImage: `url(${playerImage})` }" class="player-image"></div>

    <!-- Player Info Section -->
    <div class="player-info">
      <div class="player-name">{{ player.name }}</div>
      <div class="player-rank">Rank: {{ player.rank_grade }}</div>
      <div class="player-dimension">Dimension: {{ player.dimension }}</div>

      <!-- Attributes Section -->
      <div class="player-attributes">
        <div
            v-for="attribute in sortedAttributes"
            :key="attribute.name"
            class="attribute"
        >
          <div class="attribute-name">{{ attribute.name }}</div>
          <AttributeBar
              :current="attribute.current"
              :max="attribute.max"
              :type="attribute.name"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AttributeBar from "./AttributeBar.vue";

export default {
  name: "PlayerComponent",
  components: {
    AttributeBar,
  },
  props: {
    player: {
      type: Object,
      required: true,
    },
    playerImage: {
      type: String,
      required: true,
    },
  },
  computed: {
    sortedAttributes() {
      const order = ["Health", "Energy", "Action Points"];
      return this.player.attributes.sort(
          (a, b) => order.indexOf(a.name) - order.indexOf(b.name)
      );
    },
  },
};
</script>

<style scoped>
/* Player Component Container */
.player-component {
  display: flex;
  align-items: flex-start;
  width: 20rem; /* Adjust as needed */
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
  box-sizing: border-box;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

/* Player Image */
.player-image {
  width: 6rem;
  height: 6rem;
  border-radius: 0.5rem;
  background-size: cover;
  background-position: center;
  margin-right: 1rem;
}

/* Player Info */
.player-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

/* Player Name */
.player-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.5rem;
}

/* Player Rank */
.player-rank,
.player-dimension {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.3rem;
}

/* Player Attributes */
.player-attributes {
  margin-top: 0.5rem;
}

.attribute {
  margin-bottom: 0.5rem;
}

/* Attribute Name */
.attribute-name {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 0.2rem;
}
</style>
