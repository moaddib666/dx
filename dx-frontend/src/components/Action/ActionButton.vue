<template>
  <div class="action-btn" @click="onClick">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "ActionButton",
  methods: {
    onClick() {
      this.$emit("click"); // Notify parent when the button is clicked
    },
  },
};
</script>

<style scoped>
/* Container for the action button */
.action-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  background-image: url('@/assets/images/action/action_btn.png'); /* Your action button image */
  background-position: center;
  background-size: contain;
  background-repeat: no-repeat;

  /* Dimensions */
  min-height: 2rem;
  min-width: 2rem;

  /* Rounded corners and smooth transition */
  border-radius: 8px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.action-btn:hover {
  cursor: pointer;
  transform: scale(1.1); /* Slightly enlarge the action button */
}
</style>
