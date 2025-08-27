<template>
  <div class="challenge-modifier" :class="{'negative-tint': negativeTint}">
    <img
        v-if="iconUrl"
        :src="iconUrl"
        :alt="props.modifier.name + ' icon'"
        class="modifier-icon"
        @error="onImageError"
    />
    <div class="modifier-value">{{ formatedValue }}</div>
    <div class="modifier-name">{{ props.modifier.name }}</div>
  </div>
</template>

<script setup lang="ts">
import {computed, ref} from 'vue'
import DefaultImage from "@/assets/icons/challenge/artifact2.png"
import {type ChallengeModifier} from "@/api/dx-backend";

interface Props {
  modifier: ChallengeModifier
}

const props = withDefaults(defineProps<Props>(), {})


const onImageError = (event: Event) => {
  console.warn(`Failed to load icon for ${props.modifier.id} modifier:`, props.modifier.icon)
}
const iconUrl = computed(() => {
  return props.modifier.icon || DefaultImage
})

const negativeTint = computed(() => {
  return props.modifier.value < 0
})

const formatedValue = computed(() => {
  return props.modifier.value > 0 ? `+${props.modifier.value}` : `${props.modifier.value}`
})

</script>

<style scoped>
.challenge-modifier {
  background: linear-gradient(145deg, #2a2a2a 0%, #1a1a1a 100%);
  border: 2px solid;
  border-image: linear-gradient(to bottom, #b8956a 0%, #5d4a37 100%) 1;
  border-radius: 1em;
  padding: 0.2em;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  gap: 0.5em;
  width: clamp(60px, 5vw, 120px);
  height: clamp(90px, 7.5vw, 180px);
  min-width: 60px;
  min-height: 90px;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3),
  inset 0 1px 0 rgba(139, 115, 85, 0.3);
  font-family: 'Cinzel', serif;
  color: #f6e1b2;
}

.challenge-modifier:hover {
  border-image: linear-gradient(to bottom, #f4d76e 0%, #a6841f 100%) 1;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4),
  0 0 20px rgba(212, 175, 55, 0.2),
  inset 0 1px 0 rgba(212, 175, 55, 0.3);
  transform: translateY(-2px);
  filter: brightness(1.2);
}

.modifier-value {
  font-size: clamp(0.8rem, 1.1em, 1.4rem);
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  letter-spacing: 0.2em;
  padding-top: 1em;
  z-index: 1;
}

.modifier-icon {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.5));
  mask: radial-gradient(circle at center, rgba(0, 0, 0, 1) 5%, rgba(0, 0, 0, 0) 100%);
  z-index: 0;
}

.modifier-name {
  z-index: 1;
  font-size: clamp(0.5rem, 0.7em, 1rem);
  font-weight: 500;
  text-align: center;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
}

.negative-tint {
  border-image: linear-gradient(to bottom, #a8c5f0 0%, #5a7ba8 100%) 1;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3),
  inset 0 1px 0 rgba(0, 70, 139, 0.3);
  color: #a0c4ff;
}

.negative-tint:hover {
  border-image: linear-gradient(to bottom, #4dc7ff 0%, #0080cc 100%) 1;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4),
  0 0 20px rgba(0, 161, 255, 0.2),
  inset 0 1px 0 rgba(0, 161, 255, 0.3);
  transform: translateY(-2px);
  filter: brightness(1.2);
}

</style>