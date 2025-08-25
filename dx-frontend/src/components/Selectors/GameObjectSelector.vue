<template>
  <div class="game-object-selector">
    <div class="header-top">
      <h3 class="title">Game Objects</h3>
      <button @click="$emit('close')" class="close-btn" title="Close Game Object Selector">
        ×
      </button>
    </div>
    <div class="selected compact-card" @click="toggleDropdown">
      <div class="card-icon" :style="{ backgroundImage: `url(${selectedObject?.icon || placeholderIcon})` }">
        <div class="card-overlay"></div>
      </div>
      <div class="card-content">
        <div class="character-name">
          {{ selectedObject?.name || 'Select Object' }}
        </div>
      </div>
      <div class="selection-glow"></div>
    </div>
    <div v-if="isDropdownOpen" class="dropdown">
      <div
        v-for="item in gameObjects"
        :key="item.id"
        class="dropdown-item compact-card"
        @click="selectItem(item.id)"
      >
        <div class="card-icon" :style="{ backgroundImage: `url(${item.icon})` }">
          <div class="card-overlay"></div>
        </div>
        <div class="card-content">
          <div class="character-name">
            {{ item.name }}
          </div>
        </div>
        <div class="selection-glow"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "GameObjectSelector",
  emits: ['update:selectedId', 'close'],
  props: {
    gameObjects: {
      type: Array,
      default: () => [],
    },
    selectedId: {
      type: String,
      default: null,
    },
    placeholderIcon: {
      type: String,
      default: "https://via.placeholder.com/150", // Fallback icon
    },
  },
  data() {
    return {
      isDropdownOpen: false,
    };
  },
  computed: {
    selectedObject() {
      return this.gameObjects?.find((item) => item.id === this.selectedId) || null;
    },
  },
  methods: {
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    selectItem(id) {
      this.$emit("update:selectedId", id); // Emit the selected ID to the parent
      this.isDropdownOpen = false; // Close the dropdown
    },
  },
};
</script>

<style scoped>
.game-object-selector {
  position: relative;
  width: 14rem;
  cursor: pointer;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
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

/* Compact Card Styling */
.compact-card {
  display: flex;
  align-items: center;
  width: 12rem;
  height: 2.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 0.5rem;
  overflow: hidden;
  position: relative;
  box-shadow:
      0 0.25rem 0.9375rem rgba(0, 0, 0, 0.4),
      0 0 0 0.125rem rgba(100, 150, 255, 0.2);
  background: rgba(0, 0, 0, 0.4);
  padding: 0.25rem;
  gap: 0.5rem;
}

.compact-card:hover {
  transform: translateY(-0.1rem) scale(1.01);
  box-shadow:
      0 0.5rem 1.5625rem rgba(0, 0, 0, 0.6),
      0 0 0 0.1875rem rgba(100, 150, 255, 0.5),
      0 0 1.25rem rgba(100, 150, 255, 0.3);
  z-index: 10;
}

.card-icon {
  width: 2rem;
  height: 2rem;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  border-radius: 0.25rem;
  flex-shrink: 0;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
      180deg,
      rgba(0, 0, 0, 0.1) 0%,
      rgba(0, 0, 0, 0.3) 40%,
      rgba(0, 0, 0, 0.8) 100%
  );
  transition: opacity 0.3s ease;
}

.compact-card:hover .card-overlay {
  background: linear-gradient(
      180deg,
      rgba(0, 0, 0, 0.05) 0%,
      rgba(0, 0, 0, 0.2) 40%,
      rgba(0, 0, 0, 0.7) 100%
  );
}

.card-content {
  position: relative;
  z-index: 2;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.character-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #ffffff;
  text-shadow:
      0 0.125rem 0.25rem rgba(0, 0, 0, 0.8),
      0 0 0.5rem rgba(0, 0, 0, 0.6);
  line-height: 1.1;
  letter-spacing: 0.03em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.selection-glow {
  position: absolute;
  top: -0.125rem;
  left: -0.125rem;
  right: -0.125rem;
  bottom: -0.125rem;
  border-radius: 0.625rem;
  background: linear-gradient(45deg,
  transparent,
  rgba(100, 150, 255, 0.3),
  transparent,
  rgba(100, 150, 255, 0.3),
  transparent
  );
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
  z-index: -1;
}

.compact-card:hover .selection-glow {
  opacity: 1;
  animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

/* Selected Item Specific Styling */
.selected {
  margin-bottom: 0.5rem;
}

/* Dropdown Specific Styling */
.dropdown {
  position: absolute;
  top: calc(100% + 0.25rem);
  left: 0;
  z-index: 100;
  width: 100%;
  max-height: 15rem;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 0.5rem;
  padding: 0.375rem;
  box-shadow: 0 0.5rem 1.5625rem rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  scrollbar-width: thin;
  scrollbar-color: rgba(100, 150, 255, 0.3) transparent;
}

.dropdown::-webkit-scrollbar {
  width: 0.28125rem;
}

.dropdown::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 0.140625rem;
}

.dropdown::-webkit-scrollbar-thumb {
  background: rgba(100, 150, 255, 0.3);
  border-radius: 0.140625rem;
}

.dropdown::-webkit-scrollbar-thumb:hover {
  background: rgba(100, 150, 255, 0.5);
}

/* Responsive Design for different viewport sizes */
@media (max-width: 75em) { /* 1200px */
  .compact-card {
    width: 11rem;
  }

  .character-name {
    font-size: 0.8rem;
  }
}

@media (max-width: 48em) { /* 768px */
  .compact-card {
    width: 10rem;
    height: 2.25rem;
  }

  .card-icon {
    width: 1.75rem;
    height: 1.75rem;
    border-radius: 0.2rem;
  }

  .character-name {
    font-size: 0.75rem;
  }
}

@media (max-width: 30em) { /* 480px */
  .compact-card {
    width: 9rem;
    height: 2rem;
  }

  .card-icon {
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 0.15rem;
  }

  .character-name {
    font-size: 0.7rem;
  }
}
</style>
