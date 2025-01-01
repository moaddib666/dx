<template>
  <div class="vertical-player-list">
    <CharacterInlineCard
        v-for="item in gameObjects"
        :key="item.id"
        :icon="item.biography.avatar"
        :name="item.name"
        @click="selectItem(item.id)"
        class="player-item"
    />
  </div>
</template>

<script>

import CharacterInlineCard from "@/components/Game/Location/CharacterInlineCard.vue";

export default {
  name: "VerticalPlayerList",
  components: {
    CharacterInlineCard,
  },
  props: {
    gameObjects: {
      type: Array,
      required: true, // Array of player data
    },
  },
  methods: {
    selectItem(id) {
      this.$emit("item-selected", id); // Emit selected item's ID
    },
  },
};
</script>

<style scoped>
.vertical-player-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem; /* Space between items */
  max-height: 100%; /* Restrict height */
  overflow-y: auto; /* Scrollable if content exceeds height */
  padding: 0.5rem; /* Add padding around the list */
  box-sizing: border-box;
  background: rgba(0, 0, 0, 0.6); /* Optional background styling */
  border-radius: 0.5rem;
}

/* Styling for each player item */
.player-item {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.player-item:hover {
  transform: scale(1.05); /* Slightly enlarge on hover */
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5); /* Glow effect */
}

/* Responsive Design */
@media (max-width: 768px) {
  .vertical-player-list {
    gap: 0.3rem; /* Smaller gap for smaller screens */
    padding: 0.3rem;
  }

  .player-item {
    transform: scale(0.9); /* Reduce item size for smaller screens */
  }
}
</style>
