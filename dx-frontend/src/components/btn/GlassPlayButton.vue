<template>
  <div class="glass-play-button" @click="onClick">
    <span class="play-icon">▶</span>
  </div>
</template>

<script>
export default {
  name: "GlassPlayButton",
  methods: {
    onClick() {
      this.$emit("click"); // Emit a click event
    },
  },
};
</script>

<style scoped>
.glass-play-button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 2.5rem; /* Fixed size for button */
  height: 2.5rem; /* Fixed size for button */
  border-radius: 50%; /* Circular button */
  background: rgba(255, 255, 255, 0.1); /* Glass-style semi-transparent background */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), inset 0 0 10px rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px); /* Glass effect */
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out, background 0.2s ease-in-out;
  overflow: hidden;
}

.glass-play-button:hover {
  transform: scale(1.05); /* Slightly enlarge on hover */
  background: rgba(50, 255, 50, 0.2); /* Change to green tint */
  box-shadow: 0 0 12px rgba(50, 255, 50, 0.8); /* Green glowing effect */
}

/* Play Icon Styling */
.play-icon {
  font-size: 1.2rem; /* Size of play icon */
  color: rgba(255, 255, 255, 0.8); /* Default white color */
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5); /* Slight glow */
  transition: color 0.2s ease-in-out;
}

.glass-play-button:hover .play-icon {
  color: rgba(50, 255, 50, 1); /* Change play icon to green */
  text-shadow: 0 0 8px rgba(50, 255, 50, 1); /* Enhance glow effect */
}
</style>
