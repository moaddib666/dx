<template>
  <div class="location-view">
    <FightStartOverlay
        v-if="hasPendingFight"
        :attacker="fightAttacker"
        :defender="fightDefender"
        :joined="fightParticipants"
    />
    <FightOverlay :side="playerGeneralInfo?.path?.name" v-if="isInFight"/>

    <div class="rpg-action-holder"
         v-if="!hasPendingFight"
    >
      <ActionHolder
          :items="availableItems"
          :skills="availableActions"
          :specials="playerSpecials"
          :player-service="playerService"
          @skill-selected="handleSkillSelected"
          @item-selected="handleItemSelected"
          @special-selected="handleSpecialSelected"
      />
      <ActionTriggerGroup
          class="trigger"
          @next-turn-triggered="handleEndTurn"
          @safe-place-triggered="() => {}"
          @roll-dice-triggered="toogleDice"
          @backpack-triggered="toggleInventory"
      />
    </div>
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
          v-if="getCharacters().length > 0"
          :class="{ 'no-target-feedback': showNoTargetFeedback }"
          :characters="getCharacters()"
          :selectedCharacterId="selectedGameObjectId"
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
            :resetBaseStats="playerGeneralInfo.resetting_base_stats || false"
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
        <DiceRollerModal :visible="isDiceVisible" :challenge="currentChallenge" @close="toogleDice"
                         @roll-complete="onDiceRollComplete"/>
        <RPGPlayerProfile
            :is-open="playerProfileVisible"
            @close="closePlayerProfile"
        />
        <CompassRPG
            v-if="isCompassVisible"
            :position="position"
            @move="handleMove"
        />


      </div>
      <div class="center-right">
        <MapColumn :map-data="mapData" :coordinates="playerInfo?.coordinates" class="mini-map"></MapColumn>
        <div class="map--effect-overlay"></div>
        <RPGActionLog :actions="actionLog" class="action-log"></RPGActionLog>
      </div>
      <DimensionalGlitch v-for="an in position?.anomalies || []" :key="an" :force-visible="false"
                         :glitch-id="an" @glitch-found="handleAnomalyClick"/>
    </div>
    <!-- Bottom Row -->
  </div>
  <div class="bottom">
    <!-- Current Turn Component (Bottom, Left) -->
    <div class="left-action-group">
      <CurrentTurnComponent
          class="current-turn-component"
          :current-turn="currentCycleNumber"
      />
    </div>
    <!-- Dice Component (Bottom, Right) -->
  </div>

  <!-- Player Profile Modal -->
  <RPGPlayerProfile
    :isOpen="isPlayerProfileVisible"
    @close="handlePlayerProfileClose"
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
  WorldGameApi,
  DiceGameApi
} from "@/api/backendService.js";
import CharacterCardHolder from "@/components/Game/Location/CharacterCardHolder.vue";
import PlayerComponent from "@/components/Game/Location/PlayerComponent.vue";
import BackgroundView from "@/components/Game/Location/BackgroundView.vue";
import ActionService from "@/services/actionsService.js";
import PlayerService from "@/services/playerService";
import DiceComponent from "@/components/Dice/DiceComponent.vue";
import CurrentTurnComponent from "@/components/Game/CurrentTurnComponent.vue";
import GameObjectSelector from "@/components/Selectors/GameObjectSelector.vue";
import SkillSelector from "@/components/Selectors/SkillSelector.vue";
import ActionPreview from "@/components/Pickers/ActionPreview.vue";
import CompactPlayButton from "@/components/btn/CompactPlayButton.vue";
import DiceRollerModal from "@/components/DiceRoller/DiceRollerModal.vue";
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
import ActionTrigger from "@/components/ActionArea/ActionTrigger/ActionTrigger.vue";
import ActionTriggerGroup from "@/components/ActionArea/ActionTriggerGroup/ActionTriggerGroup.vue";
import CompassRPG from "@/components/Compass/CompassRPG.vue";
import MapColumn from "@/components/MapColumn/MapColumn.vue";
import RPGActionLog from "@/components/RPGActionLog/RPGActionLog.vue";
import FightStartOverlay from "@/components/Fight/FightStartOverlay.vue";
import {FightService} from "@/services/PlayerFight";
import FightOverlay from "@/components/Fight/FightOverlay.vue";
import CharacterCurrentLocationService from "@/services/CharacterCurrentLocationService";
import RPGPlayerProfile from "@/components/Player/RPGPlayerProfile.vue";
export default {
  name: 'LocationView',
  components: {
    FightOverlay,
    FightStartOverlay,
    RPGActionLog,
    MapColumn,
    CompassRPG,
    DiceRollerModal,
    ActionTriggerGroup,
    ActionTrigger,
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
    CompactPlayButton,
    ActionPicker: ActionPreview,
    ActionSelector: SkillSelector,
    GameObjectSelector,
    CurrentTurnComponent,
    DiceComponent,
    BackgroundView,
    PlayerComponent,
    CharacterCardHolder,
    CompassComponent,
    RPGPlayerProfile
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
      actionService: new ActionService(ActionGameApi),
      playerService: null,
      playerSkills: null,
      playerSpecials: [],
      diceResult: null,
      inventoryItems: null,
      activeEffects: [],
      shields: [],
      additionalCharactersData: null,
      diceVisible: false,
      bargainVisible: false,
      inventoryVisible: false,
      playerProfileVisible: false,
      isMoving: false,
      mapData: {},
      actionLog: [],
      bargains: null,
      currentCycleNumber: null,
      fightService: new FightService(),
      isInFight: false,
      hasPendingFight: false,
      fightAttacker: null,
      fightDefender: null,
      fightParticipants: [],
      currentChallenge: null,
      showNoTargetFeedback: false,
      isPlayerProfileVisible: false,
    };
  },
  async mounted() {
    this.bus = ensureConnection();
    this.bus.on("world::new_cycle", this.handleCycleChange);
    this.bus.on("character::challenge_created", this.handleChallengeCreated);
    this.currentCycleNumber = (await ActionGameApi.actionCurrentCycleRetrieve()).data.id;
  },
  beforeUnmount() {
  },
  computed: {
    currentBargainId() {
      return this.bargains?.[0]?.id;
    },
    centerAreaNotInteractive() {
      return !this.isDiceVisible && !this.isInventoryVisible;
    },
    isCompassVisible() {
      return this.hasActionPoints && !this.isDiceVisible && !this.isInventoryVisible && !this.bargainVisible && !this.isInFight && !this.hasPendingFight;
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
      if (!this.playerSkills) return [];

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
      // Initialize the CharacterCurrentLocationService
      await CharacterCurrentLocationService.initialize();

      await this.updateAll();
      // Additional check for fight status after component is created
      if (this.playerInfo) {
        await this.checkFightStatus();
      }
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
      this.mapData = {};
      this.actionLog = [];
      this.inventoryItems = [];
      this.bargains = [];
      this.isInFight = false;
      this.hasPendingFight = false;
    }
  },
  methods: {
    getCharacters() {
      return CharacterCurrentLocationService.getAllCharacters();
    },
    refreshCharactersFromService() {
      try {
        // Update characters and npcCharacters from the service
        this.characters = CharacterCurrentLocationService.getPlayerCharacters();
        this.npcCharacters = CharacterCurrentLocationService.getNpcCharacters();
      } catch (error) {
        console.error("Error refreshing characters from service:", error);
      }
    },
    async checkFightStatus() {
      if (!this.playerInfo) {
        this.isInFight = false;
        this.hasPendingFight = false;
        this.resetFightData();
        return;
      }

      try {
        this.isInFight = await this.fightService.isInFight(this.playerInfo);
        if (this.isInFight) {
          // Refresh fight data to ensure we have the latest information
          await this.fightService.refreshFight(this.playerInfo);

          // Fetch and store the resolved fighter data
          await this.updateFightData();
          this.hasPendingFight = await this.fightService.isPendingJoin(this.playerInfo);
        } else {
          // Reset fight data if not in a fight or pending
          this.resetFightData();
        }
      } catch (error) {
        console.error("Error checking fight status:", error);
        this.isInFight = false;
        this.hasPendingFight = false;
        this.resetFightData();
      }
    },

    async updateFightData() {
      try {
        // Fetch and store the resolved fighter data
        const [attacker, defender, participants] = await Promise.all([
          this.fightService.getAttacker(this.playerInfo),
          this.fightService.getDefender(this.playerInfo),
          this.fightService.getFightParticipants(this.playerInfo)
        ]);

        this.fightAttacker = attacker;
        this.fightDefender = defender;
        this.fightParticipants = participants || [];
      } catch (error) {
        console.error("Error updating fight data:", error);
        this.resetFightData();
      }
    },

    resetFightData() {
      this.fightAttacker = null;
      this.fightDefender = null;
      this.fightParticipants = [];
    },

    async handleSkillSelected(skill) {
      if (!this.selectedGameObjectId) {
        console.warn("Cannot use skill without a selected target");
        this.triggerNoTargetFeedback();
        return;
      }
      const action = {
        actionType: "USE_SKILL",
        actionData: {},
        skill: skill.id,
        item: null,
        targets: [this.selectedGameObjectId],
      };
      await this.applyAction(action);
    },
    async handleItemSelected(item) {
      if (!this.selectedGameObjectId) {
        console.warn("Cannot use item without a selected target");
        this.triggerNoTargetFeedback();
        return;
      }
      const action = {
        actionType: "USE_ITEM",
        actionData: {},
        skill: null,
        item: item.id,
        targets: [this.selectedGameObjectId],
      };
      await this.applyAction(action);
    },
    async handleSpecialSelected(special) {
      if (!this.selectedGameObjectId) {
        console.warn("Cannot use special ability without a selected target");
        this.triggerNoTargetFeedback();
        return;
      }
      const action = {
        actionType: special.action_type,
        actionData: special.action_data || {},
        skill: null,
        item: null,
        targets: [this.selectedGameObjectId],
      };
      await this.applyAction(action);
    },
    triggerNoTargetFeedback() {
      // Trigger visual feedback for no target selected
      this.showNoTargetFeedback = true;
      // Reset the feedback after animation duration (1 second)
      setTimeout(() => {
        this.showNoTargetFeedback = false;
      }, 1000);
    },
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
    async handleChallengeCreated(challengeData) {
      try {
        if (!challengeData) {
          console.error("Invalid challenge data received:", challengeData);
          return;
        }
        console.log("Challenge created event received", challengeData);

        // Fetch the challenge data using DiceGameApi
        const challengeResponse = await DiceGameApi.diceChallengeRetrieve(challengeData.id);
        const challenge = challengeResponse.data;

        console.log("Challenge fetched successfully:", challenge);

        // Store the challenge and open the dice modal
        this.currentChallenge = challenge;
        await this.openDice();

      } catch (error) {
        console.error("Error handling challenge created event:", error);
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
        this.mapData = {};
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
        this.bargainVisible = false;
        this.$nextTick(() => {
          resolve();
        });
      });
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
      // Check if there's a current challenge - don't close modal if challenge is present
      if (this.currentChallenge && this.playerGeneralInfo && this.playerGeneralInfo.challenge) {
        console.log("Cannot close dice modal - current challenge is active:", this.currentChallenge.id);
        return;
      }

      // Clear the current challenge when closing the modal to ensure fresh state on reopen
      this.currentChallenge = null;
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
      // Not hiding all elements as per requirement to keep the right section visible
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
        // Refresh the action log after applying the action
        await this.refreshActionLog();
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
      } catch (error) {
        console.error("Error updating selected game object ID:", error);
        // Reset state in case of error
        this.selectedGameObjectId = null;
      }
    },
    async updateAll() {
      this.resetAdditionalPlayerData();
      await this.unsetMovement();
      await this.getCurrentPositionInfo();
      this.refreshCharactersFromService();
      await this.getPlayerInfo();
      await this.checkFightStatus(); // Check if player is in a fight
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
      // Show player profile modal instead of opening new window
      this.playerProfileVisible = true;
    },
    closePlayerProfile() {
      this.playerProfileVisible = false;
    },
    async diceRoll({dice, index}) {
      try {
        // sleep for 1 second
        await new Promise(r => setTimeout(r, 1000));
        this.diceResult = await this.actionService.diceRoll(dice.value);
        this.refreshActionLog();
      } catch (error) {
        console.error(`Error rolling dice:`, error);
        this.diceResult = null;
      }
    },

    async onDiceRollComplete(result) {
      try {
        // Store the dice roll result
        this.diceResult = result.number;
        console.log('Dice roll complete:', result);

        // Check if the roll was successful and there's a current challenge
        if (result.outcome && (result.outcome === 'Success' || result.outcome === 'Critical Success') && this.currentChallenge) {
          console.log('Challenge completed successfully, updating character...');

          // Clear the current challenge since it's been fulfilled
          this.currentChallenge = null;

          // Update character information to reflect the completed challenge
          await this.getPlayerInfo();

          // Close the dice modal since the challenge is complete
          this.isDiceVisible = false;

          console.log('Character updated after successful challenge completion');
        }
      } catch (error) {
        console.error('Error handling dice roll result:', error);
        this.diceResult = null;
      }
    },
    async handleEndTurn() {
      try {
        console.log('End turn triggered');
        if (!this.playerInfo || !this.playerGeneralInfo) {
          console.error('Player info not available');
          return;
        }

        // Construct the OpenaiCharacterRequest object
        const request = {
          name: this.playerGeneralInfo.name || '',
          biography: {
            character: this.playerGeneralInfo.biography?.character || ''
          },
          rank: {
            name: this.playerGeneralInfo.rank?.name || ''
          },
          path: {
            name: this.playerGeneralInfo.path?.name || ''
          },
          campaign: {
            id: this.playerGeneralInfo.campaign?.id || ''
          }
        };

        // Call the end turn API
        await CharacterGameApi.characterPlayerEndTurnCreate(request);

        // Update the game state
        await this.updateAll();

        console.log('End turn completed');
      } catch (error) {
        console.error('Error ending turn:', error);
      }
    },
    async handleMove(connection) {
      // Prevent movement if the character is in a fight or has a pending fight
      if (this.isInFight || this.hasPendingFight) {
        console.warn("Cannot move while in a fight or with a pending fight");
        return;
      }

      const direction = connection.direction;
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
        await this.checkFightStatus(); // Check fight status after moving
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
        // Use CharacterCurrentLocationService to get position data
        this.position = await CharacterCurrentLocationService.getCurrentPositionInfo();

        // Process connections from position data
        this.connections = {}
        if (this.position && this.position.connections) {
          this.position.connections.forEach((conn) => {
            this.connections[conn.direction] = conn;
          });
        }

        // Get characters from CharacterCurrentLocationService
        this.characters = CharacterCurrentLocationService.getPlayerCharacters();
        this.npcCharacters = CharacterCurrentLocationService.getNpcCharacters();
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

        // Check if character has a current challenge
        if (this.playerGeneralInfo && this.playerGeneralInfo.challenge) {
          console.log("Character has current challenge:", this.playerGeneralInfo.challenge);
          await this.loadCurrentChallenge(this.playerGeneralInfo.challenge);
        }
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
    async loadCurrentChallenge(challengeId) {
      try {
        console.log("Loading current challenge with ID:", challengeId);

        // Fetch the challenge data using DiceGameApi
        const challengeResponse = await DiceGameApi.diceChallengeRetrieve(challengeId);
        const challenge = challengeResponse.data;

        console.log("Current challenge loaded successfully:", challenge);

        // Store the challenge and open the dice modal
        this.currentChallenge = challenge;
        await this.openDice();

      } catch (error) {
        console.error("Error loading current challenge:", error);
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
    hasPendingFight(newValue) {
      if (newValue) {
        // When hasPendingFight becomes true, update the fighter data
        this.updateFightData();
      } else {
        // When hasPendingFight becomes false, reset the fighter data
        this.resetFightData();
      }
    },
  },
};
</script>

<style scoped>
.rpg-action-holder {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}

.trigger {
  display: flex;
  width: 12rem;
  height: 11rem;
  margin-left: -2.5rem;
  transform: translateY(35%);

}

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
  position: relative;
  flex: 1;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  display: flex;
  height: 100%;
  margin-right: 0.5rem;
  background: url("@/assets/images/RightBar/GlowFlowBG.png") no-repeat top;
  background-size: calc(100%) calc(100% - 6rem);
}


.mini-map {
  display: flex;
  flex: 1;
  width: 55%;
  min-width: 10rem;
  margin-bottom: -2.7rem;
}

.center-right .map--effect-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url("@/assets/images/RightBar/GlowFlowFG.png") no-repeat center center;
  background-size: cover;
  mask-image: linear-gradient(to top, transparent, rgba(0, 0, 0, 1));
  z-index: 1;
  mix-blend-mode: screen;
}

.action-log {
  display: flex;
  flex: 5;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) rgba(0, 0, 0, 0.5);
  scroll-behavior: smooth;
  font-size: 0.6rem;
  z-index: 10;
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


.left-action-group {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  flex-direction: row;
  z-index: 20;
  padding-left: 1rem;
}

.right-action-group {
  position: fixed;
  bottom: 2rem;
  right: 0;
  width: 10rem;
  height: 3rem;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 0.5rem;
  backdrop-filter: blur(5px);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  flex: 1;
  flex-direction: row;
  flex-wrap: nowrap;
  padding: 1.5rem;
  box-sizing: border-box;
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  z-index: 20;
  margin-right: 0.5rem;
  gap: 1rem;
}

.right-action-group * {
  height: 2rem;
  width: 2rem;
  flex: 0 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
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

.center-left {
  margin-left: 0.5rem;
}

/* Visual feedback for no target selected */
.no-target-feedback {
  animation: shake-highlight 1s ease-in-out;
}

@keyframes shake-highlight {
  0% {
    transform: translateX(0);
    box-shadow: 0 0 0 rgba(255, 87, 87, 0);
  }
  10% {
    transform: translateX(-5px);
  }
  20% {
    transform: translateX(5px);
  }
  30% {
    transform: translateX(-5px);
  }
  40% {
    transform: translateX(5px);
  }
  50% {
    transform: translateX(-3px);
  }
  60% {
    transform: translateX(3px);
  }
  70% {
    transform: translateX(-2px);
  }
  80% {
    transform: translateX(2px);
  }
  90% {
    transform: translateX(-1px);
  }
  100% {
    transform: translateX(0);
    box-shadow: 0 0 0 rgba(255, 87, 87, 0);
  }
}
</style>
