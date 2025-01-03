<template>
  <div class="dashboard">
    <!-- Left Full Height Section -->
    <div class="left-section">
      <ActionLog :actions="actions" :gmMode="true" @refresh="refreshActions"/>
    </div>
    <!-- Center Full Height Section -->
    <div class="center-section">
      <!-- Top Bar -->
      <div class="top-bar">
        <CharacterCardHolder
            v-if="characters && characters.length > 0"
            :characters="characters"
            :selectedCharacterId="selectedCharacterId"
            class="top-center-left card-holder"
            @characterSelected="selectCharacter"
        />
        <CharacterCardHolder

            v-if="npcCharacters && npcCharacters.length > 0"
            :characters="npcCharacters"
            :selectedCharacterId="selectedCharacterId"
            @characterSelected="selectCharacter"
            class="top-center-right card-holder"
        />
        <div class="work-area">
          <GameMasterImpact @impact="handleImpact" ref="Impact" @applied="refresh"/>
          <DynamicBackground :backgroundUrl="selectedCharacterPositionBackground"
                             v-if="selectedCharacterData && selectedCharacterInfo">
            <PlayerComponent

                :player="selectedCharacterData"
                :playerImage="selectedCharacterInfo.biography.avatar"
                :extended="true"
            />
            <ShieldHolder v-if="selectedCharacterShields.length > 0" :shields="selectedCharacterShields"/>
            <TeleportComponent @teleportToCoordinates="teleportToCoordinates" @teleportToPosition="teleportToPosition"/>
          </DynamicBackground>
        </div>
      </div>
    </div>
    <!-- Right Full Height Section -->
    <div class="right-section">
      <GameObjectRawSelector @gameObjectSelected="selectLocationId" item-name="Position"
                             placeholder="Enter Position UUID"/>
      <GameObjectRawSelector @gameObjectSelected="selectCharacter" item-name="Character"
                             placeholder="Enter Character UUID"/>

      <VerticalPlayerList :game-objects="activePlayersCharacters" @item-selected="selectCharacter"/>
    </div>

    <CurrentTurnComponent @turnChanged="refresh" class="current-turn"/>
    <EndTurnComponent class="end-turn"/>
  </div>
</template>


<script>
import GameMasterImpact from "@/components/GameMaster/GameMasterImpact.vue";
import EndTurnComponent from "@/components/GameMaster/EndTurnComponent.vue";
import CurrentTurnComponent from "@/components/Game/CurrentTurnComponent.vue";
import ActionLog from "@/components/GameMaster/ActionLog/ActionLogComponent.vue";
import {ActionGameApi, CharacterGameApi, ShieldsGameApi} from "@/api/backendService.js";
import CharacterCardHolder from "@/components/Game/Location/CharacterCardHolder.vue";
import GameObjectRawSelector from "@/components/GameMaster/GameObjectRawSelector.vue";
import PlayerComponent from "@/components/Game/Location/PlayerComponent.vue";
import BackgroundView from "@/components/Game/Location/BackgroundView.vue";
import {LocationInfoGameService} from "@/services/locationInfoService.js";
import DynamicBackground from "@/components/Background/DynamicBackground.vue";
import VerticalPlayerList from "@/components/GameMaster/PlayerList/VerticalPlayerList.vue";
import TeleportComponent from "@/components/GameMaster/TeleportComponent.vue";
import ShieldHolder from "@/components/Shield/ShieldHolder.vue";

export default {
  components: {
    ShieldHolder,
    TeleportComponent,
    VerticalPlayerList,
    DynamicBackground,
    BackgroundView,
    PlayerComponent,
    GameObjectRawSelector,
    CharacterCardHolder, ActionLog, CurrentTurnComponent, EndTurnComponent, GameMasterImpact
  },
  data() {
    return {
      actions: [],
      activePlayersCharacters: [],
      characters: [],
      npcCharacters: [],
      selectedLocationId: null,
      selectedCharacterId: null,
      selectedCharacterPositionBackground: null,
      selectedCharacterInfo: null,
      selectedCharacterData: null,
      locationGMService: LocationInfoGameService,
      selectedCharacterShields: [],
    };
  },
  async mounted() {
    await this.refresh();
    await this.refreshCharacters();
    await this.refreshActivePlayersCharacters();
  },
  methods: {
    async refreshSelectedCharacterShields() {
      this.selectedCharacterShields = (await ShieldsGameApi.shieldsGmActiveList(
          this.selectedCharacterId,
      )).data;
    },
    async teleportToCoordinates(x, y, z) {
      await this.locationGMService.teleportToCoordinates(this.selectedCharacterId, x, y, z);
      await this.refresh()
      await this.refreshCharacterPosition();
      await this.refreshCharacters();
      await this.refreshSelectedCharacterShields();
    },
    async teleportToPosition(id) {
      await this.locationGMService.teleportToPosition(this.selectedCharacterId, id);
      await this.refresh()
      await this.refreshCharacterPosition();
      await this.refreshCharacters();
    },
    async selectCharacter(id) {
      if (id === this.selectedCharacterId) {
        await this.refreshSelectedTargets();
      }
      this.selectedCharacterId = id;
      this.selectedCharacterData = (await CharacterGameApi.characterGmCharacterInfoRetrieve(id)).data;
      this.selectedCharacterInfo = (await CharacterGameApi.characterGmRetrieve(id)).data;
      if (this.selectedLocationId !== this.selectedCharacterData.position) {
        await this.selectLocationId(this.selectedCharacterData.position);
      }
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
    async refreshActivePlayersCharacters() {
      this.activePlayersCharacters = (await CharacterGameApi.characterGmList(
          false,
      )).data;
    },
    async refreshCharacters() {
      this.characters = (await CharacterGameApi.characterGmList(
          false, this.selectedLocationId,
      )).data;
    },
    async refreshNPCharacters() {
      this.npcCharacters = (await CharacterGameApi.characterGmList(
          true, this.selectedLocationId,
      )).data;
    },
    async refreshCharacterPosition() {
      this.selectedCharacterPositionBackground = await this.locationGMService.getBackgroundUrl(this.selectedCharacterData.position);
    },
    async refreshSelectedTargets() {
      // if initiator is not selected, select it first
      if (!this.$refs.Impact.initiator) {
        await this.$refs.Impact.setInitiator(this.selectedCharacterId);
        return
      }
      // if targets are not selected, select them first
      if (!this.$refs.Impact.target) {
        await this.$refs.Impact.setTarget(this.selectedCharacterId);
        return
      }
    },
    handleImpact(impact) {
      console.log("Impact Applied:", impact);
      this.refreshActions();
    },
  },
  watch: {
    selectedLocationId() {
      this.refreshNPCharacters();
      this.refreshCharacters()
    },
    selectedCharacterId() {
      this.refreshSelectedTargets();
      this.refreshSelectedCharacterShields();
    },
    selectedCharacterData() {
      this.refreshCharacterPosition();
    },
  }
};
</script>

<style scoped>
.dashboard {
  background-color: #1c1c1c;
  display: flex;
  gap: 0.3rem;
  box-sizing: border-box;
}

/* Left Full Height Section */
.left-section {
  flex: 3;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
  max-height: 90vh;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) transparent;
}

/* Right Full Height Section */
.center-section {
  flex: 4;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
}

/* Right Full Height Section */
.right-section {
  flex: 1;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.1);
  padding: 0.5rem;
}

.work-area {
  display: flex;
  flex-direction: row;
  gap: 0.3rem;
}

.current-turn {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 100;
}

.end-turn {
  z-index: 100;
  position: fixed;
  bottom: 2rem;
  right: 2rem;
}

.card-holder * * {
  height: 5.5rem;
  width: 4rem;
}

.card-holder * * *:first-child {
  height: 3rem;
  width: 3rem;
}

.card-holder * * *:first-child {
  height: 3rem;
  width: 3rem;
}

.card-holder * * *:last-child {
  background: rgba(0, 0, 0, 0.5);
  justify-content: center;
  align-items: center;
}
</style>
