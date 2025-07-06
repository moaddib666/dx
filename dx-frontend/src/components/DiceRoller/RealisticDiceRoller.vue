<template>
  <div class="realistic-dice-roller">
    <DiceInfoPanel />
    
    <DiceCanvas 
      ref="diceCanvas"
      @ready="onCanvasReady"
      @error="onCanvasError"
      @number-change="onNumberChange"
      @state-change="onStateChange"
    />
    
    <DiceControlPanel
      @roll-dice="handleRollDice"
      @random-roll="handleRandomRoll"
      @reset-camera="handleResetCamera"
      @toggle-wireframe="handleToggleWireframe"
      @camera-view="handleCameraView"
      @texture-upload="handleTextureUpload"
      :is-rolling="isRolling"
      :current-number="currentDisplayNumber"
      :status="rollStatus"
    />
    
    <DiceResultDisplay
      v-if="showResult"
      :result="lastResult"
      @close="showResult = false"
    />
  </div>
</template>

<script>
import DiceInfoPanel from './DiceInfoPanel.vue'
import DiceControlPanel from './DiceControlPanel.vue'
import DiceCanvas from './DiceCanvas.vue'
import DiceResultDisplay from './DiceResultDisplay.vue'

export default {
  name: 'RealisticDiceRoller',
  
  components: {
    DiceInfoPanel,
    DiceControlPanel,
    DiceCanvas,
    DiceResultDisplay
  },

  props: {
    width: {
      type: Number,
      default: 800
    },
    height: {
      type: Number,
      default: 600
    },
    autoHideResult: {
      type: Boolean,
      default: true
    },
    resultDisplayTime: {
      type: Number,
      default: 5000
    }
  },

  data() {
    return {
      isCanvasReady: false,
      isRolling: false,
      currentDisplayNumber: null,
      rollStatus: 'Ready to roll',
      showResult: false,
      lastResult: null,
      resultTimeout: null
    }
  },

  beforeUnmount() {
    if (this.resultTimeout) {
      clearTimeout(this.resultTimeout)
    }
  },

  methods: {
    onCanvasReady() {
      this.isCanvasReady = true
      this.rollStatus = 'Ready to roll'
      this.$emit('ready')
    },

    onCanvasError(error) {
      this.rollStatus = 'Error initializing dice'
      this.$emit('error', error)
    },

    onNumberChange(number) {
      this.currentDisplayNumber = number
    },

    onStateChange(state) {
      this.rollStatus = state.status
      this.isRolling = state.isRolling
    },

    async handleRollDice(targetNumber) {
      if (!this.isCanvasReady || this.isRolling) return

      try {
        this.isRolling = true
        this.showResult = false
        
        const result = await this.$refs.diceCanvas.rollToTarget(targetNumber)
        this.handleRollComplete(result)
      } catch (error) {
        console.error('Roll failed:', error)
        this.isRolling = false
        this.rollStatus = 'Roll failed'
      }
    },

    async handleRandomRoll() {
      if (!this.isCanvasReady || this.isRolling) return

      try {
        this.isRolling = true
        this.showResult = false
        
        const result = await this.$refs.diceCanvas.rollRandom()
        this.handleRollComplete(result)
      } catch (error) {
        console.error('Random roll failed:', error)
        this.isRolling = false
        this.rollStatus = 'Roll failed'
      }
    },

    handleRollComplete(result) {
      this.isRolling = false
      this.lastResult = result
      this.showResult = true
      this.rollStatus = `Landed on ${result.number}`

      // Auto-hide result
      if (this.autoHideResult) {
        this.resultTimeout = setTimeout(() => {
          this.showResult = false
        }, this.resultDisplayTime)
      }

      this.$emit('roll-complete', result)
    },

    handleResetCamera() {
      if (this.$refs.diceCanvas) {
        this.$refs.diceCanvas.resetCamera()
      }
    },

    handleToggleWireframe() {
      if (this.$refs.diceCanvas) {
        this.$refs.diceCanvas.toggleWireframe()
      }
    },

    handleCameraView(viewType) {
      if (this.$refs.diceCanvas) {
        this.$refs.diceCanvas.setCameraView(viewType)
      }
    },

    async handleTextureUpload(file) {
      if (this.$refs.diceCanvas) {
        const success = await this.$refs.diceCanvas.setUserTexture(file)
        if (success) {
          this.rollStatus = 'Custom texture loaded'
        } else {
          this.rollStatus = 'Failed to load texture'
        }
      }
    },

    // Public API methods
    roll(targetNumber) {
      return this.handleRollDice(targetNumber)
    },

    rollRandom() {
      return this.handleRandomRoll()
    },

    resetCamera() {
      this.handleResetCamera()
    },

    getCurrentResult() {
      return this.lastResult
    },

    isCurrentlyRolling() {
      return this.isRolling
    }
  }
}
</script>

<style scoped>
.realistic-dice-roller {
  position: relative;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
  border-radius: 10px;
  overflow: hidden;
  font-family: Arial, sans-serif;
}
</style>