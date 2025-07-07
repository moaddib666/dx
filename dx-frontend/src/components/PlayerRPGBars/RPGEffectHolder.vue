<script setup lang="ts">

import {ActiveEffect} from '@/api/dx-backend';

type Props = {
  effect: ActiveEffect;
};

const props = withDefaults(defineProps<Props>(), {});
import {defineProps, withDefaults} from 'vue';
</script>

<template>
  <div
      class="rpg-effect-holder"
      :title="`${props.effect.effect.id} - Duration: ${props.effect.cycle_left} cycles`"
  >
    <div class="rpg-effect-holder__wrapper">
      <img
          :src="props.effect.effect.icon"
          class="rpg-effect-holder__image"
          sizes="content"
          :alt="props.effect.effect.id"
      />
    </div>
    <span class="rpg-effect-holder__duration">
        {{ props.effect.cycle_left }}
      </span>
  </div>
</template>

<style scoped>
.rpg-effect-holder {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 2rem;
  height: 2rem;
  background: url('@/assets/rpg_bars/shield_holder_with_border.png') no-repeat center center;
  background-size: cover;
}

.rpg-effect-holder__wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-size: cover;
  mask: url('@/assets/rpg_bars/shield_holder_mask_invented.png') no-repeat center;
  mask-size: cover;
}
.rpg-effect-holder__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
.rpg-effect-holder__duration {
  font-size: 0.7rem;
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
}

</style>