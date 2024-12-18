<template>
  <div v-if="schools && spells" class="school-and-spell-selector">
    <!-- School List -->
    <div class="school-list">
      <h2>Schools</h2>
      <div
          v-for="school in schools"
          :key="school.id"
          :class="['school-item', { selected: selectedSchools.includes(school.id) }]"
          @click="toggleSchool(school.id)"
      >
        <img :alt="school.name" :src="school.icon" class="school-icon"/>
        <div class="school-details">
          <h3>{{ school.name }}</h3>
          <p>{{ school.description }}</p>
        </div>
      </div>
    </div>

    <!-- Spell List -->
    <div v-if="selectedSchools.length > 0" class="spell-list">
      <h2>Spells</h2>
      <div
          v-for="school in schools"
          :key="school.id"
          class="spell-group"

      >
        <div v-if="selectedSchools.includes(school.id)">
          <h3>{{ school.name }}</h3>
          <div class="spell-group-list">
            <div
                v-for="spell in getSpellsForSchool(school.id)"
                :key="spell.id"
                :class="['spell-item', { disabled: spell.grade > 1, selected: selectedSpells.includes(spell.id) }]"
                @click="spell.grade > 1 ? null : toggleSpell(spell.id)"
            >
              <span>{{ spell.name }}</span>
              <div
                  class="spell-hover"
                  @mouseenter="showTooltip(spell)"
                  @mouseleave="hideTooltip"
              >
                <span v-if="tooltipSpell === spell.id" class="tooltip">{{ spell.description }}</span>
            </div>
          </div>
        </div>
        </div>
      </div>
      <p v-if="selectedSpells.length >= 5" class="spell-limit-warning">
        Only 5 active spells can be selected.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "SchoolAndSpellSelector",
  props: {
    schools: {
      type: Array,
      required: true,
      default: () => [],
    },
    spells: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  data() {
    return {
      selectedSchools: [], // Tracks selected school IDs
      selectedSpells: [], // Tracks selected spell IDs
      tooltipSpell: null, // Tracks spell being hovered for tooltip
    };
  },
  computed: {
    filteredSpells() {
      return this.spells.filter(spell => this.selectedSchools.includes(spell.school));
    },
  },
  methods: {
    toggleSchool(schoolId) {
      if (this.selectedSchools.includes(schoolId)) {
        this.selectedSchools = this.selectedSchools.filter(id => id !== schoolId);
        // Remove spells from deselected schools
        this.selectedSpells = this.selectedSpells.filter(
            spellId => this.filteredSpells.some(spell => spell.id === spellId)
        );
      } else if (this.selectedSchools.length < 2) {
        this.selectedSchools.push(schoolId);
      }
    },
    toggleSpell(spellId) {
      if (this.selectedSpells.includes(spellId)) {
        this.selectedSpells = this.selectedSpells.filter(id => id !== spellId);
      } else if (this.selectedSpells.length < 5) {
        this.selectedSpells.push(spellId);
      }
    },
    getSpellsForSchool(schoolId) {
      return this.spells.filter(spell => spell.school === schoolId);
    },
    showTooltip(spell) {
      this.tooltipSpell = spell.id;
    },
    hideTooltip() {
      this.tooltipSpell = null;
    },
  },
};
</script>

<style scoped>
.school-and-spell-selector {
  display: flex;
  gap: 20px;
  padding: 20px;
  border-radius: 8px;
  background-color: #222;
  color: #fff;
  height: 50vh; /* Ensures the component takes the full height */
}

/* School List */
.school-list {
  flex: 1;
  padding: 10px;
  border: 1px solid #444;
  border-radius: 8px;
  background-color: #333;
  overflow-y: auto; /* Independent scroll */
  max-height: 100%; /* Prevents overflow into the page */
}

h2 {
  margin-bottom: 10px;
  text-align: center;
}

.school-item {
  display: flex;
  gap: 10px;
  padding: 10px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.school-item:hover {
  transform: translateY(-5px);
  background-color: rgba(255, 255, 255, 0.2);
}

.school-item.selected {
  background-color: rgba(33, 150, 243, 0.8);
}

.school-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  object-fit: cover;
}

.school-details h3 {
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.school-details p {
  font-size: 0.9rem;
  color: #ddd;
}

/* Spell List */
.spell-list {
  flex: 2;
  padding: 10px;
  border: 1px solid #444;
  border-radius: 8px;
  background-color: #333;
  overflow-y: auto; /* Independent scroll */
  max-height: 100%; /* Prevents overflow into the page */
}

.spell-group {
  margin-bottom: 20px;
}

.spell-group h3 {
  font-size: 1.1rem;
  color: #fff;
  margin-bottom: 10px;
}

.spell-group-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.spell-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
  position: relative;
}

.spell-item.disabled {
  background-color: rgba(100, 100, 100, 0.3);
  cursor: not-allowed;
}

.spell-item.selected {
  background-color: rgba(33, 150, 243, 0.8);
  transform: scale(1.05);
}

.spell-item span {
  font-size: 0.8rem;
  color: #fff;
}

/* Tooltip */
.spell-hover .tooltip {
  position: absolute;
  top: -50px;
  background-color: #444;
  color: #fff;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  white-space: nowrap;
  z-index: 10;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.spell-hover:hover .tooltip {
  opacity: 1;
}

.spell-limit-warning {
  margin-top: 10px;
  font-size: 0.9rem;
  color: #f44336;
  text-align: center;
}
</style>
