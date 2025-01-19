<template>
  <div class="character-card">
    <!-- Character Icon with Overlay -->
    <div :style="{ backgroundImage: `url(${icon})` }" class="character-icon">
      <!-- Display Overlay Only if Details Exist -->
      <div class="icon-overlay" v-if="details && Object.keys(details).length > 0">
        <!-- Display Rank -->
        <div class="overlay-item rank" v-if="details.rankGrade">
          <span class="rank-title">Rank:</span>
          <span class="rank-value">{{ details.rankGrade }}</span>
        </div>

        <!-- Display Attributes -->
        <div
            v-for="(attribute, key) in details.attributes || {}"
            :key="key"
            class="overlay-item attribute"
        >
<!--          <span :class="`${key}-name`">-->
<!--            {{ key.charAt(0).toUpperCase() + key.slice(1) }}:-->
<!--          </span>-->
          <span>
            <span :class="`${key}-value`">
              {{ attribute.current !== undefined ? attribute.current : "xx" }}
            </span>
            /
            <span :class="`${key}-value`">
              {{ attribute.max !== undefined ? attribute.max : "xx" }}
            </span>
          </span>
        </div>
      </div>
    </div>

    <!-- Character Name -->
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
    details: {
      type: Object,
      required: false, // Details are optional
      default: null,   // Default to null if not provided
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
  position: relative;
  width: 6rem; /* Fixed width */
  height: 8rem; /* Fixed height */
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
  width: 5em; /* Fixed size */
  height: 5em;
  position: relative; /* To position the overlay */
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  border: 2px solid rgba(255, 255, 255, 0.8);
  margin-bottom: 0.5rem;
}

/* Icon Overlay Styling */
.icon-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6); /* Dark transparent background */
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.6rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 50%; /* Match icon shape */
  pointer-events: none; /* Prevent interactions */
  padding: 0.3rem;
  text-align: center;
  box-sizing: border-box;
}

.overlay-item {
  margin: 0.2em 0; /* Space between items */
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

/* Rank Styling */
.rank-title {
  color: #f8eb67; /* Purple for action points */
}

.rank-value {
  color: #f8eb67; /* Pu /* Purple for action points */
  font-weight: bold;
}

/* Attribute-specific colors */
.health-name,
.health-value {
  color: #e91e63; /* Red for health */
  font-weight: bold;
}

.energy-name,
.energy-value {
  color: #2196f3; /* Blue for energy */
  font-weight: bold;
}

.action-name,
.action-value {
  color: #9c27b0; /* Purple for action points */
  font-weight: bold;
}

/* Character Name Styling */
.character-name {
  font-size: 0.7em;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2; /* Limit to 2 lines */
  max-height: 2.4em; /* Ensure consistent height */
}
</style>
