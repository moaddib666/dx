<template>
  <div class="character-card">
    <div :style="{ backgroundImage: `url(${icon})` }" class="character-icon"></div>
    <div class="character-name">{{ name }}</div>
  </div>
</template>

<script>
export default {
  name: "CharacterCard",
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
/* Character Card Container */
.character-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  width: 8rem; /* Fixed width */
  height: 10rem; /* Fixed height */
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 0.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(6px);
  box-sizing: border-box;
  padding: 0.5rem;
  text-align: center;
  transition: transform 0.2s ease-in-out;
  cursor: pointer;
}

.character-card:hover {
  transform: scale(1.05);
}

/* Character Icon Styling */
.character-icon {
  width: 5rem; /* Fixed size for consistency */
  height: 5rem;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  border: 2px solid rgba(255, 255, 255, 0.8);
  margin-bottom: 0.5rem;
}

/* Character Name Styling */
.character-name {
  font-size: 1rem; /* Scalable font size */
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.2; /* Control line spacing */
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2; /* Limit to 2 lines */
  max-height: 2.4rem; /* Ensure consistent height */
}
</style>
