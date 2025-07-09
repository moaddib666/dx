<template>
  <div class="location-view">
    <!-- Background View -->
    <BackgroundView
        :key="position?.id"
        :background="position?.image"
        :movementActivated="isMoving"
        class="background-view"
    ></BackgroundView>

    <!-- Top Row (Character Cards) -->
    <div class="top-row">
      <NewCharacterCardHolder
          v-if="characters.length > 0 || npcCharacters.length > 0"
          :characters="characters.concat(npcCharacters)"
          :selectedCharacterId="selectedCharacterId"
          :additionalCharactersData="additionalCharactersData"
          @characterSelected="updateSelectedGameObjectId"
      />
    </div>

    <!-- Compass Component (Centered) -->
    <div class="center-section">
      <div class="center-left">
        <CharacterRPGBars
            :character="{
          name: playerInfo?.name || 'Unknown',
          level: playerInfo?.rank_grade || 0,
          health: playerInfo?.attributes.find(attr => attr.name === 'Health')?.current || 0,
          maxHealth: playerInfo?.attributes.find(attr => attr.name === 'Health')?.max || 100,
          flow: playerInfo?.attributes.find(attr => attr.name === 'Energy')?.current || 0,
          maxFlow: playerInfo?.attributes.find(attr => attr.name === 'Energy')?.max || 100,
          actionPoints: playerInfo?.attributes.find(attr => attr.name === 'Action Points')?.current || 0,
          maxActionPoints: playerInfo?.attributes.find(attr => attr.name === 'Action Points')?.max || 10,
          avatar: playerGeneralInfo?.biography?.avatar || '',
        }"
            :shields="shields"
            :effects="activeEffects"
            @openInfo="openInfo"
        ></CharacterRPGBars>
      </div>
      <div class="center-center">
        <!-- Add more glitches with empty content for a more distributed cracked screen effect -->
        <BargainComponent :inventory="inventoryItems" v-if="isBargainVisible" @bargain-completed="toggleBargain"
                          :bargain-id="currentBargainId"/>
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
                           :playerService="playerService"
                           @applyAction="applyAction"
                           @cancelAction="closeActionConstructor"
                           class="action-constructor"
                           :isSafe="position ? position.is_safe : false"
        />


      </div>
      <div class="center-right" v-if="centerAreaNotInteractive">
        <CoordinatesDisplay :coordinates="playerInfo?.coordinates"/>
        <MiniMapComponent v-if="mapData" :mapData="mapData" class="mini-map"/>
        <UserActionLog v-if="actionLog" :actions="actionLog" class="action-log"/>
      </div>
      <DimensionalGlitch v-for="an in position?.anomalies || []" :key="an" :force-visible="false"
                         :glitch-id="an" @glitch-found="handleAnomalyClick"/>
    </div>
    <!-- Bottom Row -->
    <div class="bottom">
      <!-- Current Turn Component (Bottom, Left) -->
      <div class="left-action-group">
        <CurrentTurnComponent
            class="current-turn-component"
            :current-turn="currentCycleNumber"
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
  <ActionHolder
    :items="availableItems"
    :skills="availableActions"
    :specials="playerSpecials"
  />
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
import CompactPlayButton from "@/components/btn/CompactPlayButton.vue";
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
import BargainComponent from "@/components/bargain/BargainComponent.vue";
import bargainService from "@/services/bargainService.js";
import {ensureConnection} from "@/api/dx-websocket/index.ts";
import DimensionalGlitch from "@/components/Glitch/DimensionalGlitch.vue";
import CharacterRPGBars from "@/components/PlayerRPGBars/CharacterRPGBars.vue";
import NewCharacterCardHolder from "@/components/Game/Location/NewCharacterCardHolder.vue";
import ActionHolder from "@/components/ActionArea/ActionHolder/ActionHolder.vue";
import ActionItem from "@/components/ActionArea/ActionItem/ActionItem.vue";

export default {
  name: 'LocationView',
  components: {
    ActionItem,
    ActionHolder,
    CharacterRPGBars,
    NewCharacterCardHolder,
    DimensionalGlitch,
    BargainComponent,
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
    CompactPlayButton,
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
      bus: undefined,
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
      bargainVisible: false,
      inventoryVisible: false,
      actionConstructorVisible: false,
      isMoving: false,
      mapData: null,
      actionLog: null,
      bargains: null,
      currentCycleNumber: null,
    };
  },
  async mounted() {
    this.bus = ensureConnection();
    this.bus.on("world::new_cycle", this.handleCycleChange);
    this.currentCycleNumber = (await ActionGameApi.actionCurrentCycleRetrieve()).data.id
  },
  computed: {
    currentBargainId() {
      return this.bargains?.[0]?.id;
    },
    centerAreaNotInteractive() {
      return !this.isDiceVisible && !this.isInventoryVisible && !this.isActionConstructorVisible;
    },
    isCompassVisible() {
      return this.hasActionPoints && !this.isActionConstructorVisible && !this.isDiceVisible && !this.isInventoryVisible && !this.bargainVisible;
    },
    isActionConstructorVisible() {
      return this.hasActionPoints && this.actionConstructorVisible;
    },
    isDiceVisible() {
      return this.diceVisible;
    },
    isBargainVisible() {
      return this.bargainVisible && this.bargains?.length > 0;
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
          icon: char.biography?.avatar || '',
        };
      });
      const npcGameObjects = this.npcCharacters.map((char) => {
        return {
          id: char.id,
          name: char.name,
          icon: char.biography?.avatar || '',
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
    try {
      await this.updateAll();
    } catch (error) {
      console.error("Error during component creation:", error);
      // Initialize with default values to prevent errors
      this.position = {id: null, image: null, anomalies: [], connections: [], characters: []};
      this.connections = {};
      this.characters = [];
      this.npcCharacters = [];
      this.playerInfo = {id: null, coordinates: null, attributes: []};
      this.playerGeneralInfo = {biography: {avatar: null}};
      this.playerSkills = [];
      this.activeEffects = [];
      this.shields = [];
      this.playerSpecials = [];
      this.mapData = null;
      this.actionLog = [];
      this.inventoryItems = [];
      this.bargains = [];
    }
  },
  methods: {
    async handleCycleChange(data) {
      try {
        console.log("Cycle change event received", data);
        if (!data || !data.id) {
          console.error("Invalid cycle data received:", data);
          return;
        }
        if (data.id === this.currentCycleNumber) {
          console.debug("Cycle number is the same, skipping update");
          return;
        }
        this.currentCycleNumber = data.id;
        await this.updateAll();
      } catch (error) {
        console.error("Error handling cycle change:", error);
      }
    },
    async refreshBargains() {
      try {
        this.bargains = await bargainService.getOpenBargains();
      } catch (error) {
        console.error("Error refreshing bargains:", error);
        this.bargains = [];
      }
    },
    async refreshActionLog() {
      try {
        this.actionLog = (await ActionGameApi.actionLogList()).data;
      } catch (error) {
        console.error("Error refreshing action log:", error);
        this.actionLog = [];
      }
    },
    async refreshMiniMap() {
      try {
        this.mapData = (await WorldGameApi.worldMapsMiniMapRetrieve()).data;
      } catch (error) {
        console.debug("Problem refreshing mini map:", error);
      }
    },
    resetAdditionalPlayerData() {
      console.log("resetting additional characters data");
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
        console.debug("Processing character:", {id, name, attributes, dimension, rank_grade, path});
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
          console.debug("Processing attributes:", attributes);
          attributes.forEach(attr => {
            formattedData.attributes[attr.name.toLowerCase()] = {
              current: attr.current !== undefined ? attr.current : "xx",
              max: attr.max !== undefined ? attr.max : "xx"
            };
          });
        }
        console.debug("Formatted data:", formattedData, "for character:", id);
        // Store the formatted data in resetAdditionalPlayerData
        this.additionalCharactersData[id] = formattedData;
      });
    },
    async hideAll() {
      // Set all visibility flags to false
      // Using Vue.nextTick to ensure DOM updates are complete before continuing
      return new Promise(resolve => {
        this.diceVisible = false;
        this.inventoryVisible = false;
        this.actionConstructorVisible = false;
        this.bargainVisible = false;
        this.$nextTick(() => {
          resolve();
        });
      });
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
      try {
        // Wait for hideAll to complete before setting actionConstructorVisible
        await this.hideAll();

        // Use nextTick to ensure DOM is updated before setting actionConstructorVisible
        await this.$nextTick();
        this.actionConstructorVisible = true;

        console.debug("Opening action constructor", this.selectedGameObjectId);
      } catch (error) {
        console.error("Error opening action constructor:", error);
        // Reset state in case of error
        this.actionConstructorVisible = false;
      }
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
    async openBargain() {
      await this.refreshBargains();
      await this.hideAll();
      this.bargainVisible = true;
    },
    async toggleBargain() {
      await this.refreshInventory();
      if (this.bargainVisible) {
        this.bargainVisible = false;
      } else {
        this.bargainVisible = true;
      }
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
      try {
        const response = await ItemsGameApi.itemsCharacterList();
        this.inventoryItems = response.data.map((item) => item.world_item);
      } catch (error) {
        console.error("Error refreshing inventory:", error);
        this.inventoryItems = [];
      }
    },
    async selectSelf() {
      if (this.playerInfo && this.playerInfo.id) {
        this.selectedGameObjectId = this.playerInfo.id;
      }
    },
    async refreshShields() {
      try {
        this.shields = (await ShieldsGameApi.shieldsActiveList()).data;
      } catch (error) {
        console.error("Error refreshing shields:", error);
        this.shields = [];
      }
    },
    async cancelAction() {
      this.selectedGameObjectId = null;
    },
    async handleAnomalyClick(anomalyId) {
      const action = {
        actionType: "ANOMALY",
        targets: [anomalyId],
      }
      console.debug("Anomaly clicked:", anomalyId, "Action to perform:", action);
      await this.applyAction(action);
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
        console.debug("Action result:", {result});
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
          case "GIFT":
            await this.openBargain();
            break;
          case "ANOMALY":
            // Handle anomaly action result
            console.debug("Anomaly action result:", {result});
            // Refresh player info and action log to reflect changes from anomaly interaction
            await this.getPlayerInfo();
            await this.refreshActionLog();
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
      try {
        // Set the selected game object ID
        this.selectedGameObjectId = id;

        // Wait for the next tick to ensure the state is updated
        await this.$nextTick();

        // Open the action constructor
        await this.openActionConstructor();
      } catch (error) {
        console.error("Error updating selected game object ID:", error);
        // Reset state in case of error
        this.selectedGameObjectId = null;
        this.actionConstructorVisible = false;
      }
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
      await this.refreshBargains();
    },
    openInfo() {
      // open window with character info
      const routePath = this.$router.resolve({name: 'CharacterInfo'}).href;
      // Open in a new floating window
      window.open(routePath, '_blank', 'width=1024,height=1280,scrollbars=yes,resizable=yes');
    },
    async diceRoll({dice, index}) {
      try {
        // sleep for 1 second
        await new Promise(r => setTimeout(r, 1000));
        this.diceResult = await this.actionService.diceRoll(dice.value);
      } catch (error) {
        console.error(`Error rolling dice:`, error);
        this.diceResult = null;
      }
    },
    async handleMove(direction) {
      try {
        const move_direction = this.connections[direction];
        if (!move_direction) {
          console.error(`No connection found for direction: ${direction}`);
          return;
        }
        const new_postion_id = move_direction.to_position;
        await this.actionService.move(new_postion_id);
        // await this.getCurrentPositionInfo();
        await this.getPlayerInfo();
        await this.setMovement();
      } catch (error) {
        console.error(`Error handling move to direction ${direction}:`, error);
      }
    },
    async resolveCharacter(characterId) {
      try {
        const data = await CharacterInfoGameService.getCharacterInfo(characterId);
        // const data = (await CharacterGameApi.characterPlayerRetrieve(characterId)).data;
        if (data && data.npc) {
          this.npcCharacters.push(data);
        } else if (data) {
          this.characters.push(data);
        }
      } catch (error) {
        console.error(`Error resolving character ${characterId}:`, error);
      }
    },
    async getCurrentPositionInfo() {
      try {
        this.position = (await WorldGameApi.worldPositionCurrentRetrieve()).data;
        this.connections = {}
        if (this.position && this.position.connections) {
          this.position.connections.forEach((conn) => {
            this.connections[conn.direction] = conn;
          });
        }
        this.characters = [];
        this.npcCharacters = [];
        if (this.position && this.position.characters) {
          this.position.characters.forEach((char) => {
            this.resolveCharacter(char);
          });
        }
      } catch (error) {
        console.error("Error getting current position info:", error);
        // Initialize with empty values to prevent errors
        this.position = {id: null, image: null, anomalies: [], connections: [], characters: []};
        this.connections = {};
        this.characters = [];
        this.npcCharacters = [];
      }
    },
    async getPlayerInfo() {
      try {
        this.playerInfo = (await CharacterGameApi.characterPlayerCharacterInfoRetrieve()).data;
        if (this.playerGeneralInfo === null && this.playerInfo && this.playerInfo.id) {
          this.playerGeneralInfo = (await CharacterGameApi.characterPlayerRetrieve(this.playerInfo.id)).data;
        }
        this.playerService = new PlayerService(this.playerInfo);
      } catch (error) {
        console.error("Error getting player info:", error);
        // Initialize with default values to prevent errors
        this.playerInfo = {
          id: null,
          coordinates: null,
          attributes: [] // Add empty attributes array to prevent errors
        };
        if (this.playerGeneralInfo === null) {
          this.playerGeneralInfo = {biography: {avatar: null}};
        }
        this.playerService = new PlayerService(this.playerInfo);
      }
    },
    async getPlayerSkills() {
      try {
        this.playerSkills = (await SkillsGameApi.skillsSkillsList()).data;
      } catch (error) {
        console.error("Error getting player skills:", error);
        this.playerSkills = [];
      }
    },
    async getPlayerSpecials() {
      try {
        this.playerSpecials = (await ActionGameApi.actionSpecialAvailableRetrieve()).data;
      } catch (error) {
        console.error("Error getting player specials:", error);
        this.playerSpecials = [];
      }
    },
    async getActiveEffects() {
      try {
        this.activeEffects = (await EffectsGameApi.effectsActiveList()).data;
      } catch (error) {
        console.error("Error getting active effects:", error);
        this.activeEffects = [];
      }
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
  flex: 1;
  flex-direction: column;
  width: 100%;
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
