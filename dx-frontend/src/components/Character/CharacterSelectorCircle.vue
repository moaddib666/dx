<script setup lang="ts">
import PlaceholderImage from '@/assets/images/character/arbiter.png';
import {computed} from "vue";

interface Participant {
  id: string;
  name: string;
  imageUrl?: string;
}

interface Props {
  participant?: Participant;
}

const props = withDefaults(defineProps<Props>(), {
  participant: undefined,
});

const emit = defineEmits<{
  select: [id: Participant | undefined];
}>();

const characterImageUrl = computed(() => {
  return props.participant?.imageUrl || PlaceholderImage;
});
</script>

<template>
  <div class="container">
    <div
        class="image-circle"
        :class="{'placeholder': !props.participant}"
        @click="emit('select', props.participant)">
      <img :src="characterImageUrl" alt="Character" class="character-image"/>
    </div>
  </div>
</template>

<style scoped>
.container {
  aspect-ratio: 1 / 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: url("@/assets/images/action-area/Holder.png") no-repeat center center;
  background-size: contain;
}

.image-circle {
  width: 70%;
  height: 60%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  position: relative;
  cursor: pointer;
  mask: radial-gradient(circle, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0) 100%);
  mask-repeat: no-repeat;
  mask-size: contain;
}

.character-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  position: absolute;
  top: 0;
  left: 0;
  object-fit: cover;
}

.placeholder {
  filter: grayscale(100%);
  opacity: 0.5;
}

.image-circle:hover {
  transform: scale(1.05);
  filter: brightness(1.3);
}

.image-circle:active {
  transform: scale(0.95);
}
</style>