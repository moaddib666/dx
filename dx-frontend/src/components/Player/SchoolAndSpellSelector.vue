<template>
  <div v-if="schools && spells" class="school-and-spell-selector">
    <!-- Description Section -->
<!--    <div class="description">-->
<!--      <h2>Guidance</h2>-->
<!--      <p>-->
<!--        As a Yang Seeker, you can align with up to <strong>{{ maxSchools }}</strong> schools of knowledge and harness the power of <strong>{{ maxSpells }}</strong> spells. Each school represents a unique philosophy and mastery over the Flow, shaping your abilities and your destiny.-->
<!--        Choose carefully—your selections will define your path, enhance your strengths, and unlock your potential to face the challenges ahead. The balance you create will determine your success in this ever-shifting world.-->
<!--      </p>-->
<!--    </div>-->

    <!-- School List -->
    <div class="school-list" v-if="chosenPath">
      <h2>{{ t('playerComponents.schoolAndSpellSelector.schools') }}</h2>
      <div
          v-for="school in filteredSchools"
          :key="school.id"
          :class="['school-item', { selected: selectedSchools.includes(school.id) }]"
          @click="toggleSchool(school.id)"
      >
        <img :alt="school.name" :src="school.icon" class="school-icon" />
        <div v-if="!school.is_default" class="default-school-label">
          <div class="school-details">
            <h3>{{ school.name }}</h3>
            <p>{{ school.description }}</p>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="placeholder">
      <p>{{ t('playerComponents.schoolAndSpellSelector.selectPath') }}</p>
    </div>

    <!-- Spell List -->
    <div v-if="selectedSchools.length > 0" class="spell-list">
      <h2>{{ t('playerComponents.schoolAndSpellSelector.spells') }}</h2>
      <div
          v-for="school in selectedSchoolsDetails"
          :key="school.id"
          class="spell-group"
      >
        <h3>{{ school.name }}</h3>
        <div class="spell-group-list">
          <div
              v-for="spell in getSpellsForSchool(school.id)"
              :key="spell.id"
              :class="['spell-item', { disabled: spell.grade < playerRank, selected: selectedSpells.includes(spell.id) }]"
              @click="spell.grade < playerRank ? null : toggleSpell(spell.id)"
          >
            <SkillIcon :skill="spell" :fade="spell.grade < playerRank"/>
            <!--            <span>{{ spell.name }}</span>-->
            <!--            <div-->
            <!--                class="spell-hover"-->
            <!--                @mouseenter="tooltipSpell = spell.id"-->
            <!--                @mouseleave="tooltipSpell = null"-->
            <!--            >-->
            <!--              <span-->
            <!--                  v-if="tooltipSpell === spell.id"-->
            <!--                  class="tooltip"-->
            <!--              >-->
            <!--                {{ spell.description }}-->
            <!--              </span>-->
            <!--            </div>-->
          </div>
        </div>
      </div>
      <p v-if="selectedSpells.length >= maxSpells" class="spell-limit-warning">
        {{ t('playerComponents.schoolAndSpellSelector.spellLimitWarning', { maxSpells: maxSpells }) }}
      </p>
    </div>
  </div>

</template>

<script>
import SkillIcon from "@/components/Action/ActionIcon.vue";
import { useI18n } from 'vue-i18n';

export default {
  name: "SchoolAndSpellSelector",
  components: {SkillIcon},
  setup() {
    const { t } = useI18n();
    return { t };
  },
  props: {
    maxSpells: {
      type: Number,
      required: true,
      default: 1,
    },
    maxSchools: {
      type: Number,
      required: true,
      default: 1,
    },
    chosenPath: {
      type: String,
      required: true,
    },
    playerRank: {
      type: Number,
      required: true,
      default: 9,
    },
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
    selectedSchools: {
      type: Array,
      default: () => [],
    },
    selectedSpells: {
      type: Array,
      default: () => [],
    },
    setPlayerSchools: {
      type: Function,
      required: true,
    },
    setPlayerSpells: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
      tooltipSpell: null, // Tracks hovered spell ID for tooltips
    };
  },
  computed: {
    filteredSchools() {
      // Filters schools by the chosen path
      return this.schools.filter(
          (school) => school.path.includes(this.chosenPath) && !school.is_base
      );
    },
    selectedSchoolsDetails() {
      // Returns details of selected schools
      return this.filteredSchools.filter((school) =>
          this.selectedSchools.includes(school.id)
      );
    },
  },
  methods: {
    toggleSchool(schoolId) {
      let updatedSchools;
      if (this.selectedSchools.includes(schoolId)) {
        updatedSchools = this.selectedSchools.filter((id) => id !== schoolId);
      } else if (this.selectedSchools.length < this.maxSchools) {
        updatedSchools = [...this.selectedSchools, schoolId];
      } else {
        return;
      }
      this.setPlayerSchools(updatedSchools);
    },
    toggleSpell(spellId) {
      let updatedSpells;
      if (this.selectedSpells.includes(spellId)) {
        updatedSpells = this.selectedSpells.filter((id) => id !== spellId);
      } else if (this.selectedSpells.length < this.maxSpells) {
        updatedSpells = [...this.selectedSpells, spellId];
      } else {
        return;
      }
      this.setPlayerSpells(updatedSpells);
    },
    getSpellsForSchool(schoolId) {
      return this.spells.filter((spell) => spell.school === schoolId);
    },
  },
};
</script>

<style scoped>
/* School and Spell Selector - Responsive */
.school-and-spell-selector {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  border-radius: 0.5rem;
  background: transparent;
  color: #fada95;
  min-height: 60vh;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  width: 100%;
  box-sizing: border-box;
}

/* Responsive layout - two columns on larger screens */
@media (min-width: 768px) {
  .school-and-spell-selector {
    flex-direction: row;
    gap: 1.5rem;
    padding: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .school-and-spell-selector {
    gap: 2rem;
    padding: 2rem;
  }
}

.placeholder {
  text-align: center;
  color: rgba(250, 218, 149, 0.8);
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  padding: 2rem;
}

/* School List - Responsive */
.school-list {
  flex: 1;
  padding: 1rem;
  border: 1px solid rgba(127, 255, 22, 0.2);
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  box-sizing: border-box;
  max-height: 80vh;
}

/* Responsive school list padding */
@media (min-width: 768px) {
  .school-list {
    padding: 1.25rem;
  }
}

@media (min-width: 1024px) {
  .school-list {
    padding: 1.5rem;
  }
}

h2 {
  margin-bottom: 1rem;
  text-align: center;
  font-size: 1.25rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

/* Responsive heading */
@media (min-width: 768px) {
  h2 {
    font-size: 1.4rem;
    margin-bottom: 1.25rem;
  }
}

@media (min-width: 1024px) {
  h2 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }
}

.school-item {
  display: flex;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 0.75rem;
  border: 1px solid rgba(127, 255, 22, 0.2);
  box-sizing: border-box;
  position: relative;
}

/* Responsive school item */
@media (min-width: 768px) {
  .school-item {
    gap: 1rem;
    padding: 1rem;
    margin-bottom: 1rem;
  }
}

.school-item:hover {
  transform: translateY(-1px);
  background: rgba(127, 255, 22, 0.05);
  border-color: rgba(127, 255, 22, 0.5);
}

.school-item.selected {
  background: rgba(127, 255, 22, 0.1);
  border-color: #7fff16;
}

.school-icon {
  position: absolute;
  height: 100%;
  width: 40%;
  object-fit: cover;
  right: 0;
  top: 0;
  mask: linear-gradient(to left, rgba(0, 0, 0, 0.8) 60%, rgba(0, 0, 0, 0) 100%);
  z-index: 0;
}

.school-details h3 {

  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

/* Responsive school details */
@media (min-width: 768px) {
  .school-details h3 {
    font-size: 1.1rem;
  }
}

@media (min-width: 1024px) {
  .school-details h3 {
    font-size: 1.2rem;
  }
}

.school-details p {
  font-size: 0.8rem;
  color: rgba(250, 218, 149, 0.8);
  line-height: 1.4;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

/* Responsive school description */
@media (min-width: 768px) {
  .school-details p {
    font-size: 0.85rem;
  }
}

@media (min-width: 1024px) {
  .school-details p {
    font-size: 0.9rem;
  }
}

/* Spell List - Responsive */
.spell-list {
  flex: 2;
  padding: 1rem;
  border: 1px solid rgba(127, 255, 22, 0.2);
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  box-sizing: border-box;
}

/* Responsive spell list padding */
@media (min-width: 768px) {
  .spell-list {
    padding: 1.25rem;
  }
}

@media (min-width: 1024px) {
  .spell-list {
    padding: 1.5rem;
  }
}

.spell-group {
  margin-bottom: 1.5rem;
}

/* Responsive spell group spacing */
@media (min-width: 768px) {
  .spell-group {
    margin-bottom: 2rem;
  }
}

.spell-group h3 {
  font-size: 1rem;
  color: #fada95;
  margin-bottom: 0.75rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

/* Responsive spell group heading */
@media (min-width: 768px) {
  .spell-group h3 {
    font-size: 1.1rem;
    margin-bottom: 1rem;
  }
}

@media (min-width: 1024px) {
  .spell-group h3 {
    font-size: 1.2rem;
  }
}

.spell-group-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
  gap: 0.75rem;
}

/* Responsive spell grid */
@media (min-width: 768px) {
  .spell-group-list {
    grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
    gap: 1rem;
  }
}

@media (min-width: 1024px) {
  .spell-group-list {
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  }
}

.spell-item {
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 1;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(127, 255, 22, 0.2);
  box-sizing: border-box;
}

.spell-item:hover {
  transform: translateY(-1px);
  border-color: rgba(127, 255, 22, 0.5);
}

.spell-item.disabled {
  background: rgba(100, 100, 100, 0.2);
  cursor: not-allowed;
  opacity: 0.4;
  border-color: rgba(127, 255, 22, 0.1);
}

.spell-item.selected {
  background: rgba(127, 255, 22, 0.1);
  border-color: #7fff16;
}

.spell-item span {
  font-size: 0.7rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

/* Responsive spell item text */
@media (min-width: 768px) {
  .spell-item span {
    font-size: 0.75rem;
  }
}

@media (min-width: 1024px) {
  .spell-item span {
    font-size: 0.8rem;
  }
}

/* Tooltip */
.spell-hover .tooltip {
  position: absolute;
  top: -50px;
  background: rgba(0, 0, 0, 0.9);
  color: #fada95;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
  white-space: nowrap;
  z-index: 10;
  opacity: 0;
  transition: opacity 0.3s ease;
  border: 1px solid rgba(127, 255, 22, 0.3);
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.spell-hover:hover .tooltip {
  opacity: 1;
}

.spell-limit-warning {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #ff6b6b;
  text-align: center;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 500;
}

.description {
  text-align: center;
  padding: 1.5rem 2rem;
  margin-bottom: 1rem;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 0.5rem;
  font-size: 1rem;
  color: rgba(250, 218, 149, 0.8);
  display: flex;
  flex: 1;
  border: 2px solid rgba(127, 255, 22, 0.3);
  backdrop-filter: blur(2px);
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.description p {
  margin: 0.5rem 0;
  line-height: 1.5;
}

.description strong {
  color: #7fff16;
}

</style>
