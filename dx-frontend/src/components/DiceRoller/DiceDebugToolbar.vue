<template>
  <div class="dice-debug-toolbar" v-if="showDebugToolbar">
    <div class="debug-panel">
      <h4 class="debug-title">🔧 Debug Toolbar</h4>

      <div class="debug-controls">
        <div class="target-input-group">
          <label for="targetNumber" class="input-label">Target Face:</label>
          <input
            id="targetNumber"
            v-model.number="targetNumber"
            type="number"
            min="1"
            max="20"
            class="target-input"
            :disabled="isRolling"
            @keyup.enter="rollToTarget"
          />
        </div>

        <button
          @click="rollToTarget"
          :disabled="isRolling || !isValidTarget"
          class="roll-button"
          :class="{ rolling: isRolling }"
        >
          {{ isRolling ? 'Rolling...' : 'Roll to Target' }}
        </button>

        <button
          @click="rollRandom"
          :disabled="isRolling"
          class="random-button"
          :class="{ rolling: isRolling }"
        >
          {{ isRolling ? 'Rolling...' : 'Roll Random' }}
        </button>
      </div>

      <div class="quick-targets">
        <span class="quick-label">Quick Targets:</span>
        <div class="target-buttons">
          <button
            v-for="num in quickTargets"
            :key="num"
            @click="setAndRoll(num)"
            :disabled="isRolling"
            class="quick-target-btn"
            :class="{ active: targetNumber === num }"
          >
            {{ num }}
          </button>
        </div>
      </div>

      <div class="debug-info" v-if="lastResult">
        <div class="result-display">
          <span class="result-label">Last Result:</span>
          <span class="result-value" :class="getResultClass(lastResult.number)">
            {{ lastResult.number }}
          </span>
          <span class="result-type">{{ lastResult.isDeterministic ? '(Deterministic)' : '(Random)' }}</span>
        </div>
      </div>

      <div class="toolbar-toggle">
        <button @click="toggleToolbar" class="toggle-btn">
          {{ showDebugToolbar ? 'Hide Debug' : 'Show Debug' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DiceDebugToolbar',

  props: {
    diceCanvas: {
      type: Object,
      default: null
    },
    visible: {
      type: Boolean,
      default: true
    }
  },

  emits: ['roll-started', 'roll-completed', 'visibility-changed'],

  data() {
    return {
      targetNumber: 20,
      isRolling: false,
      lastResult: null,
      showDebugToolbar: this.visible,
      quickTargets: [1, 5, 10, 15, 20] // Common test targets
    }
  },

  computed: {
    isValidTarget() {
      return this.targetNumber >= 1 && this.targetNumber <= 20 && Number.isInteger(this.targetNumber)
    }
  },

  watch: {
    visible(newVal) {
      this.showDebugToolbar = newVal
    },

    showDebugToolbar(newVal) {
      this.$emit('visibility-changed', newVal)
    }
  },

  methods: {
    async rollToTarget() {
      if (!this.diceCanvas || !this.isValidTarget || this.isRolling) {
        return
      }

      this.isRolling = true
      this.$emit('roll-started', { target: this.targetNumber, type: 'deterministic' })

      try {
        const result = await this.diceCanvas.rollToTarget(this.targetNumber)
        if (result) {
          this.lastResult = {
            ...result,
            isDeterministic: true
          }
          this.$emit('roll-completed', this.lastResult)
        }
      } catch (error) {
        console.error('Debug roll failed:', error)
      } finally {
        this.isRolling = false
      }
    },

    async rollRandom() {
      if (!this.diceCanvas || this.isRolling) {
        return
      }

      this.isRolling = true
      this.$emit('roll-started', { type: 'random' })

      try {
        const result = await this.diceCanvas.rollRandom()
        if (result) {
          this.lastResult = {
            ...result,
            isDeterministic: false
          }
          this.$emit('roll-completed', this.lastResult)
        }
      } catch (error) {
        console.error('Debug random roll failed:', error)
      } finally {
        this.isRolling = false
      }
    },

    async setAndRoll(targetNum) {
      this.targetNumber = targetNum
      await this.$nextTick() // Wait for reactivity
      await this.rollToTarget()
    },

    toggleToolbar() {
      this.showDebugToolbar = !this.showDebugToolbar
    },

    getResultClass(number) {
      if (number === 1) return 'critical-fail'
      if (number === 20) return 'critical-success'
      if (number >= 15) return 'high-roll'
      if (number <= 5) return 'low-roll'
      return 'normal-roll'
    }
  }
}
</script>

<style scoped>
.dice-debug-toolbar {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  font-family: 'Courier New', monospace;
}

.debug-panel {
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid #00ffff;
  border-radius: 8px;
  padding: 16px;
  min-width: 280px;
  box-shadow: 0 4px 20px rgba(0, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.debug-title {
  color: #00ffff;
  margin: 0 0 16px 0;
  font-size: 16px;
  text-align: center;
  text-shadow: 0 0 10px #00ffff;
}

.debug-controls {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.target-input-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.input-label {
  color: #ffffff;
  font-size: 14px;
  min-width: 80px;
}

.target-input {
  flex: 1;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid #00ffff;
  border-radius: 4px;
  color: #ffffff;
  font-size: 16px;
  text-align: center;
  transition: all 0.3s ease;
}

.target-input:focus {
  outline: none;
  border-color: #ffff00;
  box-shadow: 0 0 10px rgba(255, 255, 0, 0.5);
}

.target-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.roll-button, .random-button {
  padding: 10px 16px;
  background: linear-gradient(45deg, #00ffff, #0080ff);
  border: none;
  border-radius: 4px;
  color: #000000;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
}

.roll-button:hover, .random-button:hover {
  background: linear-gradient(45deg, #ffff00, #ff8000);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 255, 0, 0.4);
}

.roll-button:disabled, .random-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.roll-button.rolling, .random-button.rolling {
  background: linear-gradient(45deg, #ff6600, #ff0066);
  animation: pulse 1s infinite;
}

.quick-targets {
  border-top: 1px solid #333;
  padding-top: 12px;
  margin-bottom: 16px;
}

.quick-label {
  color: #ffffff;
  font-size: 12px;
  display: block;
  margin-bottom: 8px;
}

.target-buttons {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.quick-target-btn {
  padding: 6px 12px;
  background: rgba(0, 255, 255, 0.2);
  border: 1px solid #00ffff;
  border-radius: 4px;
  color: #00ffff;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 40px;
}

.quick-target-btn:hover {
  background: rgba(0, 255, 255, 0.4);
  transform: scale(1.1);
}

.quick-target-btn.active {
  background: #00ffff;
  color: #000000;
  font-weight: bold;
}

.quick-target-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  transform: none;
}

.debug-info {
  border-top: 1px solid #333;
  padding-top: 12px;
  margin-bottom: 16px;
}

.result-display {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
}

.result-label {
  color: #ffffff;
  font-size: 12px;
}

.result-value {
  font-size: 24px;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 4px;
  min-width: 40px;
  text-align: center;
}

.result-value.critical-fail {
  color: #ff0000;
  background: rgba(255, 0, 0, 0.2);
  text-shadow: 0 0 10px #ff0000;
}

.result-value.critical-success {
  color: #ffff00;
  background: rgba(255, 255, 0, 0.2);
  text-shadow: 0 0 10px #ffff00;
}

.result-value.high-roll {
  color: #00ff00;
  background: rgba(0, 255, 0, 0.2);
}

.result-value.low-roll {
  color: #ff8000;
  background: rgba(255, 128, 0, 0.2);
}

.result-value.normal-roll {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.2);
}

.result-type {
  color: #888;
  font-size: 10px;
  font-style: italic;
}

.toolbar-toggle {
  border-top: 1px solid #333;
  padding-top: 12px;
  text-align: center;
}

.toggle-btn {
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid #666;
  border-radius: 4px;
  color: #ffffff;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: #999;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

/* Responsive design */
@media (max-width: 768px) {
  .dice-debug-toolbar {
    top: 10px;
    right: 10px;
    left: 10px;
  }

  .debug-panel {
    min-width: auto;
    padding: 12px;
  }

  .target-buttons {
    justify-content: center;
  }
}
</style>