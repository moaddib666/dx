<template>
  <div :class="['background', backgroundClass]">
    <!--    <slot></slot>-->
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
}
</style>
