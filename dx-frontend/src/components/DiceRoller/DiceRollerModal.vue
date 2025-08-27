<template>
  <div class="dice-roller-modal" v-if="visible">
    <div class="modal-overlay" @click="closeModal"></div>
    <div class="modal-container">
      <!-- Challenge Description -->
      <div class="challenge-description">
        <p> {{ descriptionText }}</p>
      </div>

      <div class="modal-container--mask">
        <!-- Difficulty Class at the top -->
        <div class="difficulty-class">
          <h2>Difficulty</h2>
          <h1>{{props.challenge?.difficulty || 12 }}</h1>
        </div>

        <!-- Dice Canvas -->
        <div class="dice-canvas-content" @click="rollDice">
          <DiceCanvas
              ref="diceCanvas"
              :preloaded-texture="file"
              @ready="onCanvasReady"
              @error="onCanvasError"
              @roll-complete="onRollComplete"
              class="dice-canvas"
          />
          <!-- CTA Text -->
          <div v-if="showCTA" class="dice-cta">Click to roll the dice</div>
        </div>
      </div>

      <!-- Outcome Banner at the bottom with cool styling -->
      <div v-if="currentState === 'results' && lastResult" class="outcome-banner" :class="outcomeClass">
        {{ currentOutcome }}
      </div>
    </div>

    <!-- Dice Modifier Holder -->
    <DiceModifierHolder
        v-if="props.challenge?.modifiers"
        class="modifier-holder"
        :modifiers="props.challenge.modifiers"
        :highlighted-index="currentlyHighlightedModifier"
        :is-animating="isAnimatingModifiers"
    />

    <!-- Debug Toolbar -->
    <DiceDebugToolbar
        v-if="props.debug"
        :dice-canvas="$refs.diceCanvas"
        :visible="props.debug"
        @roll-started="onDebugRollStarted"
        @roll-completed="onDebugRollCompleted"
        @visibility-changed="onDebugVisibilityChanged"
    />
  </div>
</template>

<script setup lang="ts">
import {ref, computed, onMounted, type PropType} from 'vue';
import DiceCanvas from "@/components/DiceRoller/DiceCanvas.vue";
import DiceBackendService from "@/services/dice/DiceBackendService.js";
import DiceModifierHolder from "@/components/DiceRoller/DiceModifier/DiceModifierHolder.vue";
import DiceDebugToolbar from "@/components/DiceRoller/DiceDebugToolbar.vue";
import type {ChallengeGeneric} from "@/api/dx-backend/api";

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

type Props = {
  visible: boolean;
  debug: boolean | undefined;
  challenge: ChallengeGeneric | null | undefined;
};

// Props
const props = withDefaults(defineProps<Props>(), {
  visible: false,
  debug: false,
  challenge: null
});

// Emits
const emit = defineEmits<{
  close: [];
  error: [error: Error];
  'roll-complete': [result: RollResult];
}>();

// Reactive data
const currentState = ref<'initial' | 'rolling' | 'results' | 'applying-modifiers'>('initial');
const isCanvasReady = ref(false);
const lastResult = ref<RollResult | null>(null);
const lastApiResult = ref<RollResult | null>(null);
const file = ref<File | null>(null);
const currentOutcome = ref<OutcomeType | null>(null);
const showCTA = ref(true);
const diceBackendService = new DiceBackendService();

// Animation state for modifiers
const isAnimatingModifiers = ref(false);
const currentlyHighlightedModifier = ref<number>(-1);
const modifiedRollValue = ref<number>(0);
const originalRollValue = ref<number>(0);
const descriptionText = computed((): string => {
  return props.challenge?.description || 'Roll a d20 to determine the outcome of your challenge.';
});
// Template refs
const diceCanvas = ref<InstanceType<typeof DiceCanvas> | null>(null);

// Computed properties
const canRoll = computed((): boolean => {
  return isCanvasReady.value && currentState.value !== 'rolling';
});

const outcomeClass = computed((): string => {
  if (!currentOutcome.value) return '';

  switch (currentOutcome.value) {
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
});

// Methods
const closeModal = (): void => {
  emit('close');
};

const onCanvasReady = async (): Promise<void> => {
  isCanvasReady.value = true;
  // Texture is now applied during initialization via the preloaded-texture prop
};

const onCanvasError = (error: Error): void => {
  console.error('Canvas error:', error);
  emit('error', error);
};


const rollDice = async (): Promise<void> => {
  if (!canRoll.value || !diceCanvas.value) return;

  try {
    currentState.value = 'rolling';
    showCTA.value = false; // Hide CTA after first roll

    // Get dice roll result from backend API
    const apiResult = await diceBackendService.rollD20Dice();

    // Store the API result BEFORE starting visual animation
    lastApiResult.value = apiResult;

    // Use the target number from the API response for the visual dice roll
    const result = await diceCanvas.value.rollToTarget(apiResult.number);

    lastResult.value = result;

    // Result will be handled by onRollComplete
  } catch (error) {
    console.error('Error rolling dice:', error);
    currentState.value = 'initial';
  }
};

const onRollComplete = (result: RollResult): void => {
  // Ensure we have fresh API result data - if not, something went wrong
  if (!lastApiResult.value) {
    console.warn('onRollComplete called without API result data');
    return;
  }

  // Combine the visual roll result with the API result, prioritizing API data
  const combinedResult = {
    ...result,
    // Always use the API result for the actual outcome
    number: lastApiResult.value.number,
    targetNumber: lastApiResult.value.targetNumber
  };

  lastResult.value = combinedResult;
  originalRollValue.value = combinedResult.number;
  modifiedRollValue.value = combinedResult.number;

  // Always use the outcome from the API result, which is determined by the service
  if (lastApiResult.value?.outcome) {
    currentOutcome.value = lastApiResult.value.outcome as OutcomeType;
  } else {
    // If for some reason we don't have an API result, use the service to determine the outcome
    currentOutcome.value = diceBackendService.determineOutcome(combinedResult.number) as OutcomeType;
  }

  currentState.value = 'results';

  // Check if we have modifiers to animate
  if (props.challenge?.modifiers && props.challenge.modifiers.length > 0) {
    // Start modifier animation sequence
    setTimeout(() => {
      animateModifiers();
    }, 1000); // Wait 1 second after initial roll result display
  } else {
    // No modifiers, emit result immediately
    emit('roll-complete', combinedResult);
  }

  // Clear the API result after using it
  lastApiResult.value = null;
};

// Debug toolbar event handlers
const onDebugRollStarted = (debugInfo: any): void => {
  console.log('Debug roll started:', debugInfo);
  currentState.value = 'rolling';
};

const onDebugRollCompleted = (result: RollResult): void => {
  console.log('Debug roll completed:', result);
  lastResult.value = result;

  // For debug rolls, determine outcome based on the result number
  currentOutcome.value = diceBackendService.determineOutcome(result.number) as OutcomeType;
  currentState.value = 'results';

  // Emit the debug result
  emit('roll-complete', result);
};

const onDebugVisibilityChanged = (visible: boolean): void => {
  showDebugToolbar.value = visible;
  console.log('Debug toolbar visibility changed:', visible);
};

// Modifier animation functions
const animateModifiers = async (): Promise<void> => {
  if (!props.challenge?.modifiers || props.challenge.modifiers.length === 0) {
    return;
  }

  currentState.value = 'applying-modifiers';
  isAnimatingModifiers.value = true;

  // Animate each modifier sequentially
  for (let i = 0; i < props.challenge.modifiers.length; i++) {
    const modifier = props.challenge.modifiers[i];

    // Highlight current modifier
    currentlyHighlightedModifier.value = i;

    // Wait for highlight animation
    await new Promise(resolve => setTimeout(resolve, 800));

    // Apply modifier value
    const previousValue = modifiedRollValue.value;
    modifiedRollValue.value += modifier.value;

    // Ensure the modified value stays within valid dice range (1-20 for display purposes)
    const displayValue = Math.max(1, Math.min(20, modifiedRollValue.value));

    // Trigger dice shake and number update
    await shakeDiceAndUpdateNumber(displayValue);

    // Wait before next modifier
    await new Promise(resolve => setTimeout(resolve, 500));
  }

  // Clear highlighting
  currentlyHighlightedModifier.value = -1;
  isAnimatingModifiers.value = false;

  // Update final outcome based on modified roll value
  const finalResult = {
    ...lastResult.value!,
    number: modifiedRollValue.value,
    originalNumber: originalRollValue.value,
    modifiedBy: modifiedRollValue.value - originalRollValue.value
  };

  // Determine new outcome based on modified value
  currentOutcome.value = diceBackendService.determineOutcome(modifiedRollValue.value) as OutcomeType;

  currentState.value = 'results';
  emit('roll-complete', finalResult);
};

const shakeDiceAndUpdateNumber = async (newNumber: number): Promise<void> => {
  if (!diceCanvas.value) return;

  // Create a subtle shake effect by slightly moving the dice
  const originalPosition = { x: 0, y: 1, z: 0 };
  const shakeIntensity = 0.1;
  const shakeDuration = 300; // ms
  const shakeSteps = 6;

  // Perform shake animation
  for (let i = 0; i < shakeSteps; i++) {
    const offsetX = (Math.random() - 0.5) * shakeIntensity;
    const offsetY = (Math.random() - 0.5) * shakeIntensity * 0.5; // Less vertical shake
    const offsetZ = (Math.random() - 0.5) * shakeIntensity;

    // Note: We would need to add a method to DiceCanvas to update position
    // For now, we'll simulate the shake with a visual effect

    await new Promise(resolve => setTimeout(resolve, shakeDuration / shakeSteps));
  }

  // Roll dice to show new number
  try {
    await diceCanvas.value.rollToTarget(newNumber);
  } catch (error) {
    console.warn('Could not update dice to show new number:', error);
  }
};

// Lifecycle hooks
onMounted(async () => {
  // Reset CTA visibility on mount
  showCTA.value = true;

  try {
    // Load the texture
    const textureModule = await import('@/assets/textures/dice-texture.png');
    const textureUrl = textureModule.default;

    // Fetch the texture image
    const response = await fetch(textureUrl);
    const blob = await response.blob();

    // Create a File object from the blob
    file.value = new File([blob], 'dice-texture.png', {type: blob.type});
  } catch (error) {
    console.error('Failed to load dice texture:', error);
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

/* Challenge Description Styles */
.challenge-description {
  position: absolute;
  top: 0.5rem;
  width: 90%;
  text-align: center;
  z-index: 10;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 8px;
  padding: 0.8rem;
  backdrop-filter: blur(10px);
}

.challenge-description p {
  color: #f0f0f0;
  font-size: 0.9rem;
  line-height: 1.4;
  margin: 0;
  font-family: 'Arial', sans-serif;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
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

/* Difficulty Class Styles */
.difficulty-class {
  position: absolute;
  top: 7rem;
  width: 90%;
  text-align: center;
  z-index: 10;
  padding: 0.5rem;
  border-radius: 8px;
  backdrop-filter: blur(5px);
  color: #d4af37;
  text-transform: uppercase;
}

.difficulty-class h2 {
  font-size: 1.5rem;
  margin: 0 0 0.5rem 0;
  font-family: 'Copperplate Gothic', 'Gothic', serif;
  letter-spacing: 1px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
}

.difficulty-class h1 {
  font-size: 3.5rem;
  margin: 0;
  font-family: 'Copperplate Gothic', 'Gothic', serif;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
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

.dice-cta {
  position: absolute;
  bottom: -1rem;
  left: 50%;
  transform: translateX(-50%);
  color: #f0f0f0;
  font-size: 0.9rem;
  font-family: 'Arial', sans-serif;
  text-align: center;
  background: rgba(0, 0, 0, 0.6);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  cursor: pointer;
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
  bottom: 10rem;
  width: 80%;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  font-family: 'Copperplate Gothic', 'Gothic', serif;
  letter-spacing: 2px;
  padding: 0.8rem;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  z-index: 10;
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