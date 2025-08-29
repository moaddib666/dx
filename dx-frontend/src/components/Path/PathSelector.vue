<template>
  <div class="path-selector">
    <div
        v-for="path in paths"
        :key="path.id"
        :class="['path-card', { selected: selectedPath === path.id }]"
        @click="selectPath(path.id)"
        @keydown.enter="selectPath(path.id)"
        @keydown.space.prevent="selectPath(path.id)"
        tabindex="0"
    >
      <img :alt="`${path.name} Icon`" :src="path.icon" class="path-icon"/>
      <div class="path-details">
        <h3 class="path-name">{{ path.name }}</h3>
        <p class="path-description">{{ path.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PathSelector",
  props: {
    paths: {
      type: Array,
      required: true,
    },
    selectedPathId: {
      type: Number,
      default: null,
    },
    setPlayerPathId: {
      type: Function,
      required: true,
    },
  },
  computed: {
    selectedPath() {
      return this.selectedPathId;
    },
  },
  methods: {
    selectPath(pathId) {
      this.setPlayerPathId(pathId);
    },
  },
};
</script>

<style scoped>
/* Container Styling - Responsive Grid */
.path-selector {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
}

/* Responsive grid breakpoints */
@media (min-width: 768px) {
  .path-selector {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
    padding: 1.5rem;
    margin: 0 auto;
  }
}

@media (min-width: 1024px) {
  .path-selector {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    padding: 2rem;
  }
}

/* Path Card Styling - Simplified */
.path-card {
  width: 100%;
  max-width: 20vw;
  text-align: center;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: all 0.3s ease;
  filter: grayscale(50%);
  cursor: pointer;
  background: rgba(0, 0, 0, 0.2);
  outline: none;
  border: 1px solid rgba(127, 255, 22, 0.3);
  box-sizing: border-box;
}

.path-card:hover {
  filter: grayscale(0%);
  transform: translateY(-2px);
  border-color: rgba(127, 255, 22, 0.6);
}

.path-card.selected {
  filter: grayscale(0%);
  border: 1px solid #7fff16;
  background: rgba(127, 255, 22, 0.05);
}

/* Icon Styling */
.path-icon {
  width: 100%;
  height: auto;
  border-bottom: 1px solid rgba(127, 255, 22, 0.3);
}

/* Text Styling - Responsive */
.path-details {
  padding: 1rem;
  color: #fada95;
}

/* Responsive text padding */
@media (min-width: 768px) {
  .path-details {
    padding: 1.25rem;
  }
}

@media (min-width: 1024px) {
  .path-details {
    padding: 1.5rem;
  }
}

.path-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0.5rem 0;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

/* Responsive path name sizing */
@media (min-width: 768px) {
  .path-name {
    font-size: 1.2rem;
  }
}

@media (min-width: 1024px) {
  .path-name {
    font-size: 1.3rem;
  }
}

.path-description {
  font-size: 0.8rem;
  color: rgba(250, 218, 149, 0.8);
  line-height: 1.4;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 400;
}

/* Responsive description sizing */
@media (min-width: 768px) {
  .path-description {
    font-size: 0.85rem;
  }
}

@media (min-width: 1024px) {
  .path-description {
    font-size: 0.9rem;
  }
}

/* Simplified Focus State */
.path-card:focus {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.05);
}
</style>
