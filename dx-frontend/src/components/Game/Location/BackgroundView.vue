<template>
  <div :class="['background', backgroundClass]">
    <div
        class="overlay"
        :class="{ 'overlay-visible': movementActivated }">
    </div>
  </div>
</template>

<script>
export default {
  name: "BackgroundView",
  props: {
    background: {
      type: String,
      required: true,
    },
    movementActivated: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    backgroundClass() {
      // Generate a unique class name based on the background URL
      const className = `background-${btoa(this.background).replace(/=/g, "")}`;
      this.updateDynamicStyle(className, this.background);
      return className;
    },
  },
  methods: {
    updateDynamicStyle(className, imageUrl) {
      const existingStyle = document.getElementById(className);
      if (!existingStyle) {
        const style = document.createElement("style");
        style.id = className;
        style.textContent = `
          .${className} {
            background-image: url('${imageUrl}');
          }
        `;
        document.head.appendChild(style);
      }
    },
  },
};
</script>

<style scoped>
.background {
  width: 100%;
  height: 80vh;
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;

  /* Smooth transition effect for background */
  transition: background-image 1s ease-in-out, opacity 1s ease-in-out;
}

.overlay {
  background: url("@/assets/images/backgrounds/moveOverlay.webp") no-repeat center;
  display: flex;
  background-blend-mode: hard-light;
  opacity: 0; /* Start fully transparent */
  width: 100%;
  height: 100%;
  background-size: cover;
  transition: opacity 2s ease-in-out; /* Smooth transition */
}

.overlay-visible {
  opacity: 0.5; /* Normal opacity */
}
</style>
