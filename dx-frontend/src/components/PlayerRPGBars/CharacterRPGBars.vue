<script setup lang="ts">
import RPGAvatar from './RPGAvatar.vue'
import RpgHealthStatBar from './RPGHealthStatBar.vue'
import RPGFlowStatBar from "@/components/PlayerRPGBars/RPGFlowStatBar.vue";
import RPGActionPointsStatBar from "@/components/PlayerRPGBars/RPGActionPointsStatBar.vue";
import RpgEffectHolder from "@/components/PlayerRPGBars/RPGEffectHolder.vue";
import {ActiveEffect, ActiveShield} from "@/api/dx-backend";
import RPGShieldHolder from "@/components/PlayerRPGBars/RPGShieldHolder.vue";
import {defineEmits} from 'vue';

interface Character {
  name: string;
  level?: number;
  health: number;
  maxHealth: number;
  flow: number;
  maxFlow: number;
  actionPoints: number;
  maxActionPoints: number;
  avatar?: string;
}

interface Props {
  character: Character;
  shields?: ActiveShield[];
  effects?: ActiveEffect[];
  resetBaseStats: boolean;
}


const emits = defineEmits<{
  (e: 'openInfo', character: Character): void;
}>();

const props = withDefaults(defineProps<Props>(), {});

</script>

<template>
  <div class="rpg-bars-container">
    <!-- Character Avatar -->
    <RPGAvatar
        :avatar-url="props.character.avatar"
        :statsIncrementIcon="props.resetBaseStats"
        @click="emits('openInfo', props.character)"
    />
    <!-- Bars -->
    <div class="rpg-bars-holder">
      <RpgHealthStatBar
          :current="props.character.health"
          :max="props.character.maxHealth"
      ></RpgHealthStatBar>
      <RPGFlowStatBar
          :current="props.character.flow"
          :max="props.character.maxFlow"
      ></RPGFlowStatBar>
      <RPGActionPointsStatBar
          :current="props.character.actionPoints"
          :max="props.character.maxActionPoints"
      ></RPGActionPointsStatBar>
      <!-- Shields -->
      <div class="rpg-shields-holder" v-if="props.shields && props.shields.length > 0">
        <RPGShieldHolder
            v-for="shield in props.shields"
            :shield="shield"
            :key="shield.shield.id"
        />
      </div>
    </div>
  </div>
  <!-- Effects -->
  <div class="rpg-effects-container" v-if="props.effects && props.effects.length > 0">
    <RpgEffectHolder
        v-for="effect in props.effects"
        :key="effect.id"
        :effect="effect"
    ></RpgEffectHolder>
  </div>

</template>

<style scoped>
.rpg-effects-container {
  display: flex;
  flex-direction: row;
  justify-content: left;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: -1.5rem;
  margin-left: 6rem;
}

.rpg-bars-container {
  display: flex;
  align-items: center;
}

.rpg-bars-holder {
  display: flex;
  flex-direction: column;
  flex: 1;
  justify-items: center;
  margin-left: -2rem;
}

.rpg-shields-holder {
  display: flex;
  flex-direction: row;
  justify-content: left;
  height: auto;
  gap: 0.2rem;
  margin-top: 0.5rem;
}

</style>