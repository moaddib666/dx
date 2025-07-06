<template>
  <div class="dice-result-display" @click="handleClick">
    <div class="result-content">
      <div class="result-number" :class="resultClass">
        {{ result.number }}
      </div>
      
      <div class="result-text">
        You rolled {{ result.number }}!
      </div>
      
      <div v-if="result.isDeterministic" class="result-type">
        Deterministic Roll
      </div>
      <div v-else class="result-type">
        Random Roll
      </div>
      
      <div class="result-details">
        <span>Roll Time: {{ formatTime(result.rollTime) }}</span>
        <span v-if="result.targetNumber">Target: {{ result.targetNumber }}</span>
      </div>
      
      <button class="close-btn" @click.stop="$emit('close')" aria-label="Close">
        ✕
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DiceResultDisplay',

  props: {
    result: {
      type: Object,
      required: true,
      validator(value) {
        return value && typeof value.number === 'number'
      }
    }
  },

  emits: ['close'],

  computed: {
    resultClass() {
      const number = this.result.number
      if (number === 1) {
        return 'critical-fail'
      } else if (number === 20) {
        return 'critical-success'
      } else if (number >= 15) {
        return 'high-roll'
      } else if (number <= 5) {
        return 'low-roll'
      }
      return 'normal-roll'
    }
  },

  methods: {
    handleClick() {
      // Close when clicking the background
      this.$emit('close')
    },

    formatTime(seconds) {
      return `${seconds.toFixed(1)}s`
    }
  }
}
</script>

<style scoped>
.dice-result-display {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  background: rgba(0, 0, 0, 0.95);
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  color: #fff;
  font-family: Arial, sans-serif;
  backdrop-filter: blur(15px);
  border: 2px solid #ff0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
  cursor: pointer;
  animation: slideUp 0.5s ease-out;
  min-width: 280px;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(100%);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

.result-content {
  position: relative;
}

.result-number {
  font-size: 64px;
  font-weight: bold;
  margin-bottom: 10px;
  text-shadow: 0 0 20px currentColor;
  line-height: 1;
}

.result-number.critical-fail {
  color: #ff0505;
  animation: criticalFailPulse 2s infinite;
}

.result-number.critical-success {
  color: #ffff00;
  animation: criticalSuccessPulse 2s infinite;
}

.result-number.high-roll {
  color: #00ff88;
}

.result-number.low-roll {
  color: #ff8844;
}

.result-number.normal-roll {
  color: #88ddff;
}

@keyframes criticalFailPulse {
  0%, 100% { 
    text-shadow: 0 0 20px #ff0505; 
    transform: scale(1);
  }
  50% { 
    text-shadow: 0 0 40px #ff0505, 0 0 60px #ff0505; 
    transform: scale(1.05);
  }
}

@keyframes criticalSuccessPulse {
  0%, 100% { 
    text-shadow: 0 0 20px #ffff00; 
    transform: scale(1);
  }
  50% { 
    text-shadow: 0 0 40px #ffff00, 0 0 60px #ffff00; 
    transform: scale(1.05);
  }
}

.result-text {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #fff;
}

.result-type {
  font-size: 14px;
  color: #aaa;
  margin-bottom: 15px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.result-details {
  display: flex;
  justify-content: center;
  gap: 20px;
  font-size: 12px;
  color: #ccc;
  margin-bottom: 10px;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: #fff;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

/* Responsive design */
@media (max-width: 768px) {
  .dice-result-display {
    min-width: 250px;
    padding: 15px;
  }

  .result-number {
    font-size: 48px;
  }

  .result-text {
    font-size: 20px;
  }

  .result-details {
    flex-direction: column;
    gap: 5px;
  }
}

@media (max-width: 480px) {
  .dice-result-display {
    min-width: 200px;
    padding: 12px;
    bottom: 20px;
  }

  .result-number {
    font-size: 40px;
  }

  .result-text {
    font-size: 18px;
  }
}

/* Special effects for different outcomes */
.dice-result-display:has(.critical-fail) {
  border-color: #ff0505;
  box-shadow: 0 8px 32px rgba(255, 5, 5, 0.4);
}

.dice-result-display:has(.critical-success) {
  border-color: #ffff00;
  box-shadow: 0 8px 32px rgba(255, 255, 0, 0.4);
}

.dice-result-display:has(.high-roll) {
  border-color: #00ff88;
  box-shadow: 0 8px 32px rgba(0, 255, 136, 0.3);
}

.dice-result-display:has(.low-roll) {
  border-color: #ff8844;
  box-shadow: 0 8px 32px rgba(255, 136, 68, 0.3);
}
</style>