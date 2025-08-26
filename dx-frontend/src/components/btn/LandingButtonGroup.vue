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
  background: linear-gradient(135deg, #1c1c1c, #333333);
  border: 2px solid #444;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  max-width: 90vw;
  margin: 0 auto;
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
