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
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, #1c1c1c, #333333);
  border: 2px solid #444;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}
</style>
