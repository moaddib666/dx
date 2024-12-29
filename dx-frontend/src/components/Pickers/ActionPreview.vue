<template>
  <div class="action-picker" @click="selectAction">
    <div v-if="!action" class="placeholder">
      <span class="plus-icon">+</span>
    </div>
    <div v-else-if="action.icon" :style="{ backgroundImage: `url(${action.icon})` }" class="action-image"></div>
    <img v-else class="action-image" src="@/assets/images/skill/default.webp"/>

  </div>
</template>

<script>
export default {
  name: "ActionPicker",
  props: {
    action: {
      type: Object,
      default: null, // The selected action or null if not picked
    },
  },
  methods: {
    selectAction() {
      this.$emit("pick-action"); // Emit an event to open the action picker
    },
  },
};
</script>

<style scoped>
.action-picker {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 2.5rem; /* Compact size for the picker */
  height: 2.5rem; /* Compact size for the picker */
  border-radius: 50%; /* Circular shape */
  background: rgba(255, 255, 255, 0.1); /* Glass-style semi-transparent background */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), inset 0 0 10px rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px); /* Glass effect */
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  overflow: hidden; /* Ensure content stays within the circle */
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.action-picker:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
}

/* Placeholder for when no action is picked */
.placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1rem; /* Adjusted size for smaller icon */
  color: rgba(255, 255, 255, 0.7);
}

.plus-icon {
  font-size: 1.5rem; /* Smaller size for compact layout */
  font-weight: bold;
  line-height: 1;
  color: rgba(255, 255, 255, 0.8);
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}

/* Style for the action image */
.action-image {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  border-radius: 50%;

}
</style>
