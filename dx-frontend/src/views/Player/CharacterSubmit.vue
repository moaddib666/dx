<template>
  <div class="character-creation" v-if="loaded">
    <!-- Step Loader -->
    <div class="step-loader">
      <div
          v-for="(step, index) in steps"
          :key="index"
          :class="['step', { active: currentStep === index, completed: index < currentStep }]"
          @click="goToStep(index)"
      >
        <span class="step-number">{{ index + 1 }}</span>
        <span class="step-label">{{ step.label }}</span>
      </div>
    </div>
    <!-- Navigation Buttons -->
    <div class="navigation-buttons">
      <CompactButton
          v-if="currentStep > 0"
          buttonType="default"
          @click="goToPreviousStep"
      >
        Back
      </CompactButton>
      <CharacterTool :character="playerData.data" @import="updatePlayerData" />
      <CompactButton
          v-if="currentStep < steps.length - 1"
          buttonType="default"
          @click="goToNextStep"
      >
        Next
      </CompactButton>
      <CompactButton
          v-if="currentStep === steps.length - 1"
          buttonType="default"
          @click="finishCreation"
      >
        Finish
      </CompactButton>
    </div>
    <!-- Step Content -->
    <div class="step-content">
      <component :is="steps[currentStep].component"
                 v-if="steps[currentStep] && steps[currentStep].component"
                 v-bind="steps[currentStep].data"
                 @back="goToPreviousStep"
                 @next="goToNextStep"
      />
    </div>


  </div>
</template>

<script>
import PathPathSelector from "@/components/Path/PathSelector.vue";
import BioComponent from "@/components/Player/Bio.vue";
import FeatureSelector from "@/components/Player/FeatureSelector.vue";
import ActionPointAllocator from "@/components/Player/ActionPointsComponent.vue";
import SchoolAndSpellSelector from "@/components/Player/SchoolAndSpellSelector.vue";
import {CharacterGameApi, CoreGameApi, ModificatorsGameApi, SchoolGameApi} from "@/api/backendService.js";
import CharacterReview from "@/components/Player/CharacterReview.vue";
import CharacterTool from "@/components/Player/Transfer.vue";
import CompactButton from "@/components/btn/CompactButton.vue";

export default {
  name: "CharacterCreation",
  components: {CompactButton, CharacterTool},
  computed: {
    loaded() {
      return this.playerData !== null && this.availablePaths !== null && this.availiableModificators !== null && this.availableStats !== null
          && this.availableSchools !== null && this.availableSpells !== null;
    },
    steps() {
      return [
        {
          label: "Bio",
          component: BioComponent,
          data: {
            name: this.playerData?.data.name, // FIXME Make this reactive as not it's not
            age: this.playerData?.data.bio.age,
            background: this.playerData?.data.bio.background,
            appearance: this.playerData?.data.bio.appearance,
            gender: this.playerData?.data.bio.gender,
            setPlayerName: (name) => {
              this.playerData.data.name = name;
            },
            setPlayerAge: (age) => {
              this.playerData.data.bio.age = age;
            },
            setPlayerGender: (gender) => {
              this.playerData.data.bio.gender = gender
            },
            setPlayerAppearance: (appearance) => {
              this.playerData.data.bio.appearance = appearance
            },
            setPlayerBackground: (background) => {
              this.playerData.data.bio.background = background
            }
          }
        },
        {
          label: "Path",
          component: PathPathSelector,
          data: {
            paths: this.availablePaths || [],
            selectedPathId: this.playerData?.data.path,
            setPlayerPathId: (pathId) => {
              this.playerData.data.path = pathId;
            }
          }
        },
        {
          label: "Features",
          component: FeatureSelector,
          data: {
            maxModificators: this.playerData?.validation.max_modificators_count || 0,
            modificators: this.availiableModificators || [],
            selectedModificators: this.playerData?.data.modificators,
            setPlayerModificators: (modificators) => {
              this.playerData.data.modificators = modificators;
            }
          }
        },
        // {
        //   label: "Stats",
        //   component: ActionPointAllocator,
        //   data: {
        //     currentPlayerStats: this.playerData?.data.stats,
        //     stats: this.availableStats,
        //     totalPoints: this.playerData?.validation.max_stats_points_count || 100,
        //     setPlayerStats: (stats) => {
        //       this.playerData.data.stats = stats;
        //     },
        //   }
        // },
        {
          label: "School & Spells",
          component: SchoolAndSpellSelector,
          data: {
            chosenPath: this.playerData?.data.path,
            schools: this.availableSchools,
            spells: this.availableSpells,
            selectedSchools: this.playerData?.data.schools,
            selectedSpells: this.playerData?.data.spells,
            maxSchools: this.playerData?.validation.max_schools_count || 0,
            maxSpells: this.playerData?.validation.max_spells_count || 0,
            setPlayerSchools: (schools) => {
              this.playerData.data.schools = schools;
              this.playerData.data.spells = [];
            },
            setPlayerSpells: (spells) => {
              this.playerData.data.spells = spells;
            }
          }
        },
        {
          label: "Character Review",
          component: CharacterReview,
          data: {
            character: this.playerData?.data,
            spellsRegistry: this.availableSpells,
            schoolsRegistry: this.availableSchools,
            modificatorsRegistry: this.availiableModificators,
            statsRegistry: this.availableStats,
            pathRegistry: this.availablePaths
          }
        }
      ];
    },
  },
  data() {
    return {
      playerData: {
        "data": {
          "name": "string",
          "tags": [],
          "bio": {
            "age": 0,
            "gender": "Male",
            "appearance": "string",
            "background": "string"
          },
          "rank": 0,
          "path": null,
          "stats": [],
          "modificators": [],
          "items": [],
          "schools": [],
          "spells": []
        },
        "validation": {
          "max_stats_points_count": 0,
          "max_modificators_count": 0,
          "max_items_count": 0,
          "max_spells_count": 0,
          "max_rank_grade": 0,
          "max_schools_count": 0
        }
      },
      availablePaths: null,
      availiableModificators: null,
      availableStats: null,
      availableSpells: null,
      availableSchools: null,
      availableItems: null,
      currentStep: 0,
    };
  },
  async mounted() {
    await this.getPlayerTemplate()
    await this.getPlayerPaths()
    await this.getPlayerModificators()
    await this.getPlayerStats()
    await this.getPlayerSpells()
    await this.getPlayerSchools()
  },
  methods: {
    updatePlayerData(data) {
      this.playerData.data = data;
      // remount the component to update the data
      const currentStep = this.currentStep;
      this.currentStep = -1;
      this.$nextTick(() => {
        this.currentStep = currentStep;
      });
    },
    goToStep(index) {
      if (index >= 0 && index < this.steps.length) {
        this.currentStep = index;
      }
    },
    goToNextStep() {
      if (this.currentStep < this.steps.length - 1) {
        this.currentStep += 1;
      }
    },
    goToPreviousStep() {
      if (this.currentStep > 0) {
        this.currentStep -= 1;
      }
    },
    async finishCreation() {
      // Handle character creation completion
      console.log("Character Creation Finished", this.steps.map(step => step.data));
      try {
        await this.submitCharacter();
        // Navigate to the player dashboard after character creation
        this.$router.push({name: 'PlayerHomeDashboard'})
      } catch (error) {
        console.error(error);
      }
    },
    async getPlayerTemplate() {
      this.playerData = (await CharacterGameApi.characterPlayerCharacterTemplateRetrieve()).data;
    },
    async getPlayerPaths() {
      this.availablePaths = (await SchoolGameApi.schoolPathsGetAllPathsRetrieve()).data;
    },
    async getPlayerModificators() {
      this.availiableModificators = (await ModificatorsGameApi.modificatorsWorldGetAllModificatorsRetrieve()).data;
    },
    async getPlayerStats() {
      this.availableStats = (await CoreGameApi.coreCharacterStatsList()).data;
    },
    async getPlayerSpells() {
      this.availableSpells = (await SchoolGameApi.schoolSchoolsGetAllSkillsRetrieve()).data;
    },
    async getPlayerSchools() {
      this.availableSchools = (await SchoolGameApi.schoolSchoolsGetAllSchoolsRetrieve()).data;
    },
    async submitCharacter() {
      await CharacterGameApi.characterPlayerImportCharacterCreate(this.playerData.data);
    }
  },
};
</script>

<style scoped>
/* Character Creation Container */
.character-creation {
  width: 100%;
  max-width: 100vw;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  padding: 1rem;
  box-sizing: border-box;
}

/* Step Loader - Mobile First Responsive */
.step-loader {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0.5rem;
  border: 1px solid rgba(127, 255, 22, 0.2);
  backdrop-filter: blur(2px);
}

/* Responsive breakpoints for step loader */
@media (min-width: 768px) {
  .step-loader {
    flex-wrap: nowrap;
    justify-content: space-around;
    padding: 1.5rem;
    gap: 1rem;
  }
}

.step {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0.25rem;
  border-radius: 0.25rem;
  min-width: 0;
  flex: 1;
}

.step:hover {
  transform: scale(1.05);
}

.step.completed .step-number {
  background: linear-gradient(45deg, #7fff16, #fada95);
  color: #000;
  box-shadow: 0 1px 4px rgba(127, 255, 22, 0.3);
}

.step.active .step-number {
  background: linear-gradient(45deg, #fada95, #7fff16);
  color: #000;
  box-shadow: 0 1px 4px rgba(250, 218, 149, 0.3);
}

.step-number {
  display: inline-block;
  width: 2rem;
  height: 2rem;
  line-height: 2rem;
  border-radius: 50%;
  background: rgba(127, 255, 22, 0.2);
  color: #fada95;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  transition: all 0.3s ease;
  border: 1px solid rgba(127, 255, 22, 0.3);
}

.step-label {
  color: rgba(250, 218, 149, 0.8);
  font-size: 0.75rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 500;
  transition: all 0.3s ease;
  word-break: break-word;
  padding-left: 0.5em;
}

.step.active .step-label {
  font-weight: 600;
  color: #fada95;
}

.step.completed .step-label {
  color: #fada95;
}

/* Responsive step sizing */
@media (min-width: 768px) {
  .step {
    padding: 0.5rem;
    flex: none;
  }

  .step-number {
    width: 2.5rem;
    height: 2.5rem;
    line-height: 2.5rem;
    font-size: 1rem;
    margin-bottom: 0.5rem;
  }

  .step-label {
    font-size: 0.875rem;
  }
}

/* Step Content - Responsive */
.step-content {
  flex: 1;
  margin: 1rem 0;
  padding: 1rem;
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  color: #fada95;
  border: 1px solid rgba(127, 255, 22, 0.2);
  backdrop-filter: blur(2px);
  overflow-y: auto;
}

/* Responsive step content */
@media (min-width: 768px) {
  .step-content {
    margin: 1.5rem 0;
    padding: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .step-content {
    margin: 2rem 0;
    padding: 2rem;
  }
}

/* Navigation Buttons - Responsive */
.navigation-buttons {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  margin-top: 1rem;
  align-items: center;
  flex-wrap: wrap;
  padding: 0 1rem;
}

/* Responsive navigation spacing */
@media (min-width: 768px) {
  .navigation-buttons {
    gap: 1rem;
    margin-top: 1.5rem;
    padding: 0;
  }
}

@media (min-width: 1024px) {
  .navigation-buttons {
    gap: 1.5rem;
    margin-top: 2rem;
  }
}

/* Simplified button styles */
button {
  padding: 0.5rem 1rem;
  border: 1px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(0, 0, 0, 0.3);
  color: #fada95;
  backdrop-filter: blur(2px);
  min-width: 80px;
}

/* Responsive button sizing */
@media (min-width: 768px) {
  button {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    min-width: 100px;
  }
}

button:hover {
  background: rgba(127, 255, 22, 0.1);
  border-color: rgba(127, 255, 22, 0.5);
}

button:active {
  transform: scale(0.98);
}
</style>
