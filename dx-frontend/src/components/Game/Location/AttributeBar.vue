<template>
  <div class="attribute-bar">
    <!-- Current Value Bar -->
    <div
        :style="{
        width: `${(current / max) * 100}%`,
        background: gradientColor,
      }"
        class="attribute-bar-current"
    ></div>
    <!-- Shadow for the bar -->
    <div class="attribute-bar-shadow"></div>
    <!-- Display Current and Max Values -->
    <div class="attribute-bar-values">
      {{ current }} / {{ max }}
    </div>
  </div>
</template>

<script>
export default {
  name: "AttributeBar",
  props: {
    current: {
      type: Number,
      required: true,
    },
    max: {
      type: Number,
      required: true,
    },
    type: {
      type: String,
      required: true, // "Health", "Energy", "Action Points"
    },
  },
  computed: {
    gradientColor() {
      switch (this.type) {
        case "Health":
          return "linear-gradient(90deg, rgba(255,69,58,1) 0%, rgba(255,165,0,1) 100%)";
        case "Energy":
          return "linear-gradient(90deg, rgba(0,123,255,1) 0%, rgba(0,232,255,1) 100%)";
        case "Action Points":
          return "linear-gradient(90deg, rgba(50,205,50,1) 0%, rgba(144,238,144,1) 100%)";
        default:
          return "rgba(255,255,255,0.5)"; // Fallback color
      }
    },
  },
};
</script>

<style scoped>
/* Attribute Bar Container */
.attribute-bar {
  position: relative;
  width: 100%;
  height: 0.6rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.25rem;
  overflow: hidden;
  margin-bottom: 0.4rem;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
}

/* Current Value Bar */
.attribute-bar-current {
  height: 100%;
  transition: width 0.3s ease, background-color 0.3s ease;
}

/* Shadow Effect */
.attribute-bar-shadow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.6);
  pointer-events: none;
}

/* Attribute Values */
.attribute-bar-values {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.6rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: bold;
  white-space: nowrap;
  pointer-events: none;
}
</style>
