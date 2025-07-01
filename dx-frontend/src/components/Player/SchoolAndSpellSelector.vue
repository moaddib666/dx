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
        <div v-if="!school.is_default" class="default-school-label">
          <img :alt="school.name" :src="school.icon" class="school-icon" />
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
.school-and-spell-selector {
  display: flex;
  gap: 20px;
  padding: 20px;
  border-radius: 8px;
  background-color: #222;
  color: #fff;
  height: 50vh;
}


.placeholder {
  text-align: center;
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

.description {
  text-align: center;
  padding: 10px 20px;
  margin-bottom: 10px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  font-size: 1rem;
  color: #ddd;
  display: flex;
  flex: 1;
}

.description p {
  margin: 5px 0;
}

.description strong {
  color: #4caf50;
}

</style>
