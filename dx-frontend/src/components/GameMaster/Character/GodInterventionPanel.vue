<template>
  <div class="god-intervention-panel">
    <!-- Horizontal panel with buttons and loading indicator inline -->
    <div class="intervention-controls">
      <div class="panel-label">God Powers:</div>

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

      <!-- Inline loading indicator -->
      <div v-if="isLoading" class="loading-indicator">
        <span class="loading-spinner"></span>
      </div>
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
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-top: 1px solid rgba(30, 144, 255, 0.2);
  margin-top: 0.25rem;
}

.intervention-controls {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 0.5rem;
}

.panel-label {
  font-size: 0.7rem;
  color: #aaa;
  margin-right: 0.25rem;
}

.intervention-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(30, 30, 30, 0.6);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.intervention-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.2);
}

.intervention-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.kill-button {
  background: rgba(60, 20, 20, 0.8);
  border-color: rgba(180, 0, 0, 0.3);
}

.kill-button:hover {
  background: rgba(80, 20, 20, 0.9);
  border-color: rgba(220, 0, 0, 0.4);
}

.heal-button {
  background: rgba(20, 60, 20, 0.8);
  border-color: rgba(0, 150, 0, 0.3);
}

.heal-button:hover {
  background: rgba(20, 80, 20, 0.9);
  border-color: rgba(0, 180, 0, 0.4);
}

.custom-button {
  background: rgba(20, 40, 80, 0.8);
  border-color: rgba(30, 144, 255, 0.3);
}

.custom-button:hover {
  background: rgba(30, 50, 100, 0.9);
  border-color: rgba(30, 144, 255, 0.4);
}

.intervention-icon {
  font-size: 0.9rem;
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.1);
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
  padding: 0.2rem;
  border-radius: 3px;
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.8);
}

.message.success {
  background: rgba(0, 150, 0, 0.1);
  border-left: 2px solid #4CAF50;
}

.message.error {
  background: rgba(180, 0, 0, 0.1);
  border-left: 2px solid #f44336;
}

/* Custom Dialog */
.custom-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.custom-dialog {
  background: rgba(30, 30, 30, 0.95);
  border: 1px solid #555;
  border-radius: 8px;
  padding: 0.75rem;
  width: 280px;
  max-width: 90vw;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.7);
}

.custom-dialog h3 {
  margin-top: 0;
  margin-bottom: 0.75rem;
  color: #1E90FF;
  text-align: center;
  font-size: 1rem;
  border-bottom: 1px solid rgba(30, 144, 255, 0.2);
  padding-bottom: 0.5rem;
}

.form-group {
  margin-bottom: 0.75rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.25rem;
  color: #aaa;
  font-weight: 500;
  font-size: 0.8rem;
}

.radio-group, .checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  background: rgba(20, 20, 20, 0.5);
  border-radius: 4px;
  padding: 0.4rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.radio-group label, .checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-weight: normal;
  cursor: pointer;
  font-size: 0.8rem;
  color: #ddd;
}

select {
  width: 100%;
  padding: 0.4rem;
  background: rgba(20, 20, 20, 0.5);
  color: #ddd;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  appearance: none;
  cursor: pointer;
  font-size: 0.8rem;
}

select:focus {
  border-color: rgba(30, 144, 255, 0.5);
  outline: none;
}

.dialog-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  gap: 0.5rem;
}

.apply-button, .cancel-button {
  flex: 1;
  padding: 0.4rem 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.8rem;
}

.apply-button {
  background: rgba(30, 144, 255, 0.2);
  color: #1E90FF;
  border-color: rgba(30, 144, 255, 0.3);
}

.apply-button:hover {
  background: rgba(30, 144, 255, 0.3);
  border-color: rgba(30, 144, 255, 0.5);
}

.apply-button:disabled {
  background: rgba(50, 50, 50, 0.3);
  color: #888;
  border-color: rgba(255, 255, 255, 0.1);
  cursor: not-allowed;
}

.cancel-button {
  background: rgba(50, 50, 50, 0.3);
  color: #ccc;
}

.cancel-button:hover {
  background: rgba(80, 80, 80, 0.4);
  border-color: rgba(255, 255, 255, 0.2);
}
</style>
