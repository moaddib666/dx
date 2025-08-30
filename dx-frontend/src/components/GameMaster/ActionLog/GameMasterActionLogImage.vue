<script setup lang="ts">
import {ActionType5f8Enum, GameMasterCharacterActionLog} from "@/api/dx-backend";
import ActionIconMini from "@/components/Action/ActionIconMini.vue";

interface Props {
  action: GameMasterCharacterActionLog
}

// Props definition
const props = defineProps<Props>()
</script>

<template>
  <img v-if="action.skill" :src="action.skill.icon" :alt="action.action_type"/>
  <img v-else-if="action.action_type === ActionType5f8Enum.Move" class="action-image" :alt="action.action_type"
       src="@/assets/images/action/move.png"/>
  <img v-else-if="action.action_type === 'LONG_REST'" :alt="action.action_type" class="action-icon"
       src="@/assets/images/action/long_rest.webp"/>
  <img v-else-if="action.action_type === 'SNATCH_ITEM'" :alt="action.action_type" class="action-icon"
       src="@/assets/images/action/snatch.webp"/>
  <img v-else-if="action.action_type === 'GIFT'" class="action-icon" :alt="action.action_type"
       src="@/assets/images/action/gift.webp"/>
  <img v-else-if="action.action_type === 'BACK_TO_SAFE_ZONE'" class="action-icon" :alt="action.action_type"
       src="@/assets/images/action/safe.webp"/>
  <img v-else-if="action.action_type === 'INSPECT'" class="action-icon" alt="Inspect"
       src="@/assets/images/action/inspect.webp"/>
  <img v-else-if="action.action_type === 'DICE_ROLL'" class="action-icon" :alt="action.action_type"
       src="@/assets/images/action/dice_roll.png"/>
  <img v-else-if="action.action_type === 'ANOMALY'" class="action-icon" alt="Anomaly"
       src="@/assets/images/action/anomaly.png"/>
  <img v-else-if="action.action_type === 'GOD_INTERVENTION'" class="action-icon" alt="God Intervention"
       src="@/assets/images/action/godintervention.png"/>
</template>

<style scoped>

</style>