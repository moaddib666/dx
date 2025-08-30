<template>
  <div class="impact">
    <span class="impact-size">{{ impact.size }}</span>

    <DiceRollResult v-if="impact.dice_roll_result" :result="impact.dice_roll_result"/>
    <ImpactViolationTypeImage :violation-type="impact.violation" class="icon__image"
                              :title="`Violation type: ${props.violationType}`"/>
    <ImpactViolationTypeImage :violation-type="impact.violation" class="background__image"/>
  </div>
</template>

<script setup lang="ts">
import DiceRollResult from './DiceRollResult.vue';
import ImpactViolationTypeImage from "@/components/Impact/ImpactViolationTypeImage.vue";

interface Impact {
  type: string;
  violation: string;
  size: string;
  dice_roll_result?: any;
}

interface Props {
  impact: Impact;
}

// Props definition
const props = defineProps<Props>();

// Emit definition
const emit = defineEmits<{
  selectTarget: [id: string];
}>();

// Method to handle target selection
const handleSelect = (id: string) => {
  emit('selectTarget', id);
};
</script>

<style scoped>
.impact {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #1c1c1c;
  border: 1px solid #444;
  border-radius: 4px;
  padding: 0.5rem;
  gap: 0.25rem;
  font-size: 0.8rem;
  margin: 0.25rem 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
}

.background__image {
  position: absolute;
  width: 60%;
  height: 100%;
  object-fit: cover;
  right: 0;
  top: 0;
  mask: radial-gradient(circle at top, rgba(0, 0, 0, 0.2) 30%, rgba(0, 0, 0, 0) 90%);
}

.icon__image {
  width: 1.6rem;
  height: 1.6rem;
  object-fit: cover;
  border-radius: 0.2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.impact-size {
  font-weight: bold;
  color: #ffcc00;
  margin-right: auto;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
  font-size: 2rem;
  line-height: 1;
}
</style>
