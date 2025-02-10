<template>
  <div class="location-view">
    <!-- Background View -->
    <BackgroundView
        :key="position.id"
        :background="position.image"
        :movementActivated="isMoving"
        class="background-view"
    ></BackgroundView>

    <!-- Top Row (Character Cards) -->
    <div class="top-row">
      <CharacterCardHolder
          v-if="characters.length > 0"
          :characters="characters"
          :selectedCharacterId="selectedCharacterId"
          class="top-left"
          @characterSelected="updateSelectedGameObjectId"
      />
      <div class="top-separator"></div>
      <CharacterCardHolder
          v-if="npcCharacters.length > 0"
          :characters="npcCharacters"
          :selectedCharacterId="selectedCharacterId"
          :additionalCharactersData="additionalCharactersData"
          class="top-right"
          @characterSelected="updateSelectedGameObjectId"
      />
    </div>

    <!-- Compass Component (Centered) -->
    <div class="center-section">
      <div class="center-left">
        <!-- Player Component (Left) -->
        <PlayerComponent
            :player="playerInfo"
            :playerImage="playerGeneralInfo.biography.avatar"
            @click="openInfo"
            style="cursor: pointer"
        />
        <EffectsHolder :effects="activeEffects"/>
        <ShieldHolder :shields="shields"/>
        <CoordinatesDisplay :coordinates="playerInfo.coordinates"/>
      </div>
      <div class="center-center">
        <ItemHolder
            v-if="isInventoryVisible"
            :items="inventoryItems" @item-clicked="alert('itemClicked')" @close="toggleInventory">
          <template #header>
            <span>Inventory</span>
          </template>
        </ItemHolder>
        <DiceVisualizer v-if="isDiceVisible" :result="diceResult" @close="toogleDice"
                        @selectedDice="diceRoll"/>
        <CompassComponent
            v-if="isCompassVisible"
            :connections="activeConnections"
            centerAction="true"
            centerLabel="Up"
            class="compass-component"
            @move="handleMove"
        />
        <ActionConstructor v-if="isActionConstructorVisible"
                           :availableSkills="availableActions"
                           :availableSpecials="playerSpecials"
                           :availableItems="availableItems"
                           :availableGameObjects="availableGameObjects"
                           :preSelectedTarget="selectedGameObjectId"
                           @applyAction="applyAction"
                           @cancelAction="closeActionConstructor"
                           class="action-constructor"
                           :isSafe="position ? position.is_safe : false"
        />


      </div>
      <div class="center-right" v-if="centerAreaNotInteractive">
        <MiniMapComponent v-if="mapData" :mapData="mapData" class="mini-map"/>
        <UserActionLog v-if="actionLog" :actions="actionLog" class="action-log"/>
      </div>
    </div>
    <!-- Bottom Row -->
    <div class="bottom">
      <!-- Current Turn Component (Bottom, Left) -->
      <div class="left-action-group">
        <CurrentTurnComponent
            class="current-turn-component"
            @turnChanged="updateAll"
        />
      </div>
      <!-- Dice Component (Bottom, Right) -->
      <div class="right-action-group">
        <InventoryButton
            @click="toggleInventory"
        />
        <ActionButton
            v-if="hasActionPoints"
            @click="toggleActionConstructor"
        />
        <DiceComponent
            @click="toogleDice"
        />
      </div>
    </div>
  </div>
</template>


<script>
import CompassComponent from '@/components/Game/Location/Compass.vue';
import {
  ActionGameApi,
  CharacterGameApi,
  EffectsGameApi,
  ItemsGameApi,
  ShieldsGameApi,
  SkillsGameApi,
  WorldGameApi
} from "@/api/backendService.js";
import CharacterCardHolder from "@/components/Game/Location/CharacterCardHolder.vue";
import PlayerComponent from "@/components/Game/Location/PlayerComponent.vue";
import BackgroundView from "@/components/Game/Location/BackgroundView.vue";
import ActionService from "@/services/actionsService.js";
import PlayerService from "@/services/playerService.js";
import DiceComponent from "@/components/Dice/DiceComponent.vue";
import CurrentTurnComponent from "@/components/Game/CurrentTurnComponent.vue";
import GameObjectSelector from "@/components/Selectors/GameObjectSelector.vue";
import SkillSelector from "@/components/Selectors/SkillSelector.vue";
import ActionPreview from "@/components/Pickers/ActionPreview.vue";
import GlassPlayButton from "@/components/btn/GlassPlayButton.vue";
import ActionConstructor from "@/components/Action/ActionConstructor.vue";
import ActionButton from "@/components/Action/ActionButton.vue";
import DiceVisualizer from "@/components/Dice/DiceVisualizer.vue";
import CoordinatesDisplay from "@/components/Map/Coordinates.vue";
import EffectItem from "@/components/Effect/EffectItem.vue";
import EffectsHolder from "@/components/Effect/EffectsHolder.vue";
import {CharacterInfoGameService} from "@/services/characterInfoService.js";
import ItemCell from "@/components/Item/ItemCell.vue";
import ItemHolder from "@/components/Item/ItemHolder.vue";
import InventoryButton from "@/components/Action/InventoryButton.vue";
import ShieldHolder from "@/components/Shield/ShieldHolder.vue";
import MiniMapComponent from "@/components/Map/MiniMapComponent.vue";
import UserActionLogItem from "@/components/ActionLog/UserActionLogItem.vue";
import UserActionLog from "@/components/ActionLog/UserActionLog.vue";

export default {
  name: 'LocationView',
  components: {
    UserActionLog,
    UserActionLogItem,
    MiniMapComponent,
    ShieldHolder,
    InventoryButton,
    ItemHolder,
    ItemCell,
    EffectsHolder,
    EffectItem,
    CoordinatesDisplay,
    DiceVisualizer,
    ActionButton,
    ActionConstructor,
    GlassPlayButton,
    ActionPicker: ActionPreview,
    ActionSelector: SkillSelector,
    GameObjectSelector,
    CurrentTurnComponent,
    DiceComponent,
    BackgroundView,
    PlayerComponent,
    CharacterCardHolder,
    CompassComponent
  },
  data() {
    return {
      selectedGameObjectId: null,
      selectedAction: null,
      position: null,
      connections: null,
      playerInfo: null,
      playerGeneralInfo: null,
      characters: [],
      npcCharacters: [],
      selectedCharacterId: 'f3c4216f-cbaa-4792-b6e6-1cedd502deae',
      actionService: new ActionService(ActionGameApi),
      playerService: null,
      playerSkills: null,
      playerSpecials: null,
      diceResult: null,
      inventoryItems: null,
      activeEffects: [],
      shields: [],
      additionalCharactersData: null,
      diceVisible: false,
      inventoryVisible: false,
      actionConstructorVisible: false,
      isMoving: false,
      mapData: null,
      actionLog: null,
    };
  },
  computed: {
    centerAreaNotInteractive() {
      return !this.isDiceVisible && !this.isInventoryVisible && !this.isActionConstructorVisible;
    },
    isCompassVisible() {
      return this.hasActionPoints && !this.isActionConstructorVisible && !this.isDiceVisible && !this.isInventoryVisible;
    },
    isActionConstructorVisible() {
      return this.hasActionPoints && this.actionConstructorVisible;
    },
    isDiceVisible() {
      return this.diceVisible;
    },
    isInventoryVisible() {
      return this.inventoryVisible;
    },
    availableActions() {
      return this.playerSkills.map((knownSkill) => {
        return knownSkill.skill;
      });
    },
    availableItems() {
      if (!this.inventoryItems) return [];

      return this.inventoryItems
          .filter(
              (word_item) =>
                  word_item.item.skill !== null &&
                  word_item.charges_left > 0
          );
    },
    availableGameObjects() {
      // Return a list of game objects that are available to the player in current location
      // Players, Items, etc.
      const playersGameObjects = this.characters.map((char) => {
        return {
          id: char.id,
          name: char.name,
          icon: char.biography.avatar,
        };
      });
      const npcGameObjects = this.npcCharacters.map((char) => {
        return {
          id: char.id,
          name: char.name,
          icon: char.biography.avatar,
        };
      });
      const itemsGameObjects = [];
      return playersGameObjects.concat(itemsGameObjects).concat(npcGameObjects);
    },
    hasActionPoints() {
      return this.playerService?.hasActionPoints();
    },
    activeConnections() {
      if (!this.connections) return [];
      console.log(this.connections);
      // this.connections is an object, so we need to convert it to an array
      return Object.values(this.connections);
    },
  },
  async created() {
    await this.updateAll();
  },
  methods: {
    async refreshActionLog() {
      this.actionLog = (await ActionGameApi.actionLogList()).data;
    },
    async refreshMiniMap() {
      try {
        this.mapData = (await WorldGameApi.worldMapsMiniMapRetrieve()).data;
      } catch (error) {
        console.debug("Problem refreshing mini map:", error);
      }
    },
    resetAdditionalPlayerData() {
      this.additionalCharactersData = {};
    },
    updateAdditionalPlayerData(characters) {
      console.debug("updating additional characters data", {characters});
      if (!this.additionalCharactersData) {
        this.additionalCharactersData = {};
      }

      // Iterate through the characters array
      characters.forEach(character => {
        const {id, name, attributes, dimension, rank_grade, path} = character;

        // Prepare the formatted data for the character
        const formattedData = {
          name: name || "xx",
          rankGrade: rank_grade !== undefined ? rank_grade : "xx",
          dimension: dimension !== undefined ? dimension : "xx",
          path: path || {name: "xx", icon: null},
          attributes: {}
        };

        // Process attributes into a key-value structure
        if (Array.isArray(attributes)) {
          attributes.forEach(attr => {
            formattedData.attributes[attr.name.toLowerCase()] = {
              current: attr.current !== undefined ? attr.current : "xx",
              max: attr.max !== undefined ? attr.max : "xx"
            };
          });
        }

        // Store the formatted data in resetAdditionalPlayerData
        this.additionalCharactersData[id] = formattedData;
      });
    },
    async hideAll() {
      this.diceVisible = false;
      this.inventoryVisible = false;
      this.actionConstructorVisible = false;
    },
    async toggleActionConstructor() {
      console.debug("Toggling action constructor");
      if (this.actionConstructorVisible) {
        await this.closeActionConstructor();
      } else {
        await this.openActionConstructor();
      }
    },
    async openActionConstructor() {
      await this.hideAll();
      this.actionConstructorVisible = true;
      console.debug("Opening action constructor", this.selectedGameObjectId);
    },
    async closeActionConstructor() {
      this.actionConstructorVisible = false;
      this.selectedGameObjectId = null;
      console.debug("Closing action constructor");
    },
    async setMovement() {
      this.isMoving = true;
    },
    async unsetMovement() {
      this.isMoving = false;
    },
    async toogleDice() {
      if (this.diceVisible) {
        await this.closeDice();
      } else {
        await this.openDice();
      }
    },
    async openDice() {
      await this.hideAll();
      this.diceVisible = true;
    },
    async closeDice() {
      this.diceVisible = false;
    },
    async toggleInventory() {
      if (this.inventoryVisible) {
        await this.closeInventory();
      } else {
        await this.openInventory();
      }
    },
    async openInventory() {
      await this.refreshInventory();
      await this.hideAll();
      this.inventoryVisible = true;
    },
    async closeInventory() {
      this.inventoryVisible = false;
    },
    async refreshInventory() {
      this.inventoryItems = (await ItemsGameApi.itemsCharacterList()).data.map((item) => item.world_item);
    },
    async selectSelf() {
      this.selectedGameObjectId = this.playerInfo.id;
    },
    async refreshShields() {
      this.shields = (await ShieldsGameApi.shieldsActiveList()).data;
    },
    async cancelAction() {
      this.selectedGameObjectId = null;
    },
    async applyAction(action) {
      try {
        const result = await this.actionService.performAction(action);
        await this.getPlayerInfo();

        // Ensure result is valid and handle based on action type
        if (!result || !result.action_type) {
          console.error("Invalid action result:", result);
          return;
        }

        switch (result.action_type) {
          case "INSPECT":
            // Update additional player data if characters are present
            if (result.data?.characters?.length) {
              console.debug("result of inspection", {result});
              this.updateAdditionalPlayerData(result.data.characters);
            } else {
              console.warn("No characters data found in INSPECT action.");
            }
            break;

          default:
            console.log(`Unhandled action type: ${result.action_type}`);
            break;
        }
      } catch (error) {
        console.error("Error applying action:", error);
      }
    },
    async updateSelectedGameObjectId(id) {
      this.selectedGameObjectId = id;
      await this.openActionConstructor();
    },
    async updateAll() {
      this.resetAdditionalPlayerData();
      await this.unsetMovement();
      await this.getCurrentPositionInfo();
      await this.getPlayerInfo();
      await this.getPlayerSkills();
      await this.getActiveEffects();
      await this.refreshShields();
      await this.getPlayerSpecials();
      await this.refreshMiniMap();
      await this.refreshActionLog();
      await this.refreshInventory();
    },
    openInfo() {
      // open window with character info
      const routePath = this.$router.resolve({name: 'CharacterInfo'}).href;
      // Open in a new floating window
      window.open(routePath, '_blank', 'width=1024,height=1280,scrollbars=yes,resizable=yes');
    },
    async diceRoll({dice, index}) {
      // sleep for 1 second
      await new Promise(r => setTimeout(r, 1000));
      this.diceResult = await this.actionService.diceRoll(dice.value);
    },
    async handleMove(direction) {
      const move_direction = this.connections[direction]
      const new_postion_id = move_direction.to_position;
      await this.actionService.move(new_postion_id);
      // await this.getCurrentPositionInfo();
      await this.getPlayerInfo();
      await this.setMovement();
    },
    async resolveCharacter(characterId) {
      const data = await CharacterInfoGameService.getCharacterInfo(characterId);
      // const data = (await CharacterGameApi.characterPlayerRetrieve(characterId)).data;
      if (data.npc) {
        this.npcCharacters.push(data);
      } else {
        this.characters.push(data);
      }
    },
    async getCurrentPositionInfo() {
      this.position = (await WorldGameApi.worldPositionCurrentRetrieve()).data;
      this.connections = {}
      this.position.connections.forEach((conn) => {
        this.connections[conn.direction] = conn;
      });
      this.characters = [];
      this.npcCharacters = [];
      this.position.characters.forEach((char) => {
        this.resolveCharacter(char);
      });
    },
    async getPlayerInfo() {
      this.playerInfo = (await CharacterGameApi.characterPlayerCharacterInfoRetrieve()).data;
      if (this.playerGeneralInfo === null) {
        this.playerGeneralInfo = (await CharacterGameApi.characterPlayerRetrieve(this.playerInfo.id)).data;
      }
      this.playerService = new PlayerService(this.playerInfo)
    },
    async getPlayerSkills() {
      this.playerSkills = (await SkillsGameApi.skillsSkillsList()).data;
    },
    async getPlayerSpecials() {
      this.playerSpecials = (await ActionGameApi.actionSpecialAvailableRetrieve()).data;
    },
    async getActiveEffects() {
      this.activeEffects = (await EffectsGameApi.effectsActiveList()).data;
    },
  },
  watch: {
    selectedGameObjectId(newId) {
      this.refreshInventory();
    },
  },
};
</script>

<style scoped>
.center-section {
  display: flex;
  justify-content: space-between;
  gap: 3rem;
  align-items: center;
  height: 60vh;
  max-height: 60vh;
}

.location-view {
  display: flex;
  flex-direction: column;
  position: relative;
  height: 85vh;
  overflow: hidden;
  gap: 1rem;
}

.background-view {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  display: flex;
}

.center-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  flex: 3;
}

.center-right {
  flex: 1;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 1rem;
  display: flex;
  height: 100%;
  margin-right: 0.5rem;
}


.top-row {
  width: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 5%;
  z-index: 5;
}

.top-right {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  flex: 1;
}

.top-separator {
  width: 1rem;
  height: 100%;
}

.top-left {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex: 1;
}

.current-turn-component {
  position: absolute;
  bottom: 20px;
  left: 20px;
  z-index: 20;
}

.action-constructor {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 0.5rem;

}

.left-action-group {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  flex-direction: row;
  z-index: 20;
  padding-left: 1rem;
}

.right-action-group {
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  flex-direction: row;
  z-index: 20;
  margin-right: 0.5rem;
  gap: 1rem;
  height: 3rem;
}

.right-action-group * {
  height: 3rem;
  width: 3rem;
}

@media (max-width: 480px) {
  .compass-component {
    width: 90%;
  }

  .top-row {
    flex-direction: column;
    align-items: center;
  }
}

.mini-map {
  display: flex;
  justify-self: flex-end;
  align-self: flex-end;
}
.action-log {
  display: flex;
  flex: 1;
  width: 90%;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 0.5rem;
  padding: 0.5rem;
  max-height: 30vh;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) rgba(0, 0, 0, 0.5);
  scroll-behavior: smooth;
  font-size: 0.6rem;
}
.center-left {
  margin-left: 0.5rem;
}
</style>
