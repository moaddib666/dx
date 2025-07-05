<template>
    <main class="app-main">
      <!-- Quick Roll Buttons -->
      <section class="quick-roll-section">
        <h2>Quick Rolls</h2>
        <div class="quick-roll-buttons">
          <button
              v-for="quickRoll in quickRolls"
              :key="quickRoll.name"
              class="quick-roll-btn"
              @click="performQuickRoll(quickRoll)"
          >
            {{ quickRoll.name }}
            <small>{{ quickRoll.description }}</small>
          </button>
        </div>
      </section>

      <!-- Custom Roll Section -->
      <section class="custom-roll-section">
        <h2>Custom Roll</h2>
        <div class="custom-roll-controls">
          <button class="open-dice-modal-btn" @click="openDiceModal">
            🎲 Open Dice Roller
          </button>
          <div v-if="lastRollResults.length > 0" class="last-roll-display">
            <h3>Last Roll Results:</h3>
            <div class="roll-summary">
              <div class="dice-results">
                <span
                    v-for="result in lastRollResults"
                    :key="result.id"
                    class="dice-result"
                    :style="{ backgroundColor: result.color }"
                >
                  {{ result.type.toUpperCase() }}: {{ result.result }}
                </span>
              </div>
              <div class="total-result">
                Total: {{ totalRoll }}
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Battle Simulator -->
      <section class="battle-section">
        <h2>Battle Simulator</h2>
        <div class="battle-controls">
          <div class="character-stats">
            <h3>Character</h3>
            <div class="stat-input">
              <label>Attack Bonus:</label>
              <input v-model.number="character.attackBonus" type="number" min="0" max="20">
            </div>
            <div class="stat-input">
              <label>Damage Dice:</label>
              <select v-model="character.damageDice">
                <option value="d4">1d4</option>
                <option value="d6">1d6</option>
                <option value="d8">1d8</option>
                <option value="d10">1d10</option>
                <option value="d12">1d12</option>
              </select>
            </div>
          </div>
          <div class="enemy-stats">
            <h3>Enemy</h3>
            <div class="stat-input">
              <label>Armor Class:</label>
              <input v-model.number="enemy.armorClass" type="number" min="1" max="30">
            </div>
            <div class="stat-input">
              <label>Hit Points:</label>
              <input v-model.number="enemy.hitPoints" type="number" min="1" max="1000">
            </div>
          </div>
          <button class="attack-btn" @click="performAttack">
            ⚔️ Attack!
          </button>
        </div>
        <div v-if="battleLog.length > 0" class="battle-log">
          <h3>Battle Log:</h3>
          <div class="log-entries">
            <div
                v-for="(entry, index) in battleLog"
                :key="index"
                class="log-entry"
                :class="entry.type"
            >
              {{ entry.message }}
            </div>
          </div>
        </div>
      </section>

      <!-- Dice Collection -->
      <section class="dice-collection-section">
        <h2>Your Dice Collection</h2>
        <div class="dice-collection">
          <div
              v-for="diceType in diceTypes"
              :key="diceType.type"
              class="dice-card"
              :style="{ borderColor: diceType.color }"
          >
            <div class="dice-icon" :style="{ backgroundColor: diceType.color }">
              {{ diceType.type.toUpperCase() }}
            </div>
            <div class="dice-info">
              <h4>{{ diceType.type.toUpperCase() }}</h4>
              <p>{{ diceType.sides }} sides</p>
              <p class="dice-description">{{ getDiceDescription(diceType.type) }}</p>
            </div>
            <div class="dice-stats">
              <small>Rolled: {{ diceStats[diceType.type]?.rolls || 0 }} times</small>
              <small>Avg: {{ getDiceAverage(diceType.type) }}</small>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Dice Rolling Modal -->
    <DiceRollingModal
        :isOpen="isDiceModalOpen"
        :predefinedResults="predefinedResults"
        @close="closeDiceModal"
        @roll-complete="handleRollComplete"
    />
</template>

<script>
import { ref, computed, reactive } from 'vue'
import DiceRollingModal from '@/components/DiceRoller/DiceRollingModal.vue'

export default {
  name: 'App',
  components: {
    DiceRollingModal
  },
  setup() {
    const isDiceModalOpen = ref(false)
    const predefinedResults = ref(null)
    const lastRollResults = ref([])
    const battleLog = ref([])

    const diceTypes = [
      { type: 'd4', sides: 4, color: '#ff6b6b' },
      { type: 'd6', sides: 6, color: '#4ecdc4' },
      { type: 'd8', sides: 8, color: '#45b7d1' },
      { type: 'd10', sides: 10, color: '#96ceb4' },
      { type: 'd12', sides: 12, color: '#feca57' },
      { type: 'd20', sides: 20, color: '#ff9ff3' },
      { type: 'd100', sides: 100, color: '#a8e6cf' }
    ]

    const quickRolls = [
      {
        name: 'D20 Attack',
        description: 'Standard attack roll',
        dice: ['d20']
      },
      {
        name: 'Ability Check',
        description: 'D20 + modifier',
        dice: ['d20']
      },
      {
        name: 'Damage Roll',
        description: '1d8 + 1d6',
        dice: ['d8', 'd6']
      },
      {
        name: 'Stats Roll',
        description: '4d6 drop lowest',
        dice: ['d6', 'd6', 'd6', 'd6']
      },
      {
        name: 'Fireball',
        description: '8d6 fire damage',
        dice: Array(8).fill('d6')
      },
      {
        name: 'Critical Hit',
        description: '2d20 + 2d8',
        dice: ['d20', 'd20', 'd8', 'd8']
      }
    ]

    const character = reactive({
      attackBonus: 5,
      damageDice: 'd8'
    })

    const enemy = reactive({
      armorClass: 15,
      hitPoints: 30
    })

    const diceStats = reactive({})

    const totalRoll = computed(() => {
      return lastRollResults.value.reduce((sum, result) => sum + result.result, 0)
    })

    const openDiceModal = () => {
      predefinedResults.value = null
      isDiceModalOpen.value = true
    }

    const closeDiceModal = () => {
      isDiceModalOpen.value = false
    }

    const handleRollComplete = (results) => {
      lastRollResults.value = results

      // Update dice statistics
      results.forEach(result => {
        if (!diceStats[result.type]) {
          diceStats[result.type] = { rolls: 0, total: 0 }
        }
        diceStats[result.type].rolls++
        diceStats[result.type].total += result.result
      })

      console.log('Roll completed:', results)
    }

    const performQuickRoll = (quickRoll) => {
      // Simulate quick roll with random results
      const results = quickRoll.dice.map((diceType, index) => {
        const die = diceTypes.find(d => d.type === diceType)
        const result = Math.floor(Math.random() * die.sides) + 1

        return {
          id: Date.now() + index,
          ...die,
          result
        }
      })

      lastRollResults.value = results

      // Update stats
      results.forEach(result => {
        if (!diceStats[result.type]) {
          diceStats[result.type] = { rolls: 0, total: 0 }
        }
        diceStats[result.type].rolls++
        diceStats[result.type].total += result.result
      })

      // Add to battle log
      const total = results.reduce((sum, r) => sum + r.result, 0)
      battleLog.value.unshift({
        type: 'info',
        message: `${quickRoll.name}: ${results.map(r => r.result).join(' + ')} = ${total}`
      })
    }

    const performAttack = () => {
      // Roll d20 for attack
      const attackRoll = Math.floor(Math.random() * 20) + 1
      const totalAttack = attackRoll + character.attackBonus

      let message = `Attack Roll: ${attackRoll} + ${character.attackBonus} = ${totalAttack}`

      if (attackRoll === 20) {
        message += ' (CRITICAL HIT!)'
        battleLog.value.unshift({
          type: 'critical',
          message
        })

        // Roll damage (doubled for critical)
        const damageRoll1 = Math.floor(Math.random() * parseInt(character.damageDice.slice(1))) + 1
        const damageRoll2 = Math.floor(Math.random() * parseInt(character.damageDice.slice(1))) + 1
        const totalDamage = damageRoll1 + damageRoll2

        enemy.hitPoints = Math.max(0, enemy.hitPoints - totalDamage)

        battleLog.value.unshift({
          type: 'damage',
          message: `Critical Damage: ${damageRoll1} + ${damageRoll2} = ${totalDamage} damage! Enemy HP: ${enemy.hitPoints}`
        })
      } else if (attackRoll === 1) {
        message += ' (CRITICAL MISS!)'
        battleLog.value.unshift({
          type: 'miss',
          message
        })
      } else if (totalAttack >= enemy.armorClass) {
        battleLog.value.unshift({
          type: 'hit',
          message: message + ' - HIT!'
        })

        // Roll damage
        const damageRoll = Math.floor(Math.random() * parseInt(character.damageDice.slice(1))) + 1
        enemy.hitPoints = Math.max(0, enemy.hitPoints - damageRoll)

        battleLog.value.unshift({
          type: 'damage',
          message: `Damage: ${damageRoll}! Enemy HP: ${enemy.hitPoints}`
        })
      } else {
        battleLog.value.unshift({
          type: 'miss',
          message: message + ' - MISS!'
        })
      }

      if (enemy.hitPoints === 0) {
        battleLog.value.unshift({
          type: 'victory',
          message: '🎉 Enemy defeated!'
        })
      }

      // Keep log manageable
      if (battleLog.value.length > 20) {
        battleLog.value = battleLog.value.slice(0, 20)
      }
    }

    const getDiceDescription = (diceType) => {
      const descriptions = {
        'd4': 'Damage, small weapons',
        'd6': 'Versatile, common rolls',
        'd8': 'Longsword, moderate spells',
        'd10': 'Heavy weapons, percentile',
        'd12': 'Greataxe, powerful spells',
        'd20': 'Attacks, saves, checks',
        'd100': 'Percentile, random tables'
      }
      return descriptions[diceType] || 'Special purpose'
    }

    const getDiceAverage = (diceType) => {
      const stats = diceStats[diceType]
      if (!stats || stats.rolls === 0) return '0.0'
      return (stats.total / stats.rolls).toFixed(1)
    }

    return {
      isDiceModalOpen,
      predefinedResults,
      lastRollResults,
      diceTypes,
      quickRolls,
      character,
      enemy,
      battleLog,
      diceStats,
      totalRoll,
      openDiceModal,
      closeDiceModal,
      handleRollComplete,
      performQuickRoll,
      performAttack,
      getDiceDescription,
      getDiceAverage
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
  color: #ffffff;
  min-height: 100vh;
}

#app {
  min-height: 100vh;
}

.app-header {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.app-header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-header p {
  font-size: 1.2em;
  opacity: 0.8;
}

.app-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

section h2 {
  font-size: 1.8em;
  margin-bottom: 20px;
  color: #ffffff;
}

.quick-roll-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.quick-roll-btn {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.quick-roll-btn:hover {
  transform: translateY(-2px);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08));
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.quick-roll-btn small {
  opacity: 0.7;
  font-size: 0.9em;
}

.custom-roll-controls {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.open-dice-modal-btn {
  background: linear-gradient(135deg, #4ade80, #22c55e);
  border: none;
  color: white;
  padding: 20px 40px;
  border-radius: 12px;
  font-size: 1.2em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: flex-start;
}

.open-dice-modal-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(74, 222, 128, 0.3);
}

.last-roll-display {
  background: rgba(255, 255, 255, 0.05);
  padding: 20px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.dice-results {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
}

.dice-result {
  padding: 8px 12px;
  border-radius: 20px;
  color: white;
  font-weight: 500;
  font-size: 0.9em;
}

.total-result {
  font-size: 1.5em;
  font-weight: bold;
  color: #ffd700;
}

.battle-controls {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 30px;
  align-items: start;
}

.character-stats,
.enemy-stats {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.character-stats h3,
.enemy-stats h3 {
  color: #ffffff;
  margin-bottom: 10px;
}

.stat-input {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.stat-input label {
  font-size: 0.9em;
  opacity: 0.8;
}

.stat-input input,
.stat-input select {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 10px;
  border-radius: 6px;
}

.attack-btn {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border: none;
  color: white;
  padding: 20px 30px;
  border-radius: 12px;
  font-size: 1.1em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  height: fit-content;
}

.attack-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(239, 68, 68, 0.3);
}

.battle-log {
  margin-top: 20px;
}

.log-entries {
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.log-entry {
  padding: 10px;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.log-entry.info {
  background: rgba(59, 130, 246, 0.2);
  border-left: 3px solid #3b82f6;
}

.log-entry.hit {
  background: rgba(34, 197, 94, 0.2);
  border-left: 3px solid #22c55e;
}

.log-entry.miss {
  background: rgba(156, 163, 175, 0.2);
  border-left: 3px solid #9ca3af;
}

.log-entry.critical {
  background: rgba(255, 215, 0, 0.2);
  border-left: 3px solid #ffd700;
}

.log-entry.damage {
  background: rgba(239, 68, 68, 0.2);
  border-left: 3px solid #ef4444;
}

.log-entry.victory {
  background: rgba(168, 85, 247, 0.2);
  border-left: 3px solid #a855f7;
  font-weight: bold;
}

.dice-collection {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.dice-card {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
}

.dice-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.08);
}

.dice-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.1em;
}

.dice-info {
  text-align: center;
}

.dice-info h4 {
  font-size: 1.2em;
  margin-bottom: 5px;
}

.dice-info p {
  margin-bottom: 5px;
  opacity: 0.8;
}

.dice-description {
  font-size: 0.9em;
  opacity: 0.6;
}

.dice-stats {
  display: flex;
  flex-direction: column;
  gap: 5px;
  text-align: center;
}

.dice-stats small {
  opacity: 0.7;
  font-size: 0.8em;
}

@media (max-width: 768px) {
  .app-header h1 {
    font-size: 2em;
  }

  .app-main {
    padding: 20px 15px;
  }

  .battle-controls {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .dice-collection {
    grid-template-columns: 1fr;
  }

  .quick-roll-buttons {
    grid-template-columns: 1fr;
  }
}
</style>