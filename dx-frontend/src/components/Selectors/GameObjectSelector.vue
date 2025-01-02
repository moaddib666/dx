<template>
  <div class="game-object-selector">
    <div class="selected" @click="toggleDropdown">
      <CharacterInlineCard
          :icon="selectedObject?.icon || placeholderIcon"
          :name="selectedObject?.name || 'Select Object'"
      />
    </div>
    <div v-if="isDropdownOpen" class="dropdown">
      <CharacterInlineCard
          v-for="item in gameObjects"
          :key="item.id"
          :icon="item.icon"
          :name="item.name"
          @click="selectItem(item.id)"
      />
    </div>
  </div>
</template>

<script>

import CharacterInlineCard from "@/components/Game/Location/CharacterInlineCard.vue";

export default {
  name: "GameObjectSelector",
  components: {CharacterInlineCard},
  props: {
    gameObjects: {
      type: Array,
      required: true,
    },
    selectedId: {
      type: String,
      default: null,
    },
    placeholderIcon: {
      type: String,
      default: "https://via.placeholder.com/150", // Fallback icon
    },
  },
  data() {
    return {
      isDropdownOpen: false,
    };
  },
  computed: {
    selectedObject() {
      return this.gameObjects.find((item) => item.id === this.selectedId) || null;
    },
  },
  methods: {
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    selectItem(id) {
      this.$emit("update:selectedId", id); // Emit the selected ID to the parent
      this.isDropdownOpen = false; // Close the dropdown
    },
  },
};
</script>

<style scoped>
.game-object-selector {
  position: relative;
  width: 14rem; /* Adjust width as needed */
  cursor: pointer;
}

/* Selected Item */
.selected {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.3rem;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

/* Dropdown List */
.dropdown {
  position: absolute;
  top: 100%;
  left: 1rem; /* Adjust dropdown position */
  z-index: 100;
  width: 100%;
  max-height: 15rem; /* Limit dropdown height */
  overflow-y: auto; /* Scroll if too many items */
}

/* Dropdown Items */
.dropdown > * {
  margin: 0.5rem 0; /* Spacing between items */
}
</style>
