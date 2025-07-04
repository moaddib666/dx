<template>
  <button
    :class="['compact-button', buttonType]"
    @click="$emit('click')"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: "CompactButton",
  props: {
    buttonType: {
      type: String,
      default: "default", // 'default', 'icon-only', or 'labeled'
    },
  },
  emits: ['click']
};
</script>

<style scoped>
.compact-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  margin: 0.25rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  color: white;
  background: rgba(0, 0, 0, 0.4);
  box-shadow:
    0 0.25rem 0.9375rem rgba(0, 0, 0, 0.4),
    0 0 0 0.125rem rgba(100, 150, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.compact-button:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.05) 40%,
    rgba(0, 0, 0, 0.1) 100%
  );
  transition: opacity 0.3s ease;
}

.compact-button:hover {
  transform: translateY(-0.1rem) scale(1.01);
  box-shadow:
    0 0.5rem 1.5625rem rgba(0, 0, 0, 0.6),
    0 0 0 0.1875rem rgba(100, 150, 255, 0.5),
    0 0 1.25rem rgba(100, 150, 255, 0.3);
}

.compact-button:hover:before {
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.15) 0%,
    rgba(255, 255, 255, 0.1) 40%,
    rgba(0, 0, 0, 0.05) 100%
  );
}

.compact-button:active {
  transform: translateY(0);
  box-shadow:
    0 0.125rem 0.375rem rgba(0, 0, 0, 0.2),
    0 0 0 0.125rem rgba(100, 150, 255, 0.3);
}

.compact-button.icon-only {
  width: 2.5rem;
  height: 2.5rem;
  padding: 0;
  border-radius: 0.25rem;
}

.compact-button.labeled {
  padding: 0.5rem 1.5rem;
}

/* Selection glow effect */
.compact-button:after {
  content: '';
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

.compact-button:hover:after {
  opacity: 1;
  animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

/* Responsive Design for different viewport sizes */
@media (max-width: 75em) { /* 1200px */
  .compact-button {
    font-size: 0.85rem;
    padding: 0.45rem 0.9rem;
  }

  .compact-button.labeled {
    padding: 0.45rem 1.35rem;
  }

  .compact-button.icon-only {
    width: 2.25rem;
    height: 2.25rem;
  }
}

@media (max-width: 48em) { /* 768px */
  .compact-button {
    font-size: 0.8rem;
    padding: 0.4rem 0.8rem;
  }

  .compact-button.labeled {
    padding: 0.4rem 1.2rem;
  }

  .compact-button.icon-only {
    width: 2rem;
    height: 2rem;
  }
}

@media (max-width: 30em) { /* 480px */
  .compact-button {
    font-size: 0.75rem;
    padding: 0.35rem 0.7rem;
  }

  .compact-button.labeled {
    padding: 0.35rem 1.05rem;
  }

  .compact-button.icon-only {
    width: 1.75rem;
    height: 1.75rem;
  }
}
</style>