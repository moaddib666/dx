<template>
  <div :class="typeClass" class="skill-holder">
    <img class="icon" v-if="icon" :src="icon" alt="Skill Icon"/>
    <slot class="icon" v-else-if="useSlotIcon"/>
    <img class="icon" v-else alt="Skill Icon" src="@/assets/images/skill/default.webp"/>
    <div class="required-stats">
      <div v-if="costByKind('Action Points')" :title="'Action Points Cost: ' + costByKind('Action Points')!.value"
           class="cost ap-cost">
        <span>{{ costByKind('Action Points')!.value }}</span>
      </div>
      <div v-if="costByKind('Energy')" :title="'Energy Cost: ' + costByKind('Energy')!.value" class="cost energy-cost">
        <span>{{ costByKind('Energy')!.value }}</span>
      </div>
      <div v-if="costByKind('Health')" :title="'Health Cost: ' + costByKind('Health')!.value" class="cost health-cost">
        <span>{{ costByKind('Health')!.value }}</span>
      </div>
    </div>
    <div class="skill-name">
      <span>{{ name }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// TypeScript interfaces
interface SkillCost {
  kind: string
  value: number
}

interface Skill {
  name?: string
  type?: 'attack' | 'defense' | 'heal' | 'buff' | 'debuff' | 'utility' | 'special'
  icon?: string | null
  cost?: SkillCost[]
}

// Props with TypeScript typing
interface Props {
  fade?: boolean
  skill: Skill
  useSlotIcon?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  fade: false,
  useSlotIcon: false
})

// Computed properties
const name = computed(() => props.skill.name || "Unnamed Skill")

const type = computed(() => props.skill.type || "utility")

const icon = computed(() => props.skill.icon || null)

const typeClass = computed(() => `skill-${type.value}` + (props.fade ? " fade" : ""))

// Methods converted to functions
const costByKind = (kind: string): SkillCost | null => {
  return props.skill.cost?.find((cost) => cost.kind === kind) || null
}
</script>
<style scoped>
.skill-holder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  border-radius: 0.5rem;
  cursor: pointer;
  position: relative;
  color: #fada95;
  padding: 0.35rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.3s;
}

.skill-holder:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.skill-holder:active {
  transform: translateY(0);
}

/* Dynamic Skill Type Colors - Updated to match GMCharSelector theme */
.skill-attack {
  border: 2px solid rgba(255, 23, 68, 0.6);
  box-shadow: 0 0 8px rgba(255, 23, 68, 0.3);
}

.skill-attack:hover {
  border-color: #ff1744;
  box-shadow: 0 4px 12px rgba(255, 23, 68, 0.4);
}

.skill-defense {
  border: 2px solid rgba(127, 255, 22, 0.6);
  box-shadow: 0 0 8px rgba(127, 255, 22, 0.3);
}

.skill-defense:hover {
  border-color: #7fff16;
  box-shadow: 0 4px 12px rgba(127, 255, 22, 0.4);
}

.skill-heal {
  border: 2px solid rgba(76, 175, 80, 0.6);
  box-shadow: 0 0 8px rgba(76, 175, 80, 0.3);
}

.skill-heal:hover {
  border-color: #4caf50;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.skill-buff {
  border: 2px solid rgba(255, 193, 7, 0.6);
  box-shadow: 0 0 8px rgba(255, 193, 7, 0.3);
}

.skill-buff:hover {
  border-color: #ffc107;
  box-shadow: 0 4px 12px rgba(255, 193, 7, 0.4);
}

.skill-debuff {
  border: 2px solid rgba(183, 28, 28, 0.6);
  box-shadow: 0 0 8px rgba(183, 28, 28, 0.3);
}

.skill-debuff:hover {
  border-color: #b71c1c;
  box-shadow: 0 4px 12px rgba(183, 28, 28, 0.4);
}

.skill-utility {
  border: 2px solid rgba(158, 158, 158, 0.6);
  box-shadow: 0 0 8px rgba(158, 158, 158, 0.3);
}

.skill-utility:hover {
  border-color: #9e9e9e;
  box-shadow: 0 4px 12px rgba(158, 158, 158, 0.4);
}

.skill-special {
  border: 2px solid rgba(103, 58, 183, 0.6);
  box-shadow: 0 0 8px rgba(103, 58, 183, 0.3);
}

.skill-special:hover {
  border-color: #673ab7;
  box-shadow: 0 4px 12px rgba(103, 58, 183, 0.4);
}

.required-stats {
  z-index: 2;
  display: flex;
  flex-direction: row;
  font-size: 0.75rem;
  gap: 0.175rem;
}

/* Cost Icons - Updated with GMCharSelector styling */
.cost {
  width: calc(1rem + 0.1vw);
  height: calc(1rem + 0.1vw);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: calc(0.5rem + 0.1vw);
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  border-radius: 0.263rem;
  transition: all 0.2s ease;
}

.energy-cost {
  background: rgba(0, 123, 255, 0.3);
  border: 1px solid rgba(0, 232, 255, 0.5);
  color: #fada95;
  box-shadow: 0 0 5px rgba(0, 232, 255, 0.3);
}

.energy-cost:hover {
  background: rgba(0, 123, 255, 0.4);
  border-color: rgba(0, 232, 255, 0.7);
  transform: scale(1.05);
}

.ap-cost {
  background: rgba(127, 255, 22, 0.3);
  border: 1px solid rgba(127, 255, 22, 0.5);
  color: #fada95;
  box-shadow: 0 0 5px rgba(127, 255, 22, 0.3);
}

.ap-cost:hover {
  background: rgba(127, 255, 22, 0.4);
  border-color: rgba(127, 255, 22, 0.7);
  transform: scale(1.05);
}

.health-cost {
  background: rgba(255, 69, 58, 0.3);
  border: 1px solid rgba(255, 165, 0, 0.5);
  color: #fada95;
  box-shadow: 0 0 5px rgba(255, 165, 0, 0.3);
}

.health-cost:hover {
  background: rgba(255, 69, 58, 0.4);
  border-color: rgba(255, 165, 0, 0.7);
  transform: scale(1.05);
}

/* Skill Type */
.skill-type {
  position: absolute;
  bottom: 0.175rem;
  right: 0.175rem;
  font-size: 0.875rem;
  color: #fada95;
  text-shadow: 0 0 3px rgba(250, 218, 149, 0.5);
}

/* Icon */
.icon {
  position: absolute;
  width: 3.5rem;
  height: 3.5rem;
  left: 0.75rem;
  top: 0.75rem;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(127, 255, 22, 0.2);
  border-radius: 0.263rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  transition: all 0.2s ease;
}

.icon:hover {
  border-color: rgba(127, 255, 22, 0.4);
  background: rgba(0, 0, 0, 0.3);
}

.icon {
  position: absolute;
  left: 0;
  top: 0;
  z-index: 1;
  width: 100%;
  height: 100%;
  object-fit: cover;
  mask: radial-gradient(circle at center, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0) 80%);
}

.icon .placeholder {
  font-size: 1.5rem;
  color: rgba(250, 218, 149, 0.5);
}

/* Skill Name */
.skill-name {
  z-index: 2;
  font-size: calc(0.3rem + 0.25vw);
  font-weight: 500;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-transform: uppercase;
  color: #fada95;
  text-shadow: 0 0 3px rgb(0, 0, 0);
  width: 100%;
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  transition: all 0.2s ease;
  backdrop-filter: blur(2px);
}

.skill-name:hover {
  text-shadow: 0 0 5px rgba(250, 218, 149, 0.8);
}

.fade {
  filter: grayscale(100%);
  opacity: 0.5;
  transform: none !important;
}

.fade:hover {
  transform: none !important;
  box-shadow: none !important;
}
</style>
