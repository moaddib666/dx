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
  padding: 0.75rem 1.5rem;
  margin: 0.25rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 25px;
  font-size: 0.9rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-transform: none;
  color: #fada95;
  background: linear-gradient(45deg, rgba(250, 218, 149, 0.1), rgba(127, 255, 22, 0.1));
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(2px);
}

.compact-button:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg,
    transparent,
    rgba(127, 255, 22, 0.05),
    transparent,
    rgba(127, 255, 22, 0.05),
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

.compact-button:hover {
  transform: translateY(-2px);
  background: linear-gradient(45deg, rgba(250, 218, 149, 0.2), rgba(127, 255, 22, 0.2));
  box-shadow: 0 6px 20px rgba(127, 255, 22, 0.4);
  border-color: #7fff16;
}

.compact-button:hover:before {
  opacity: 1;
}

.compact-button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 8px rgba(127, 255, 22, 0.2);
}

.compact-button.icon-only {
  width: 2.5rem;
  height: 2.5rem;
  padding: 0;
  border-radius: 50%;
}

.compact-button.labeled {
  padding: 0.75rem 2rem;
}

/* Selection glow effect */
.compact-button:after {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 25px;
  background: linear-gradient(45deg,
    transparent,
    rgba(127, 255, 22, 0.3),
    transparent,
    rgba(127, 255, 22, 0.3),
    transparent
  );
  background-size: 300% 300%;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
  z-index: -1;
  animation: flowBorder 4s ease-in-out infinite;
}

.compact-button:hover:after {
  opacity: 1;
}

.compact-button.icon-only:after {
  border-radius: 50%;
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