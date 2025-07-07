<template>
  <div class="character-card-holder">
      <CharacterCard
          v-for="character in characters"
          :key="character.id"
          :class="{ selected: character.id === selectedCharacterId }"
          :icon="character.biography?.avatar || ''"
          :name="character.name"
          :details="getCharDetails(character.id)"
          @click="selectCharacter(character.id)"
      />
  </div>
</template>

<script>
import CharacterCard from '@/components/CharacterCard/CharacterCard.vue';

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
    /**
     * Additional character data to be displayed in the character card details
     * @type {Object}
     * {"3f7d8e07-cf63-45fd-a9b0-19568b64234f":{"name":"Ororon","rankGrade":9,"dimension":1,"path":{"name":"xx","icon":null},"attributes":{"energy":{"current":150,"max":150},"health":{"current":75,"max":75}, "action_points":{"current":1,"max":10}}}}
     */
    additionalCharactersData: {
      type: Object,
      required: false,
    }
  },
  data() {
    return {};
  },
  computed: {},
  methods: {
    getCharDetails(charId) {
      if (this.additionalCharactersData === undefined) {
        return
      }
      return this?.additionalCharactersData[charId]
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
  overflow-x: auto;
  padding: 0.7rem;
  gap: 0.1em;
  scrollbar-width: none; /* Hide scrollbar for Firefox */
  -ms-overflow-style: none; /* Hide scrollbar for Internet Explorer and Edge */
  scrollbar-color: transparent transparent; /* Hide scrollbar for Chrome, Safari, and Opera */
  &::-webkit-scrollbar {
    display: none; /* Hide scrollbar for Chrome, Safari, and Opera */
  }
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
  width: 100%;
  scroll-snap-type: x mandatory; /* Enable horizontal snap scrolling */
  overscroll-behavior-x: contain; /* Prevents overscrolling */
  overflow-y: hidden; /* Hide vertical scrollbar */
  scroll-behavior: smooth; /* Smooth scrolling */
}

</style>
