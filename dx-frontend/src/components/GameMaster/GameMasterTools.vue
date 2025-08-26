<template>
  <div class="container character-info">
      <!-- ID Icon -->
      <RPGCell class="icon-button" @click="handleIdClick" title="ID (Click to copy)">
        <img src="@/assets/icons/gm-tools/id.png" alt="ID" class="icon-image" />
      </RPGCell>

      <!-- Position Icon -->
      <RPGCell class="icon-button" @click="handlePositionClick" title="Position (Click to copy)">
        <img src="@/assets/icons/gm-tools/position_v2.png" alt="Position" class="icon-image" />
      </RPGCell>

      <!-- Teleport Icon -->
      <RPGCell class="icon-button" @click="handleTeleportClick" title="Open Teleport">
        <img src="@/assets/icons/gm-tools/teleport.png" alt="Teleport" class="icon-image" />
      </RPGCell>

      <!-- Admin Icon -->
      <RPGCell class="icon-button" @click="handleAdminClick" title="Open in Django Admin">
        <img src="@/assets/icons/gm-tools/admin.png" alt="Admin" class="icon-image" />
      </RPGCell>

    <!-- NPC AI Icon -->
    <RPGCell class="icon-button" @click="handleAIManageClick" title="Manage NPC AI">
      <img src="@/assets/icons/gm-tools/npc_ai.png" alt="Admin" class="icon-image" />
    </RPGCell>

    <!-- DiceRoll Challenge Icon -->
    <RPGCell class="icon-button" @click="handleDiceRollChallenge" title="Trigger DiceRoll Challenge">
      <img src="@/assets/icons/gm-tools/dice.png" alt="Dice Roll Challenge" class="icon-image" />
    </RPGCell>

    <!-- Action Constructor Icon -->
    <RPGCell class="icon-button" @click="handleActionConstructor" title="Trigger Open Action Constructor">
      <img src="@/assets/icons/gm-tools/action-constructor.png" alt="Action Constructor" class="icon-image" />
    </RPGCell>

    <!-- Display text when clicked -->
      <RPGCell v-if="displayText" class="display-text">
        {{ displayText }}
      </RPGCell>
  </div>
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
    handleTeleportClick() {
      this.$emit('open-teleport', this.characterData);
    },
    handleDiceRollChallenge() {
      this.$emit('open-dice-roll-challenge', this.characterData);
    },
    handleAIManageClick() {
      if (!this.characterData?.id) {
        return;
      }
      this.$emit('open-npc-ai-manage', this.characterData.id);
    },
    handleAdminClick() {
      if (!this.characterData?.id) {
        this.showText('No character selected');
        return;
      }
      const baseUrl = window.location.origin;
      const adminUrl = `${baseUrl}/admin/character/character/${this.characterData.id}/change/`;
      window.open(adminUrl, '_blank', 'noopener,noreferrer');
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
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}

.icon-button {
  display: flex;
  padding: 1rem;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  height: 5rem;
  width: 5rem;
  filter: brightness(0.9);
  transition: transform 0.1s ease, filter 0.1s ease, color 0.1s ease;
}

.icon-button:hover {
  color: #fff;
  filter: brightness(1.1);
}

.icon-button:active {
  transform: scale(0.95);
}


.icon-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
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


</style>