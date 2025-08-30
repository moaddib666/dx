<template>
  <div class="action-log--container">
    <div class="action-log-item">
      <AvatarImage :char-id="action.initiator.id" :gm-mode="true" class="initiator-image" v-if="action.initiator"/>
      <!-- TODO: Add support multitarget actions -->
      <AvatarImage v-if="hasTarget"
                   :char-id="action.targets[0].id"
                   :gm-mode="true" class="target-image"/>
      <div class="npc-label" v-if="action.initiator.npc">NPC</div>


      <div class="not-accepted-label status-label" v-if="!action.accepted">Not Accepted</div>
      <div class="not-performed-label status-label" v-else-if="!action.performed">Not Performed</div>

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
    </div>
    <div v-if="action.performed" class="impacts">
      <ImpactComponent
          v-for="impact in action.impacts.filter( impact => impact.size && impact.size > 0 )"
          :key="impact.id"
          :impact="impact"

      />
                <SnatchAction class="snatch-action-impact" v-if="action.action_type === 'SNATCH_ITEM' && action.data"
                              :data="hasTarget" v-for="hasTarget in action.data.targets" :key="hasTarget.id"/>
    </div>
  </div>

</template>

<script setup lang="ts">
import AvatarImage from "@/components/Character/AvatarImage.vue";
import {GameMasterCharacterActionLog} from "@/api/dx-backend";
import GameMasterActionLogImage from "@/components/GameMaster/ActionLog/GameMasterActionLogImage.vue";
import {computed} from "vue";
import CharacterInlineDetails from "@/components/Character/CharacterInlineDetails.vue";
import {useI18n} from 'vue-i18n';
import ImpactComponent from "@/components/GameMaster/ActionLog/ImpactComponent.vue";
import SnatchAction from "@/components/GameMaster/ActionLog/SnatchAction.vue";

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
const {t} = useI18n();

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
.action-log--container {
  display: flex;
  flex-direction: column;
  margin-bottom: 0.2rem;
  border: 1px solid #444;
  border-radius: 4px;
  background: #1c1c1c;
  font-size: 0.68rem;
}

.action-log-item {
  display: flex;
  align-items: center;
  position: relative;
  min-height: 6.5vh;

}

.impacts {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  border-top: 1px solid #444;
  margin: 0;
  padding-left: 2.3em;
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
  font-size: 0.5rem;
  font-weight: bold;
  padding: 0.1rem 0.3rem;
  border-radius: 4px;
  position: absolute;
  top: 0.1rem;
  left: 0.1rem;
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
  flex: 1;
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
  text-wrap: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
