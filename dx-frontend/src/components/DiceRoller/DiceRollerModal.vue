<template>
  <div class="dice-roller-modal" v-if="visible">
    <div class="modal-overlay" @click="closeModal"></div>
    <div class="modal-container" @click="handleContainerClick">
      <div class="dice-canvas-overlay" @click="rollDice"></div>
      <DiceCanvas
          ref="diceCanvas"
          @ready="onCanvasReady"
          @error="onCanvasError"
          @roll-complete="onRollComplete"
          class="dice-canvas"
      />
      <div class="instruction-text">Click to roll D20</div>
    </div>
  </div>
</template>

<script>
import DiceCanvas from "@/components/DiceRoller/DiceCanvas.vue";

const DICE_ROLL_TARGET = 10; // Predefined constant - not changeable
const TextureImage = () => import('@/assets/textures/dice-texture.png'); // Lazy load texture

export default {
  name: 'DiceRollerModal',

  components: {
    DiceCanvas
  },

  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      currentState: 'initial', // initial, rolling, results
      isCanvasReady: false,
      lastResult: null
    }
  },
  computed: {
    canRoll() {
      return this.isCanvasReady && this.currentState !== 'rolling'
    }
  },

  methods: {
    async setUserTexture(file) {
      if (!this.d20Service) return false
      const success = await this.d20Service.setUserTexture(file)
      this.d20Service.createDice()
      return success
    },
    closeModal() {
      this.$emit('close')
    },

    async onCanvasReady() {
      this.isCanvasReady = true

      // Automatically apply the texture when canvas is ready
      try {
        const textureModule = await import('@/assets/textures/dice-texture.png')
        const textureUrl = textureModule.default

        // Fetch the texture image
        const response = await fetch(textureUrl)
        const blob = await response.blob()

        // Create a File object from the blob
        const file = new File([blob], 'dice-texture.png', { type: blob.type })

        // Apply the texture to the dice
        await this.$refs.diceCanvas.setUserTexture(file)
      } catch (error) {
        console.error('Failed to apply dice texture:', error)
      }
    },

    onCanvasError(error) {
      console.error('Canvas error:', error)
      this.$emit('error', error)
    },

    handleContainerClick(event) {
      // Prevent closing modal when clicking inside
      event.stopPropagation()

      if (this.canRoll) {
        this.rollDice()
      }
    },

    async rollDice() {
      if (!this.canRoll || !this.$refs.diceCanvas) return

      try {
        this.currentState = 'rolling'

        // Use random roll for simplicity - the target is just for visual effect
        const result = await this.$refs.diceCanvas.rollRandom()

        // Result will be handled by onRollComplete
      } catch (error) {
        console.error('Error rolling dice:', error)
        this.currentState = 'initial'
      }
    },

    onRollComplete(result) {
      this.lastResult = result
      this.currentState = 'results'
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
  background-color: rgba(0, 0, 0, 0.7);
}

.modal-container {
  position: relative;
  border-radius: 12px;
  background-color: #2a2a2a;
  width: 400px;
  height: 300px;
  cursor: pointer;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.state-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}

.dice-canvas {
  flex: 1;
  display: block;
  width: 100%;
  background-color: #1a1a1a;
}

.instruction-text {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  color: #ffffff;
  font-size: 14px;
  font-weight: 500;
  text-align: center;
  background-color: rgba(0, 0, 0, 0.6);
  padding: 8px 16px;
  border-radius: 20px;
  backdrop-filter: blur(4px);
}

.instruction-text.rolling {
  animation: pulse 1.5s infinite;
}

.result-display {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.8);
  padding: 12px;
  border-radius: 8px;
  backdrop-filter: blur(4px);
}

.result-number {
  font-size: 32px;
  font-weight: bold;
  color: #00ff88;
  text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
  margin-bottom: 4px;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

.modal-container:hover {
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6);
}

.dice-canvas-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}
</style>