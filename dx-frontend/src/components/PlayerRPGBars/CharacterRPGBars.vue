<script setup lang="ts">
import { computed } from 'vue'
import RPGAvatar from './RPGAvatar.vue'
import RpgHealthStatBar from './RPGHealthStatBar.vue'
import RPGFlowStatBar from "@/components/PlayerRPGBars/RPGFlowStatBar.vue";
import RPGActionPointsStatBar from "@/components/PlayerRPGBars/RPGActionPointsStatBar.vue";
// import RPGShieldHolder from './RPGShieldHolder.vue'
// import RPGEffectsHolder from './RPGEffectsHolder.vue'

interface Shield {
  type: 'physical' | 'energy' | 'heat' | 'cold' | 'light' | 'dark' | 'mental'
  value: number
  maxValue?: number
  icon?: string
}

interface Effect {
  id: string
  name: string
  icon?: string
  duration?: number
  maxDuration?: number
  stacks?: number
  type?: 'buff' | 'debuff' | 'neutral'
}

interface CharacterStats {
  health: number
  maxHealth: number
  flow: number
  maxFlow: number
  actionPoints: number
  maxActionPoints: number
  avatar?: string
  name?: string
  level?: number
  shields?: Shield[]
  effects?: Effect[]
}

const props = withDefaults(defineProps<{
  character?: CharacterStats
  size?: 'small' | 'medium' | 'large'
}>(), {
  size: 'medium',
  character: () => ({
    health: 85,
    maxHealth: 100,
    flow: 45,
    maxFlow: 60,
    actionPoints: 3,
    maxActionPoints: 5,
    name: 'Character',
    level: 12,
    shields: [],
    effects: []
  })
})

const sizeClasses = computed(() => ({
  small: 'rpg-bars--small',
  medium: 'rpg-bars--medium',
  large: 'rpg-bars--large'
}[props.size]))
</script>

<template>
  <div class="rpg-bars-container" :class="sizeClasses">
    <!-- Character Avatar -->
    <RPGAvatar
      :name="character.name"
      :level="character.level"
      :avatar-url="character.avatar"
      :size="size"
    />
    <!-- Bars -->
    <div class="rpg-bars-holder">
      <RpgHealthStatBar :current="7" :max="10"></RpgHealthStatBar>
      <RPGFlowStatBar :current="10" :max="20"></RPGFlowStatBar>
      <RPGActionPointsStatBar :current="9" :max="9"></RPGActionPointsStatBar>
    </div>
  </div>
</template>

<style scoped>
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

</style>