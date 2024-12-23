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
/* Container Styling */
.path-selector {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 20px;
}

/* Path Card Styling */
.path-card {
  width: 200px;
  text-align: center;
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.3s ease;
  filter: grayscale(100%); /* Desaturate by default */
  cursor: pointer;
  background-color: #222;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  outline: none; /* Remove default focus outline */
}

.path-card:hover {
  filter: grayscale(0%); /* Saturate on hover */
  transform: scale(1.05); /* Slight zoom effect */
}

.path-card.selected {
  filter: grayscale(0%); /* Fully saturated */
  border: 2px solid #ffbf00; /* Highlight border for selection */
  box-shadow: 0 6px 12px rgba(255, 191, 0, 0.5);
}

/* Icon Styling */
.path-icon {
  width: 100%;
  height: auto;
  border-bottom: 1px solid #444;
}

/* Text Styling */
.path-details {
  padding: 10px;
  color: #eee;
}

.path-name {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 5px 0;
}

.path-description {
  font-size: 0.9rem;
  color: #ccc;
}

/* Accessibility Focus */
.path-card:focus {
  border: 2px solid #ffbf00; /* Highlight on keyboard focus */
  box-shadow: 0 6px 12px rgba(255, 191, 0, 0.5);
}
</style>
