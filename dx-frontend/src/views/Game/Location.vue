<template>
  <div class="location-view">
    <!-- Background View -->
    <BackgroundView
        :key="position.id"
        :background="position.image"
        class="background-view"
    ></BackgroundView>

    <!-- Compass Component (Centered) -->
    <div class="center-section">

      <CompassComponent
          v-if="hasActionPoints && selectedGameObjectId === null"
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
                         @applyAction="alert"
                         @cancelAction="cancelAction"
      />
    </div>
    <!-- Top Row (Character Cards) -->
    <div class="top-row">
      <CharacterCardHolder
          :characters="activeCharacters"
          :selectedCharacterId="selectedCharacterId"
          @characterSelected="updateSelectedGameObjectId"
      />
    </div>

    <!-- Side Columns -->
    <div class="side-columns">
      <!-- Player Component (Left) -->
      <PlayerComponent
          :player="playerInfo"
          :playerImage="playerGeneralInfo.biography.avatar"
          class="player-component"
      />

      <!-- Current Turn Component (Right, Top) -->

    </div>
    <CurrentTurnComponent
        class="current-turn-component"
        @turnChanged="updateAll"
    />
    <!-- Dice Component (Bottom, Right) -->
    <DiceComponent
        :result="diceResult"
        class="dice-component"
        @selectedDice="diceRoll"
    />
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

export default {
  name: 'LocationView',
  components: {
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
      selectedCharacterId: 'f3c4216f-cbaa-4792-b6e6-1cedd502deae',
      actionService: new ActionService(ActionGameApi),
      playerService: null,
      playerSkills: null,
      diceResult: null,
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
      const itemsGameObjects = [];
      return playersGameObjects.concat(itemsGameObjects);
    },
    hasActionPoints() {
      return this.playerService?.hasActionPoints();
    },
    activeCharacters() {
      return this.characters
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
    async cancelAction() {
      this.selectedGameObjectId = null;
    },
    async updateSelectedAction(action) {
      this.selectedAction = action;
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
      const data = await CharacterGameApi.characterRetrieve(characterId);
      this.characters.push(data.data);
    },
    async getCurrentPositionInfo() {
      this.position = (await WorldGameApi.worldPositionCurrentRetrieve()).data;
      this.connections = {}
      this.position.connections.forEach((conn) => {
        this.connections[conn.direction] = conn;
      });
      this.characters = [];
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
.action-constructor-holder {
  display: flex;
  align-items: center;
  flex-direction: row;
  gap: 0.1rem;
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

.compass-component {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
}

.top-row {
  padding: 10px;
  display: flex;
  justify-content: center;
  z-index: 5;
}

.side-columns {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  position: absolute;
  top: 150px;
  width: 100%;
  padding: 10px;
}

.current-turn-component {
  position: absolute;
  bottom: 20px;
  left: 20px;
  z-index: 20;
}

.dice-component {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 200;
}

.player-component {
  position: fixed;
  top: 50%;
  transform: translate(0, -50%);
  z-index: 10;
}

/* Responsive Design */
@media (max-width: 768px) {
  .side-columns {
    flex-direction: column;
    align-items: center;
  }

}

@media (max-width: 480px) {
  .compass-component {
    width: 90%;
  }

  .dice-component {
    bottom: 10px;
    right: 10px;
  }

  .top-row {
    flex-direction: column;
    align-items: center;
  }
}
</style>
