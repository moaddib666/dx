<template>
  <RPGContainer class="container character-info">
      <!-- Rank Icon -->
      <RPGCell class="icon-button" @click="handleRankClick" title="Rank">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2L15.09 8.26L22 9L17 14L18.18 21L12 17.77L5.82 21L7 14L2 9L8.91 8.26L12 2Z"/>
        </svg>
      </RPGCell>

      <!-- Dimension Icon -->
      <RPGCell class="icon-button" @click="handleDimensionClick" title="Dimension">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path
              d="M12 2C6.48 2 2 6.48 2 12S6.48 22 12 22 22 17.52 22 12 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12S7.59 4 12 4 20 7.59 20 12 16.41 20 12 20ZM12 6C8.69 6 6 8.69 6 12S8.69 18 12 18 18 15.31 18 12 15.31 6 12 6Z"/>
        </svg>
      </RPGCell>

      <!-- ID Icon -->
      <RPGCell class="icon-button" @click="handleIdClick" title="ID (Click to copy)">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path
              d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1H5C3.89 1 3 1.89 3 3V21C3 22.11 3.89 23 5 23H19C20.11 23 21 22.11 21 21V9M19 21H5V3H13V9H19Z"/>
        </svg>
      </RPGCell>

      <!-- Position Icon -->
      <RPGCell class="icon-button" @click="handlePositionClick" title="Position (Click to copy)">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path
              d="M12 2C8.13 2 5 5.13 5 9C5 14.25 12 22 12 22S19 14.25 19 9C19 5.13 15.87 2 12 2ZM12 11.5C10.62 11.5 9.5 10.38 9.5 9S10.62 6.5 12 6.5 14.5 7.62 14.5 9 13.38 11.5 12 11.5Z"/>
        </svg>
      </RPGCell>

      <!-- Tags Icon -->
      <RPGCell class="icon-button" @click="handleTagsClick" title="Tags">
        <svg viewBox="0 0 24 24" fill="currentColor">
          <path
              d="M5.5 7A1.5 1.5 0 1 1 4 5.5A1.5 1.5 0 0 1 5.5 7ZM21.41 11.58L12.41 2.58A2 2 0 0 0 11 2H4A2 2 0 0 0 2 4V11A2 2 0 0 0 2.59 12.42L11.59 21.42A2 2 0 0 0 13 22A2 2 0 0 0 14.41 21.41L21.41 14.41A2 2 0 0 0 22 13A2 2 0 0 0 21.41 11.58Z"/>
        </svg>
      </RPGCell>

      <!-- Display text when clicked -->
      <RPGCell v-if="displayText" class="display-text">
        {{ displayText }}
      </RPGCell>
  </RPGContainer>
</template>

<script>
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import RPGCell from "@/components/RPGGrid/RPGCell.vue";

export default {
  name: 'GameMasterCharacterInfo',
  components: {RPGCell, RPGContainer},
  props: {
    characterData: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      displayText: ''
    }
  },
  methods: {
    handleNameClick() {
      const name = this.characterData?.name || 'No Character Selected';
      this.showText(`Name: ${name}`);
    },
    handleRankClick() {
      const rank = this.characterData?.rank_grade || 'N/A';
      this.showText(`Rank: ${rank}`);
    },
    handleDimensionClick() {
      const dimension = this.characterData?.dimension || 'N/A';
      this.showText(`Dimension: ${dimension}`);
    },
    handleIdClick() {
      const id = this.characterData?.id || 'N/A';
      this.copyToClipboard(id, 'ID');
    },
    handlePositionClick() {
      const position = this.characterData?.position || 'N/A';
      this.copyToClipboard(position, 'Position');
    },
    handleTagsClick() {
      const tags = this.characterData?.tags?.join(', ') || 'N/A';
      this.showText(`Tags: ${tags}`);
    },
    showText(text) {
      this.displayText = text;
      // Auto-hide after 3 seconds
      setTimeout(() => {
        this.displayText = '';
      }, 3000);
    },
    async copyToClipboard(text, label) {
      try {
        await navigator.clipboard.writeText(text);
        this.showText(`${label} copied: ${text}`);
      } catch (err) {
        console.error('Failed to copy: ', err);
        this.showText(`Failed to copy ${label}`);
      }
    }
  }
}
</script>

<style scoped>
.character-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.icon-button {
  display: flex;
  padding: 1rem;
  align-items: center;
  justify-content: center;
  color: #fada95;
  cursor: pointer;
}

.icon-button:hover {
  color: #fff;
  transform: scale(1.05);
}

.icon-button:active {
  transform: scale(0.95);
}

.icon-button svg {
  width: 24px;
  height: 24px;
  display: block;
}

.display-text {
  position: absolute;
  top: 50%;
  right: 100%;
  transform: translateY(-50%);
  margin-right: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.9);
  border: 1px solid #fada95;
  border-radius: 0.3rem;
  color: #fada95;
  font-size: 1.1rem;
  font-weight: 600;
  font-family: 'Cinzel', serif;
  white-space: nowrap;
  z-index: 1000;
  animation: slideInFromRight 0.2s ease;
}

@keyframes slideInFromRight {
  from {
    opacity: 0;
    transform: translateY(-50%) translateX(10px);
  }
  to {
    opacity: 1;
    transform: translateY(-50%) translateX(0);
  }
}

/* Make the container relative for absolute positioning of display text */
.character-info {
  position: relative;
  padding: 0;
  margin: 0;
}

.container {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
</style>