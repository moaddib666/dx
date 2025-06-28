<script>
import SkillDetails from "@/components/Skill/SkillDetails.vue";
import StatHolder from "@/components/Stat/StatHolder.vue";
import PlayerProfile from "@/components/Player/PlayerProfile.vue";
import SchoolSelector from "@/components/Scool/SchoolSelector.vue";
import StatsGameService from "@/services/statService.js";
import ViolationsGameService from "@/services/violationService.js";
import SchoolManagement from "@/components/Scool/SchoolManagement.vue";
import ModificatorHolder from "@/components/Modificator/ModificatorHolder.vue";
import {CharacterGameApi, ModificatorsGameApi, SchoolGameApi, SkillsGameApi} from "@/api/backendService.js";
import LandingButton from "@/components/btn/LandingButton.vue";

export default {
  name: "CharacterInfo",
  components: {
    LandingButton,
    ModificatorHolder, SchoolManagement, SchoolSelector, PlayerProfile, StatHolder, SkillDetails},
  data() {
    return {
      modificatorData: null,
      playerInfo: null,
      playerStats: null,
      pathDetails: null,
      learnedSchools: null,
      learnedSkills: null,
      loading: true,
      statService: StatsGameService,
      violationService: ViolationsGameService,
    };
  },
  computed: {
    ready() {
      return this.playerInfo && this.playerStats && this.pathDetails && this.learnedSchools && this.learnedSkills;
    },
  },
  async mounted() {
    try {
      this.loading = true;
      await this.statService.refreshStats();
      await this.violationService.refreshViolations();
      await this.syncAll();
    } catch (error) {
      console.error("Error during data synchronization:", error);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    playGame() {
      this.$router.push({name: 'Game'});
    },
    handleStatUpdate(stat) {
      alert(`Stat Updated: ${stat}`);
    },
    handleLearnSchool(school) {
      alert(`Learned School: ${school}`);
    },
    handleLearnSkill(skill) {
      alert(`Learned Skill: ${skill}`);
    },
    async syncModificators() {
      try {
        const response = await ModificatorsGameApi.modificatorsCharacterList();
        this.modificatorData = response.data;
      } catch (error) {
        console.error("Failed to fetch modificators:", error);
      }
    },
    async syncPlayer() {
      try {
        const response = await CharacterGameApi.characterPlayerCharacterDetailsRetrieve();
        this.playerInfo = response.data;
        await this.syncPathDetails()
      } catch (error) {
        console.error("Failed to fetch player info:", error);
      }
    },
    async syncStats() {
      try {
        const response = await CharacterGameApi.characterStatsList();
        this.playerStats = response.data;
      } catch (error) {
        console.error("Failed to fetch stats:", error);
      }
    },
    async syncPathDetails() {
      try {
        const response = await SchoolGameApi.schoolPathsRetrieve(this.playerInfo.path.id);
        this.pathDetails = response.data;
      } catch (error) {
        console.error("Failed to fetch path details:", error);
      }
    },
    async switchBaseStats({fromStatId, toStatId}) {
      try {
        const response = await CharacterGameApi.characterStatsSwipeBaseStatCreate({
              from_stat: fromStatId,
              to_stat: toStatId,
            }
        );
        this.playerStats = response.data;
      } catch (error) {
        console.error("Failed to fetch learned skills:", error);
      }
    },
    async syncLearnedSkills() {
      try {
        const response = await SkillsGameApi.skillsSkillsList();
        this.learnedSkills = response.data;
      } catch (error) {
        console.error("Failed to fetch learned skills:", error);
      }
    },
    async syncLearnedSchools() {
      try {
        const response = await SkillsGameApi.skillsShoolsList();
        this.learnedSchools = response.data;
      } catch (error) {
        console.error("Failed to fetch learned schools:", error);
      }
    },
    async syncAll() {
      await Promise.all([
        this.syncPlayer(),
        this.syncStats(),
        this.syncLearnedSkills(),
        this.syncLearnedSchools(),
        this.syncModificators(),
      ]);
    },
  },
};
</script>

<template>
  <div>
    <!-- Loading Indicator -->
    <div v-if="loading" class="loading-indicator">
      Loading character info...
    </div>

    <!-- Character Info Layout -->
    <div v-else-if="ready" class="layout">
      <!-- Left Side -->
      <div class="left">
        <player-profile :player="playerInfo" :modificators="modificatorData"/>
        <stat-holder :stats="playerStats" :editable="false"
                     :allowResetBaseStats="playerInfo?.resetting_base_stats"
                     @updateStat="handleStatUpdate"
                     @switchBaseStats="switchBaseStats"/>
      </div>

      <!-- Right Side -->
      <div class="right">
        <school-management
            :schools="pathDetails.schools"
            :learnedSchools="learnedSchools"
            :skills="learnedSkills"
            :activeSlots="0"
            @learn-school="handleLearnSchool"
            :path="playerInfo.path.name"
            :selected="[]"
        />
      </div>
    </div>
    <!-- Error or Not Ready -->
    <div v-else class="error-message">
      Unable to load character data. Please try again later.
    </div>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  font-size: 0.7rem;
  height: 80vh;
}

.layout .left {
  flex: 1;
  scroll-behavior: smooth;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) rgba(0, 0, 0, 0.5);
  max-height: 100%;
  min-width: 30rem;
}

.layout .right {
  flex: 2;
  scroll-behavior: smooth;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) rgba(0, 0, 0, 0.5);
  max-height: 100%;
  gap: 1rem;
}

.loading-indicator {
  text-align: center;
  font-size: 1rem;
  color: gray;
}

.error-message {
  text-align: center;
  font-size: 1rem;
  color: red;
}

.play {
  margin: 0.5rem;
  display: flex;
  justify-content: center;
}
</style>

