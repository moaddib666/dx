<template>
  <div class="small-char-preview">
    <div class="char-avatar">
      <img :src="char.avatar || placeholder" alt="Character Avatar" class="char-avatar-img"/>
    </div>
    <div class="char-details">
      <span class="char-name">{{ char.name }}</span>
      <span v-if="char.npc" class="char-npc">(NPC)</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SmallCharPreview',
  props: {
    char: Object,
  },
  data() {
    return {
      placeholder: 'https://via.placeholder.com/24',
    };
  },
};
</script>

<style scoped>
.char-avatar-img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #555;
}

.small-char-preview {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.1rem 0.5rem;
  border: 1px solid #444;
  border-radius: 4px;
  background: #292929;
}

.char-avatar img {
  width: 24px;
  height: 24px;
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
  font-size: 0.8rem;
}

.char-npc {
  font-size: 0.7rem;
  color: #aaa;
}
</style>
