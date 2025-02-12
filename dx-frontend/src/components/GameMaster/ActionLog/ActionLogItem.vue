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

<script>
import SmallCharPreview from './SmallCharPreview.vue';
import ImpactComponent from './ImpactComponent.vue';
import SkillIcon from "@/components/Action/ActionIcon.vue";
import ActionIconMini from "@/components/Action/ActionIconMini.vue";
import DiceComponent from "@/components/Dice/DiceComponent.vue";
import InspectionResult from "@/components/GameMaster/ActionLog/InspectionResult.vue";
import SnatchAction from "@/components/GameMaster/ActionLog/SnatchAction.vue";

export default {
  name: 'ActionLogItem',
  components: {
    SnatchAction,
    InspectionResult,
    DiceComponent,
    ActionIconMini,
    SkillIcon,
    SmallCharPreview,
    ImpactComponent,
  },
  props: {
    action: Object,
    gmMode: {
      type: Boolean,
      default: false,
    }
  },
  methods: {
    mapTargetById(id) {
      return this.action.targets.find(target => target.id === id);
    },
    handleSelect(id) {
      console.log('Selected ID:', id);
    },
  },
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
  flex: 0 0 10rem; /* Fixed size for action-info */
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
  gap: 0.5rem;
  font-size: 0.75rem;
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
  gap: 0.5rem;
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
