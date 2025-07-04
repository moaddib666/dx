<template>
  <div class="compact-play-button" @click="onClick">
    <span class="play-icon">▶</span>
  </div>
</template>

<script>
export default {
  name: "CompactPlayButton",
  methods: {
    onClick() {
      this.$emit("click"); // Emit a click event
    },
  },
};
</script>

<style scoped>
.compact-play-button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.25rem;
  background: rgba(0, 0, 0, 0.4);
  box-shadow:
    0 0.25rem 0.9375rem rgba(0, 0, 0, 0.4),
    0 0 0 0.125rem rgba(100, 150, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.compact-play-button:before {
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

.compact-play-button:hover {
  transform: translateY(-0.1rem) scale(1.01);
  box-shadow:
    0 0.5rem 1.5625rem rgba(0, 0, 0, 0.6),
    0 0 0 0.1875rem rgba(100, 150, 255, 0.5),
    0 0 1.25rem rgba(100, 150, 255, 0.3);
}

.compact-play-button:hover:before {
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.15) 0%,
    rgba(255, 255, 255, 0.1) 40%,
    rgba(0, 0, 0, 0.05) 100%
  );
}

/* Play Icon Styling */
.play-icon {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.8);
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
  transition: color 0.2s ease-in-out;
  position: relative;
  z-index: 2;
}

.compact-play-button:hover .play-icon {
  color: rgba(100, 150, 255, 1);
  text-shadow: 0 0 8px rgba(100, 150, 255, 1);
}

/* Selection glow effect */
.compact-play-button:after {
  content: '';
  position: absolute;
  top: -0.125rem;
  left: -0.125rem;
  right: -0.125rem;
  bottom: -0.125rem;
  border-radius: 0.375rem;
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

.compact-play-button:hover:after {
  opacity: 1;
  animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

/* Responsive Design for different viewport sizes */
@media (max-width: 75em) { /* 1200px */
  .compact-play-button {
    width: 2.25rem;
    height: 2.25rem;
  }

  .play-icon {
    font-size: 1.1rem;
  }
}

@media (max-width: 48em) { /* 768px */
  .compact-play-button {
    width: 2rem;
    height: 2rem;
    border-radius: 0.2rem;
  }

  .play-icon {
    font-size: 1rem;
  }
}

@media (max-width: 30em) { /* 480px */
  .compact-play-button {
    width: 1.75rem;
    height: 1.75rem;
    border-radius: 0.15rem;
  }

  .play-icon {
    font-size: 0.9rem;
  }
}
</style>