<template>
  <div class="action-log-item">
    <!-- Action Details -->
    <div class="action-details">
      <SmallCharPreview
          :char="{
            id: initiator,
          }"
          :gmMode="false"
      />
      <ActionIconMini v-if="skill" :skill="skillService.getSkill(skill)"/>
      <div v-else-if="actionType === 'MOVE'" class="action-icon">
        <img alt="Move" src="@/assets/images/action/move.png"/>
        <span> Move </span>
      </div>
      <div v-else-if="actionType === 'LONG_REST'" class="action-icon">
        <img alt="Long Rest" src="@/assets/images/action/long_rest.webp"/>
        <span> Long Rest </span>
      </div>
      <div v-else-if="actionType === 'SNATCH_ITEM'" class="action-icon">
        <img alt="Snatch" src="@/assets/images/action/snatch.webp"/>
        <span> Snatch </span>
      </div>
      <div v-else-if="actionType === 'BACK_TO_SAFE_ZONE'" class="action-icon">
        <img alt="Teleport" src="@/assets/images/action/safe.webp"/>
        <span> Teleport To Safety </span>
      </div>
      <div v-else-if="actionType === 'INSPECT'" class="action-icon">
        <img alt="Inspect" src="@/assets/images/action/inspect.webp"/>
        <span> Inspect </span>
      </div>
      <div v-else-if="actionType === 'DICE_ROLL'" class="action-icon">
        <DiceComponent/>
        <span> Dice Roll </span>
      </div>
      <div v-else-if="actionType === 'GOD_INTERVENTION'" class="action-icon">
        <img alt="God Intervention" src="@/assets/images/action/godintervention.png"/>
        <span> God Intervention </span>
      </div>
      <div v-else>
        <span class="action-type">Type: {{ actionType }}</span>
      </div>
    </div>
    <!-- Impacts -->
    <div class="impacts" v-if="impacts && impacts.length">
      <div class="impact-list">
        <RPGActionImpactItem
            v-for="impact in impacts"
            :key="impact.id"
            :impact="impact"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, withDefaults } from 'vue';
import RPGActionImpactItem from "./RPGActionImpactItem.vue";
import SmallCharPreview from "@/components/GameMaster/ActionLog/SmallCharPreview.vue";
import DiceComponent from "@/components/Dice/DiceComponent.vue";
import ActionIconMini from "@/components/Action/ActionIconMini.vue";
import defaultSkillServiceInstance from "@/services/skillService.js";
import { CharacterLogActionImpact } from '@/api/dx-backend/api';

const props = withDefaults(defineProps<{
  initiator: string;
  actionType: string;
  skill: number;
  data?: Record<string, any>;
  impacts: CharacterLogActionImpact[];
}>(), {
  data: () => ({}),
});

const skillService = defaultSkillServiceInstance;
</script>

<style scoped>
.action-log-item {
  display: flex;
  flex-direction: column;
  border-bottom: 0.1rem dashed rgba(255, 255, 255, 0.5);
}

.action-details {
  display: flex;
  align-items: center;
  flex-direction: row;
  gap: 1rem;
}

.impact-list {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.action-icon {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: "Roboto", sans-serif;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
}

.action-icon img {
  width: 2.3em;
  height: 2.3em;
  object-fit: contain;
  border-radius: 0.2em;
}
</style>