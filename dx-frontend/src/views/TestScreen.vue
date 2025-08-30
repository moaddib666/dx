<template>
  <div class="test-screen">
    <HeroBackground></HeroBackground>
    <RpgSpawnerConstructorModal position-id="111"/>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import HeroBackground from "@/components/WhatIsIt/HeroBackground.vue"
import RPGCharactersTemplatesModal from "@/components/GameMaster/RPGCharacterTempaltes/RPGCharactersTemplatesModal.vue";
import RpgSpawnerConstructorModal from "@/components/GameMaster/RPGSpawners/RPGSpawnerConstructorModal.vue";
</script>

<style scoped>
.test-screen {
  position: relative;
  width: 100%;
  height: 100vh;
}

</style>