<template>
  <div class="dice-modal-overlay" v-if="isOpen" @click="handleOverlayClick">
    <div class="dice-modal" @click.stop>
      <div class="dice-modal-header">
        <h2>Roll Dice</h2>
        <button class="close-button" @click="$emit('close')">✕</button>
      </div>

      <div class="dice-modal-content">
        <!-- Dice Selection Panel -->
        <div class="dice-selection-panel">
          <h3>Select Dice</h3>
          <div class="dice-type-grid">
            <button
                v-for="diceType in diceTypes"
                :key="diceType.type"
                class="dice-type-button"
                :style="{ backgroundColor: diceType.color }"
                @click="addDie(diceType)"
            >
              <div class="dice-label">{{ diceType.type.toUpperCase() }}</div>
              <div class="dice-sides">{{ diceType.sides }} sides</div>
            </button>
          </div>
        </div>

        <!-- 3D Dice Display -->
        <div class="dice-display-container">
          <h3>Dice Preview</h3>
          <div class="three-js-container" ref="threeContainer">
            <canvas ref="canvas"></canvas>
            <div v-if="selectedDice.length === 0" class="empty-state">
              Select dice to see 3D preview
            </div>
          </div>
        </div>

        <!-- Selected Dice Info -->
        <div v-if="selectedDice.length > 0" class="selected-dice-panel">
          <h3>Selected Dice ({{ selectedDice.length }})</h3>
          <div class="dice-chips">
            <div
                v-for="die in selectedDice"
                :key="die.id"
                class="dice-chip"
                :style="{ backgroundColor: die.color }"
            >
              <span>{{ die.type.toUpperCase() }}</span>
              <span v-if="die.result">: {{ die.result }}</span>
              <button class="remove-die" @click="removeDie(die.id)">×</button>
            </div>
          </div>
        </div>

        <!-- Roll Results -->
        <div v-if="rollResults.length > 0" class="results-panel">
          <h3>Results</h3>
          <div class="results-grid">
            <div class="individual-results">
              <h4>Individual Results:</h4>
              <div class="result-list">
                <div v-for="die in rollResults" :key="die.id" class="result-item">
                  <span>{{ die.type.toUpperCase() }}</span>
                  <span class="result-value">{{ die.result }}</span>
                </div>
              </div>
            </div>
            <div class="summary-results">
              <h4>Summary:</h4>
              <div class="total-result">
                Total: {{ totalResult }}
              </div>
              <div class="average-result">
                Average: {{ averageResult }}
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <div class="left-buttons">
            <button
                class="roll-button"
                :disabled="selectedDice.length === 0 || isRolling"
                @click="rollDice"
            >
              {{ isRolling ? 'Rolling...' : 'Roll Dice' }}
            </button>
            <button class="clear-button" @click="clearDice">
              Clear All
            </button>
            <button
                v-if="predefinedResults"
                class="predefined-button"
                @click="setPredefinedResults"
            >
              Set Results
            </button>
          </div>
          <button class="close-button-alt" @click="$emit('close')">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import DiceRenderer from '@/services/dice/DiceRenderer.js'

export default {
  name: 'DiceRollingModal',
  props: {
    isOpen: {
      type: Boolean,
      required: true
    },
    predefinedResults: {
      type: Array,
      default: null
    }
  },
  emits: ['close', 'roll-complete'],
  setup(props, { emit }) {
    const threeContainer = ref(null)
    const canvas = ref(null)
    const selectedDice = ref([])
    const rollResults = ref([])
    const isRolling = ref(false)
    let diceRenderer = null

    const diceTypes = [
      { type: 'd4', sides: 4, color: '#ff6b6b', geometry: 'tetrahedron' },
      { type: 'd6', sides: 6, color: '#4ecdc4', geometry: 'cube' },
      { type: 'd8', sides: 8, color: '#45b7d1', geometry: 'octahedron' },
      { type: 'd10', sides: 10, color: '#96ceb4', geometry: 'pentagonal' },
      { type: 'd12', sides: 12, color: '#feca57', geometry: 'dodecahedron' },
      { type: 'd20', sides: 20, color: '#ff9ff3', geometry: 'icosahedron' },
      { type: 'd100', sides: 100, color: '#a8e6cf', geometry: 'sphere' }
    ]

    const totalResult = computed(() => {
      return rollResults.value.reduce((sum, die) => sum + die.result, 0)
    })

    const averageResult = computed(() => {
      if (rollResults.value.length === 0) return 0
      return (totalResult.value / rollResults.value.length).toFixed(1)
    })

    const addDie = (diceType) => {
      const newDie = {
        id: Date.now() + Math.random(),
        ...diceType,
        result: null,
        position: selectedDice.value.length
      }
      selectedDice.value.push(newDie)

      if (diceRenderer) {
        diceRenderer.addDie(newDie)
      }
    }

    const removeDie = (id) => {
      const index = selectedDice.value.findIndex(die => die.id === id)
      if (index !== -1) {
        selectedDice.value.splice(index, 1)
        if (diceRenderer) {
          diceRenderer.removeDie(id)
        }
      }
    }

    const clearDice = () => {
      selectedDice.value = []
      rollResults.value = []
      if (diceRenderer) {
        diceRenderer.clearDice()
      }
    }

    const rollDice = async () => {
      if (selectedDice.value.length === 0 || isRolling.value) return

      isRolling.value = true
      rollResults.value = []

      // Start 3D rolling animation
      if (diceRenderer) {
        await diceRenderer.rollDice()
      }

      // Calculate results (or use predefined)
      const results = selectedDice.value.map((die, index) => {
        let result
        if (props.predefinedResults && props.predefinedResults[index]) {
          result = props.predefinedResults[index]
        } else {
          result = Math.floor(Math.random() * die.sides) + 1
        }

        return { ...die, result }
      })

      // Update dice with results
      selectedDice.value = results
      rollResults.value = results

      // Show results on 3D dice
      if (diceRenderer) {
        diceRenderer.showResults(results)
      }

      isRolling.value = false
      emit('roll-complete', results)
    }

    const setPredefinedResults = () => {
      if (!props.predefinedResults) return

      const results = selectedDice.value.map((die, index) => ({
        ...die,
        result: props.predefinedResults[index] || 1
      }))

      selectedDice.value = results
      rollResults.value = results

      if (diceRenderer) {
        diceRenderer.showResults(results)
      }
    }

    const handleOverlayClick = () => {
      emit('close')
    }

    const initializeRenderer = () => {
      if (canvas.value && threeContainer.value) {
        diceRenderer = new DiceRenderer(canvas.value, threeContainer.value)
        diceRenderer.initialize()
      }
    }

    const destroyRenderer = () => {
      if (diceRenderer) {
        diceRenderer.destroy()
        diceRenderer = null
      }
    }

    watch(() => props.isOpen, (newValue) => {
      if (newValue) {
        // Small delay to ensure DOM is ready
        setTimeout(initializeRenderer, 100)
      } else {
        destroyRenderer()
      }
    })

    onMounted(() => {
      if (props.isOpen) {
        initializeRenderer()
      }
    })

    onUnmounted(() => {
      destroyRenderer()
    })

    return {
      threeContainer,
      canvas,
      selectedDice,
      rollResults,
      isRolling,
      diceTypes,
      totalResult,
      averageResult,
      addDie,
      removeDie,
      clearDice,
      rollDice,
      setPredefinedResults,
      handleOverlayClick
    }
  }
}
</script>

<style scoped>
.dice-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}

.dice-modal {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  max-width: 90vw;
  max-height: 90vh;
  width: 1000px;
  overflow-y: auto;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.dice-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.dice-modal-header h2 {
  color: #ffffff;
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.close-button {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #ffffff;
  font-size: 20px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.2s ease;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.dice-modal-content {
  padding: 20px;
  color: #ffffff;
}

.dice-selection-panel,
.selected-dice-panel,
.results-panel {
  margin-bottom: 24px;
}

.dice-selection-panel h3,
.selected-dice-panel h3,
.results-panel h3 {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
}

.dice-type-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.dice-type-button {
  height: 80px;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.dice-type-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.dice-type-button:active {
  transform: translateY(0);
}

.dice-type-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.dice-type-button:hover::before {
  left: 100%;
}

.dice-label {
  font-size: 16px;
  font-weight: bold;
}

.dice-sides {
  font-size: 10px;
  opacity: 0.8;
}

.dice-display-container {
  margin-bottom: 24px;
}

.dice-display-container h3 {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
}

.three-js-container {
  width: 100%;
  height: 300px;
  background: linear-gradient(45deg, #0f0f23, #1a1a2e);
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.three-js-container canvas {
  width: 100%;
  height: 100%;
  display: block;
}

.empty-state {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: rgba(255, 255, 255, 0.5);
  font-size: 16px;
  text-align: center;
}

.dice-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.dice-chip {
  padding: 8px 12px;
  border-radius: 20px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
  position: relative;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.remove-die {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 12px;
  margin-left: 4px;
  transition: background 0.2s ease;
}

.remove-die:hover {
  background: rgba(255, 255, 255, 0.3);
}

.results-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.individual-results h4,
.summary-results h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.result-value {
  font-weight: bold;
  color: #ffd700;
}

.total-result {
  font-size: 24px;
  font-weight: bold;
  color: #ffd700;
  margin-bottom: 4px;
}

.average-result {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 20px;
}

.left-buttons {
  display: flex;
  gap: 12px;
}

.roll-button {
  background: linear-gradient(135deg, #4ade80, #22c55e);
  border: none;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.roll-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.roll-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.clear-button,
.predefined-button,
.close-button-alt {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-button:hover,
.predefined-button:hover,
.close-button-alt:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .dice-modal {
    width: 95vw;
    margin: 20px;
  }

  .dice-type-grid {
    grid-template-columns: repeat(4, 1fr);
  }

  .results-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
    gap: 12px;
  }

  .left-buttons {
    width: 100%;
    justify-content: center;
  }
}
</style>