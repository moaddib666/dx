<template>
  <div class="feature-selector">
    <div class="header-top">
      <h2>{{ t('playerComponents.featureSelector.title') }}</h2>
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
/* Feature Selector - Responsive */
.feature-selector {
  padding: 1rem;
  border-radius: 0.5rem;
  background: transparent;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-align: center;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

/* Responsive padding */
@media (min-width: 768px) {
  .feature-selector {
    padding: 1.5rem;
    margin: 0 auto;
  }
}

@media (min-width: 1024px) {
  .feature-selector {
    padding: 2rem;
  }
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

/* Responsive header spacing */
@media (min-width: 768px) {
  .header-top {
    margin-bottom: 1.5rem;
  }
}

h2 {
  margin: 0;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  flex: 1;
  text-align: center;
  font-size: 1.5rem;
  font-weight: 600;
}

/* Responsive heading */
@media (min-width: 768px) {
  h2 {
    font-size: 1.75rem;
  }
}

p {
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  color: rgba(250, 218, 149, 0.8);
}

/* Responsive description */
@media (min-width: 768px) {
  p {
    margin-bottom: 2rem;
    font-size: 1rem;
  }
}

/* Features Container - Responsive Grid */
.features-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  overflow-y: auto;
  padding: 1rem;
  border: 1px solid rgba(127, 255, 22, 0.2);
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

/* Responsive grid breakpoints */
@media (min-width: 768px) {
  .features-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
    padding: 1.25rem;
  }
}

@media (min-width: 1024px) {
  .features-container {
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    padding: 1.5rem;
  }
}

@media (min-width: 1200px) {
  .features-container {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Feature Cards - Simplified */
.feature-card {
  background: rgba(0, 0, 0, 0.2);
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  opacity: 0.8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  text-align: left;
  border: 1px solid rgba(127, 255, 22, 0.2);
  box-sizing: border-box;
  min-height: 120px;
}

/* Responsive card padding */
@media (min-width: 768px) {
  .feature-card {
    padding: 1.25rem;
    min-height: 140px;
  }
}

@media (min-width: 1024px) {
  .feature-card {
    padding: 1.5rem;
    min-height: 160px;
  }
}

.feature-card:hover {
  opacity: 1;
  transform: translateY(-1px);
  border-color: rgba(127, 255, 22, 0.5);
}

.feature-card.selected {
  opacity: 1;
  background: rgba(127, 255, 22, 0.1);
  border-color: #7fff16;
}

.feature-card h3 {
  font-size: 1rem;
  margin-bottom: 0.75rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

/* Responsive card text */
@media (min-width: 768px) {
  .feature-card h3 {
    font-size: 1.1rem;
    margin-bottom: 1rem;
  }
}

@media (min-width: 1024px) {
  .feature-card h3 {
    font-size: 1.2rem;
  }
}

.feature-card p {
  font-size: 0.8rem;
  color: rgba(250, 218, 149, 0.8);
  margin: 0;
  line-height: 1.4;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

/* Responsive card description */
@media (min-width: 768px) {
  .feature-card p {
    font-size: 0.85rem;
  }
}

@media (min-width: 1024px) {
  .feature-card p {
    font-size: 0.9rem;
  }
}
</style>
