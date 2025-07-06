<template>
  <div class="dice-roller-view">
    <HeroBackground/>
    <RealisticDiceRoller
      :width="windowWidth"
      :height="windowHeight"
      @ready="onReady"
      @error="onError"
      @roll-complete="onRollComplete"
    />
  </div>
</template>

<script>
import RealisticDiceRoller from '@/components/DiceRoller/RealisticDiceRoller.vue'
import HeroBackground from "@/components/WhatIsIt/HeroBackground.vue";

export default {
  name: 'DiceRollerView',

  components: {
    HeroBackground,
    RealisticDiceRoller
  },

  data() {
    return {
      windowWidth: window.innerWidth,
      windowHeight: window.innerHeight
    }
  },

  mounted() {
    window.addEventListener('resize', this.handleResize)
  },

  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
  },

  methods: {
    handleResize() {
      this.windowWidth = window.innerWidth
      this.windowHeight = window.innerHeight
    },

    onReady() {
      console.log('Dice roller is ready!')
    },

    onError(error) {
      console.error('Dice roller error:', error)
    },

    onRollComplete(result) {
      console.log('Roll completed:', result)
    }
  }
}
</script>

<style scoped>
.dice-roller-view {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
</style>