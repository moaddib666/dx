<script setup lang="ts">
interface Props {
  avatarUrl?: string;
  statsIncrementIcon: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  avatarUrl: 'https://images.squarespace-cdn.com/content/v1/605e90f9c17ee25104dba783/1684973142360-DGM2VVQ5D1356WLMWZQD/Screenshot+2023-05-24+170440.png?format=1500w',
  statsIncrementIcon: false
});
</script>

<template>
  <div class="rpg-avatar" title="Character Info">
    <div class="rpg-avatar__wrapper">
      <img
          :src="props.avatarUrl"
          alt="Character Avatar"
          class="rpg-avatar__image"
          sizes="content"
      />
      <div
        v-if="props.statsIncrementIcon"
        class="rpg-avatar__increment-overlay"
        title="Stats can be incremented"
      >
        <span class="rpg-avatar__increment-symbol">+</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rpg-avatar {
  width: 10rem;
  height: 15rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  background: url("@/assets/rpg_bars/rpg_avatar_border.png") no-repeat center;
  background-size: cover;

  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;

}

.rpg-avatar__wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: start;
  background-size: cover;
  mask: url("@/assets/rpg_bars/rpg_avatar_border_mask_invented.png") no-repeat center;
  mask-size: cover;
}

.rpg-avatar__image {
  width: 65%;
  height: 60%;
  object-fit: cover;
  object-position: center;
  position: absolute;
  top: 10%;
}

.rpg-avatar__increment-overlay {
  position: absolute;
  top: 10%;
  left: 17.5%;
  width: 65%;
  height: 60%;
  background: rgba(255, 215, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: gentle-pulse 1.5s ease-in-out infinite;
  z-index: 5;
}

.rpg-avatar__increment-symbol {
  font-size: 32px;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  text-shadow:
    0 2px 4px rgba(0, 0, 0, 0.8),
    0 0 8px rgba(255, 215, 0, 0.6);
  filter: drop-shadow(0 0 4px rgba(255, 215, 0, 0.5));
}

@keyframes gentle-pulse {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.5;
  }
}

</style>