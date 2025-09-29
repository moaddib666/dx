<template>
  <div class="button-group dx-theme">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "LandingButtonGroup",
};
</script>

<style scoped>
.dx-theme {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(8, 12, 18, 0.85), rgba(18, 24, 32, 0.95));
  border: 2px solid rgba(35, 45, 55, 0.9);
  border-top: 2px solid rgba(25, 35, 45, 0.7);
  border-radius: 10px;
  box-shadow:
    0 8px 16px rgba(0, 0, 0, 0.6),
    0 4px 8px rgba(0, 0, 0, 0.8),
    inset 0 2px 4px rgba(30, 40, 50, 0.4),
    inset 0 -2px 6px rgba(5, 8, 12, 0.8);
  max-width: 90vw;
  margin: 0 auto;
  position: relative;
}

/* Mobile-first responsive design */
@media (min-width: 480px) {
  .dx-theme {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
    max-width: 100%;
  }
}

@media (min-width: 768px) {
  .dx-theme {
    flex-wrap: nowrap;
    padding: 1.25rem;
    gap: 1.5rem;
  }
}

@media (min-width: 1200px) {
  .dx-theme {
    padding: 1.5rem 2rem;
    gap: 2rem;
  }
}
</style>
