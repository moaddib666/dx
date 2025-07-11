<template>
  <div class="dice-roller-modal" v-if="visible">
    <div class="modal-overlay" @click="closeModal"></div>
    <div class="modal-container">
      <DiceCanvas
          ref="diceCanvas"
          @ready="onCanvasReady"
          @error="onCanvasError"
          @number-change="onNumberChange"
          @state-change="onStateChange"
          class="dice-canvas"
      />
    </div>
  </div>
</template>

<script>
import RealisticDiceRoller from './RealisticDiceRoller.vue'
import DiceCanvas from "@/components/DiceRoller/DiceCanvas.vue";

export default {
  name: 'DiceRollerModal',

  components: {
    DiceCanvas,
    RealisticDiceRoller
  },

  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      isRolling: false,
      lastResult: null
    }
  },

  methods: {
    closeModal() {
      this.$emit('close')
    },

    async rollRandomDice() {
      if (this.isRolling || !this.$refs.diceRoller) return

      this.isRolling = true
      try {
        await this.$refs.diceRoller.rollRandom()
      } catch (error) {
        console.error('Error rolling dice:', error)
      }
    },

    onRollComplete(result) {
      this.isRolling = false
      this.lastResult = result
      this.$emit('roll-complete', result)
    }
  }
}
</script>

<style scoped>
.dice-roller-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}
.modal-container {
  position: relative;
  border-radius: 8px;
  background-color: #ef9898;
  height: 14rem;
}
.dice-canvas {
  display: block;
  position: relative;
  border-radius: 8px;
  width: 100%;
  height: 100%;
  background-color: #fff;
}
</style>