<template>
  <div class="action-preview compact-card" @click="selectAction">
    <div class="card-icon" :class="{ 'placeholder-icon': !action }">
      <div v-if="!action" class="placeholder">
        <span class="plus-icon">+</span>
      </div>
      <div v-else-if="action.icon" :style="{ backgroundImage: `url(${action.icon})` }" class="action-image"></div>
      <img v-else class="action-image" src="@/assets/images/skill/default.webp"/>
      <div class="card-overlay"></div>
    </div>
    <div class="card-content" v-if="action">
      <div class="action-name">
        {{ action.name || 'Action' }}
      </div>
    </div>
    <div class="selection-glow"></div>
  </div>
</template>

<script>
export default {
  name: "ActionPreview",
  props: {
    action: {
      type: Object,
      default: null, // The selected action or null if not picked
    },
  },
  methods: {
    selectAction() {
      this.$emit("pick-action"); // Emit an event to open the action picker
    },
  },
};
</script>

<style scoped>
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
  display: flex;
  justify-content: center;
  align-items: center;
}

.placeholder-icon {
  background-color: rgba(0, 0, 0, 0.3);
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

.action-name {
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

/* Placeholder for when no action is picked */
.placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 2;
}

.plus-icon {
  font-size: 1.5rem;
  font-weight: bold;
  line-height: 1;
  color: rgba(255, 255, 255, 0.8);
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}

/* Style for the action image */
.action-image {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  border-radius: 0.25rem;
  position: relative;
  z-index: 1;
}

/* Responsive Design for different viewport sizes */
@media (max-width: 75em) { /* 1200px */
  .compact-card {
    width: 11rem;
  }

  .action-name {
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

  .action-name {
    font-size: 0.75rem;
  }

  .plus-icon {
    font-size: 1.3rem;
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

  .action-name {
    font-size: 0.7rem;
  }

  .plus-icon {
    font-size: 1.2rem;
  }
}
</style>
