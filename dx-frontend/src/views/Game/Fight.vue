<template>
  <div class="battlefield-background horizontal-layout" v-if="player">
    <div id="left-container" class="vertical-layout">
      <player-component ref="playerBlockComponent" :player="player"></player-component>
      <SpellHolderComponent @cast="tryCast" :spells="skills" v-if="!disableUiElements"/>
      <div class="action-buttons-group" v-if="!disableUiElements">
        <ActionButtonComponent>
          <template v-slot:label>Attack</template>
          <template v-slot:icon>⚔️</template>
        </ActionButtonComponent>

        <ActionButtonComponent>
          <template v-slot:label>Defend</template>
          <template v-slot:icon>🛡️</template>
        </ActionButtonComponent>

        <ActionButtonComponent :onclick="activateDXSwitcher">
          <template v-slot:label>DX Shift</template>
          <template v-slot:icon>🌀</template>
        </ActionButtonComponent>

        <ActionButtonComponent>
          <template v-slot:label>History</template>
          <template v-slot:icon>📜</template>
        </ActionButtonComponent>
      </div>
    </div>
    <div id="center-container" class="vertical-layout">
      <CountDown v-if="turn !== undefined" :turn="turn"></CountDown>
      <CardHolderComponent v-if="!disableUiElements" :cards="currentActions" :overlap="100"
                           @move="moveCard" @delete="deleteCard" @duplicate="duplicateCard"
      />
    </div>
    <div id="right-container" class="vertical-layout">
      <div id="right-top-container" class="layout">
      </div>
      <div id="right-center-container" class="layout">
      <enemy-block-component

          v-if="fight"
          @selection="selectTarget"
          ref="enemyBlockComponent"
          :enemies="fight.enemies"
          :class="{ 'non-interactive': disableUiElements }"
      ></enemy-block-component>
      </div>
      <div id="right-bottom-container" class="layout">
        <div id="endTurn" v-if="!disableUiElements">
        <ActionButtonComponent @click="endTurn">
          <template v-slot:label>End Turn</template>
          <template v-slot:icon>
            ⏳
          </template>
        </ActionButtonComponent>
      </div>
      </div>
    </div>
    <div id="actionHistoryList"></div>
    <div id="availableActionList"></div>

    <dimension-switcher-component
        :activated="dsActivated"
        :dimension="player.dimension"
        @switch="switchDimension"
        @abort="deactivateDXSwitcher"
    >
    </dimension-switcher-component>
  </div>
</template>

<script>

import {CharacterGameApi, FightGameApi, SkillsGameApi} from "@/api/backendService.js";
import PlayerComponent from "@/components/Game/Fight/PlayerComponent.vue";
import EnemyComponent from "@/components/Game/Fight/EnemyComponent.vue";
import EnemyBlockComponent from "@/components/Game/Fight/EnemyBlockComponent.vue";
import ActionButtonComponent from "@/components/Game/Fight/ActionButtonComponent.vue";
import ActionCardComponent from "@/components/Game/Fight/ActionCardComponent.vue";
import CardHolderComponent from "@/components/Game/Fight/CardHolderComponent.vue";
import DimensionSwitcherComponent from "@/components/Game/Fight/DimensionSwitcherComponent.vue";
import SpellButtonComponent from "@/components/Game/Fight/SpellButtonComponent.vue";
import SpellHolderComponent from "@/components/Game/Fight/SpellHolderComponent.vue";
import Action from "@/models/Action";
import Player from "@/models/Player";
import {ActionTypeEnum} from "@/api/dx-backend/index";
import {Fight} from "@/models/Fight";
import CountDown from "@/components/Game/Fight/CountDown.vue";
import {Turn} from "@/models/Turn";

export default {
  name: 'FightView',
  components: {
    CountDown,
    SpellHolderComponent,
    SpellButtonComponent,
    DimensionSwitcherComponent,
    CardHolderComponent,
    ActionCardComponent,
    ActionButtonComponent,
    EnemyBlockComponent,
    EnemyComponent,
    PlayerComponent,
  },
  data() {
    return {
      awaitingTurnResults: false,
      displayingTurnResults: false,
      fight: undefined,
      turn: undefined,
      player: undefined,
      skills: undefined,
      target: undefined,
      currentActions: [],
      dsActivated: false,
      loading: true,
    }
  },
  computed: {
    disableUiElements() {
      return this.awaitingTurnResults || this.displayingTurnResults;
    }
  },
  methods: {
    endTurn() {
      console.log('Ending turn');
      this.currentActions.forEach(({action}) => {
        const request = {
          action_type: action.actionType,
          skill: action.actionType === ActionTypeEnum.UseSkill ? action.id : null,
          targets: [action.target.id, ],
          target_dimension: action.actionType === ActionTypeEnum.DimensionShift ? action.id : null,
        };
        console.debug("Commiting Action", request)
        FightGameApi.fightActionCreate(
            request
        )
          .then(response => {
            console.log('Action committed:', response.data);
          })
          .catch(error => {
            console.error('Error committing action', error);
          });
      });
      this.currentActions = [];
      this.$refs.enemyBlockComponent.selectNone()
      this.awaitingTurnResults = true;
    },
    moveCard(action, direction) {
      console.log('Moving card:', action, direction);
      const index = this.currentActions.findIndex(a => a.action === action);
      if (index > -1) {
        const newIndex = direction === 'left' ? index - 1 : index + 1;
        if (newIndex >= 0 && newIndex < this.currentActions.length) {
          this.currentActions.splice(index, 1);
          this.currentActions.splice(newIndex, 0, { target: action.target, action: action, order: newIndex + 1 });
        }
      }
    },
    deleteCard(action) {
      console.log('Deleting card:', action);
      const index = this.currentActions.findIndex(a => a.action === action);
      if (index > -1) {
        this.currentActions.splice(index, 1);
        this.player.discardAction(action);
      }
    },
    duplicateCard(action) {
      console.log('Duplicating card:', action);
      const index = this.currentActions.findIndex(a => a.action === action);
      if (index > -1) {
        const newAction = new Action(action.id, action.name, action.cost, action.target, action.type);
        if (this.player.makeAction(newAction)) {
          this.currentActions.splice(index, 0, { target: action.target, action: newAction, order: index + 1 });
        } else {
          console.warn('Not enough resources to duplicate action');
          this.$refs.playerBlockComponent.blinkattributes();
        }
      }
    },
    tryCast(spell) {
      console.log('Casting spell', spell);
      if (this.target) {
        const action = new Action(spell.id, spell.name, spell.cost, this.target, ActionTypeEnum.UseSkill);
        if (this.player.makeAction(action)) {
          this.makeAction(action, this.target);
        } else {
          console.warn('Not enough resources to cast spell');
          this.$refs.playerBlockComponent.blinkattributes();
        }
      } else {
        console.warn('No target selected');
        this.$refs.enemyBlockComponent.blink();
      }
    },
    makeAction(action, target) {
        this.currentActions.push({ target: target, action: action, order: this.currentActions.length + 1 });
    },
    selectTarget(target) {
      console.log('Selected target:', {target});
      this.target = target;
    },
    activateDXSwitcher() {
      console.debug('Activating DX Switcher')
      this.dsActivated = true;
    },
    deactivateDXSwitcher() {
      this.dsActivated = false;
    },
    switchDimension(direction) {
      console.log('Switching to dimension', direction);
      const newDimension = direction === 'next' ? this.player.dimension + 1: this.player.dimension - 1;
      const action = new Action(direction, 'Dimension Shift', [
        {kind: "Action Points", value: this.player.attributes.ap},
      ], this.player, ActionTypeEnum.DimensionShift);

      console.log('Action:', {action});
      if (this.player.makeAction(action)) {
        this.currentActions = [];
        this.makeAction(action, this.player);
      }
      this.deactivateDXSwitcher()
    },
  },
  mounted() {
    this.$dxBus.on("fight::player_turn_init", (data) => {
      console.log('Player turn started', data);
      this.player = new Player(data.player_info);
      this.turn = new Turn(data.current_turn);
      this.awaitingTurnResults = !this.player.hasUnusedActionPoints()
    });
    Promise.all([
      CharacterGameApi.playerPlayerInfoRetrieve()
          .then(response => {
            this.player = new Player(response.data);
            this.awaitingTurnResults = !this.player.hasUnusedActionPoints()
          })
          .catch(error => {
            console.error('Error fetching player info', error);
          }),
      SkillsGameApi.skillsSkillsList()
          .then(response => {
            this.skills = response.data;
          })
          .catch(error => {
            console.error('Error fetching skills', error);
          }),
      FightGameApi.fightFightCurrentRetrieve()
          .then(response => {
            console.log('Current fight:', response.data);
            this.fight = new Fight(response.data);
          })
          .catch(error => {
            console.error('Error fetching current fight', error);
          })
    ]).then(() => {
      this.loading = false;
    });
    },
};
</script>

<style scoped>
.battlefield-background {
  width: 100%;
  height: 80vh; /* Adjust as needed */
  background-image: url('@/assets/images/fight/fight_1.webp');
  background-size: cover;
  background-position: center;
}
#endTurn {
  position: absolute;
  bottom: 20vh;
  right: 5vh;
  width: 15vh;
  height: 15vh;
}
.action-buttons-group {
  display: flex;
  justify-content: center;
  position: absolute;
  bottom: 20vh;
  width: 30vh;
}
.non-interactive {
  pointer-events: none;
}

#right-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  width: 30%;
  height: 100%;
}
</style>
