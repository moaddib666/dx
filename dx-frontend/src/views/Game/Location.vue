<template>
  <div class="location-view">
    <!-- Background View -->
    <BackgroundView
        :key="position.id"
        :background="position.image"
        class="background-view"
    ></BackgroundView>

    <!-- Top Row (Character Cards) -->
    <div class="top-row">
      <CharacterCardHolder
          :characters="characters"
          :selectedCharacterId="selectedCharacterId"
          class="top-left"
          @characterSelected="updateSelectedGameObjectId"
      />
      <div class="top-separator"></div>
      <CharacterCardHolder
          :characters="npcCharacters"
          :selectedCharacterId="selectedCharacterId"
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
        />
        <CoordinatesDisplay :coordinates="playerInfo.coordinates"/>
      </div>
      <div class="center-center">
        <DiceVisualizer v-if="diceActivated" :result="diceResult" @close="deactivateDice" @selectedDice="diceRoll"/>
        <CompassComponent
            v-else-if="hasActionPoints && selectedGameObjectId === null"
            :connections="activeConnections"
            centerAction="true"
            centerLabel="Up"
            class="compass-component"
            @move="handleMove"
        />
        <ActionConstructor v-else-if="hasActionPoints && selectedGameObjectId !== null"
                           :availableActions="availableActions"
                           :availableGameObjects="availableGameObjects"
                           :preSelectedTarget="selectedGameObjectId"
                           @applyAction="applyAction"
                           @cancelAction="cancelAction"
        />


      </div>
      <div class="center-right">
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
        <ActionButton
            v-if="hasActionPoints"
            @click="selectSelf"
        />
        <DiceComponent
            @click="activateDice"
        />
      </div>
    </div>
  </div>
</template>


<script>
import CompassComponent from '@/components/Game/Location/Compass.vue';
import {ActionGameApi, CharacterGameApi, SkillsGameApi, WorldGameApi} from "@/api/backendService.js";
import CharacterCardHolder from "@/components/Game/Location/CharacterCardHolder.vue";
import PlayerComponent from "@/components/Game/Location/PlayerComponent.vue";
import BackgroundView from "@/components/Game/Location/BackgroundView.vue";
import ActionService from "@/services/actionsService.js";
import PlayerService from "@/services/playerService.js";
import DiceComponent from "@/components/Dice/DiceComponent.vue";
import CurrentTurnComponent from "@/components/Game/CurrentTurnComponent.vue";
import GameObjectSelector from "@/components/Selectors/GameObjectSelector.vue";
import ActionSelector from "@/components/Selectors/ActionSelector.vue";
import ActionPreview from "@/components/Pickers/ActionPreview.vue";
import GlassPlayButton from "@/components/btn/GlassPlayButton.vue";
import ActionConstructor from "@/components/Action/ActionConstructor.vue";
import ActionButton from "@/components/Action/ActionButton.vue";
import DiceVisualizer from "@/components/Dice/DiceVisualizer.vue";
import CoordinatesDisplay from "@/components/Map/Coordinates.vue";

export default {
  name: 'LocationView',
  components: {
    CoordinatesDisplay,
    DiceVisualizer,
    ActionButton,
    ActionConstructor,
    GlassPlayButton,
    ActionPicker: ActionPreview,
    ActionSelector,
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
      diceResult: null,
      diceActivated: false,
    };
  },
  computed: {
    availableActions() {
      const skills = this.playerSkills.map((knownSkill) => {
        return knownSkill.skill;
      });
      const actions = []
      return actions.concat(skills);
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
    async selectSelf() {
      this.selectedGameObjectId = this.playerInfo.id;
    },
    async activateDice() {
      this.diceActivated = true;
    },
    async deactivateDice() {
      this.diceActivated = false;
    },
    async cancelAction() {
      this.selectedGameObjectId = null;
    },
    async applyAction(action) {
      await this.actionService.performAction(action);
      await this.getPlayerInfo();
    },
    async updateSelectedGameObjectId(id) {
      this.selectedGameObjectId = id;
    },
    async updateAll() {
      await this.getCurrentPositionInfo();
      await this.getPlayerInfo();
      await this.getPlayerSkills();
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
    },
    async resolveCharacter(characterId) {
      const data = (await CharacterGameApi.characterRetrieve(characterId)).data;
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
      this.playerInfo = (await CharacterGameApi.characterCharacterInfoRetrieve()).data;
      if (this.playerGeneralInfo === null) {
        this.playerGeneralInfo = (await CharacterGameApi.characterRetrieve(this.playerInfo.id)).data;
      }
      this.playerService = new PlayerService(this.playerInfo)
    },
    async getPlayerSkills() {
      this.playerSkills = (await SkillsGameApi.skillsSkillsList()).data;
    }
  },
};
</script>

<style scoped>
.center-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60vh;
}

.location-view {
  display: flex;
  flex-direction: column;
  position: relative;
  height: 80vh;
  overflow: hidden;
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
  align-items: flex-end;
  justify-content: flex-end;
  gap: 1rem;
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
  background: rgba(255, 255, 255, 0.3);
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
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  flex-direction: row;
  z-index: 20;
  padding-right: 1rem;
  gap: 1rem;
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
</style>
