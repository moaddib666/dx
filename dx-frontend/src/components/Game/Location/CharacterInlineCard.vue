<template>
  <div class="character-inline-card">
    <div :style="{ backgroundImage: `url(${icon})` }" class="character-icon"></div>
    <div class="character-name">{{ name }}</div>
  </div>
</template>

<script>
export default {
  name: "CharacterInlineCard",
  props: {
    name: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
/* Character Inline Card Container */
.character-inline-card {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 12rem; /* Compact horizontal width */
  height: 3rem; /* Compact vertical height */
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(6px);
  box-sizing: border-box;
  padding: 0.5rem;
  gap: 0.5rem; /* Spacing between icon and name */
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  cursor: pointer;
}

.character-inline-card:hover {
  transform: scale(1.02);
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
}

/* Character Icon Styling */
.character-icon {
  width: 2.5rem; /* Smaller circular size */
  height: 2.5rem;
  background-size: cover;
  background-position: center;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.8);
}

/* Character Name Styling */
.character-name {
  font-size: 0.9rem; /* Text size aligned with icon */
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap; /* Ensures text remains in one line */
  flex-grow: 1; /* Allows name to take remaining space */
  text-align: left; /* Align text to the left */
}
</style>
