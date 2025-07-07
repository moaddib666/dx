<script setup lang="ts">
import RPGAvatar from './RPGAvatar.vue'
import RpgHealthStatBar from './RPGHealthStatBar.vue'
import RPGFlowStatBar from "@/components/PlayerRPGBars/RPGFlowStatBar.vue";
import RPGActionPointsStatBar from "@/components/PlayerRPGBars/RPGActionPointsStatBar.vue";
import RpgMiniHolder from "@/components/PlayerRPGBars/RPGMiniHolder.vue";

</script>

<template>
  <!-- Shields and Effects can be added here later -->
  <div class="rpg-effects-holder">
    <RpgMiniHolder></RpgMiniHolder>
    <RpgMiniHolder></RpgMiniHolder>
    <RpgMiniHolder></RpgMiniHolder>
    <RpgMiniHolder></RpgMiniHolder>
    <RpgMiniHolder></RpgMiniHolder>
    <RpgMiniHolder></RpgMiniHolder>
    <RpgMiniHolder></RpgMiniHolder>
    <RpgMiniHolder></RpgMiniHolder>
    <RpgMiniHolder></RpgMiniHolder>
    <RpgMiniHolder></RpgMiniHolder>
  </div>
  <div class="rpg-bars-container">
    <!-- Character Avatar -->
    <RPGAvatar/>
    <!-- Bars -->
    <div class="rpg-bars-holder">
      <RpgHealthStatBar :current="7" :max="10"></RpgHealthStatBar>
      <RPGFlowStatBar :current="10" :max="20"></RPGFlowStatBar>
      <RPGActionPointsStatBar :current="9" :max="9"></RPGActionPointsStatBar>
      <div class="rpg-shield-holder">
        <RpgMiniHolder></RpgMiniHolder>
        <RpgMiniHolder></RpgMiniHolder>
        <RpgMiniHolder></RpgMiniHolder>
        <RpgMiniHolder></RpgMiniHolder>
        <RpgMiniHolder></RpgMiniHolder>
        <RpgMiniHolder></RpgMiniHolder>
        <RpgMiniHolder></RpgMiniHolder>
        <RpgMiniHolder></RpgMiniHolder>
        <RpgMiniHolder></RpgMiniHolder>
        <RpgMiniHolder></RpgMiniHolder>
        <RpgMiniHolder></RpgMiniHolder>
        <RpgMiniHolder></RpgMiniHolder>
      </div>
    </div>
  </div>

</template>

<style scoped>
.rpg-bars-container {
  display: flex;
  align-items: center;
}

.rpg-bars-holder {
  display: flex;
  flex-direction: column;
  flex: 1;
  justify-items: center;
  margin-left: -2rem;
}

.rpg-shield-holder {
  display: flex;
  flex-direction: row;
  justify-content: left;
  height: auto;
}

</style>