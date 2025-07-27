<script setup lang="ts">
// FightFooter component
import {computed} from "vue";
import CharacterCardHolder from "@/components/Game/Location/NewCharacterCardHolder.vue";
const characters = computed(() => {
  const characterList = [{"_custom":{"type":"reactive","stateTypeName":"Reactive","value":{"id":"9b66a56f-2c5d-4db3-86d9-4b75aed0406d","name":"Max","biography":{"id":"975a1a31-650a-4897-ba6e-f6ceca872d47","created_at":"2024-12-26T20:26:35.138000Z","updated_at":"2025-01-10T16:40:59.041000Z","age":300,"gender":"Other","background":"Placeholder for background. Suggestions: 'Born in a small village and trained in combat by a retired warrior. Now seeking adventure to uncover the mysteries of the Flow.'","appearance":"Placeholder for appearance. Suggestions: 'Tall with an athletic build, sharp features, piercing blue eyes.'","avatar":"http://localhost:8000/media/avatars/max.webp","character":"9b66a56f-2c5d-4db3-86d9-4b75aed0406d"},"npc":false,"rank":{"name":"Novice","grade":9,"experience_needed":200},"path":{"name":"Path of JSon","description":"A path focusing on magical abilities.","icon":"http://localhost:8000/media/icons/path/json.webp","id":"7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"},"experience":0,"tags":["test"],"resetting_base_stats":false,"is_active":true,"campaign":{"id":"b6de2027-2372-434f-bff4-b799ef5d1cd2","name":"First Campaign"}}}},{"_custom":{"type":"reactive","stateTypeName":"Reactive","value":{"id":"f3c4216f-cbaa-4792-b6e6-1cedd502defe","name":"The Veiled Arbiter","biography":{"id":"012e5d6e-bad2-459c-a7a6-62329ecd7508","created_at":"2024-12-24T14:18:04.753000Z","updated_at":"2024-12-24T14:19:28.959000Z","age":900,"gender":"Other","background":"The Veiled Arbiter exists beyond the bounds of mortal realms, serving as the omniscient overseer of the game world. It appears to inspect, guide, or intervene when the balance of Flow or the integrity of the realm is threatened. With mastery over teleportation, invisibility, and Flow manipulation, its presence is both awe-inspiring and unsettling.","appearance":"A translucent figure cloaked in flowing, dark robes inscribed with glowing blue and silver symbols. Its hood obscures its face, revealing only glowing white eyes. Tendrils of spectral mist swirl around its form, giving it an ethereal and ever-shifting presence.","avatar":"http://localhost:8000/media/avatars/83A73E18-2066-4263-B8F3-F299660160F4.PNG","character":"f3c4216f-cbaa-4792-b6e6-1cedd502defe"},"npc":false,"rank":{"name":"Mythical Paragon","grade":2,"experience_needed":284460},"path":{"name":"Path of JSon","description":"A path focusing on magical abilities.","icon":"http://localhost:8000/media/icons/path/json.webp","id":"7f4e36d3-3f43-4e13-bdae-3e3777e1d3a6"},"experience":0,"tags":["Game Master","Phantom","Flow Manipulator"],"resetting_base_stats":false,"is_active":true,"campaign_name":"First Campaign"}}}]
  return characterList.map(character => character._custom.value);
})
</script>

<template>
  <div class="fight-footer">
    <div class="background-container">
      <div class="png-background-effect-bg"></div>
      <div class="png-background"></div>
      <div class="png-background-effect"></div>
    </div>
    <CharacterCardHolder :characters="characters" class="character-card-holder" />
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