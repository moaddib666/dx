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
  gap: 2rem;
  padding: 2rem;
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  height: 50vh;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  border: 2px solid rgba(127, 255, 22, 0.3);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
}

/* Flow border effect */
.school-and-spell-selector::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 0.5rem;
  background: linear-gradient(45deg,
    transparent,
    rgba(127, 255, 22, 0.05),
    transparent,
    rgba(127, 255, 22, 0.05),
    transparent
  );
  background-size: 300% 300%;
  animation: flowBorder 8s ease-in-out infinite;
  opacity: 0.3;
  pointer-events: none;
}

@keyframes flowBorder {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.placeholder {
  text-align: center;
  color: rgba(250, 218, 149, 0.8);
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  position: relative;
  z-index: 2;
}

/* School List */
.school-list {
  flex: 1;
  padding: 1.5rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  overflow-y: auto;
  max-height: 100%;
  backdrop-filter: blur(2px);
  position: relative;
  z-index: 2;
}

h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.5rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

.school-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 1rem;
  border: 2px solid rgba(127, 255, 22, 0.2);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
}

/* Flow border effect for school items */
.school-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 0.5rem;
  background: linear-gradient(45deg,
    transparent,
    rgba(127, 255, 22, 0.1),
    transparent,
    rgba(127, 255, 22, 0.1),
    transparent
  );
  background-size: 300% 300%;
  animation: flowBorder 6s ease-in-out infinite;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.school-item:hover {
  transform: translateY(-2px);
  background: rgba(127, 255, 22, 0.05);
  border-color: rgba(127, 255, 22, 0.5);
  box-shadow: 0 4px 15px rgba(127, 255, 22, 0.2);
}

.school-item:hover::before {
  opacity: 1;
}

.school-item.selected {
  background: rgba(127, 255, 22, 0.1);
  border-color: #7fff16;
  box-shadow: 0 4px 15px rgba(127, 255, 22, 0.4);
}

.school-item.selected::before {
  opacity: 1;
}

.school-icon {
  width: 60px;
  height: 60px;
  border-radius: 0.5rem;
  object-fit: cover;
  border: 2px solid rgba(127, 255, 22, 0.3);
  position: relative;
  z-index: 2;
}

.school-details {
  position: relative;
  z-index: 2;
}

.school-details h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

.school-details p {
  font-size: 0.9rem;
  color: rgba(250, 218, 149, 0.8);
  line-height: 1.4;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

/* Spell List */
.spell-list {
  flex: 2;
  padding: 1.5rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  overflow-y: auto;
  max-height: 100%;
  backdrop-filter: blur(2px);
  position: relative;
  z-index: 2;
}

.spell-group {
  margin-bottom: 2rem;
}

.spell-group h3 {
  font-size: 1.2rem;
  color: #fada95;
  margin-bottom: 1rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

.spell-group-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.spell-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 0.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  border: 2px solid rgba(127, 255, 22, 0.2);
  backdrop-filter: blur(2px);
  overflow: hidden;
}

/* Flow border effect for spell items */
.spell-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 0.5rem;
  background: linear-gradient(45deg,
    transparent,
    rgba(127, 255, 22, 0.1),
    transparent,
    rgba(127, 255, 22, 0.1),
    transparent
  );
  background-size: 300% 300%;
  animation: flowBorder 6s ease-in-out infinite;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.spell-item:hover::before {
  opacity: 1;
}

.spell-item:hover {
  transform: translateY(-2px);
  border-color: rgba(127, 255, 22, 0.5);
  box-shadow: 0 4px 15px rgba(127, 255, 22, 0.2);
}

.spell-item.disabled {
  background: rgba(100, 100, 100, 0.2);
  cursor: not-allowed;
  opacity: 0.4;
  border-color: rgba(127, 255, 22, 0.1);
}

.spell-item.selected {
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-2px);
  border-color: #7fff16;
  box-shadow: 0 4px 15px rgba(127, 255, 22, 0.4);
}

.spell-item.selected::before {
  opacity: 1;
}

.spell-item span {
  font-size: 0.8rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  position: relative;
  z-index: 2;
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
