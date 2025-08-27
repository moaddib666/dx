<script setup lang="ts">
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import {ref, computed} from "vue";
import {GameMasterCreateChallengeRequest, IdEa2Enum} from "@/api/dx-backend";
import {GameMasterApi} from "@/api/backendService";

interface Props {
  selectedCharacterId: string;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  close: [];
  challengeCreated: [challengeId: string];
}>();

// Form state
const difficulty = ref<number>(10);
const diceSides = ref<number>(20);
const selectedStat = ref<IdEa2Enum | ''>('');
const advantage = ref<boolean>(false);
const disadvantage = ref<boolean>(false);
const description = ref<string>('');
const isLoading = ref<boolean>(false);
const error = ref<string>('');

// Available stats from the enum
const availableStats = computed(() => [
  {value: IdEa2Enum.PhysicalStrength, label: 'Physical Strength'},
  {value: IdEa2Enum.MentalStrength, label: 'Mental Strength'},
  {value: IdEa2Enum.FlowResonance, label: 'Flow Resonance'},
  {value: IdEa2Enum.Concentration, label: 'Concentration'},
  {value: IdEa2Enum.FlowManipulation, label: 'Flow Manipulation'},
  {value: IdEa2Enum.FlowConnection, label: 'Flow Connection'},
  {value: IdEa2Enum.Knowledge, label: 'Knowledge'},
  {value: IdEa2Enum.Speed, label: 'Speed'},
  {value: IdEa2Enum.Luck, label: 'Luck'},
  {value: IdEa2Enum.Charisma, label: 'Charisma'}
]);

// Form validation
const isFormValid = computed(() => {
  return props.selectedCharacterId &&
      difficulty.value > 0 &&
      diceSides.value > 0 &&
      selectedStat.value !== '';
});

// Create challenge
const createChallenge = async () => {
  if (!isFormValid.value) {
    error.value = 'Please fill in all required fields';
    return;
  }

  isLoading.value = true;
  error.value = '';

  try {
    const api = GameMasterApi;
    const challengeRequest: GameMasterCreateChallengeRequest = {
      target_character: props.selectedCharacterId,
      difficulty: difficulty.value,
      dice_sides: diceSides.value,
      stat: selectedStat.value as IdEa2Enum,
      advantage: advantage.value,
      disadvantage: disadvantage.value,
      description: description.value || undefined,
      modifiers: [] // Empty list as specified
    };

    const response = await api.gamemasterChallengesCreateCreate(challengeRequest);
    emit('challengeCreated', response.data.id || 'challenge-created');
    resetForm();
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Failed to create challenge';
  } finally {
    isLoading.value = false;
  }
};

// Reset form
const resetForm = () => {
  difficulty.value = 10;
  diceSides.value = 20;
  selectedStat.value = '';
  advantage.value = false;
  disadvantage.value = false;
  description.value = '';
  error.value = '';
};

// Clear error
const clearError = () => {
  error.value = '';
};
</script>

<template>
  <RPGContainer class="dice-challenge-container">
    <div class="header">
      <div class="header-top">
        <h2 class="title">Create Dice Challenge</h2>
        <button @click="emit('close')" class="close-btn" title="Close Challenge Creator">
          ×
        </button>
      </div>
    </div>

    <div class="form-wrapper">
      <form @submit.prevent="createChallenge" class="challenge-form">
        <!-- Error Display -->
        <div v-if="error" class="error-message">
          <span>{{ error }}</span>
          <button type="button" @click="clearError" class="error-close">×</button>
        </div>

        <!-- Target Character Display -->
        <div class="form-group">
          <label class="form-label">Target Character</label>
          <div class="character-display">
            {{ selectedCharacterId.slice(0, 8) }}...
          </div>
        </div>

        <!-- Difficulty -->
        <div class="form-group">
          <label for="difficulty" class="form-label">Difficulty Class (DC) *</label>
          <input
              id="difficulty"
              v-model.number="difficulty"
              type="number"
              min="1"
              max="30"
              class="form-input"
              placeholder="Enter DC (1-30)"
              required
          />
        </div>

        <!-- Dice Sides -->
        <div class="form-group">
          <label for="diceSides" class="form-label">Dice Sides</label>
          <input
              id="diceSides"
              v-model.number="diceSides"
              type="number"
              min="4"
              max="100"
              class="form-input"
              placeholder="Default: 20"
          />
        </div>

        <!-- Stat Selection -->
        <div class="form-group">
          <label for="stat" class="form-label">Character Stat *</label>
          <select
              id="stat"
              v-model="selectedStat"
              class="form-select"
              required
          >
            <option value="">Select a stat...</option>
            <option
                v-for="stat in availableStats"
                :key="stat.value"
                :value="stat.value"
            >
              {{ stat.label }}
            </option>
          </select>
        </div>

        <!-- Advantage/Disadvantage -->
        <div class="form-group checkbox-group">
          <div class="checkbox-wrapper">
            <input
                id="advantage"
                v-model="advantage"
                type="checkbox"
                class="form-checkbox"
                :disabled="disadvantage"
            />
            <label for="advantage" class="checkbox-label">Advantage</label>
          </div>
          <div class="checkbox-wrapper">
            <input
                id="disadvantage"
                v-model="disadvantage"
                type="checkbox"
                class="form-checkbox"
                :disabled="advantage"
            />
            <label for="disadvantage" class="checkbox-label">Disadvantage</label>
          </div>
        </div>

        <!-- Description -->
        <div class="form-group">
          <label for="description" class="form-label">Description (Optional)</label>
          <textarea
              id="description"
              v-model="description"
              class="form-textarea"
              placeholder="Describe the challenge..."
              rows="3"
          ></textarea>
        </div>

        <!-- Submit Button -->
        <div class="form-actions">
          <button
              type="submit"
              class="submit-btn"
              :disabled="!isFormValid || isLoading"
          >
            <span v-if="isLoading">Creating...</span>
            <span v-else>Create Challenge</span>
          </button>
          <button
              type="button"
              @click="resetForm"
              class="reset-btn"
              :disabled="isLoading"
          >
            Reset
          </button>
        </div>
      </form>
    </div>
  </RPGContainer>
</template>

<style scoped>
.dice-challenge-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 400px;
  max-height: 600px;
}

.header {
  flex-shrink: 0;
  margin-bottom: 0.7rem;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.7rem;
  position: relative;
}

.title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  flex: 1;
  text-align: center;
}

.close-btn {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  line-height: 1;
}

.close-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-50%) scale(1.1);
  color: #7fff16;
}

.close-btn:active {
  transform: translateY(-50%) scale(0.95);
}

.form-wrapper {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 0.35rem;
}

.challenge-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0.175rem;
}

.error-message {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: rgba(255, 0, 0, 0.1);
  border: 1px solid rgba(255, 0, 0, 0.3);
  border-radius: 0.263rem;
  color: #ff6b6b;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
}

.error-close {
  background: none;
  border: none;
  color: #ff6b6b;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-label {
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 500;
  color: #fada95;
}

.character-display {
  padding: 0.35rem 0.525rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.2);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 400;
}

.form-input,
.form-select,
.form-textarea {
  padding: 0.35rem 0.525rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 400;
  transition: border-color 0.3s, background-color 0.3s;
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: rgba(250, 218, 149, 0.5);
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #7fff16;
  background: rgba(0, 0, 0, 0.6);
}

.form-select option {
  background: rgba(0, 0, 0, 0.9);
  color: #fada95;
}

.form-textarea {
  resize: vertical;
  min-height: 3rem;
}

.checkbox-group {
  flex-direction: row;
  gap: 1rem;
  flex-wrap: wrap;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.form-checkbox {
  width: 1rem;
  height: 1rem;
  accent-color: #7fff16;
}

.checkbox-label {
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 400;
  color: #fada95;
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 0.7rem;
  margin-top: 0.7rem;
}

.submit-btn,
.reset-btn {
  flex: 1;
  padding: 0.525rem 1rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled),
.reset-btn:hover:not(:disabled) {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-1px);
}

.submit-btn:active:not(:disabled),
.reset-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled,
.reset-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border-color: rgba(127, 255, 22, 0.1);
}

.submit-btn {
  background: rgba(127, 255, 22, 0.1);
  border-color: rgba(127, 255, 22, 0.5);
}

.submit-btn:hover:not(:disabled) {
  background: rgba(127, 255, 22, 0.2);
  border-color: #7fff16;
}

/* Custom scrollbar styling for RPG theme */
.form-wrapper::-webkit-scrollbar {
  width: 8px;
}

.form-wrapper::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.form-wrapper::-webkit-scrollbar-thumb {
  background: rgba(127, 255, 22, 0.6);
  border-radius: 4px;
}

.form-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(127, 255, 22, 0.8);
}

/* Responsive design */
@media (max-width: 640px) {
  .checkbox-group {
    flex-direction: column;
    gap: 0.5rem;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>