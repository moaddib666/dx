<template>
  <div class="dice-game">
    <h1>Dimension-X Dice Roller</h1>

    <div class="game-controls">
      <div class="dice-settings">
        <label>
          Number of Dice:
          <select v-model.number="numberOfDice">
            <option v-for="n in 6" :key="n" :value="n">{{ n }}</option>
          </select>
        </label>

        <label>
          Dice Type:
          <select v-model.number="numberOfEdges">
            <option value="4">D4 (Tetrahedron)</option>
            <option value="6">D6 (Cube)</option>
            <option value="8">D8 (Octahedron)</option>
            <option value="10">D10 (Decahedron)</option>
            <option value="12">D12 (Dodecahedron)</option>
            <option value="20">D20 (Icosahedron)</option>
          </select>
        </label>
      </div>

      <div class="target-section" v-if="showTargets">
        <h3>Target Numbers:</h3>
        <div class="targets">
          <input
              v-for="(target, index) in expectedResults"
              :key="index"
              v-model.number="expectedResults[index]"
              type="number"
              :min="1"
              :max="numberOfEdges"
              class="target-input"
          />
        </div>
        <button @click="generateRandomTargets" class="generate-targets">
          Generate Random Targets
        </button>
      </div>

      <!-- Weighted dice controls -->
      <div class="weighted-dice-section">
        <h3>Weighted Dice:</h3>
        <div class="weighted-toggle">
          <label class="toggle-switch">
            <input type="checkbox" v-model="useWeightedDice">
            <span class="toggle-slider"></span>
          </label>
          <span>{{ useWeightedDice ? 'Enabled' : 'Disabled' }}</span>
        </div>

        <div v-if="useWeightedDice" class="forced-results">
          <p>Set the exact results you want the dice to show:</p>
          <div class="targets">
            <input
                v-for="(result, index) in forcedResults"
                :key="index"
                v-model.number="forcedResults[index]"
                type="number"
                :min="1"
                :max="numberOfEdges"
                class="target-input forced-input"
            />
          </div>
          <button @click="generateRandomForced" class="generate-targets forced-button">
            Generate Random Results
          </button>
        </div>
      </div>
    </div>

    <!-- The main dice roller component -->
    <DXDiceRoller
        :numberOfDice="numberOfDice"
        :numberOfEdges="numberOfEdges"
        :expectedResults="expectedResults"
        :forcedResults="useWeightedDice ? forcedResults : []"
        @diceRolled="handleDiceRolled"
    />

    <!-- Results and statistics -->
    <div class="game-stats" v-if="rollHistory.length > 0">
      <h3>Roll History</h3>
      <div class="history">
        <div
            v-for="(roll, index) in rollHistory.slice(-5)"
            :key="index"
            class="roll-entry"
            :class="{ success: roll.isSuccess }"
        >
          <span class="roll-number">Roll {{ rollHistory.length - 5 + index + 1 }}:</span>
          <span class="roll-results">{{ roll.results.join(', ') }}</span>
          <span class="roll-total">({{ roll.total }})</span>
          <span v-if="roll.isSuccess" class="success-indicator">✓</span>
        </div>
      </div>

      <div class="statistics">
        <div class="stat">
          <strong>Total Rolls:</strong> {{ rollHistory.length }}
        </div>
        <div class="stat">
          <strong>Successful Rolls:</strong> {{ successfulRolls }}
        </div>
        <div class="stat">
          <strong>Success Rate:</strong> {{ successRate }}%
        </div>
        <div class="stat">
          <strong>Average Total:</strong> {{ averageTotal }}
        </div>
      </div>
    </div>

    <!-- Battle system integration example -->
    <div class="battle-integration" v-if="showBattleMode">
      <h3>Battle Mode</h3>
      <div class="battle-controls">
        <button @click="rollAttack" :disabled="isInBattle" class="battle-action">
          Roll Attack (2D6 + modifier)
        </button>
        <button @click="rollDefense" :disabled="isInBattle" class="battle-action">
          Roll Defense (1D8 + luck)
        </button>
        <button @click="rollHexModifier" class="battle-action hex-roll">
          Roll Hex Modifier (1D16)
        </button>
      </div>

      <div class="battle-result" v-if="lastBattleRoll">
        <h4>{{ lastBattleRoll.type }} Result:</h4>
        <p>{{ lastBattleRoll.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import DXDiceRoller from '@/components/DiceRoller/NewDiceRoller.vue'

export default {
  name: 'DiceRollerDemo',
  components: {
    DXDiceRoller
  },
  data() {
    return {
      numberOfDice: 2,
      numberOfEdges: 6,
      expectedResults: [3, 4],
      forcedResults: [], // Array to store forced dice results
      useWeightedDice: false, // Flag to enable/disable weighted dice
      rollHistory: [],
      showTargets: true,
      showBattleMode: true,
      isInBattle: false,
      lastBattleRoll: null
    }
  },
  computed: {
    successfulRolls() {
      return this.rollHistory.filter(roll => roll.isSuccess).length
    },
    successRate() {
      if (this.rollHistory.length === 0) return 0
      return Math.round((this.successfulRolls / this.rollHistory.length) * 100)
    },
    averageTotal() {
      if (this.rollHistory.length === 0) return 0
      const sum = this.rollHistory.reduce((acc, roll) => acc + roll.total, 0)
      return Math.round((sum / this.rollHistory.length) * 10) / 10
    }
  },
  watch: {
    numberOfDice(newVal) {
      // Adjust expected results array when number of dice changes
      this.expectedResults = Array(newVal).fill(0).map((_, i) =>
          this.expectedResults[i] || Math.ceil(Math.random() * this.numberOfEdges)
      )

      // Adjust forced results array when number of dice changes
      this.forcedResults = Array(newVal).fill(0).map((_, i) =>
          this.forcedResults[i] || Math.ceil(Math.random() * this.numberOfEdges)
      )
    },
    numberOfEdges() {
      // Ensure forced results are within valid range when dice type changes
      this.forcedResults = this.forcedResults.map(val =>
          Math.min(Math.max(1, val || 1), this.numberOfEdges)
      )
    }
  },
  methods: {
    handleDiceRolled(rollData) {
      console.log('Dice rolled:', rollData)

      // Check if roll matches expected results (for target mode)
      const isSuccess = this.expectedResults.length === 0 ||
          rollData.results.every((result, index) =>
              !this.expectedResults[index] || result === this.expectedResults[index]
          )

      const rollEntry = {
        ...rollData,
        isSuccess,
        timestamp: new Date()
      }

      this.rollHistory.push(rollEntry)

      // Emit event for parent components
      this.$emit('rollComplete', rollEntry)
    },

    generateRandomTargets() {
      this.expectedResults = Array(this.numberOfDice).fill(0).map(() =>
          Math.ceil(Math.random() * this.numberOfEdges)
      )
    },

    generateRandomForced() {
      this.forcedResults = Array(this.numberOfDice).fill(0).map(() =>
          Math.ceil(Math.random() * this.numberOfEdges)
      )
    },

    // Battle system integration examples
    rollAttack() {
      this.isInBattle = true
      this.numberOfDice = 2
      this.numberOfEdges = 6
      this.expectedResults = [] // No specific target

      // Simulate getting results (you would listen to the diceRolled event)
      setTimeout(() => {
        this.lastBattleRoll = {
          type: 'Attack',
          description: 'Attack roll complete. Add your Flow Manipulation modifier to the total.'
        }
        this.isInBattle = false
      }, 3000)
    },

    rollDefense() {
      this.isInBattle = true
      this.numberOfDice = 1
      this.numberOfEdges = 8
      this.expectedResults = []

      setTimeout(() => {
        this.lastBattleRoll = {
          type: 'Defense',
          description: 'Defense roll complete. Add your luck modifier to the result.'
        }
        this.isInBattle = false
      }, 3000)
    },

    rollHexModifier() {
      this.numberOfDice = 1
      this.numberOfEdges = 16
      this.expectedResults = []

      // Hex modifier logic based on Dimension-X rules
      setTimeout(() => {
        const hexResult = Math.ceil(Math.random() * 16)
        let effect = ''

        if (hexResult < 8) {
          effect = 'Negative modifier: Environmental interference reduces effectiveness'
        } else if (hexResult > 8) {
          effect = 'Positive modifier: Environmental boost enhances the action'
        } else {
          effect = 'Neutral: No environmental modifier'
        }

        this.lastBattleRoll = {
          type: 'Hex Modifier',
          description: `Rolled ${hexResult}: ${effect}`
        }
      }, 3000)
    }
  }
}
</script>

<style scoped>
.dice-game {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  background: linear-gradient(135deg, #0a0a0a, #1a1a2e);
  color: #00ffff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
}

h1 {
  text-align: center;
  color: #00ffff;
  text-shadow: 0 0 20px #00ffff;
  margin-bottom: 2rem;
  font-size: 2.5rem;
}

.game-controls {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: rgba(0, 255, 255, 0.1);
  border-radius: 10px;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

.dice-settings {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.dice-settings label {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-weight: bold;
}

.dice-settings select {
  padding: 0.5rem;
  background: #1a1a2e;
  color: #00ffff;
  border: 1px solid #00ffff;
  border-radius: 4px;
}

.target-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.targets {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.target-input {
  width: 60px;
  padding: 0.5rem;
  background: #1a1a2e;
  color: #00ffff;
  border: 1px solid #00ffff;
  border-radius: 4px;
  text-align: center;
}

.generate-targets {
  padding: 0.5rem 1rem;
  background: linear-gradient(45deg, #ff00ff, #00ffff);
  color: #000;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  align-self: flex-start;
}

.weighted-dice-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 0, 255, 0.1);
  border-radius: 10px;
  border: 1px solid rgba(255, 0, 255, 0.3);
}

.weighted-toggle {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #1a1a2e;
  border: 1px solid #00ffff;
  transition: .4s;
  border-radius: 34px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 3px;
  background-color: #00ffff;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: #0f3460;
}

input:checked + .toggle-slider:before {
  transform: translateX(26px);
  background-color: #ff00ff;
}

.forced-results {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 0, 255, 0.05);
  border-radius: 8px;
}

.forced-input {
  border-color: #ff00ff;
  background: rgba(255, 0, 255, 0.1);
}

.forced-button {
  background: linear-gradient(45deg, #ff00ff, #ff6600);
}

.game-stats {
  margin-top: 2rem;
  padding: 1.5rem;
  background: rgba(255, 0, 255, 0.1);
  border-radius: 10px;
  border: 1px solid rgba(255, 0, 255, 0.3);
}

.history {
  margin-bottom: 1rem;
}

.roll-entry {
  display: flex;
  gap: 1rem;
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  align-items: center;
}

.roll-entry.success {
  border-left: 4px solid #00ff00;
  background: rgba(0, 255, 0, 0.1);
}

.success-indicator {
  color: #00ff00;
  font-weight: bold;
  font-size: 1.2rem;
}

.statistics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.stat {
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  text-align: center;
}

.battle-integration {
  margin-top: 2rem;
  padding: 1.5rem;
  background: rgba(255, 100, 0, 0.1);
  border-radius: 10px;
  border: 1px solid rgba(255, 100, 0, 0.3);
}

.battle-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.battle-action {
  padding: 0.75rem 1rem;
  background: linear-gradient(45deg, #ff6600, #ffaa00);
  color: #000;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.hex-roll {
  background: linear-gradient(45deg, #ff0066, #6600ff) !important;
}

.battle-action:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 100, 0, 0.4);
}

.battle-action:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.battle-result {
  padding: 1rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  border-left: 4px solid #ff6600;
}

@media (max-width: 768px) {
  .game-controls {
    grid-template-columns: 1fr;
  }

  .battle-controls {
    flex-direction: column;
  }

  .statistics {
    grid-template-columns: 1fr;
  }
}
</style>