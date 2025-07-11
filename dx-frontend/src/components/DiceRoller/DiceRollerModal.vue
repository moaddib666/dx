<template>
  <div class="dice-roller-modal" v-if="visible">
    <div class="modal-overlay" @click="closeModal"></div>
    <div class="modal-container" @click="handleContainerClick">
      <div class="modal-container--mask">
        <div class="dice-canvas-content" @click="rollDice">
          <DiceCanvas
              ref="diceCanvas"
              @ready="onCanvasReady"
              @error="onCanvasError"
              @roll-complete="onRollComplete"
              class="dice-canvas"
          />
        </div>
        <div class="instruction-text">Click to roll D20</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, ref, PropType} from 'vue';
import DiceCanvas from "@/components/DiceRoller/DiceCanvas.vue";

// Define types for component
interface RollResult {
  number: number;
  rollTime: number;

  [key: string]: any; // For any additional properties in the result
}

const DICE_ROLL_TARGET = 10; // Predefined constant - not changeable
const textureModule = await import('@/assets/textures/dice-texture.png');
const textureUrl = textureModule.default;

// Fetch the texture image
const response = await fetch(textureUrl);
const blob = await response.blob();

// Create a File object from the blob
const file = new File([blob], 'dice-texture.png', {type: blob.type});
export default defineComponent({
  name: 'DiceRollerModal',

  components: {
    DiceCanvas
  },

  props: {
    visible: {
      type: Boolean as PropType<boolean>,
      default: false
    }
  },

  emits: ['close', 'error', 'roll-complete'],

  setup() {
    // Return empty setup to use options API with TypeScript
    return {};
  },

  data() {
    return {
      currentState: 'initial' as 'initial' | 'rolling' | 'results',
      isCanvasReady: false,
      lastResult: null as RollResult | null
    }
  },

  computed: {
    canRoll(): boolean {
      return this.isCanvasReady && this.currentState !== 'rolling'
    }
  },

  methods: {
    closeModal(): void {
      this.$emit('close');
    },

    async onCanvasReady(): Promise<void> {
      this.isCanvasReady = true;

      // Automatically apply the texture when canvas is ready
      try {
        // Apply the texture to the dice
        await this.$refs.diceCanvas.setUserTexture(file);
      } catch (error) {
        console.error('Failed to apply dice texture:', error);
      }
    },

    onCanvasError(error: Error): void {
      console.error('Canvas error:', error);
      this.$emit('error', error);
    },

    handleContainerClick(event: MouseEvent): void {
      // Prevent closing modal when clicking inside
      event.stopPropagation();

      if (this.canRoll) {
        this.rollDice();
      }
    },

    async rollDice(): Promise<void> {
      if (!this.canRoll || !this.$refs.diceCanvas) return;

      try {
        this.currentState = 'rolling';

        // Use random roll for simplicity - the target is just for visual effect
        const result = await this.$refs.diceCanvas.rollToTarget(DICE_ROLL_TARGET);

        // Result will be handled by onRollComplete
      } catch (error) {
        console.error('Error rolling dice:', error);
        this.currentState = 'initial';
      }
    },

    onRollComplete(result: RollResult): void {
      this.lastResult = result;
      this.currentState = 'results';
      this.$emit('roll-complete', result);
    }
  }
});
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
  background-color: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(7px);
}

.modal-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  width: 30rem;
  height: 45rem;
  overflow: hidden;
  background: url("@/assets/images/dice/Frame.png") no-repeat center center;
  background-size: contain;
  mask-size: contain;
}

.modal-container--mask {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  mask: url("@/assets/images/dice/Mask.png") no-repeat center center;
  mask-size: contain;
  -webkit-mask: url("@/assets/images/dice/Mask.png") no-repeat center center;
  -webkit-mask-size: contain;
  overflow: hidden;
  background: rgba(80, 75, 75, 0.1);
  backdrop-filter: blur(25px);
}

.dice-canvas-content {
  width: 62%;
  margin-top: 5rem;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.dice-canvas {
  pointer-events: none;
}
</style>