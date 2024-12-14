<script>
export default {
  name: "PlayerAvatarComponent",
  props: {
    avatarUrl: {
      type: String,
      required: true
    },
    playerName: {
      type: String,
      required: true
    },
    rank: {
      type: Number,
      required: true
    }
  }
}
</script>

<template>
  <div class="avatar-container">
    <div class="hexagon avatar-bg">
      <img :src="avatarUrl" alt="Player Avatar" class="avatar-image" />
    </div>
    <div class="player-name">{{ playerName }}</div>
  </div>
</template>

<style scoped>
.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  height: 100%;
}

.hexagon {
  display: flex;
  justify-content: center;
  align-items: center;
  clip-path: polygon(25% 6.7%, 75% 6.7%, 100% 50%, 75% 93.3%, 25% 93.3%, 0% 50%);
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
}

.avatar-image {
  object-fit: cover;
  scale: 0.6;
}

.avatar-bg {
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  overflow: hidden;
}

.player-name {
  z-index: 5;
  margin-top: -3vh;
  font-family: 'Orbitron', sans-serif;
  font-size: 16px;
  color: #fff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
  text-align: center;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 1vh 4vh;
  border-radius: 5px;
}
</style>
