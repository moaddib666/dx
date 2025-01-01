<template>
  <div :style="backgroundStyle" class="background-container">
    <!-- Slot for dynamic content -->
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "DynamicBackground",
  props: {
    backgroundUrl: {
      type: String,
      required: false, // Background URL is optional
      default: null,
    },
    defaultBackground: {
      type: String,
      required: false, // Optional default background
      default: "https://example.com/default.jpg",
    },
  },
  computed: {
    backgroundStyle() {
      return {
        backgroundImage: `url(${this.backgroundUrl || this.defaultBackground})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      };
    },
  },
};
</script>

<style scoped>
.background-container {
  transition: background 0.3s ease-in-out;
}
</style>
