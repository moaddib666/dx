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
  gap: 1.5rem;
  padding: 2rem;
  flex-wrap: wrap;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

/* Path Card Styling */
.path-card {
  width: 280px;
  text-align: center;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: all 0.3s ease;
  filter: grayscale(70%);
  cursor: pointer;
  background: rgba(0, 0, 0, 0.4);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  outline: none;
  border: 2px solid rgba(127, 255, 22, 0.2);
  backdrop-filter: blur(2px);
  position: relative;
}

/* Flow border effect */
.path-card::before {
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

@keyframes flowBorder {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.path-card:hover {
  filter: grayscale(0%);
  transform: translateY(-4px);
  border-color: rgba(127, 255, 22, 0.5);
  box-shadow: 0 6px 20px rgba(127, 255, 22, 0.2);
}

.path-card:hover::before {
  opacity: 1;
}

.path-card.selected {
  filter: grayscale(0%);
  border: 2px solid #7fff16;
  box-shadow: 0 6px 20px rgba(127, 255, 22, 0.4);
  background: rgba(127, 255, 22, 0.05);
}

.path-card.selected::before {
  opacity: 1;
}

/* Hover glow effect */
.path-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 0.5rem;
  background: radial-gradient(circle at center, rgba(127, 255, 22, 0.1) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.path-card:hover::after,
.path-card.selected::after {
  opacity: 1;
}

/* Icon Styling */
.path-icon {
  width: 100%;
  height: auto;
  border-bottom: 2px solid rgba(127, 255, 22, 0.3);
  position: relative;
  z-index: 2;
}

/* Text Styling */
.path-details {
  padding: 1.5rem;
  color: #fada95;
  position: relative;
  z-index: 2;
}

.path-name {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0.5rem 0;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.path-description {
  font-size: 0.9rem;
  color: rgba(250, 218, 149, 0.8);
  line-height: 1.4;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 400;
}

/* Accessibility Focus */
.path-card:focus {
  border: 2px solid #7fff16;
  box-shadow: 0 6px 20px rgba(127, 255, 22, 0.4);
  background: rgba(127, 255, 22, 0.05);
}

.path-card:focus::before {
  opacity: 1;
}
</style>
