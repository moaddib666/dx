<template>
  <div class="character-card-holder">
    <button
        v-if="canScrollLeft"
        class="scroll-btn left"
        @click="scrollLeft"
    >
      ←
    </button>
    <div ref="cardRow" class="character-card-row">
      <CharacterCard
          v-for="character in characters"
          :key="character.id"
          :class="{ selected: character.id === selectedCharacterId }"
          :icon="character.biography.avatar"
          :name="character.name"
          @click="selectCharacter(character.id)"
      />
    </div>
    <button
        v-if="canScrollRight"
        class="scroll-btn right"
        @click="scrollRight"
    >
      →
    </button>
  </div>
</template>

<script>
import CharacterCard from './CharacterCard.vue';

export default {
  name: "CharacterCardHolder",
  components: {
    CharacterCard,
  },
  props: {
    characters: {
      type: Array,
      required: true, // Array of character objects
    },
    selectedCharacterId: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      scrollPosition: 0, // Tracks current scroll position
      containerWidth: 0, // Visible container width
      totalContentWidth: 0, // Total width of all cards
    };
  },
  computed: {
    canScrollLeft() {
      return this.scrollPosition > 0;
    },
    canScrollRight() {
      return this.scrollPosition + this.containerWidth < this.totalContentWidth;
    },
  },
  methods: {
    updateDimensions() {
      const cardRow = this.$refs.cardRow;
      this.containerWidth = cardRow.offsetWidth;
      this.totalContentWidth = cardRow.scrollWidth;
    },
    scrollLeft() {
      const cardRow = this.$refs.cardRow;
      const scrollAmount = Math.min(this.scrollPosition, 200); // Adjust scroll amount as needed
      this.scrollPosition -= scrollAmount;
      cardRow.scrollBy({left: -scrollAmount, behavior: "smooth"});
    },
    scrollRight() {
      const cardRow = this.$refs.cardRow;
      const remainingScroll = this.totalContentWidth - (this.scrollPosition + this.containerWidth);
      const scrollAmount = Math.min(remainingScroll, 200); // Adjust scroll amount as needed
      this.scrollPosition += scrollAmount;
      cardRow.scrollBy({left: scrollAmount, behavior: "smooth"});
    },
    selectCharacter(id) {
      this.$emit("characterSelected", id);
    },
  },
  mounted() {
    this.updateDimensions();
    window.addEventListener("resize", this.updateDimensions); // Recalculate dimensions on window resize
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.updateDimensions);
  },
  watch: {
    characters() {
    },
  },
};
</script>

<style scoped>
/* Character Card Holder Styling */
.character-card-holder {
  display: flex;
  align-items: center;
  width: 100%;
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  padding: 0.5rem;
  box-sizing: border-box;
  position: relative;
  overflow: hidden;
  height: auto; /* Ensure no vertical scroll */
}

/* Scroll Buttons */
.scroll-btn {
  width: 2rem;
  height: 2rem;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
  border: none;
  border-radius: 50%;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.scroll-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  color: white;
}

.scroll-btn.left {
  position: absolute;
  left: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
}

.scroll-btn.right {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
}

/* Character Card Row */
.character-card-row {
  display: flex;
  flex-wrap: nowrap;
  gap: 1rem;
  overflow-x: auto; /* Horizontal scroll only */
  overflow-y: hidden; /* Prevent vertical scroll */
  width: calc(100% - 4rem); /* Account for buttons */
  padding: 0 1rem;
  scroll-behavior: smooth;
}

/* Hide Scrollbar */
.character-card-row::-webkit-scrollbar {
  display: none;
}

/* Selected Character Styling */
.selected {
  border: 0.2rem solid rgba(255, 215, 0, 1); /* Gold border for selected character */
  transform: scale(1.1);
}

/* Hover Effect for Cards */
.character-card-row > *:hover {
  transform: scale(1.05);
  transition: transform 0.2s ease-in-out;
  position: relative;
  z-index: 1;
}

/* Responsive Card Holder */
@media (max-width: 768px) {
  .character-card-holder {
    padding: 0.25rem;
  }

  .scroll-btn {
    width: 1.5rem;
    height: 1.5rem;
    font-size: 0.75rem;
  }

  .character-card-row {
    gap: 0.5rem;
  }
}
</style>
