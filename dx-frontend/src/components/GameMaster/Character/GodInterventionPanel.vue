<template>
  <div class="god-intervention-panel">
    <div class="intervention-buttons">
      <!-- Instant Kill Button -->
      <button
          :disabled="isLoading"
          class="intervention-button kill-button"
          title="Instant Kill"
          @click="handleInstantKill"
      >
        <span class="intervention-icon">💀</span>
      </button>

      <!-- Instant Heal Button -->
      <button
          :disabled="isLoading"
          class="intervention-button heal-button"
          title="Instant Heal"
          @click="handleInstantHeal"
      >
        <span class="intervention-icon">❤️</span>
      </button>

      <!-- Custom Intervention Button -->
      <button
          :disabled="isLoading"
          class="intervention-button custom-button"
          title="Custom Intervention"
          @click="showCustomDialog = true"
      >
        <span class="intervention-icon">⚡</span>
      </button>
    </div>

    <!-- Loading indicator -->
    <div v-if="isLoading" class="loading-indicator">
      <span class="loading-spinner"></span>
    </div>

    <!-- Success/Error message -->
    <div v-if="message" :class="['message', messageType]">
      {{ message }}
    </div>

    <!-- Custom Intervention Dialog -->
    <div v-if="showCustomDialog" class="custom-dialog-overlay" @click.self="showCustomDialog = false">
      <div class="custom-dialog">
        <h3>Custom God Intervention</h3>

        <div class="form-group">
          <label>Type:</label>
          <div class="radio-group">
            <label>
              <input
                  v-model="customIntervention.type"
                  :value="GodInterventionType.BLESSING"
                  type="radio"
              >
              Blessing
            </label>
            <label>
              <input
                  v-model="customIntervention.type"
                  :value="GodInterventionType.CURSE"
                  type="radio"
              >
              Curse
            </label>
          </div>
        </div>

        <div class="form-group">
          <label>Size:</label>
          <select v-model="customIntervention.size">
            <option :value="GodInterventionSize.SMALL">Small</option>
            <option :value="GodInterventionSize.MEDIUM">Medium</option>
            <option :value="GodInterventionSize.LARGE">Large</option>
            <option :value="GodInterventionSize.GOD">God</option>
          </select>
        </div>

        <div class="form-group">
          <label>Attributes:</label>
          <div class="checkbox-group">
            <label>
              <input
                  v-model="selectedAttributes"
                  :value="GodInterventionAttribute.HEALTH"
                  type="checkbox"
              >
              Health
            </label>
            <label>
              <input
                  v-model="selectedAttributes"
                  :value="GodInterventionAttribute.ENERGY"
                  type="checkbox"
              >
              Energy
            </label>
            <label>
              <input
                  v-model="selectedAttributes"
                  :value="GodInterventionAttribute.ACTION_POINTS"
                  type="checkbox"
              >
              Action Points
            </label>
          </div>
        </div>

        <div class="dialog-buttons">
          <button
              :disabled="!isCustomInterventionValid || isLoading"
              class="apply-button"
              @click="handleCustomIntervention"
          >
            Apply
          </button>
          <button class="cancel-button" @click="showCustomDialog = false">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  gameMasterInterventionalService,
  GodInterventionAttribute,
  GodInterventionSize,
  GodInterventionType
} from '@/services/GameMasterInterventionalService.js';
import {gameMasterCharacterService} from '@/services/GameMasterCharacterService.js';

export default {
  name: 'GodInterventionPanel',
  props: {
    characterId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      isLoading: false,
      message: '',
      messageType: 'success',
      showCustomDialog: false,
      GodInterventionType,
      GodInterventionSize,
      GodInterventionAttribute,
      customIntervention: {
        type: GodInterventionType.BLESSING,
        size: GodInterventionSize.MEDIUM
      },
      selectedAttributes: [GodInterventionAttribute.HEALTH]
    };
  },
  computed: {
    isCustomInterventionValid() {
      return this.selectedAttributes.length > 0;
    }
  },
  created() {
    // Set up event listeners
    gameMasterInterventionalService.on('loadingStarted', this.onLoadingStarted);
    gameMasterInterventionalService.on('loadingFinished', this.onLoadingFinished);
    gameMasterInterventionalService.on('interventionSuccess', this.onInterventionSuccess);
    gameMasterInterventionalService.on('interventionFailed', this.onInterventionFailed);
  },
  beforeUnmount() {
    // Clean up event listeners
    gameMasterInterventionalService.off('loadingStarted', this.onLoadingStarted);
    gameMasterInterventionalService.off('loadingFinished', this.onLoadingFinished);
    gameMasterInterventionalService.off('interventionSuccess', this.onInterventionSuccess);
    gameMasterInterventionalService.off('interventionFailed', this.onInterventionFailed);
  },
  methods: {
    // Event handlers
    onLoadingStarted(characterId) {
      if (characterId === this.characterId) {
        this.isLoading = true;
      }
    },

    onLoadingFinished(characterId) {
      if (characterId === this.characterId) {
        this.isLoading = false;
      }
    },

    onInterventionSuccess({characterId, type}) {
      if (characterId === this.characterId) {
        this.showMessage(`${this.getInterventionTypeName(type)} applied successfully!`, 'success');
        this.showCustomDialog = false;

        // Refresh character data
        gameMasterCharacterService.refreshCharacter(this.characterId);
      }
    },

    onInterventionFailed({characterId, type, error}) {
      if (characterId === this.characterId) {
        this.showMessage(`Failed to apply ${this.getInterventionTypeName(type)}: ${error.message || 'Unknown error'}`, 'error');
      }
    },

    // Action handlers
    async handleInstantKill() {
      try {
        await gameMasterInterventionalService.instantKill(this.characterId);
      } catch (error) {
        // Error is already handled by event listener
      }
    },

    async handleInstantHeal() {
      try {
        await gameMasterInterventionalService.instantHeal(this.characterId);
      } catch (error) {
        // Error is already handled by event listener
      }
    },

    async handleCustomIntervention() {
      try {
        const interventionDetails = {
          type: this.customIntervention.type,
          size: this.customIntervention.size,
          attributes: this.selectedAttributes
        };

        await gameMasterInterventionalService.customIntervention(this.characterId, interventionDetails);
      } catch (error) {
        // Error is already handled by event listener
      }
    },

    // Helper methods
    showMessage(message, type = 'success') {
      this.message = message;
      this.messageType = type;

      // Clear message after 3 seconds
      setTimeout(() => {
        this.message = '';
      }, 3000);
    },

    getInterventionTypeName(type) {
      const typeNames = {
        'kill': 'Instant Kill',
        'heal': 'Instant Heal',
        'custom': 'Custom Intervention'
      };

      return typeNames[type] || 'Intervention';
    }
  }
};
</script>

<style scoped>
.god-intervention-panel {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.intervention-buttons {
  display: flex;
  justify-content: space-around;
  gap: 0.5rem;
}

.intervention-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(30, 30, 30, 0.8);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.intervention-button:hover {
  transform: scale(1.1);
}

.intervention-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.kill-button {
  background: rgba(180, 0, 0, 0.8);
}

.kill-button:hover {
  background: rgba(220, 0, 0, 0.9);
}

.heal-button {
  background: rgba(0, 150, 0, 0.8);
}

.heal-button:hover {
  background: rgba(0, 180, 0, 0.9);
}

.custom-button {
  background: rgba(100, 100, 200, 0.8);
}

.custom-button:hover {
  background: rgba(120, 120, 220, 0.9);
}

.intervention-icon {
  font-size: 1.2rem;
}

.loading-indicator {
  display: flex;
  justify-content: center;
  margin-top: 0.5rem;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #1E90FF;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.message {
  text-align: center;
  padding: 0.3rem;
  border-radius: 4px;
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

.message.success {
  background: rgba(0, 150, 0, 0.2);
  color: #4CAF50;
}

.message.error {
  background: rgba(180, 0, 0, 0.2);
  color: #f44336;
}

/* Custom Dialog */
.custom-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.custom-dialog {
  background: #2d2d2d;
  border-radius: 8px;
  padding: 1rem;
  width: 300px;
  max-width: 90vw;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.custom-dialog h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #1E90FF;
  text-align: center;
  font-size: 1.2rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.3rem;
  color: #ccc;
  font-weight: 500;
}

.radio-group, .checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.radio-group label, .checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: normal;
  cursor: pointer;
}

select {
  width: 100%;
  padding: 0.5rem;
  background: #3d3d3d;
  color: white;
  border: 1px solid #555;
  border-radius: 4px;
  appearance: none;
  cursor: pointer;
}

.dialog-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.apply-button, .cancel-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.apply-button {
  background: #1E90FF;
  color: white;
}

.apply-button:hover {
  background: #1a7fd1;
}

.apply-button:disabled {
  background: #555;
  cursor: not-allowed;
}

.cancel-button {
  background: #555;
  color: white;
}

.cancel-button:hover {
  background: #666;
}
</style>