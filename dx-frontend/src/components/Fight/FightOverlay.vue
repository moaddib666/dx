<script setup lang="ts">

import FightSide from "@/components/Fight/FightSide.vue";
</script>

<template>
  <div class="fight-overlay">
    <div class="fight-overlay-content">
      <div class="attacker">
        <h2>Attacker</h2>
        <FightSide></FightSide>
      </div>
      <div class="defender">
        <h2>Defender</h2>
        <FightSide></FightSide>
      </div>
    </div>
    <div class="fight-overlay-footer">
    </div>
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
  flex-direction: row;
  align-items: center;
  justify-content: center;
  z-index: 1000; /* Ensure it appears above other content */
  backdrop-filter: blur(5px); /* Optional: adds a blur effect to the background */
}

.fight-overlay-content {
  display: flex;
  flex-direction: row;
  width: 80%;
  height: 80%;
  background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent background */
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.attacker, .defender {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.attacker {
  background-color: rgba(255, 0, 0, 0.1); /* Light red for attacker */
}

.defender {
  background-color: rgba(0, 0, 255, 0.1); /* Light blue for defender */
}

.fight-overlay-footer {
  width: 100%;
  height: 50px;
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent footer */
  position: absolute;
  bottom: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}


</style>