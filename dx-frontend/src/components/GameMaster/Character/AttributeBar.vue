<template>
  <div class="attribute-bar">
    <!-- Filled portion -->
    <div
        :style="{ width: `${(current / max) * 100}%`, background: gradientColor }"
        class="attribute-bar-current"
    ></div>
    <!-- Overlay (optional shadow) -->
    <div class="attribute-bar-shadow"></div>
    <!-- Value display -->
    <div class="attribute-bar-values">
      {{ current }} / {{ max }}
    </div>
  </div>
</template>

<script>
export default {
  name: "AttributeBar",
  props: {
    current: { type: Number, required: true },
    max: { type: Number, required: true },
    type: { type: String, required: true } // e.g., "Health", "Energy", "Action Points"
  },
  computed: {
    gradientColor() {
      switch (this.type) {
        case "Health":
          return "linear-gradient(90deg, #FF453A, #FFA500)";
        case "Energy":
          return "linear-gradient(90deg, #007BFF, #00E8FF)";
        case "Action Points":
          return "linear-gradient(90deg, #32CD32, #90EE90)";
        default:
          return "rgba(255,255,255,0.5)";
      }
    }
  }
};
</script>

<style scoped>
.attribute-bar {
  position: relative;
  width: 100%;
  height: 0.4rem; /* compact height */
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.25rem;
  overflow: hidden;
  box-shadow: inset 0 0 4px rgba(0, 0, 0, 0.3);
  margin-bottom: 0.3rem; /* spacing if stacking multiple bars */
}

.attribute-bar-current {
  height: 100%;
  transition: width 0.3s ease;
}

.attribute-bar-shadow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.attribute-bar-values {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.4rem;
  color: #fff;
  text-align: center;
  pointer-events: none;
}
</style>
