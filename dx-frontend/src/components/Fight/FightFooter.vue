<script setup lang="ts">
// FightFooter component
import {computed} from "vue";
import CharacterCardHolder from "@/components/Game/Location/NewCharacterCardHolder.vue";

interface Props {
  fighters: Fighter[];
}
const props = defineProps<Props>();
</script>

<template>
  <div class="fight-footer">
    <div class="background-container">
      <div class="png-background-effect-bg"></div>
      <div class="png-background"></div>
      <div class="png-background-effect"></div>
    </div>
    <CharacterCardHolder :characters="fighters" class="character-card-holder" />
  </div>
</template>

<style scoped>
.fight-footer {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  width: 100%;
  position: relative;
  overflow: hidden;
}

.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.png-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/fight/crowd.png') repeat-x center center;
  background-size: contain;
}

.png-background-effect {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/fight/texture.png') repeat-x bottom center;
  background-size: calc(100% - 20rem) 100%;
  mask: url('@/assets/fight/crowd.png') repeat-x center center;
  mask-size: contain;
  opacity: 0.7;
}

.png-background-effect-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/fight/texture.png') repeat-x bottom center;
  background-size: calc(100% - 20rem) 100%;
  mask: url('@/assets/fight/crowd.png') repeat-x center center;
  mask-size: contain;
  scale: 1.005;
  filter: blur(2rem);
}
</style>