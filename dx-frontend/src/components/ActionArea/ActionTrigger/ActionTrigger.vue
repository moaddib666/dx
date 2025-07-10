<script setup lang="ts">

import {computed} from "vue";

const Images = {
  EndTurn: require('@/assets/images/action-area/TriggerEndTurn.png'),
  RollDice: require('@/assets/images/action-area/TriggerRollDice.png'),
  ToSafe: require('@/assets/images/action-area/TriggerToSafe.png'),
};


// Image Enum
const ImagesEnum = {
  EndTurn: 'EndTurn',
  RollDice: 'RollDice',
  ToSafe: 'ToSafe'
} as const;

// More explicit type extraction
type TypeOfImageEnum = (typeof ImagesEnum)[keyof typeof ImagesEnum];

interface Props {
  id?: string;
  image?: TypeOfImageEnum;
  disabled?: boolean;
  title?: string;
}
const props = withDefaults(defineProps<Props>(), {
  id: '',
  disabled: false,
  title: ''
});

const emit = defineEmits<{
  select: [id: string];
}>();

const isEmpty = computed(() => props.id === '');
const isDisabled = computed(() => props.disabled || isEmpty.value);
const imageSrc = computed(() => {
  return props.image ? Images[props.image] : '';
});

</script>

<template>
  <div
  class="action__trigger__holder"

  >
    <div
        class="action__trigger__wrapper"
    >
      <img v-if="props.image"
          :src="imageSrc"
          class="action__trigger__image"
          :alt="props.title"
          :title="props.title"
          @click="$emit('select', props.id)"
          :class="{
            'action__trigger__image--disabled': props.disabled,
            'action__trigger__image--empty': !props.image
          }"
      />
    </div>
  </div>

</template>

<style scoped>
.action__trigger__holder {
  width: 100%;
  height: 100%;
  display: flex;
  background: url("@/assets/images/action-area/Holder.png") no-repeat center center;
  background-size: contain;
  align-items: center;
  justify-content: center;
}
.action__trigger__wrapper {
  width: 60%;
  height: 60%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}
.action__trigger__image {
  width: 50%;
  height: 50%;
  object-fit: contain;
  transition: transform 0.2s ease-in-out;
  cursor: pointer;
}
.action__trigger__image:hover {
  transform: scale(1.05);
  filter: brightness(1.3);
}

.action__trigger__image:active {
  transform: scale(0.95);
}
.action__trigger__image--disabled {
  pointer-events: none;
  opacity: 0.5;
  filter: grayscale(100%);
}

</style>