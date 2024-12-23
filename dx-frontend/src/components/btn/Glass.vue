<template>
  <button
      :class="['glass-button', buttonType]"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: "GlassButton",
  props: {
    buttonType: {
      type: String,
      default: "default", // 'default', 'icon-only', or 'labeled'
    },
  },
};
</script>

<style scoped>
.glass-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  margin: 5px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: bold;
  text-transform: uppercase;
  color: white;
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), inset 0 -2px 6px rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  cursor: pointer;
  transition: all 0.3s ease;
}

.glass-button:hover {
  background: rgba(255, 255, 255, 0.3);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2), inset 0 -4px 10px rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.glass-button:active {
  transform: translateY(0);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2), inset 0 -1px 3px rgba(255, 255, 255, 0.2);
}

.glass-button.icon-only {
  width: 50px;
  height: 50px;
  padding: 0;
}

.glass-button.labeled {
  padding: 10px 30px;
}
</style>
