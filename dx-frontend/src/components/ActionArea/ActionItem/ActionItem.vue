<script setup lang="ts">
import { computed } from 'vue';
import { TypeC27Enum } from "@/api/dx-backend";

interface CostItem {
  kind: string;
  value: number;
}

interface Props {
  id?: string;
  ctaType?: TypeC27Enum;
  image?: string;
  disabled?: boolean;
  title?: string;
  cost?: CostItem[];
}

const props = withDefaults(defineProps<Props>(), {
  id: '',
  ctaType: TypeC27Enum.Utility,
  image: '',
  disabled: false,
  title: '',
  cost: () => []
});

const costByKind = (kind: string): CostItem | null => {
  return props.cost?.find((cost) => cost.kind === kind) || null;
};

const actionPointsCost = computed(() => costByKind('Action Points'));
const energyCost = computed(() => costByKind('Energy'));
const healthCost = computed(() => costByKind('Health'));
const flowCost = computed(() => costByKind('Flow'));

const emit = defineEmits<{
  select: [id: string];
}>();

const isEmpty = computed(() => props.id === '');
const isDisabled = computed(() => props.disabled || isEmpty.value);
const hasImage = computed(() => props.image !== '');

const handleClick = () => {
  if (!isDisabled.value) {
    emit('select', props.id);
  }
};

const iconClasses = computed(() => ({
  'action-item__icon': true,
  'action-item__icon--attack': props.ctaType === TypeC27Enum.Attack,
  'action-item__icon--defense': props.ctaType === TypeC27Enum.Defense,
  'action-item__icon--heal': props.ctaType === TypeC27Enum.Heal,
  'action-item__icon--buff': props.ctaType === TypeC27Enum.Buff,
  'action-item__icon--debuff': props.ctaType === TypeC27Enum.Debuff,
  'action-item__icon--utility': props.ctaType === TypeC27Enum.Utility,
  'action-item__icon--special': props.ctaType === TypeC27Enum.Special,
  'action-item__icon--disabled': isDisabled.value
}));

const holderClasses = computed(() => ({
  'action-item': true,
  'action-item--disabled': isDisabled.value,
  'action-item--empty': isEmpty.value
}));

</script>

<template>
  <div
    :class="holderClasses"
    @click="handleClick"
    :title="title"
  >
    <img
      v-if="hasImage"
      :src="image"
      :alt="title || 'Action Icon'"
      :class="iconClasses"
    />
    <div
      v-else-if="!isEmpty"
      :class="iconClasses"
      class="action-item__placeholder"
    >
      ?
    </div>
  </div>
</template>
<style scoped>
.action-item {
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: url("@/assets/images/action-area/Cell.png") no-repeat center center;
  background-size: cover;
  transition: transform 0.2s ease-in-out;
  position: relative;
  border-radius: 0.2rem;
}

.action-item:hover:not(.action-item--disabled) {
  transform: scale(1.05);
}

.action-item:active:not(.action-item--disabled) {
  transform: scale(0.95);
}

.action-item--disabled {
  pointer-events: none;
  opacity: 0.5;
}

.action-item--empty {
  opacity: 0.3;
}

.action-item__icon {
  width: 75%;
  height: 75%;
  object-fit: contain;
  border-radius: 0.1rem;
  transition: all 0.2s ease-in-out;
}

.action-item__placeholder {
  width: 75%;
  height: 75%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: bold;
  color: #666;
  border: 1px dashed #666;
  border-radius: 0.1rem;
}

/* Action Type Styling */
.action-item__icon--attack {
  border: 0 solid #ff1744;
  box-shadow: 0 0 0.3rem rgba(255, 23, 68, 0.6);
}

.action-item__icon--defense {
  border: 0 solid #00e5ff;
  box-shadow: 0 0 0.3rem rgba(0, 229, 255, 0.6);
}

.action-item__icon--heal {
  border: 0 solid #00ff00;
  box-shadow: 0 0 0.3rem rgba(0, 255, 0, 0.6);
}

.action-item__icon--buff {
  border: 0 solid #ffc107;
  box-shadow: 0 0 0.3rem rgba(255, 193, 7, 0.6);
}

.action-item__icon--debuff {
  border: 0 solid #b71c1c;
  box-shadow: 0 0 0.3rem rgba(183, 28, 28, 0.6);
}

.action-item__icon--utility {
  border: 0 solid #9e9e9e;
  box-shadow: 0 0 0.3rem rgba(158, 158, 158, 0.6);
}

.action-item__icon--special {
  border: 0 solid #673ab7;
  box-shadow: 0 0 0.3rem rgba(103, 58, 183, 0.6);
}

.action-item__icon--disabled {
  filter: grayscale(100%);
  opacity: 0.5;
}

/* Hover Effects */
.action-item:hover:not(.action-item--disabled) .action-item__icon {
  transform: scale(1.1);
  border-width: 0.1rem;
}

.action-item:hover:not(.action-item--disabled) .action-item__icon--attack {
  box-shadow: 0 0 0.5rem rgba(255, 23, 68, 0.8);
}

.action-item:hover:not(.action-item--disabled) .action-item__icon--defense {
  box-shadow: 0 0 0.5rem rgba(0, 229, 255, 0.8);
}

.action-item:hover:not(.action-item--disabled) .action-item__icon--heal {
  box-shadow: 0 0 0.5rem rgba(0, 255, 0, 0.8);
}

.action-item:hover:not(.action-item--disabled) .action-item__icon--buff {
  box-shadow: 0 0 0.5rem rgba(255, 193, 7, 0.8);
}

.action-item:hover:not(.action-item--disabled) .action-item__icon--debuff {
  box-shadow: 0 0 0.5rem rgba(183, 28, 28, 0.8);
}

.action-item:hover:not(.action-item--disabled) .action-item__icon--utility {
  box-shadow: 0 0 0.5rem rgba(158, 158, 158, 0.8);
}

.action-item:hover:not(.action-item--disabled) .action-item__icon--special {
  box-shadow: 0 0 0.5rem rgba(103, 58, 183, 0.8);
}

/* Focus States */
.action-item:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.5);
}

.action-item:focus .action-item__icon {
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.7);
}

</style>