<template>
  <div class="action-log-character-filter">
    <div class="filter-header">
      <h4>Character Filters</h4>
      <div class="filter-controls">
        <button
          class="add-filter-button"
          @click="openCharacterSelector"
          :disabled="selectedCharacterIds.length >= maxFilters"
        >
          + Add Character Filter
        </button>
        <button
          class="reset-filters-button"
          @click="resetAllFilters"
          v-if="selectedCharacterIds.length > 0"
        >
          Reset All
        </button>
      </div>
    </div>

    <div class="active-filters" v-if="selectedCharacterIds.length > 0">
      <div
        v-for="characterId in selectedCharacterIds"
        :key="characterId"
        class="filter-tag"
      >
        <AvatarImage
          :char-id="characterId"
          :gm-mode="true"
          class="filter-avatar"
        />
        <CharacterInlineDetails
          :char-id="characterId"
          :gm-mode="true"
          class="filter-character-info"
        />
        <button
          class="remove-filter-button"
          @click="removeFilter(characterId)"
          title="Remove filter"
        >
          ×
        </button>
      </div>
    </div>

    <div class="filter-info" v-if="selectedCharacterIds.length > 0">
      <span class="filter-count">{{ selectedCharacterIds.length }}/{{ maxFilters }} filters active</span>
    </div>

    <!-- Character Selector Modal -->
    <div v-if="showCharSelector" class="modal-overlay" @click="closeCharacterSelector">
      <div class="modal-container" @click.stop>
        <GmCharSelector
          :characters="availableCharacters"
          @select="handleCharacterSelected"
          @close="closeCharacterSelector"
        />
      </div>
    </div>
  </div>
</template>

<script>
import AvatarImage from "@/components/Character/AvatarImage.vue";
import CharacterInlineDetails from "@/components/Character/CharacterInlineDetails.vue";
import GmCharSelector from "@/components/GameMaster/Character/GMCharSelector.vue";

export default {
  name: "ActionLogCharacterFilter",
  components: {
    AvatarImage,
    CharacterInlineDetails,
    GmCharSelector,
  },
  props: {
    characters: {
      type: Array,
      required: true,
    },
    npcCharacters: {
      type: Array,
      default: () => [],
    },
    maxFilters: {
      type: Number,
      default: 5,
    },
  },
  data() {
    return {
      selectedCharacterIds: [],
      showCharSelector: false,
    };
  },
  computed: {
    availableCharacters() {
      return this.characters.concat(this.npcCharacters);
    },
  },
  methods: {
    openCharacterSelector() {
      if (this.selectedCharacterIds.length < this.maxFilters) {
        this.showCharSelector = true;
      }
    },
    closeCharacterSelector() {
      this.showCharSelector = false;
    },
    handleCharacterSelected(characterId) {
      if (!this.selectedCharacterIds.includes(characterId) &&
          this.selectedCharacterIds.length < this.maxFilters) {
        this.selectedCharacterIds.push(characterId);
        this.emitFilterChange();
      }
      this.closeCharacterSelector();
    },
    removeFilter(characterId) {
      const index = this.selectedCharacterIds.indexOf(characterId);
      if (index > -1) {
        this.selectedCharacterIds.splice(index, 1);
        this.emitFilterChange();
      }
    },
    resetAllFilters() {
      this.selectedCharacterIds = [];
      this.emitFilterChange();
    },
    emitFilterChange() {
      this.$emit('filter-change', this.selectedCharacterIds);
    },
  },
};
</script>

<style scoped>
.action-log-character-filter {
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: rgba(28, 28, 28, 0.8);
  border: 1px solid #444;
  border-radius: 6px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.filter-header h4 {
  margin: 0;
  color: #ffcc00;
  font-size: 0.9rem;
  font-weight: bold;
}

.filter-controls {
  display: flex;
  gap: 0.5rem;
}

.add-filter-button {
  padding: 0.3rem 0.6rem;
  background: #ffcc00;
  border: none;
  border-radius: 4px;
  color: #1c1c1c;
  font-weight: bold;
  font-size: 0.75rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.add-filter-button:hover:not(:disabled) {
  background: #ffd633;
}

.add-filter-button:disabled {
  background: #666;
  color: #999;
  cursor: not-allowed;
}

.reset-filters-button {
  padding: 0.3rem 0.6rem;
  background: #dc3545;
  border: none;
  border-radius: 4px;
  color: white;
  font-weight: bold;
  font-size: 0.75rem;
  cursor: pointer;
  transition: background 0.2s ease;
}

.reset-filters-button:hover {
  background: #c82333;
}

.active-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.filter-tag {
  display: flex;
  align-items: center;
  background: rgba(255, 204, 0, 0.1);
  border: 1px solid #ffcc00;
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  gap: 0.5rem;
}

.filter-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

.filter-character-info {
  font-size: 0.75rem;
  color: #fff;
}

.remove-filter-button {
  background: none;
  border: none;
  color: #ffcc00;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  padding: 0;
  margin-left: 0.25rem;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s ease;
}

.remove-filter-button:hover {
  background: rgba(255, 204, 0, 0.2);
}

.filter-info {
  font-size: 0.7rem;
  color: #999;
  text-align: right;
}

.filter-count {
  font-style: italic;
}

/* Modal styles matching GameMasterMain.vue */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background: #2c2c2c;
  border-radius: 8px;
  padding: 1rem;
  max-width: 90vw;
  max-height: 90vh;
  overflow: auto;
  border: 2px solid #ffcc00;
}

/* Responsive design */
@media (max-width: 768px) {
  .filter-header {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }

  .filter-controls {
    justify-content: space-between;
  }

  .active-filters {
    flex-direction: column;
  }

  .filter-tag {
    justify-content: space-between;
  }
}
</style>