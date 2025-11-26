<template>
  <HeroBackground></HeroBackground>
  <DiceRollerModal
      :visible="true"
      :debug="false"
      @close="() => {}"
      @roll-complete="() => {}"
      :challenge="{
        id: 'test-challenge',
        description: 'This is a test challenge for demonstration purposes.',
        difficulty: 10,
        modifiers: [
            {
                id: 'mod-1',
                name: 'Test Modifier 1',
                value: 2,
            },
            {
                id: 'mod-2',
                name: 'Test Modifier 2',
                value: -1,
            },
            {
                id: 'mod-3',
                name: 'Test Modifier 3',
                value: 3,
            },
            {
                id: 'mod-4',
                name: 'Test Modifier 4',
                value: 0,
            },
            {
                id: 'mod-5',
                name: 'Test Modifier 5',
                value: 1,
            },
            {
                id: 'mod-6',
                name: 'Test Modifier 6',
                value: -2,
            },
            {
                id: 'mod-7',
                name: 'Test Modifier 7',
                value: 4,
            },
            {
                id: 'mod-8',
                name: 'Test Modifier 8',
                value: -3,
            },
            {
                id: 'mod-9',
                name: 'Test Modifier 9',
                value: 2,
            },
            {
                id: 'mod-10',
                name: 'Test Modifier 10',
                value: -5,
            },
        ],
        outcome: null,
      }"
  />
</template>

<script setup lang="ts">
import DiceModifierHolder from "@/components/DiceRoller/DiceModifier/DiceModifierHolder.vue";
import DiceRollerModal from "@/components/DiceRoller/DiceRollerModal.vue";
import HeroBackground from "@/components/WhatIsIt/HeroBackground.vue";
</script>

<style scoped>
</style>