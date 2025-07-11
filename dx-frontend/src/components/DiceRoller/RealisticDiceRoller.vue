<template>
  <div class="realistic-dice-roller">
    <DiceInfoPanel/>
    <div class="realistic-dice-roller-content">
      <DiceCanvas
          ref="diceCanvas"
          @ready="onCanvasReady"
          @error="onCanvasError"
          @number-change="onNumberChange"
          @state-change="onStateChange"
          class="dice-canvas"
      />
    </div>

    <DiceControlPanel
        @roll-dice="handleRollDice"
        @random-roll="handleRandomRoll"
        @reset-camera="handleResetCamera"
        @toggle-wireframe="handleToggleWireframe"
        @camera-view="handleCameraView"
        @texture-upload="handleTextureUpload"
        @material-change="handleMaterialChange"
        @shader-change="handleShaderChange"
        @dice-count-change="handleDiceCountChange"
        @result-mode-change="handleResultModeChange"
        :is-rolling="isRolling"
        :current-number="currentDisplayNumber"
        :status="rollStatus"
        :material-types="materialTypes"
        :shader-types="shaderTypes"
        :current-material="currentMaterial"
        :current-shader="currentShader"
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
      resultTimeout: null,
      materialTypes: [],
      shaderTypes: [],
      currentMaterial: 'metal',
      currentShader: 'none'
    }
  },

  computed: {
    canvasReady() {
      return this.isCanvasReady && this.$refs.diceCanvas
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

      // Initialize material and shader options
      if (this.$refs.diceCanvas) {
        this.materialTypes = this.$refs.diceCanvas.getMaterialTypes()
        this.shaderTypes = this.$refs.diceCanvas.getShaderTypes()
        this.currentMaterial = this.$refs.diceCanvas.getCurrentMaterialType()
        this.currentShader = this.$refs.diceCanvas.getCurrentShaderType()
      }

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

    async handleRollDice(targetNumbers) {
      if (!this.isCanvasReady || this.isRolling) return

      try {
        this.isRolling = true
        this.showResult = false

        let result
        if (Array.isArray(targetNumbers)) {
          // Multiple dice with individual targets
          result = await this.$refs.diceCanvas.rollToTargets(targetNumbers)
        } else {
          // Single dice or same target for all
          result = await this.$refs.diceCanvas.rollToTarget(targetNumbers)
        }

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

      // Update status message based on result type
      if (result.diceCount > 1) {
        if (result.resultType === 'both') {
          this.rollStatus = `Rolled ${result.numbers.join(' and ')}`
        } else {
          this.rollStatus = `${result.resultType === 'best' ? 'Best' : 'Worst'}: ${result.number} (${result.numbers.join(', ')})`
        }
      } else {
        this.rollStatus = `Landed on ${result.number}`
      }

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

    handleMaterialChange(materialType) {
      if (this.$refs.diceCanvas) {
        const success = this.$refs.diceCanvas.setMaterialType(materialType)
        if (success) {
          this.currentMaterial = materialType
          this.rollStatus = `Material changed to ${materialType}`
        } else {
          this.rollStatus = 'Failed to change material'
        }
      }
    },

    handleShaderChange(shaderType) {
      if (this.$refs.diceCanvas) {
        const success = this.$refs.diceCanvas.setShaderType(shaderType)
        if (success) {
          this.currentShader = shaderType
          this.rollStatus = shaderType === 'none'
              ? 'Shader effects disabled'
              : `Shader changed to ${shaderType}`
        } else {
          this.rollStatus = 'Failed to change shader'
        }
      }
    },

    handleDiceCountChange(diceCount) {
      if (this.$refs.diceCanvas) {
        this.$refs.diceCanvas.setDiceCount(diceCount)
        this.rollStatus = `Using ${diceCount} ${diceCount === 1 ? 'die' : 'dice'}`
      }
    },

    handleResultModeChange(resultMode) {
      if (this.$refs.diceCanvas) {
        this.$refs.diceCanvas.setResultMode(resultMode)
        this.rollStatus = `Result mode: ${resultMode}`
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
  border-radius: 10px;
  overflow: hidden;
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

}

.realistic-dice-roller-content {
  width: 60rem;
  height: 30rem;
  display: flex;
  justify-content: center;
  align-items: center;

}
</style>