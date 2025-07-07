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
import { useI18n } from 'vue-i18n';

export default {
  name: 'DiceRollerView',

  components: {
    HeroBackground,
    RealisticDiceRoller
  },

  setup() {
    const { t } = useI18n();
    return { t };
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
      console.log(this.t('diceRoller.ready'))
    },

    onError(error) {
      console.error(this.t('diceRoller.error'), error)
    },

    onRollComplete(result) {
      console.log(this.t('diceRoller.rollComplete'), result)
    }
  }
}
</script>

<style scoped>
.dice-roller-view {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  /* Site theme colors */
  --cyber-yellow: #ffd700;
  --light-steel-blue: #b0c4de;
  --bg-overlay: rgba(0, 0, 0, 0.1);
}
</style>