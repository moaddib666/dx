<template>
  <div class="dashboard">
    <!-- Left Full Height Section -->
    <ActionLog class="left-section" :actions="actions" :gmMode="true" @refresh="refreshActions"/>
    <!-- Center Full Height Section -->
    <div class="center-section">
      <!-- Top Bar -->
      <div class="top-bar">
        <CharacterCardHolder
            v-if="characters && characters.length > 0"
            :characters="characters"
            :selectedCharacterId="selectedCharacterId"
            class="top-center-left card-holder"
            :additional-characters-data="additionalCharactersData"
            @characterSelected="selectCharacter"
        />
        <CharacterCardHolder

            v-if="npcCharacters && npcCharacters.length > 0"
            :characters="npcCharacters"
            :selectedCharacterId="selectedCharacterId"
            @characterSelected="selectCharacter"
            class="top-center-right card-holder"
        />
        <DynamicBackground
            :backgroundUrl="selectedCharacterPositionBackground"
            v-if="selectedCharacterData && selectedCharacterInfo">
          <div
              class="character-bars"
          >
            <CharacterRPGBars

                :character="{
                  name: selectedCharacterData?.name || 'Unknown',
                  level: selectedCharacterData?.rank_grade || 0,
                  health: selectedCharacterData?.attributes.find(attr => attr.name === 'Health')?.current || 0,
                  maxHealth: selectedCharacterData?.attributes.find(attr => attr.name === 'Health')?.max || 100,
                  flow: selectedCharacterData?.attributes.find(attr => attr.name === 'Energy')?.current || 0,
                  maxFlow: selectedCharacterData?.attributes.find(attr => attr.name === 'Energy')?.max || 100,
                  actionPoints: selectedCharacterData?.attributes.find(attr => attr.name === 'Action Points')?.current || 0,
                  maxActionPoints: selectedCharacterData?.attributes.find(attr => attr.name === 'Action Points')?.max || 10,
                  avatar: selectedCharacterInfo?.biography?.avatar || '',
                  rank_grade: selectedCharacterData?.rank_grade || 0,
                  dimension: selectedCharacterData?.dimension || 0,
                  id: selectedCharacterData?.id || '',
                  position: selectedCharacterData?.position || '',
                  tags: selectedCharacterData?.tags || []
                }"
                :shields="shields"
                :effects="activeEffects"
                :extended="true"
                @openInfo="openInfo"
            />
            <GameMasterCharacterInfo :character-data="selectedCharacterData" @open-teleport="toggleTeleportComponent" />
          </div>
          <TeleportComponent v-if="showTeleportComponent" @teleportToCoordinates="teleportToCoordinates" @teleportToPosition="teleportToPosition"/>
          <CustomAction
              :initiator="selectedInitiator"
              :target="selectedTarget"
              :action="selectedAction"
              @selectInitiator="handleSelectInitiator"
              @selectTarget="handleSelectTarget"
              @selectAction="handleSelectAction"
              @performAction="handlePerformAction"
              @cancelAction="handleCancelAction"
          />
        </DynamicBackground>
      </div>
    </div>
    <!-- Right Full Height Section -->
    <div class="right-section">
      <GameObjectRawSelector @gameObjectSelected="selectLocationId" item-name="Position"
                             placeholder="Enter Position UUID"/>
      <GameObjectRawSelector @gameObjectSelected="selectCharacter" item-name="Character"
                             placeholder="Enter Character UUID"/>

      <VerticalPlayerList :game-objects="activePlayersCharacters" @item-selected="selectCharacter"
                          class="characters-vertical"/>
    </div>

    <CurrentTurnComponent :current-turn="currentCycleNumber" class="current-turn"/>
    <EndTurnComponent class="end-turn"/>

    <!-- Character Selector Modal -->
    <div v-if="showCharSelector" class="modal-overlay" @click="handleCharSelectorClose">
      <div class="modal-container" @click.stop>
        <GmCharSelector
            :characters="characters.concat(npcCharacters)"
            @select="handleCharacterSelected"
            @close="handleCharSelectorClose"
        />
      </div>
    </div>

    <!-- Skill Selector Modal -->
    <div v-if="showSkillSelector" class="modal-overlay" @click="handleSkillSelectorClose">
      <div class="modal-container" @click.stop>
        <GMRPGSkills
            :isDraggable="false"
            @skillSelected="handleSkillSelected"
            @close="handleSkillSelectorClose"
        />
      </div>
    </div>

    <!-- Character Card Modal -->
    <div v-if="showCharacterCard && selectedCharacterId" class="modal-overlay" @click="closeCharacterCard">
      <div class="modal-container" @click.stop>
        <GameMasterCharacterCard
            :characterId="selectedCharacterId"
            @close="closeCharacterCard"
        />
      </div>
    </div>
  </div>
</template>


<script>
import EndTurnComponent from "@/components/GameMaster/EndTurnComponent.vue";
import CurrentTurnComponent from "@/components/Game/CurrentTurnComponent.vue";
import ActionLog from "@/components/GameMaster/ActionLog/ActionLogComponent.vue";
import {ActionGameApi, CharacterGameApi, ShieldsGameApi} from "@/api/backendService.js";
import CharacterCardHolder from "@/components/GameMaster/Character/CharacterCardHolder.vue";
import GameObjectRawSelector from "@/components/GameMaster/GameObjectRawSelector.vue";
import BackgroundView from "@/components/Game/Location/BackgroundView.vue";
import {LocationInfoGameService} from "@/services/locationInfoService";
import DynamicBackground from "@/components/Background/DynamicBackground.vue";
import VerticalPlayerList from "@/components/GameMaster/PlayerList/VerticalPlayerList.vue";
import TeleportComponent from "@/components/GameMaster/TeleportComponent.vue";
import {ensureConnection} from "@/api/dx-websocket/index.ts";
import CustomAction from "@/components/GameMaster/CustomAction/CustomAction.vue";
import GmCharSelector from "@/components/GameMaster/Character/GMCharSelector.vue";
import GMRPGSkills from "@/components/GameMaster/RPGSkills/GMRPGSkills.vue";
import CharacterRPGBars from "@/components/PlayerRPGBars/CharacterRPGBars.vue";
import GameMasterCharacterInfo from "@/components/GameMaster/GameMasterCharacterInfo.vue";
import GameMasterCharacterCard from "@/components/WorldEditor/GameMasterCharacterCard.vue";

export default {
  components: {
    CharacterRPGBars,
    CustomAction,
    GmCharSelector,
    GMRPGSkills,
    TeleportComponent,
    VerticalPlayerList,
    DynamicBackground,
    BackgroundView,
    GameObjectRawSelector,
    CharacterCardHolder, ActionLog, CurrentTurnComponent, EndTurnComponent,
    GameMasterCharacterInfo,
    GameMasterCharacterCard
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
      currentCycleNumber: null,
      additionalCharactersData: {},
      selectedInitiator: undefined,
      selectedTarget: undefined,
      selectedAction: undefined,
      showCharSelector: false,
      showSkillSelector: false,
      showCharacterCard: false,
      showTeleportComponent: false,
      currentSelectionType: null,
    };
  },
  async mounted() {
    await this.refresh();
    await this.refreshActions();
    await this.refreshCharacters();
    await this.refreshActivePlayersCharacters();
    this.currentCycleNumber = (await ActionGameApi.actionCurrentCycleRetrieve()).data.id
    // Subscribe to the event bus when component mounts
    this.bus = ensureConnection();
    this.bus.on("world::new_cycle", this.handleCycleChange);
    this.bus.on("world::action_accepted", this.handleNewAction);
    this.bus.on("world::action_performed", this.handleNewAction);
    this.bus.on("world::character_changed", this.handleCharacterChange);
  },
  async beforeUnmount() {
    // Unsubscribe to prevent memory leaks
    this.bus.off("world::new_cycle", this.handleCycleChange);
    this.bus.off("world::action_accepted", this.handleNewAction);
    this.bus.off("world::action_performed", this.handleNewAction);
    this.bus.off("world::character_changed", this.handleCharacterChange);
  },
  methods: {
    async handleCharacterChange(data) {
      console.debug("Character Changed:", {data});
      this.additionalCharactersData[data.id] = data;
    },
    async handleNewAction(data) {
      console.debug("New Action Accepted:", {data});
      // check if data.id in this.actions then replace it else add it
      const index = this.actions.findIndex((action) => action.id === data.id);
      if (index !== -1) {
        this.actions[index] = data;
      } else {
        this.actions.push(data);
      }
      // re-render the actions and re order them by order
      this.actions = [...this.actions].sort((a, b) => b.order - a.order);

    },
    async handleCycleChange(data) {
      console.debug("New Cycle:", {data});
      if (data.id !== this.currentCycleNumber) {
        this.currentCycleNumber = data.id;
        await this.refresh();
      }
    },
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
    toggleTeleportComponent() {
      this.showTeleportComponent = !this.showTeleportComponent;
    },
    async selectCharacter(id) {
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
      // await this.refreshActions();
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
    handleSelectInitiator() {
      this.currentSelectionType = 'initiator';
      this.showCharSelector = true;
    },
    handleSelectTarget() {
      this.currentSelectionType = 'target';
      this.showCharSelector = true;
    },
    handleSelectAction() {
      this.showSkillSelector = true;
    },
    handleCharacterSelected(characterId) {
      const character = this.characters.concat(this.npcCharacters).find(c => c.id === characterId);
      if (character) {
        const participant = {
          id: character.id,
          name: character.name,
          imageUrl: character.biography?.avatar
        };

        if (this.currentSelectionType === 'initiator') {
          this.selectedInitiator = participant;
        } else if (this.currentSelectionType === 'target') {
          this.selectedTarget = participant;
        }
      }

      this.showCharSelector = false;
      this.currentSelectionType = null;
    },
    handleSkillSelected(skill) {
      // Transform skill to action format
      const action = {
        skillId: skill.id || skill.name, // Use skill ID or name as identifier
        name: skill.name,
        description: skill.description,
        school: skill.school,
        grade: skill.grade,
        type: skill.type
      };

      this.selectedAction = action;
      this.showSkillSelector = false;
    },
    handleCharSelectorClose() {
      this.showCharSelector = false;
      this.currentSelectionType = null;
    },
    handleSkillSelectorClose() {
      this.showSkillSelector = false;
    },
    handlePerformAction(action) {
      // Log the action being performed
      console.log('Performing action:', {
        initiator: this.selectedInitiator,
        target: this.selectedTarget,
        action: action
      });

      // Here you can add the actual action execution logic
      // For example, calling an API to perform the action
      // await ActionGameApi.performCustomAction({
      //   initiatorId: this.selectedInitiator.id,
      //   targetId: this.selectedTarget.id,
      //   action: action
      // });

      // Reset state after performing action
      this.resetCustomActionState();
    },
    handleCancelAction() {
      // Reset state when canceling
      this.resetCustomActionState();
    },
    resetCustomActionState() {
      // Reset all custom action related state
      this.selectedInitiator = undefined;
      this.selectedTarget = undefined;
      this.selectedAction = undefined;
      this.currentSelectionType = null;
    },
    openInfo() {
      // Show the character card modal when character bars are clicked
      this.showCharacterCard = true;
    },
    closeCharacterCard() {
      // Close the character card modal
      this.showCharacterCard = false;
    },
  },
  watch: {
    selectedLocationId() {
      this.refreshNPCharacters();
      this.refreshCharacters()
    },
    selectedCharacterId() {
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
  max-height: 85vh;
  width: 100%;
  flex: 1;
  flex-direction: row;
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
  flex-direction: column;
  background: #ff5252;
  width: 100%;
  height: 100%;
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

.characters-vertical {
  max-height: 40vh;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) transparent;
}

/* Modal container styles - invisible positioning containers */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal-container {
  max-width: 90vw;
  max-height: 90vh;
  overflow: auto;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
}

/* Custom scrollbar for modal container */
.modal-container::-webkit-scrollbar {
  width: 8px;
}

.modal-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.modal-container::-webkit-scrollbar-thumb {
  background: rgba(127, 255, 22, 0.6);
  border-radius: 4px;
}

.modal-container::-webkit-scrollbar-thumb:hover {
  background: rgba(127, 255, 22, 0.8);
}
.character-bars {
  scale: 0.75;
  display: flex;
  flex-direction: row;
  flex-grow: 1;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  position: relative;
}
.top-bar{
  height: 80%;
}
</style>
