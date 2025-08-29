<template>
  <div class="feature-selector">
    <div class="header-top">
      <h2>{{ t('playerComponents.featureSelector.title') }}</h2>
      <button @click="$emit('close')" class="close-btn" title="Close Feature Selector">
        ×
      </button>
    </div>
    <p>{{ t('playerComponents.featureSelector.description') }}</p>

    <!-- Feature Cards Scrollable Container -->
    <div class="features-container">
      <div
          v-for="feature in modificators"
          :key="feature.id"
          :class="['feature-card', { selected: selectedModificators.includes(feature.id) }]"
          @click="toggleFeature(feature.id)"
      >
        <h3 class="feature-name">{{ feature.name }}</h3>
        <p class="feature-description">{{ feature.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useI18n } from 'vue-i18n';

export default {
  name: "FeatureSelector",
  emits: ['close'],
  props: {
    modificators: {
      type: Array,
      required: true,
    },
    selectedModificators: {
      type: Array,
      default: () => [],
    },
    setPlayerModificators: {
      type: Function,
      required: true,
    },
    maxModificators: {
      type: Number,
      default: 0,
    },
  },
  setup() {
    const { t } = useI18n();
    return { t };
  },
  data() {
    return {
      localSelected: [...this.selectedModificators], // Local state for selected modificators
    };
  },
  methods: {
    toggleFeature(featureId) {
      if (this.localSelected.includes(featureId)) {
        this.localSelected = this.localSelected.filter((id) => id !== featureId);
      } else if (this.localSelected.length < this.maxModificators) {
        this.localSelected.push(featureId);
      }
      this.setPlayerModificators(this.localSelected);
    },
  },
  watch: {
    selectedModificators: {
      immediate: true,
      handler(newValue) {
        this.localSelected = [...newValue]; // Sync local state with prop
      },
    },
  },
};
</script>
<style scoped>
.feature-selector {
  padding: 2rem;
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-align: center;
  border: 2px solid rgba(127, 255, 22, 0.3);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
}

/* Flow border effect */
.feature-selector::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 0.5rem;
  background: linear-gradient(45deg,
    transparent,
    rgba(127, 255, 22, 0.05),
    transparent,
    rgba(127, 255, 22, 0.05),
    transparent
  );
  background-size: 300% 300%;
  animation: flowBorder 8s ease-in-out infinite;
  opacity: 0.3;
  pointer-events: none;
}

@keyframes flowBorder {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 2;
}

h2 {
  margin: 0;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  flex: 1;
  text-align: center;
  font-size: 1.8rem;
  font-weight: 600;
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

p {
  margin-bottom: 2rem;
  font-size: 1rem;
  color: rgba(250, 218, 149, 0.8);
  position: relative;
  z-index: 2;
}

/* Scrollable Container */
.features-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
  align-items: stretch;
  max-height: 500px;
  overflow-y: auto;
  padding: 1.5rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(2px);
  position: relative;
  z-index: 2;
}

/* Feature Cards */
.feature-card {
  flex: 0 1 calc(25% - 1.5rem);
  max-width: calc(25% - 1.5rem);
  background: rgba(0, 0, 0, 0.4);
  padding: 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  opacity: 0.7;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  text-align: left;
  border: 2px solid rgba(127, 255, 22, 0.2);
  backdrop-filter: blur(2px);
  position: relative;
  overflow: hidden;
}

/* Flow border effect for feature cards */
.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 0.5rem;
  background: linear-gradient(45deg,
    transparent,
    rgba(127, 255, 22, 0.1),
    transparent,
    rgba(127, 255, 22, 0.1),
    transparent
  );
  background-size: 300% 300%;
  animation: flowBorder 6s ease-in-out infinite;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.feature-card:hover {
  opacity: 1;
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(127, 255, 22, 0.2);
  border-color: rgba(127, 255, 22, 0.5);
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-card.selected {
  opacity: 1;
  background: rgba(127, 255, 22, 0.1);
  box-shadow: 0 6px 20px rgba(127, 255, 22, 0.4);
  transform: translateY(-2px);
  border-color: #7fff16;
}

.feature-card.selected::before {
  opacity: 1;
}

.feature-card h3 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
  position: relative;
  z-index: 2;
}

.feature-card p {
  font-size: 0.9rem;
  color: rgba(250, 218, 149, 0.8);
  margin: 0;
  line-height: 1.4;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  position: relative;
  z-index: 2;
}

/* Responsive Design */
@media (max-width: 1200px) {
  .feature-card {
    flex: 0 1 calc(33.33% - 20px); /* Three cards per row */
    max-width: calc(33.33% - 20px);
  }
}

@media (max-width: 768px) {
  .feature-card {
    flex: 0 1 calc(50% - 20px); /* Two cards per row */
    max-width: calc(50% - 20px);
  }
}

@media (max-width: 480px) {
  .feature-card {
    flex: 0 1 calc(100% - 20px); /* One card per row */
    max-width: calc(100% - 20px);
  }
}

/* Navigation Buttons */
.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button {
  background-color: #757575;
  color: white;
}

.back-button:hover {
  background-color: #616161;
}

.next-button {
  background-color: #2196f3;
  color: white;
}

.next-button:disabled {
  background-color: #757575;
  cursor: not-allowed;
}

.next-button:hover:not(:disabled) {
  background-color: #1976d2;
}
</style>
