<script setup lang="ts">
import { defineProps, computed } from 'vue';
import GMIconType from '@/models/GMIconTypes';

// Import all icon images
import characterIcon from '@/assets/icons/character.png';
import gameObjectIcon from '@/assets/icons/gameobject.png';
import itemsIcon from '@/assets/icons/items.png';
import mapIcon from '@/assets/icons/map.png';
import skillIcon from '@/assets/icons/skill.png';

// Define props for the component
const props = defineProps<{
  type: GMIconType;
  alt?: string;
}>();

// Map icon types to their respective image sources
const iconMap = {
  [GMIconType.CHARACTER]: characterIcon,
  [GMIconType.GAME_OBJECT]: gameObjectIcon,
  [GMIconType.ITEM]: itemsIcon,
  [GMIconType.MAP]: mapIcon,
  [GMIconType.SKILL]: skillIcon,
};

// Compute the icon source based on the type prop
const iconSrc = computed(() => iconMap[props.type]);

// Compute the alt text based on the alt prop or default to the type
const altText = computed(() => props.alt || props.type);
</script>

<template>
  <img :src="iconSrc" class="gm-icon" :alt="altText"/>
</template>

<style scoped>
.gm-icon {
  width: 90%;
  height: 90%;
  padding: 0;
  margin:0;
}
</style>