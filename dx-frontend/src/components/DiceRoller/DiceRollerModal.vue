<template>
  <div class="dice-roller-modal" v-if="visible">
    <div class="modal-overlay" @click="closeModal"></div>
    <div class="modal-container" @click="handleContainerClick">
      <div class="modal-container--mask">
        <div v-if="currentState === 'results' && lastResult" class="outcome-banner" :class="outcomeClass">
          {{ currentOutcome }}
        </div>
        <div class="dice-canvas-content" @click="rollDice">
          <DiceCanvas
              ref="diceCanvas"
              :preloaded-texture="file"
              @ready="onCanvasReady"
              @error="onCanvasError"
              @roll-complete="onRollComplete"
              class="dice-canvas"
          />
        </div>

      </div>
    </div>
    <DiceModifierHolder
        class="modifier-holder"
        :modifiers="[
      {
        id: 'mod1',
        name: 'Strength Boost',
        value: 2,
      },
      {
        id: 'mod2',
        name: 'Agility Boost',
        value: 3,
      },
      {
        id: 'mod3',
        name: 'Intelligence Boost',
        value: 1,
      },
      {
        id: 'mod4',
        name: 'Speed Debuff',
        value: -4,
      }
  ]"></DiceModifierHolder>

    <!-- Debug Toolbar -->
    <DiceDebugToolbar
        :dice-canvas="$refs.diceCanvas"
        :visible="showDebugToolbar"
        @roll-started="onDebugRollStarted"
        @roll-completed="onDebugRollCompleted"
        @visibility-changed="onDebugVisibilityChanged"
    />
  </div>
</template>

<script lang="ts">
import {defineComponent, ref, PropType} from 'vue';
import DiceCanvas from "@/components/DiceRoller/DiceCanvas.vue";
import DiceBackendService from "@/services/dice/DiceBackendService.js";
import DiceModifierHolder from "@/components/DiceRoller/DiceModifier/DiceModifierHolder.vue";
import DiceDebugToolbar from "@/components/DiceRoller/DiceDebugToolbar.vue";

// Define types for component
interface RollResult {
  number: number;
  rollTime: number;
  targetNumber?: number;
  outcome?: string;

  [key: string]: any; // For any additional properties in the result
}

// Define outcome types
type OutcomeType = 'Critical Fail' | 'Fail' | 'Success' | 'Critical Success';
export default defineComponent({
  name: 'DiceRollerModal',

  components: {
    DiceModifierHolder,
    DiceCanvas,
    DiceDebugToolbar
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
      lastResult: null as RollResult | null,
      lastApiResult: null as RollResult | null,
      file: null as File | null,
      currentOutcome: null as OutcomeType | null,
      diceBackendService: new DiceBackendService(),
      showDebugToolbar: process.env.NODE_ENV === 'development' // Show debug toolbar only in development
    }
  },

  async created() {
    try {
      // Load the texture
      const textureModule = await import('@/assets/textures/dice-texture.png');
      const textureUrl = textureModule.default;

      // Fetch the texture image
      const response = await fetch(textureUrl);
      const blob = await response.blob();

      // Create a File object from the blob
      this.file = new File([blob], 'dice-texture.png', {type: blob.type});
    } catch (error) {
      console.error('Failed to load dice texture:', error);
    }
  },

  computed: {
    canRoll(): boolean {
      return this.isCanvasReady && this.currentState !== 'rolling'
    },

    outcomeClass(): string {
      if (!this.currentOutcome) return '';

      switch (this.currentOutcome) {
        case 'Critical Fail':
          return 'outcome-critical-fail';
        case 'Fail':
          return 'outcome-fail';
        case 'Success':
          return 'outcome-success';
        case 'Critical Success':
          return 'outcome-critical-success';
        default:
          return '';
      }
    }
  },

  methods: {
    closeModal(): void {
      this.$emit('close');
    },

    async onCanvasReady(): Promise<void> {
      this.isCanvasReady = true;
      // Texture is now applied during initialization via the preloaded-texture prop
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

        // Get dice roll result from backend API
        const apiResult = await this.diceBackendService.rollD20Dice();

        // Store the API result BEFORE starting visual animation
        this.lastApiResult = apiResult;

        // Use the target number from the API response for the visual dice roll
        const result = await this.$refs.diceCanvas.rollToTarget(apiResult.number);

        this.lastResult = result;

        // Result will be handled by onRollComplete
      } catch (error) {
        console.error('Error rolling dice:', error);
        this.currentState = 'initial';
      }
    },

    onRollComplete(result: RollResult): void {
      // Ensure we have fresh API result data - if not, something went wrong
      if (!this.lastApiResult) {
        console.warn('onRollComplete called without API result data');
        return;
      }

      // Combine the visual roll result with the API result, prioritizing API data
      const combinedResult = {
        ...result,
        // Always use the API result for the actual outcome
        number: this.lastApiResult.number,
        targetNumber: this.lastApiResult.targetNumber
      };

      this.lastResult = combinedResult;

      // Always use the outcome from the API result, which is determined by the service
      if (this.lastApiResult?.outcome) {
        this.currentOutcome = this.lastApiResult.outcome as OutcomeType;
      } else {
        // If for some reason we don't have an API result, use the service to determine the outcome
        this.currentOutcome = this.diceBackendService.determineOutcome(combinedResult.number) as OutcomeType;
      }

      this.currentState = 'results';
      this.$emit('roll-complete', combinedResult);

      // Clear the API result after using it
      this.lastApiResult = null;
    },

    // Debug toolbar event handlers
    onDebugRollStarted(debugInfo: any): void {
      console.log('Debug roll started:', debugInfo);
      this.currentState = 'rolling';
    },

    onDebugRollCompleted(result: RollResult): void {
      console.log('Debug roll completed:', result);
      this.lastResult = result;

      // For debug rolls, determine outcome based on the result number
      this.currentOutcome = this.diceBackendService.determineOutcome(result.number) as OutcomeType;
      this.currentState = 'results';

      // Emit the debug result
      this.$emit('roll-complete', result);
    },

    onDebugVisibilityChanged(visible: boolean): void {
      this.showDebugToolbar = visible;
      console.log('Debug toolbar visibility changed:', visible);
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

.roll-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.roll-number {
  font-size: 3rem;
  font-weight: bold;
  color: white;
  margin-bottom: 0.5rem;
}

.roll-outcome {
  font-size: 1.5rem;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.outcome-banner {
  position: absolute;
  top: 6rem;
  width: 60%;
  flex-wrap: wrap;
  text-wrap: wrap;
  text-align: center;
  font-size: 3rem;
  font-weight: bold;
  font-family: 'Copperplate Gothic', 'Gothic', serif;
  letter-spacing: 2px;
  padding: 0.5rem;
}

.outcome-critical-fail {
  color: #ff0000;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
}

.outcome-fail {
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
}

.outcome-success, .outcome-critical-success {
  color: transparent;
  background-clip: text;
  -webkit-background-clip: text;
  background-image: linear-gradient(to bottom, #f6e27a, #d4af37, #c5a028, #f6e27a);
}

.modifier-holder {
  position: absolute;
  bottom: 1rem;
  width: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>