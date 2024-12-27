<template>
  <div class="dashboard">
    <!-- Left Full Height Section -->
    <div class="left-section">
      <ActionLog :actions="actions" @refresh="refreshActions" />
    </div>
    <!-- Top Center Section -->
    <div class="top-center">
      <CharacterCardHolder
          v-if="characters && characters.length > 0"
          :characters="characters"
          @characterSelected="selectCharacter"
      />
      <CharacterCardHolder
          v-if="npcCharacters && selectedLocationId && npcCharacters.length > 0"
          :characters="npcCharacters"
          :selectedCharacterId="selectedCharacterId"
          @characterSelected="selectCharacter"
      />
    </div>



    <!-- Center Section -->
    <div class="center-section">
      <GameMasterImpact @applyImpact="handleImpact" />
    </div>

    <!-- Floating Top Right -->
    <div class="top-right">
      <CurrentTurnComponent @turnChanged="refresh" />
      <LocationIdSelector @locationSelected="selectLocationId" />
      <PlayerComponent
          v-if="selectedCharacterData && selectedCharacterInfo"
          :player="selectedCharacterData"
          :playerImage="selectedCharacterInfo.biography.avatar"
          :extended="true"
      />

    </div>

    <!-- Center Bottom -->
    <div class="bottom-center">
      <EndTurnComponent />
    </div>

    <!-- Bottom Right -->
    <div class="bottom-right">

    </div>
  </div>
</template>


<script>
import GameMasterImpact from "@/components/GameMaster/GameMasterImpact.vue";
import EndTurnComponent from "@/components/GameMaster/EndTurnComponent.vue";
import CurrentTurnComponent from "@/components/Game/CurrentTurnComponent.vue";
import ActionLog from "@/components/GameMaster/ActionLog/ActionLogComponent.vue";
import {ActionGameApi, CharacterGameApi} from "@/api/backendService.js";
import CharacterCardHolder from "@/components/Game/Location/CharacterCardHolder.vue";
import LocationIdSelector from "@/components/GameMaster/LocatioinIdSelector.vue";
import PlayerComponent from "@/components/Game/Location/PlayerComponent.vue";

export default {
  components: {
    PlayerComponent,
    LocationIdSelector,
    CharacterCardHolder, ActionLog, CurrentTurnComponent, EndTurnComponent, GameMasterImpact
  },
  data() {
    return {
      actions: [],
      characters: [],
      npcCharacters: [],
      selectedLocationId: null,
      selectedCharacterId: null,
      selectedCharacterInfo: null,
      selectedCharacterData: null,
    };
  },
  async mounted() {
    await this.refresh();
    await this.refreshCharacters();
  },
  methods: {
    async selectCharacter(id) {
      this.selectedCharacterId = id;
      this.selectedCharacterData = (await CharacterGameApi.characterGmCharacterInfoRetrieve(id)).data;
      this.selectedCharacterInfo = (await CharacterGameApi.characterGmRetrieve(id)).data;
    },
    async selectLocationId(id) {
      this.selectedLocationId = id;
    },
    async refresh() {
      await this.refreshActions();
      if (this.selectedCharacterId) {
        await this.selectCharacter(this.selectedCharacterId);
      }
    }
    ,
    async refreshActions() {
      const newActions = (await ActionGameApi.actionGmList(
          100,
      )).data;
      this.actions = newActions.results;
    },
    async refreshCharacters() {
      this.characters = (await CharacterGameApi.characterList(
          false
      )).data;
    },
    async refreshNPCharacters() {
      this.npcCharacters = (await CharacterGameApi.characterList(
          true, this.selectedLocationId,
      )).data;
    },
    handleImpact(impact) {
      console.log("Impact Applied:", impact);
      this.refreshActions();
    },
  },
  watch: {
    selectedLocationId() {
      this.refreshNPCharacters();
    },
  },
}
;
</script>

<style scoped>
.dashboard {
  background-color: #1c1c1c;
  display: grid;
  z-index: 1000;
  grid-template-areas:
    "left-section top-center top-center"
    "left-section center-section top-right"
    "left-section bottom-center bottom-right";
  grid-template-columns: 2.2fr 2fr 1fr;
  grid-template-rows: 0.2fr 2fr 1fr;
  height: 100vh;
  max-height: 100vh;
  gap: 0.3rem;
  padding: 0.1rem;
  box-sizing: border-box;
}

/* Top Center Section */
.top-center {
  grid-area: top-center;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.2rem;
}

/* Left Full Height Section */
.left-section {
  grid-area: left-section;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
}

/* Center Section */
.center-section {
  grid-area: center-section;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}

/* Floating Top Right Section */
.top-right {
  grid-area: top-right;
  justify-self: end;
  align-self: start;
}

/* Center Bottom Section */
.bottom-center {
  grid-area: bottom-center;
  display: flex;
  justify-content: center;
}

/* Bottom Right Section */
.bottom-right {
  grid-area: bottom-right;
  justify-self: end;
  align-self: end;
}
</style>
