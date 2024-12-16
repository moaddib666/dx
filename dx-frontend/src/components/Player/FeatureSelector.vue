<template>
  <div class="feature-selector">
    <h2>Select Features</h2>
    <p>Select up to two features that suit your character best.</p>

    <!-- Feature Cards Scrollable Container -->
    <div class="features-container">
      <div
          v-for="(feature, key) in features"
          :key="key"
          :class="['feature-card', { selected: selectedFeatures.includes(key) }]"
          @click="toggleFeature(key)"
      >
        <h3 class="feature-name">{{ feature.name }}</h3>
        <p class="feature-description">{{ feature.description }}</p>
      </div>
    </div>

    <!-- Navigation Buttons -->
    <div class="navigation-buttons">
      <button
          class="back-button"
          @click="$emit('back')"
      >
        Back
      </button>
      <button
          :disabled="selectedFeatures.length < 2"
          class="next-button"
          @click="submitSelection"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "FeatureSelector",
  props: {
    features: {
      type: Object,
      required: true,
    },
    selected: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      selectedFeatures: [...this.selected], // Initialize with pre-selected features
    };
  },
  methods: {
    toggleFeature(featureKey) {
      if (this.selectedFeatures.includes(featureKey)) {
        this.selectedFeatures = this.selectedFeatures.filter((key) => key !== featureKey);
      } else if (this.selectedFeatures.length < 2) {
        this.selectedFeatures.push(featureKey);
      }
    },
    submitSelection() {
      this.$emit("next", this.selectedFeatures);
    },
  },
};
</script>

<style scoped>
.feature-selector {
  padding: 20px;
  border-radius: 8px;
  background-color: #222;
  color: #fff;
  text-align: center;
}

h2 {
  margin-bottom: 10px;
}

p {
  margin-bottom: 20px;
  font-size: 0.9rem;
  color: #ccc;
}

/* Scrollable Container */
.features-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  align-items: stretch;
  max-height: 500px; /* Limit height for scrolling */
  overflow-y: auto;
  padding: 10px;
  border: 1px solid #444;
  border-radius: 8px;
  background-color: #333;
}

/* Feature Cards */
.feature-card {
  flex: 0 1 calc(25% - 20px); /* Four cards per row on large screens */
  max-width: calc(25% - 20px);
  background-color: rgba(255, 255, 255, 0.1);
  padding: 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.3s ease, opacity 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  opacity: 0.6;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  text-align: left;
}

.feature-card:hover {
  opacity: 1;
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
}

.feature-card.selected {
  opacity: 1;
  background-color: rgba(33, 150, 243, 0.8);
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.7);
  transform: scale(1.05);
}

.feature-card h3 {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #fff;
}

.feature-card p {
  font-size: 0.9rem;
  color: #ddd;
  margin: 0;
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
