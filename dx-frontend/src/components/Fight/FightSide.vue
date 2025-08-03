<script setup lang="ts">
import FightSideImage from "@/components/Fight/FightSideImage.vue";
import FightCharacter from "@/components/Fight/FightCharacter.vue";
import {Fighter, Name535Enum} from "@/api/dx-backend";
import {computed} from "vue";
const props = defineProps<{
  direction?: 'left' | 'right';
  fighter: Fighter
}>();

enum FightSideEnum {
  MAGE = 'mage',
  TECH = 'tech'
}

// Default values if props are not provided
const direction = props.direction || 'left';
const side = computed(() => {
  return props.fighter.path_name === Name535Enum.PathOfJSon ? FightSideEnum.MAGE : FightSideEnum.TECH;
})
</script>

<template>
  <div class="fight-side">
    <FightSideImage :direction="direction" :side="side"></FightSideImage>
    <FightCharacter
        class="character-info"
        :direction="direction"
        :character="{
      name: props.fighter.name,
      title: props.fighter.rank_name,
      avatar: props.fighter.avatar,
    }"
    ></FightCharacter>
  </div>
</template>

<style scoped>
.fight-side {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.character-info {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2; /* Ensure character info is above the background */
}
</style>