<template>
  <div class="character-card-holder">
    <button v-if="canScrollLeft" class="scroll-btn left" @click="scrollLeft">
      ←
    </button>
    <div ref="cardRow" class="character-card-row">
      <CharacterCard
          v-for="character in visibleCharacters"
          :key="character.id"
          :class="{ selected: character.id === selectedCharacterId }"
          :icon="character.biography.avatar"
          :name="character.name"
          :details="getCharDetails(character.id)"
          @click="selectCharacter(character.id)"
      />
    </div>
    <button v-if="canScrollRight" class="scroll-btn right" @click="scrollRight">
      →
    </button>
  </div>
</template>

<script>
import CharacterCard from './CharacterCard.vue';

export default {
  name: "CharacterCardHolder",
  components: { CharacterCard },
  props: {
    characters: { type: Array, required: true },
    selectedCharacterId: { type: String, default: null },
    visibleCount: { type: Number, default: 8 },
    /* additionalCharactersData:
     * Additional character data to be displayed in the character card details
     * @type {Object}
     * {"f3c4216f-cbaa-4792-b6e6-1cedd502defe":{
     *     "id": "f3c4216f-cbaa-4792-b6e6-1cedd502defe",
     *     "name": "The Veiled Arbiter",
     *     "rank_grade": 2,
     *     "attributes": [
     *         {
     *             "name": "Health",
     *             "current": 59,
     *             "max": 90
     *         },
     *         {
     *             "name": "Energy",
     *             "current": 130,
     *             "max": 166
     *         },
     *         {
     *             "name": "Action Points",
     *             "current": 1196,
     *             "max": 12
     *         }
     *     ],
     *     "dimension": 1,
     *     "position": "00000000-0000-0000-0000-0193cb146bce",
     *     "coordinates": {
     *         "x": 2,
     *         "y": 1,
     *         "z": 1
     *     }
     * }}
     */
    additionalCharactersData: { type: Object, default: () => ({}) },
  },
  data() {
    return { scrollIndex: 0 };
  },
  computed: {
    visibleCharacters() {
      return this.characters.slice(this.scrollIndex, this.scrollIndex + this.visibleCount);
    },
    canScrollLeft() {
      return this.scrollIndex > 0;
    },
    canScrollRight() {
      return this.scrollIndex + this.visibleCount < this.characters.length;
    },
  },
  methods: {
    getCharDetails(charId) {
      return this.additionalCharactersData[charId] || {};
    },
    scrollLeft() {
      this.scrollIndex = Math.max(0, this.scrollIndex - this.visibleCount);
    },
    scrollRight() {
      this.scrollIndex = Math.min(
          this.characters.length - this.visibleCount,
          this.scrollIndex + this.visibleCount
      );
    },
    selectCharacter(id) {
      this.$emit("characterSelected", id);
    },
  },
};
</script>

<style scoped>
.character-card-holder {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.6);
  border: 0.1rem solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  overflow: hidden;
}

/* Scroll buttons using rem units */
.scroll-btn {
  background: rgba(255, 255, 255, 0.4);
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 2rem;
  height: 2rem;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  transition: background 0.2s ease;
}

.scroll-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.scroll-btn.left {
  position: absolute;
  left: 0.5rem;
}

.scroll-btn.right {
  position: absolute;
  right: 0.5rem;
}

/* Card row styles */
.character-card-row {
  display: flex;
  gap: 1rem;
  overflow: hidden;
  width: 100%;
  justify-content: center;
  align-items: center;
}

/* Responsive adjustments */
@media (max-width: 48em) {
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
