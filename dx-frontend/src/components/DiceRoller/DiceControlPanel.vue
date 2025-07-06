<template>
  <div class="dice-control-panel">
    <!-- Dice Count Selection -->
    <div class="input-group">
      <label><strong>Dice Count:</strong></label>
      <select v-model.number="diceCount" class="select-input">
        <option value="1">1 Die</option>
        <option value="2">2 Dice</option>
      </select>
    </div>

    <!-- Result Calculation (only show for 2 dice) -->
    <div v-if="diceCount === 2" class="input-group">
      <label><strong>Result:</strong></label>
      <select v-model="resultMode" class="select-input">
        <option value="best">Best Roll</option>
        <option value="worst">Worst Roll</option>
        <option value="both">Both Rolls</option>
      </select>
    </div>

    <!-- Target Number Input(s) -->
    <div v-if="diceCount === 1" class="input-group">
      <label><strong>Target Number:</strong></label>
      <input 
        type="number" 
        v-model.number="targetNumber" 
        class="number-input" 
        min="1" 
        max="20" 
      />
    </div>

    <div v-else class="input-group-vertical">
      <label><strong>Target Numbers:</strong></label>
      <div class="dice-targets">
        <div class="dice-target">
          <label>Dice 1:</label>
          <input 
            type="number" 
            v-model.number="dice1Target" 
            class="number-input" 
            min="1" 
            max="20" 
          />
        </div>
        <div class="dice-target">
          <label>Dice 2:</label>
          <input 
            type="number" 
            v-model.number="dice2Target" 
            class="number-input" 
            min="1" 
            max="20" 
          />
        </div>
      </div>
    </div>

    <!-- Main Action Buttons -->
    <div class="action-buttons">
      <button 
        class="roll-btn" 
        @click="rollDice"
        :disabled="isRolling"
      >
        🎲 Roll Dice
      </button>
      
      <button 
        @click="randomRoll"
        :disabled="isRolling"
        class="random-btn"
      >
        🎲 Random Roll
      </button>
    </div>

    <!-- Preset Number Buttons -->
    <div class="preset-buttons">
      <button 
        v-for="number in presetNumbers" 
        :key="number"
        @click="setTargetNumber(number)"
        class="preset-btn"
        :class="{ active: targetNumber === number }"
      >
        {{ number }}
      </button>
    </div>

    <!-- Texture Upload -->
    <div class="input-group">
      <label><strong>Custom Texture:</strong></label>
      <input 
        type="file" 
        @change="handleTextureUpload" 
        accept="image/*"
        ref="textureInput"
        class="file-input"
      />
    </div>

    <!-- Current Number Display -->
    <div class="current-number">
      {{ currentNumber || '' }}
    </div>

    <!-- Divider -->
    <hr class="divider" />

    <!-- Camera Controls -->
    <div class="camera-controls">
      <button @click="resetCamera" class="control-btn">
        Reset Camera
      </button>
      
      <button @click="toggleWireframe" class="control-btn">
        Toggle Wireframe
      </button>
    </div>

    <!-- Status Display -->
    <div class="status-section">
      <strong>Dice Status:</strong>
      <div class="status">{{ status }}</div>
    </div>

    <!-- Camera View Buttons -->
    <div class="camera-views">
      <strong>Camera Views:</strong>
      <div class="view-buttons">
        <button @click="setCameraView('top')" class="view-btn">
          Top View
        </button>
        <button @click="setCameraView('side')" class="view-btn">
          Side View
        </button>
        <button @click="setCameraView('angle')" class="view-btn">
          Angle View
        </button>
      </div>
    </div>

    <!-- Shader Selection -->
    <div class="shader-section">
      <strong>Bloom Effect:</strong>
      <div class="shader-buttons">
        <button 
          @click="setShader('none')"
          class="shader-btn"
          :class="{ active: currentShader === 'none' }"
        >
          Off
        </button>
        <button 
          @click="setShader('bloom')"
          class="shader-btn"
          :class="{ active: currentShader === 'bloom' }"
        >
          On
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DiceControlPanel',

  props: {
    isRolling: {
      type: Boolean,
      default: false
    },
    currentNumber: {
      type: Number,
      default: null
    },
    status: {
      type: String,
      default: 'Ready to roll'
    },
    materialTypes: {
      type: Array,
      default: () => ['plastic', 'metal', 'glass', 'stone']
    },
    shaderTypes: {
      type: Array,
      default: () => ['none', 'bloom', 'fire', 'metallic']
    },
    currentMaterial: {
      type: String,
      default: 'plastic'
    },
    currentShader: {
      type: String,
      default: 'none'
    }
  },

  emits: [
    'roll-dice',
    'random-roll', 
    'reset-camera',
    'toggle-wireframe',
    'camera-view',
    'texture-upload',
    'material-change',
    'shader-change',
    'dice-count-change',
    'result-mode-change'
  ],

  data() {
    return {
      targetNumber: 20,
      dice1Target: 20,
      dice2Target: 20,
      presetNumbers: Array.from({ length: 20 }, (_, i) => i + 1),
      diceCount: 1,
      resultMode: 'best'
    }
  },

  watch: {
    diceCount(newCount) {
      this.$emit('dice-count-change', newCount)
    },
    resultMode(newMode) {
      this.$emit('result-mode-change', newMode)
    }
  },

  methods: {
    rollDice() {
      if (this.diceCount === 1) {
        if (this.targetNumber < 1 || this.targetNumber > 20) {
          alert('Enter 1‑20')
          return
        }
        this.$emit('roll-dice', this.targetNumber)
      } else {
        // Multiple dice - validate all targets and send array
        if (this.dice1Target < 1 || this.dice1Target > 20 || 
            this.dice2Target < 1 || this.dice2Target > 20) {
          alert('Enter 1‑20 for each dice')
          return
        }
        this.$emit('roll-dice', [this.dice1Target, this.dice2Target])
      }
    },

    randomRoll() {
      this.$emit('random-roll')
    },

    setTargetNumber(number) {
      this.targetNumber = number
    },

    handleTextureUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.$emit('texture-upload', file)
      }
    },

    resetCamera() {
      this.$emit('reset-camera')
    },

    toggleWireframe() {
      this.$emit('toggle-wireframe')
    },

    setCameraView(viewType) {
      this.$emit('camera-view', viewType)
    },

    setMaterial(materialType) {
      this.$emit('material-change', materialType)
    },

    setShader(shaderType) {
      this.$emit('shader-change', shaderType)
    },

    formatMaterialName(material) {
      return material.charAt(0).toUpperCase() + material.slice(1)
    },

    formatShaderName(shader) {
      if (shader === 'none') return 'None'
      return shader.charAt(0).toUpperCase() + shader.slice(1)
    }
  }
}
</script>

<style scoped>
.dice-control-panel {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 100;
  background: rgba(0, 0, 0, 0.8);
  padding: 15px;
  border-radius: 5px;
  color: #fff;
  font-family: Arial, sans-serif;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  min-width: 250px;
}

.input-group {
  margin: 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.input-group label {
  color: #00ffff;
  font-size: 14px;
  min-width: 120px;
}

.input-group-vertical {
  margin: 10px 0;
}

.input-group-vertical > label {
  color: #00ffff;
  font-size: 14px;
  display: block;
  margin-bottom: 8px;
}

.dice-targets {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.dice-target {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dice-target label {
  color: #fff;
  font-size: 12px;
  min-width: 50px;
}

.number-input {
  background: #333;
  color: #fff;
  border: 2px solid #666;
  padding: 8px;
  border-radius: 5px;
  font-size: 18px;
  width: 60px;
  text-align: center;
}

.number-input:focus {
  outline: none;
  border-color: #ff6600;
}

.select-input {
  background: #333;
  color: #fff;
  border: 2px solid #666;
  padding: 8px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  flex: 1;
  min-width: 120px;
}

.select-input:focus {
  outline: none;
  border-color: #ff6600;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin: 15px 0;
  flex-wrap: wrap;
}

.roll-btn, .random-btn {
  background: #ff6600;
  color: #fff;
  border: none;
  padding: 15px 25px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  transition: all 0.3s ease;
  flex: 1;
  min-width: 120px;
}

.roll-btn:hover:not(:disabled), 
.random-btn:hover:not(:disabled) {
  background: #ff8833;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.roll-btn:disabled, 
.random-btn:disabled {
  background: #333;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.random-btn {
  background: #0066cc;
}

.random-btn:hover:not(:disabled) {
  background: #0088ff;
}

.preset-buttons {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 5px;
  margin: 10px 0;
}

.preset-btn {
  padding: 8px;
  font-size: 14px;
  background: #555;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-btn:hover {
  background: #777;
}

.preset-btn.active {
  background: #00ffff;
  color: #000;
}

.file-input {
  background: #333;
  color: #fff;
  border: 1px solid #666;
  padding: 5px;
  border-radius: 3px;
  font-size: 12px;
  flex: 1;
}

.current-number {
  font-size: 32px;
  font-weight: bold;
  color: #ff0;
  text-align: center;
  margin: 10px 0;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 0 10px rgba(255, 255, 0, 0.5);
}

.divider {
  border: none;
  border-top: 1px solid #666;
  margin: 15px 0;
}

.camera-controls {
  display: flex;
  gap: 8px;
  margin: 10px 0;
  flex-wrap: wrap;
}

.control-btn {
  background: #444;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  flex: 1;
}

.control-btn:hover {
  background: #666;
}

.status-section {
  margin: 15px 0;
}

.status-section strong {
  color: #00ffff;
  display: block;
  margin-bottom: 5px;
}

.status {
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid #00ffff;
  border-radius: 3px;
  padding: 8px;
  font-size: 14px;
}

.camera-views strong {
  color: #00ffff;
  display: block;
  margin-bottom: 8px;
}

.view-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 5px;
}

.view-btn {
  background: #333;
  color: #fff;
  border: none;
  padding: 8px;
  border-radius: 3px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s ease;
}

.view-btn:hover {
  background: #555;
}

/* Material and Shader sections */
.material-section, .shader-section {
  margin: 15px 0;
}

.material-section strong, .shader-section strong {
  color: #00ffff;
  display: block;
  margin-bottom: 8px;
}

.material-buttons, .shader-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 5px;
}

.material-btn, .shader-btn {
  background: #333;
  color: #fff;
  border: none;
  padding: 8px;
  border-radius: 3px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s ease;
}

.material-btn:hover, .shader-btn:hover {
  background: #555;
}

.material-btn.active {
  background: #ff6600;
  color: #fff;
}

.shader-btn.active {
  background: #0066cc;
  color: #fff;
}

/* Responsive design */
@media (max-width: 768px) {
  .dice-control-panel {
    min-width: 200px;
    padding: 12px;
  }

  .preset-buttons {
    grid-template-columns: repeat(4, 1fr);
  }

  .action-buttons {
    flex-direction: column;
  }

  .camera-controls {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .dice-control-panel {
    position: relative;
    margin-top: 10px;
  }

  .input-group {
    flex-direction: column;
    align-items: flex-start;
  }

  .input-group label {
    min-width: auto;
  }
}
</style>