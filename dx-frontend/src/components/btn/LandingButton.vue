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
  background: #292929;
  color: #e0e0e0;
  font-size: 0.675rem;
  font-weight: bold;
  padding: 0.656rem 0.938rem;
  border-radius: 4px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3), inset 0 -3px 6px #1a1a1a;
  background-image: linear-gradient(145deg, #404040, #292929);
  border: 2px solid #444;
  text-align: center;
  min-height: 33px; /* Minimum touch target size */
  min-width: 90px;
  white-space: nowrap;
}

.dx-button:hover {
  background-image: linear-gradient(145deg, #505050, #3a3a3a);
  transform: translateY(-2px);
}

.dx-button:active {
  transform: translateY(2px);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3), inset 0 3px 6px #1a1a1a;
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
    min-height: 36px; /* Larger touch target on mobile */
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
