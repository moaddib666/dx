<template>
  <div class="test-screen">
    <HeroBackground></HeroBackground>
    <RPGNPCSpawnerConstructor position-id="111" campaign-id="111"/>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import HeroBackground from "@/components/WhatIsIt/HeroBackground.vue"
import RPGCharactersTemplatesModal from "@/components/GameMaster/RPGCharacterTempaltes/RPGCharactersTemplatesModal.vue";
import RPGNPCSpawnerConstructor from "@/components/GameMaster/RPGSpawners/RPGNPCSpawnerConstructor.vue";
</script>

<style scoped>
.test-screen {
  position: relative;
  width: 100%;
  height: 100vh;
}

</style>