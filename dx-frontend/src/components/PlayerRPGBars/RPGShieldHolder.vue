<script setup lang="ts">

import {defineProps, withDefaults} from 'vue';
import {ActiveShield} from '@/api/dx-backend';

type Props = {
  shield: ActiveShield;
};

const props = withDefaults(defineProps<Props>(), {});

import {computed} from 'vue';
const title = computed(() => {
    return `Defend from the ${props.shield.shield.id} attacks`;
});
</script>

<template>
  <div
      class="rpg-shield-holder"
      :title="title"
  >
    <div class="rpg-shield-holder__wrapper">
      <img
          :src="props.shield.shield.icon"
          :alt="props.shield.shield.id"
          class="rpg-shield-holder__image"
          sizes="content"
      />
      <span class="rpg-shield-holder__value">
          {{ props.shield.level }}
      </span>
    </div>
    <span class="rpg-shield-holder__duration">
        {{ props.shield.cycles_left }}
      </span>
  </div>
</template>

<style scoped>
.rpg-shield-holder {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 2rem;
  height: 2rem;
  background: url('@/assets/rpg_bars/shield_holder_with_border.png') no-repeat center center;
  background-size: cover;
  gap: 0.2rem;
  cursor: pointer;
}

.rpg-shield-holder__wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-size: cover;
  mask: url('@/assets/rpg_bars/shield_holder_mask_invented.png') no-repeat center;
  mask-size: cover;
}

.rpg-shield-holder__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
.rpg-shield-holder__value {
  font-size: 0.8rem;
  color: #fff04d;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
  position: absolute;
}

.rpg-shield-holder__duration {
  font-size: 0.7rem;
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
}

</style>