<template>
  <div class="test-container">
    <h2>AttributeBar Component Test</h2>

    <div class="test-controls">
      <div class="control-group">
        <label>Health:</label>
        <button @click="decreaseHealth">-10</button>
        <button @click="increaseHealth">+10</button>
        <span>{{ health }} / {{ maxHealth }}</span>
      </div>

      <div class="control-group">
        <label>Energy:</label>
        <button @click="decreaseEnergy">-5</button>
        <button @click="increaseEnergy">+5</button>
        <span>{{ energy }} / {{ maxEnergy }}</span>
      </div>

      <div class="control-group">
        <label>Action Points:</label>
        <button @click="decreaseActionPoints">-1</button>
        <button @click="increaseActionPoints">+1</button>
        <span>{{ actionPoints }} / {{ maxActionPoints }}</span>
      </div>

      <div class="control-group">
        <label>Show Deltas:</label>
        <input type="checkbox" v-model="showDeltas">
      </div>

      <div class="control-group">
        <label>Compact Mode:</label>
        <input type="checkbox" v-model="compact">
      </div>
    </div>

    <div class="attribute-bars">
      <div class="attribute-container">
        <h3>Health</h3>
        <AttributeBar
          :current="health"
          :max="maxHealth"
          type="Health"
          :showDeltas="showDeltas"
          :compact="compact"
        />
      </div>

      <div class="attribute-container">
        <h3>Energy</h3>
        <AttributeBar
          :current="energy"
          :max="maxEnergy"
          type="Energy"
          :showDeltas="showDeltas"
          :compact="compact"
        />
      </div>

      <div class="attribute-container">
        <h3>Action Points</h3>
        <AttributeBar
          :current="actionPoints"
          :max="maxActionPoints"
          type="Action Points"
          :showDeltas="showDeltas"
          :compact="compact"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import AttributeBar from './AttributeBar.vue';

// Health
const maxHealth = 100;
const health = ref(80);

// Energy
const maxEnergy = 50;
const energy = ref(30);

// Action Points
const maxActionPoints = 5;
const actionPoints = ref(3);

// Controls
const showDeltas = ref(true);
const compact = ref(false);

// Methods
const increaseHealth = () => {
  health.value = Math.min(health.value + 10, maxHealth);
};

const decreaseHealth = () => {
  health.value = Math.max(health.value - 10, 0);
};

const increaseEnergy = () => {
  energy.value = Math.min(energy.value + 5, maxEnergy);
};

const decreaseEnergy = () => {
  energy.value = Math.max(energy.value - 5, 0);
};

const increaseActionPoints = () => {
  actionPoints.value = Math.min(actionPoints.value + 1, maxActionPoints);
};

const decreaseActionPoints = () => {
  actionPoints.value = Math.max(actionPoints.value - 1, 0);
};
</script>

<style scoped>
.test-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: rgba(0, 0, 0, 0.3);
  color: white;
  border-radius: 12px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  border: 1px solid rgba(255, 215, 0, 0.2);
  backdrop-filter: blur(1px);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: var(--cyber-yellow, #ffd700);
  letter-spacing: 0.5px;
}

h3 {
  margin: 10px 0;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.test-controls {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 30px;
  padding: 15px;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.control-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.control-group label {
  min-width: 120px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

button {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 8px;
  padding: 5px 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  font-weight: 600;
}

button:hover {
  background: rgba(255, 215, 0, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
}

.attribute-bars {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.attribute-container {
  background: rgba(0, 0, 0, 0.3);
  padding: 15px;
  border-radius: 8px;
  border: 1px solid rgba(255, 215, 0, 0.2);
}
</style>