<template>
  <div class="small-char-preview">
    <img :src="avatarLink" alt="Character Avatar" class="char-avatar-img"/>
    <div class="char-details">
      <span class="char-name">{{ char.name }}</span>
      <span v-if="char.npc" class="char-npc">(NPC)</span>
    </div>
  </div>
</template>

<script>
import {CharacterInfoGameService} from "@/services/characterInfoService.js";

export default {
  name: 'SmallCharPreview',
  props: {
    char: Object,
    gmMode: Boolean,
  },
  async created() {
    this.info = await CharacterInfoGameService.getCharacterInfo(this.char.id, this.gmMode);
    this.avatarLink = await CharacterInfoGameService.getAvatarUrl(this.char.id, this.gmMode) || this.placeholder;
    if (this.info) {
      this.char.name = this.info.name;
      this.char.npc = this.info.npc;
    }
  },
  computed: {},
  data() {
    return {
      placeholder: 'https://via.placeholder.com/24',
      avatarLink: null,
    };
  },
};
</script>

<style scoped>
.char-avatar-img {
  height: 2em;
  width: 2em;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #555;
}

.small-char-preview {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.1rem 0.5rem;
  border-radius: 4px;
}

.char-avatar img {
  width: 2em;
  height: 2em;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #555;
}

.char-details {
  display: flex;
  flex-direction: column;
}

.char-name {
  font-weight: bold;
  color: #e0e0e0;
  font-size: 0.5rem;
}

.char-npc {
  font-size: 0.5rem;
  color: #aaa;
}
</style>
