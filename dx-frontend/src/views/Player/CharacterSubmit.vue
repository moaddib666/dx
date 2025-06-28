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
      <GlassButton
          v-if="currentStep > 0"
          buttonType="default"
          @click="goToPreviousStep"
      >
        Back
      </GlassButton>
      <CharacterTool :character="playerData.data" @import="updatePlayerData" />
      <GlassButton
          v-if="currentStep < steps.length - 1"
          buttonType="default"
          @click="goToNextStep"
      >
        Next
      </GlassButton>
      <GlassButton
          v-if="currentStep === steps.length - 1"
          buttonType="default"
          @click="finishCreation"
      >
        Finish
      </GlassButton>
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
import GlassButton from "@/components/btn/Glass.vue";

export default {
  name: "CharacterCreation",
  components: {GlassButton, CharacterTool},
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
/* Step Loader */
.step-loader {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #2d2d2d;
  border-radius: 8px;
}

.step {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.step.completed .step-number {
  background-color: #4caf50; /* Green for completed steps */
}

.step.active .step-number {
  background-color: #2196f3; /* Blue for the active step */
}

.step-number {
  display: inline-block;
  width: 30px;
  height: 30px;
  line-height: 30px;
  border-radius: 50%;
  background-color: #757575;
  color: white;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}

.step-label {
  color: #ddd;
  font-size: 14px;
}

.step.active .step-label {
  font-weight: bold;
  color: white;
}

/* Step Content */
.step-content {
  margin: 20px 0;
  padding: 20px;
  border-radius: 8px;
  background-color: #222;
  color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Navigation Buttons */
.navigation-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  align-items: center;
  justify-items: center;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button {
  background-color: #757575;
  color: white;
}

.back-button:hover {
  background-color: #616161;
}

.next-button, .finish-button {
  background-color: #2196f3;
  color: white;
}

.next-button:hover, .finish-button:hover {
  background-color: #1976d2;
}
</style>
