<template>
  <div class="action-log-item">
    <div class="action-row">
      <SmallCharPreview :char="action.initiator" :gmMode="gmMode" class="initiator" @select="handleSelect"/>
      <div class="action-info">
        <ActionIconMini v-if="action.skill" :skill="action.skill"/>
        <div v-else-if="action.action_type === 'MOVE'" class="action-icon">
          <img alt="Move" src="@/assets/images/action/move.png"/>
          <span> Move </span>
        </div>
        <div v-else-if="action.action_type === 'LONG_REST'" class="action-icon">
          <img alt="Move" src="@/assets/images/action/long_rest.webp"/>
          <span> Long Rest </span>
        </div>
        <div v-else-if="action.action_type === 'SNATCH_ITEM'" class="action-icon">
          <img alt="Move" src="@/assets/images/action/snatch.webp"/>
          <span> Snatch </span>
        </div>
        <div v-else-if="action.action_type === 'GIFT'" class="action-icon">
          <img alt="Move" src="@/assets/images/action/gift.webp"/>
          <span> Gift </span>
        </div>
        <div v-else-if="action.action_type === 'BACK_TO_SAFE_ZONE'" class="action-icon">
          <img alt="Move" src="@/assets/images/action/safe.webp"/>
          <span> Teleport To Safety </span>
        </div>
        <div v-else-if="action.action_type === 'INSPECT'" class="action-icon">
          <img alt="Inspect" src="@/assets/images/action/inspect.webp"/>
          <span> Inspect </span>
          <div class="inspection-result" >
            <SmallCharPreview
                v-for="target in action.targets"
                :key="target.id"
                :char="target"
                :gmMode="gmMode"
                @select="handleSelect"
            />
            <InspectionResult :characters="action.data.characters" />

          </div>


        </div>
        <div v-else-if="action.action_type === 'DICE_ROLL'" class="action-icon">
          <DiceComponent/>
          <span> Dice Roll </span>
        </div>
        <div v-else-if="action.action_type === 'ANOMALY'" class="action-icon">
          <img alt="Anomaly" src="@/assets/images/action/anomaly.png"/>
          <span> Anomaly </span>
        </div>
        <div v-else-if="action.action_type === 'GOD_INTERVENTION'" class="action-icon">
          <img alt="God Intervention" src="@/assets/images/action/godintervention.png"/>
          <span> God Intervention </span>
        </div>
        <div v-else>
          <span class="action-id">ID: {{ action.id }}</span>
          <span class="action-type">Type: {{ action.action_type }}</span>
          <span class="cycle">Cycle: {{ action.cycle.id }}</span>
        </div>
        <span class="status">
          <span :class="{ 'status-true': action.accepted, 'status-false': !action.accepted }">
            Accepted: {{ action.accepted ? 'Yes' : 'No' }}
          </span>
          <span :class="{ 'status-true': action.performed, 'status-false': !action.performed }">
            Performed: {{ action.performed ? 'Yes' : 'No' }}
          </span>
        </span>
      </div>
      <div v-if="action.accepted && !action.performed" class="targets-row">
        <SmallCharPreview
            v-for="target in action.targets"
            :key="target.id"
            :char="target"
            :gmMode="gmMode"
            @select="handleSelect"
        />
      </div>
      <div v-if="action.performed" class="impacts-row">
        <ImpactComponent
            v-for="impact in action.impacts"
            :key="impact.id"
            :impact="impact"
            @selectTarget="handleSelect"
        />
        <SnatchAction  class="snatch-action-impact" v-if="action.action_type === 'SNATCH_ITEM' && action.data" :data="target" v-for="target in action.data.targets" :key="target.id"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import SmallCharPreview from './SmallCharPreview.vue';
import ImpactComponent from './ImpactComponent.vue';
import SkillIcon from "@/components/Action/ActionIcon.vue";
import ActionIconMini from "@/components/Action/ActionIconMini.vue";
import DiceComponent from "@/components/Dice/DiceComponent.vue";
import InspectionResult from "@/components/GameMaster/ActionLog/InspectionResult.vue";
import SnatchAction from "@/components/GameMaster/ActionLog/SnatchAction.vue";

// TypeScript Interfaces
interface Character {
  id: string | number;
  name: string;
  npc?: boolean;
}

interface Skill {
  id: string | number;
  name: string;
  // Add other skill properties as needed
}

interface Cycle {
  id: string | number;
  // Add other cycle properties as needed
}

interface DiceRollResult {
  // Define dice roll result properties as needed
  [key: string]: any;
}

interface Impact {
  id: string | number;
  target: Character;
  type: string;
  violation: string;
  size: string;
  dice_roll_result?: DiceRollResult;
}

interface ActionData {
  characters?: Character[];
  targets?: Character[];
  [key: string]: any;
}

interface Action {
  id: string | number;
  action_type: string;
  initiator: Character;
  targets?: Character[];
  impacts?: Impact[];
  skill?: Skill;
  cycle: Cycle;
  accepted: boolean;
  performed: boolean;
  data?: ActionData;
}

interface Props {
  action: Action;
  gmMode?: boolean;
}

// Props definition
const props = withDefaults(defineProps<Props>(), {
  gmMode: false
});

// Methods
const mapTargetById = (id: string | number): Character | undefined => {
  return props.action.targets?.find(target => target.id === id);
};

const handleSelect = (id: string | number): void => {
  console.log('Selected ID:', id);
};
</script>

<style scoped>
.action-log-item {
  display: flex;
  border: 1px solid #444;
  border-radius: 4px;
  padding: 0.5rem;
  background: #1c1c1c;
  align-items: center;
  gap: 0.5rem;
}

.action-row {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 0.6rem;
}

.initiator {
  flex: 0 0 3rem; /* Fixed size for SmallCharPreview */
}

.action-info {
  flex: 0 0 6rem; /* Fixed size for action-info */
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  font-size: 0.75rem;
  color: #ccc;
}

.action-id {
  font-weight: bold;
  color: #ffcc00;
}

.action-type, .cycle {
  color: #aaa;
}

.status {
  display: flex;
  gap: 0.2rem;
  font-size: 0.6rem;
  flex-direction: column;
}

.status-true {
  color: #00ff00;
}

.status-false {
  color: #ff0000;
}

.targets-row, .impacts-row {
  flex: 1; /* Dynamic size for targets or impacts */
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
}

.targets-row > *:not(:last-child), .impacts-row > *:not(:last-child) {
  margin-right: 0.3rem;
}

h4 {
  font-size: 0.8rem;
  color: #ffcc00;
}

.action-info .action-icon {
  display: flex;
  flex-direction: row;
  gap: 0.2rem;
  justify-content: flex-start;
  align-items: center;
}

.action-info .action-icon span {
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
}

.action-info .action-icon img {
  width: 2em;
  height: 2em;
}

.inspection-result {
  display: flex;
  justify-content: flex-start;
  flex-direction: row;
}

.snatch-action-impact {
  display: flex;
  flex-direction: row;
}
</style>
