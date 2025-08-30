<template>
  <div class="action-log-item">
    <AvatarImage :char-id="action.initiator.id" :gm-mode="true" class="initiator-image" v-if="action.initiator"/>
    <!-- TODO: Add support multitarget actions -->
    <AvatarImage v-if="hasTarget"
                 :char-id="action.targets[0].id"
                 :gm-mode="true" class="target-image"/>
    <div class="npc-label" v-if="action.initiator.npc">NPC</div>


    <div class="not-accepted-label status-label" v-if="!action.accepted">Not Accepted</div>
    <div class="not-performed-label status-label" v-else-if="action.performed">Not Performed</div>

    <GameMasterActionLogImage :action="action" class="action-image"/>
    <div class="action-content">
      <CharacterInlineDetails @click="() => {console.debug('selected', action.initiator.id)}" class="info"
                              id="initiator-info"
                              :char-id="action.initiator.id" :gm-mode="true"/>
      <div id="action-information">
        <span>{{ getActionTypeTranslation() }}</span>
        <h3 v-if="action.skill">{{ action.skill.name }}</h3>
      </div>

      <CharacterInlineDetails @click="() => { console.debug('selected',target.id )}" class="info" id="target-info"
                              :char-id="target.id" :gm-mode="true" v-if="hasTarget"/>
      <div v-else class="info" id="target-info"></div>
    </div>
    <!--    <div class="action-info">-->
    <!--      <ActionIconMini class="action-icon" v-if="action.skill" :skill="action.skill"/>-->
    <!--      <div v-else-if="action.action_type === 'MOVE'" class="action-icon">-->
    <!--        <img alt="Move" src="@/assets/images/action/move.png"/>-->
    <!--        <span> Move </span>-->
    <!--      </div>-->
    <!--      <div v-else-if="action.action_type === 'LONG_REST'" class="action-icon">-->
    <!--        <img alt="Move" src="@/assets/images/action/long_rest.webp"/>-->
    <!--        <span> Long Rest </span>-->
    <!--      </div>-->
    <!--      <div v-else-if="action.action_type === 'SNATCH_ITEM'" class="action-icon">-->
    <!--        <img alt="Move" src="@/assets/images/action/snatch.webp"/>-->
    <!--        <span> Snatch </span>-->
    <!--      </div>-->
    <!--      <div v-else-if="action.action_type === 'GIFT'" class="action-icon">-->
    <!--        <img alt="Move" src="@/assets/images/action/gift.webp"/>-->
    <!--        <span> Gift </span>-->
    <!--      </div>-->
    <!--      <div v-else-if="action.action_type === 'BACK_TO_SAFE_ZONE'" class="action-icon">-->
    <!--        <img alt="Move" src="@/assets/images/action/safe.webp"/>-->
    <!--        <span> Teleport To Safety </span>-->
    <!--      </div>-->
    <!--      <div v-else-if="action.action_type === 'INSPECT'" class="action-icon">-->
    <!--        <img alt="Inspect" src="@/assets/images/action/inspect.webp"/>-->
    <!--        <span> Inspect </span>-->
    <!--        <div class="inspection-result">-->
    <!--          <SmallCharPreview-->
    <!--              v-for="hasTarget in action.targets"-->
    <!--              :key="hasTarget.id"-->
    <!--              :char="hasTarget"-->
    <!--              :gmMode="gmMode"-->
    <!--              @select="handleSelect"-->
    <!--          />-->
    <!--          <InspectionResult :characters="action.data.characters"/>-->

    <!--        </div>-->


    <!--      </div>-->
    <!--      <div v-else-if="action.action_type === 'DICE_ROLL'" class="action-icon">-->
    <!--        <DiceComponent/>-->
    <!--        <span> Dice Roll </span>-->
    <!--      </div>-->
    <!--      <div v-else-if="action.action_type === 'ANOMALY'" class="action-icon">-->
    <!--        <img alt="Anomaly" src="@/assets/images/action/anomaly.png"/>-->
    <!--        <span> Anomaly </span>-->
    <!--      </div>-->
    <!--      <div v-else-if="action.action_type === 'GOD_INTERVENTION'" class="action-icon">-->
    <!--        <img alt="God Intervention" src="@/assets/images/action/godintervention.png"/>-->
    <!--        <span> God Intervention </span>-->
    <!--      </div>-->
    <!--      <div v-else>-->
    <!--        <span class="action-id">ID: {{ action.id }}</span>-->
    <!--        <span class="action-type">Type: {{ action.action_type }}</span>-->
    <!--        <span class="cycle">Cycle: {{ action.cycle.id }}</span>-->
    <!--      </div>-->
    <!--      <span class="status">-->
    <!--          <span :class="{ 'status-true': action.accepted, 'status-false': !action.accepted }">-->
    <!--            Accepted: {{ action.accepted ? 'Yes' : 'No' }}-->
    <!--          </span>-->
    <!--          <span :class="{ 'status-true': action.performed, 'status-false': !action.performed }">-->
    <!--            Performed: {{ action.performed ? 'Yes' : 'No' }}-->
    <!--          </span>-->
    <!--        </span>-->
    <!--    </div>-->
    <!--    <div v-if="action.accepted && !action.performed" class="targets-row">-->
    <!--      <SmallCharPreview-->
    <!--          v-for="hasTarget in action.targets"-->
    <!--          :key="hasTarget.id"-->
    <!--          :char="hasTarget"-->
    <!--          :gmMode="gmMode"-->
    <!--          @select="handleSelect"-->
    <!--      />-->
    <!--    </div>-->
    <!--    <div v-if="action.performed" class="impacts-row">-->
    <!--      <ImpactComponent-->
    <!--          v-for="impact in action.impacts"-->
    <!--          :key="impact.id"-->
    <!--          :impact="impact"-->
    <!--          @selectTarget="handleSelect"-->
    <!--      />-->
    <!--      <SnatchAction class="snatch-action-impact" v-if="action.action_type === 'SNATCH_ITEM' && action.data"-->
    <!--                    :data="hasTarget" v-for="hasTarget in action.data.targets" :key="hasTarget.id"/>-->
    <!--    </div>-->
  </div>
</template>

<script setup lang="ts">
import AvatarImage from "@/components/Character/AvatarImage.vue";
import {GameMasterCharacterActionLog} from "@/api/dx-backend";
import GameMasterActionLogImage from "@/components/GameMaster/ActionLog/GameMasterActionLogImage.vue";
import {computed} from "vue";
import CharacterInlineDetails from "@/components/Character/CharacterInlineDetails.vue";
import { useI18n } from 'vue-i18n';

interface Props {
  action: GameMasterCharacterActionLog;
  gmMode?: boolean;
}

// Props definition
const props = withDefaults(defineProps<Props>(), {
  gmMode: false
});

const action = props.action;

// i18n setup
const { t } = useI18n();

const hasTarget = computed(() => {
  return action.targets && action.targets.length > 0 && action.targets[0].id != action.initiator.id
})
const target = computed(() => {
  return hasTarget.value ? action.targets[0] : null;
})

// Method to get the appropriate translation based on action status
const getActionTypeTranslation = () => {
  // If action was accepted and performed, use past tense (successful)
  if (action.accepted && action.performed) {
    return t('actionTypeEnumPerformed.' + action.action_type);
  }
  // If action was not accepted or not performed, use attempted tense (failed)
  else {
    return t('actionTypeEnumAttempted.' + action.action_type);
  }
}
const emit = defineEmits<{
  characterSelected: [charId: string];
}>();
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
  position: relative;
  min-height: 10vh;
  font-size: 0.8rem;
}

.initiator-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 25%;
  height: 100%;
  object-fit: cover;
  object-position: top;
  mask: linear-gradient(to right, rgba(0, 0, 0, 1) 35%, rgba(0, 0, 0, 0) 90%);
}

.target-image {
  position: absolute;
  top: 0;
  right: 0;
  width: 25%;
  height: 100%;
  object-fit: cover;
  object-position: top;
  mask: linear-gradient(to left, rgba(0, 0, 0, 1) 35%, rgba(0, 0, 0, 0) 90%);
}


.npc-label {
  background: rgba(255, 204, 0, 1);
  color: #1c1c1c;
  font-size: 0.6rem;
  font-weight: bold;
  padding: 0.1rem 0.3rem;
  border-radius: 4px;
  margin-left: 0.3rem;
  position: absolute;
  top: 0.3rem;
  left: 0.3rem;
}


.action-image {
  width: 45%;
  height: 100%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  mask: radial-gradient(circle at top, rgba(0, 0, 0, 8) 20%, rgba(0, 0, 0, 0) 66%);
  object-fit: cover;
  object-position: center;
  opacity: 0.3;
}

.status-label {
  position: absolute;
  top: 0.3rem;
  right: 0.3rem;
  font-size: 0.6rem;
  font-weight: bold;
  padding: 0.1rem 0.3rem;
  border-radius: 4px;
  text-shadow: 0 0 3px rgba(0, 0, 0, 0.7);
}

.not-accepted-label {
  background: rgba(255, 69, 0, 0.8);
  color: white;
}

.not-performed-label {
  background: rgba(90, 90, 89, 0.8);
  color: white;
}

.action-content {
  display: flex;
  flex-direction: row;
  z-index: 1;
  width: 100%;
  justify-content: space-between;
  padding: 0 1rem;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  max-width: 25%;
  justify-content: flex-end;
  flex-wrap: wrap;
  flex:1;
}

#initiator-info {
  align-items: flex-start;
  text-align: left;
}

#target-info {
  align-items: flex-end;
  text-align: right;
}

#action-information {
  flex: 1;
  text-align: center;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-shadow: 1px 1px 2px #000;
  align-self: center;
  justify-self: center;
}

.invisible {
  visibility: hidden;
}

.info {
  cursor: pointer;
}
</style>
