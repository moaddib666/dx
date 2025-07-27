<script setup lang="ts">

import FightSide from "@/components/Fight/FightSide.vue";
import FightFooter from "@/components/Fight/FightFooter.vue";
</script>

<template>
  <div class="fight-overlay">
    <div class="bg-texture"></div>
    <div class="header">
      <h1>Misfits Pub</h1>
      <h2> Round 1</h2>
    </div>
    <div class="fight-overlay-content">
      <div class="attacker">
        <FightSide direction="right" side="tech"></FightSide>
      </div>
      <div class="defender">
        <FightSide direction="left" side="mage"></FightSide>
      </div>
    </div>
    <FightFooter class="fight-overlay-footer"/>
  </div>
</template>

<style scoped>
.fight-overlay {
  top: 0;
  left: 0;
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  z-index: 1000; /* Ensure it appears above other content */
  backdrop-filter: blur(5px); /* Optional: adds a blur effect to the background */
}

.fight-overlay-content {
  display: flex;
  flex-direction: row;
  width: 100%;
  max-height: 80%;
  flex: 4;
}

.attacker, .defender {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.fight-overlay-footer {
  flex: 1;
  width: 100%;
}

.header {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.header h1 {
  font-size: 2.5rem;
  margin: 0;
}

.header h1, .header h2 {
  z-index: 1;
  font-family: 'Cinzel', serif;
  color: #fada95;
  text-transform: uppercase;
  text-align: center;
  text-shadow: 0 0 8px rgba(216, 187, 124, 0.5);
  filter: drop-shadow(0 0.1rem rgba(0, 0, 0, 0.6)) drop-shadow(0 0.1rem rgba(0, 0, 0, 0.4));
  transition: text-shadow 0.3s ease;
}
.bg-texture {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/fight/texture.png') repeat-x bottom center;
  background-size: contain;
  z-index: -1;
  mask: linear-gradient(
    rgba(0, 0, 0, 0),
    rgba(0, 0, 0, 0.6),
    rgba(0, 0, 0, 1)
  );
}

</style>