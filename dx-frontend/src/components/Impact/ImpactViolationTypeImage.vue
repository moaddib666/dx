<script setup lang="ts">
import { computed } from 'vue';
import {ImpactViolationType} from "@/api/dx-backend";

// Import all violation type images
import physicalImage from "@/assets/images/impact_violation/Phisical.webp";
import mentalImage from "@/assets/images/impact_violation/Mental.webp";
import energyImage from "@/assets/images/impact_violation/Energy.webp";
import heatImage from "@/assets/images/impact_violation/Heat.webp";
import coldImage from "@/assets/images/impact_violation/Cold.webp";
import lightImage from "@/assets/images/impact_violation/Light.webp";
import darknessImage from "@/assets/images/impact_violation/Dark.webp";
import noneImage from "@/assets/images/impact_violation/None.webp";

interface Props {
  violationType: ImpactViolationType;
}

const props = defineProps<Props>();

// Map violation types to their corresponding imported images
const imageMap: Record<string, string> = {
  [ImpactViolationType.Physical]: physicalImage,
  [ImpactViolationType.Mental]: mentalImage,
  [ImpactViolationType.Energy]: energyImage,
  [ImpactViolationType.Heat]: heatImage,
  [ImpactViolationType.Cold]: coldImage,
  [ImpactViolationType.Light]: lightImage,
  [ImpactViolationType.Darkness]: darknessImage,
  [ImpactViolationType.None]: noneImage
};

const imageSrc = computed(() => {
  return imageMap[props.violationType] || '';
});

</script>

<template>
  <img
    v-if="imageSrc"
    :src="imageSrc"
    :alt="`${props.violationType} violation type`"
  />
</template>

<style scoped>
</style>