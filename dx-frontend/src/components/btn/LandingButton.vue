<template>
  <div class="dx-button" @click="handleClick" role="button" tabindex="0">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "LandingButton",
  props: {
    action: {
      type: Function,
      required: true,
    },
  },
  methods: {
    handleClick() {
      if (this.action) this.action();
    },
  },
};
</script>

<style scoped>
.dx-button {
  display: inline-block;
  background: rgba(15, 20, 28, 0.97);
  color: #e0e0e0;
  font-size: 0.675rem;
  font-weight: bold;
  padding: 0.656rem 0.938rem;
  border-radius: 6px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow:
    0 6px 12px rgba(0, 0, 0, 0.4),
    0 2px 4px rgba(0, 0, 0, 0.6),
    inset 0 -4px 8px rgba(8, 12, 18, 0.9),
    inset 0 1px 2px rgba(35, 45, 55, 0.6);
  background-image: linear-gradient(145deg, rgba(25, 32, 42, 0.95), rgba(12, 16, 22, 0.98));
  border: 2px solid rgba(35, 45, 55, 0.9);
  border-top: 2px solid rgba(45, 55, 65, 0.7);
  text-align: center;
  min-height: 33px; /* Minimum touch hasTarget size */
  min-width: 90px;
  white-space: nowrap;
  position: relative;
}

.dx-button:hover {
  background-image: linear-gradient(145deg, rgba(30, 38, 48, 0.98), rgba(18, 24, 32, 0.99));
  transform: translateY(-3px);
  box-shadow:
    0 8px 16px rgba(0, 0, 0, 0.5),
    0 4px 8px rgba(0, 0, 0, 0.7),
    inset 0 -5px 10px rgba(6, 10, 16, 0.95),
    inset 0 2px 4px rgba(40, 50, 60, 0.7);
  border-top: 2px solid rgba(50, 60, 70, 0.8);
}

.dx-button:active {
  transform: translateY(1px);
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.6),
    inset 0 4px 12px rgba(5, 8, 12, 0.95),
    inset 0 -2px 4px rgba(20, 28, 36, 0.5);
  background-image: linear-gradient(145deg, rgba(12, 16, 22, 0.99), rgba(20, 26, 34, 0.97));
  border-top: 2px solid rgba(25, 35, 45, 0.9);
}

.dx-button:focus {
  outline: 2px solid #e0e0e0;
  outline-offset: 2px;
}

/* Mobile optimizations */
@media (max-width: 479px) {
  .dx-button {
    font-size: 0.75rem;
    padding: 0.75rem 1.125rem;
    min-height: 36px; /* Larger touch hasTarget on mobile */
    width: 100%;
    max-width: 210px;
  }
}

/* Tablet and small desktop */
@media (min-width: 480px) and (max-width: 767px) {
  .dx-button {
    font-size: 0.713rem;
    padding: 0.675rem 1.05rem;
    min-width: 105px;
  }
}

/* Large screens */
@media (min-width: 1200px) {
  .dx-button {
    font-size: 0.825rem;
    padding: 0.75rem 1.5rem;
    min-width: 120px;
  }
}

/* Extra large screens */
@media (min-width: 1600px) {
  .dx-button {
    font-size: 0.9rem;
    padding: 0.844rem 1.688rem;
    min-width: 135px;
  }
}
</style>
