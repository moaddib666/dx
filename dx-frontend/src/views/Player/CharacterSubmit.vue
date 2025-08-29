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

    <!-- Step Content -->
    <div class="step-content">
      <component :is="steps[currentStep].component"
                 v-if="steps[currentStep] && steps[currentStep].component"
                 v-bind="steps[currentStep].data"
                 @back="goToPreviousStep"
                 @next="goToNextStep"
      />
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
  </div>
</template>

<script>
import PathSelector from "@/components/Path/Selector.vue";
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
          component: PathSelector,
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
  flex: 1;
  display: flex;
  flex-direction: column;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
}

/* Step Loader */
.step-loader {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 0.5rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
}

/* Flow border effect for step loader */
.step-loader::before {
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
  opacity: 0.5;
  pointer-events: none;
}

@keyframes flowBorder {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.step {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
  padding: 0.5rem;
  border-radius: 0.25rem;
}

.step:hover {
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-2px);
}

.step.completed .step-number {
  background: linear-gradient(45deg, #7fff16, #fada95);
  color: #000;
  box-shadow: 0 2px 8px rgba(127, 255, 22, 0.4);
}

.step.active .step-number {
  background: linear-gradient(45deg, #fada95, #7fff16);
  color: #000;
  box-shadow: 0 2px 8px rgba(250, 218, 149, 0.4);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.step-number {
  display: inline-block;
  width: 40px;
  height: 40px;
  line-height: 40px;
  border-radius: 50%;
  background: rgba(127, 255, 22, 0.2);
  color: #fada95;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  transition: all 0.3s ease;
  border: 2px solid rgba(127, 255, 22, 0.3);
}

.step-label {
  color: rgba(250, 218, 149, 0.8);
  font-size: 14px;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 500;
  transition: all 0.3s ease;
}

.step.active .step-label {
  font-weight: 600;
  color: #fada95;
}

.step.completed .step-label {
  color: #fada95;
}

/* Step Content */
.step-content {
  margin: 2rem 0;
  padding: 2rem;
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(127, 255, 22, 0.3);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
}

/* Flow border effect for step content */
.step-content::before {
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

/* Navigation Buttons */
.navigation-buttons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2rem;
  align-items: center;
  flex-wrap: wrap;
}

/* Override default button styles */
button {
  padding: 0.75rem 2rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 25px;
  font-size: 16px;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  backdrop-filter: blur(2px);
}

button:hover {
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(127, 255, 22, 0.4);
  border-color: #7fff16;
}

button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 5px rgba(127, 255, 22, 0.2);
}

.back-button {
  background: rgba(0, 0, 0, 0.4);
  color: rgba(250, 218, 149, 0.8);
  border-color: rgba(127, 255, 22, 0.2);
}

.back-button:hover {
  background: rgba(127, 255, 22, 0.05);
  color: #fada95;
  border-color: rgba(127, 255, 22, 0.4);
}

.next-button, .finish-button {
  background: linear-gradient(45deg, rgba(250, 218, 149, 0.1), rgba(127, 255, 22, 0.1));
  color: #fada95;
  border-color: #7fff16;
}

.next-button:hover, .finish-button:hover {
  background: linear-gradient(45deg, rgba(250, 218, 149, 0.2), rgba(127, 255, 22, 0.2));
  box-shadow: 0 4px 15px rgba(127, 255, 22, 0.4);
}
</style>
