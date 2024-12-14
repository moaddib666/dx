<script>
import PlayerAvatarComponent from "@/components/Game/Fight/PlayerAvatarComponent.vue";
import BarGroupComponent from "@/components/Game/Fight/BarGroupComponent.vue";
import {PlayerFightParticipant} from "@/models/Player";

export default {
  name: "EnemyComponent",
  components: {BarGroupComponent, PlayerAvatarComponent},
  props: {
    player: {
      type: PlayerFightParticipant,
      required: true
    },
    selected: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    url: function() {
      // Use Vite's import.meta.glob to dynamically load the image
      const images = import.meta.glob('@/assets/images/player_avatar.png');
      // Extract the key from the object returned by import.meta.glob
      const imagePath = Object.keys(images)[0];
      return imagePath.replace(/^@/, '');
    },
  },
  methods: {
    toggleSelection() {
      const selected = !this.selected;
      this.$emit('selection', this.player, selected);
    }
  }
}
</script>

<template>
  <div @click="toggleSelection" class="enemy" id="player" v-if="player" >
    <div class="enemy-main horizontal-layout" :class="{ selected: selected }">
      <BarGroupComponent :attributes="player.attributes"></BarGroupComponent>
      <PlayerAvatarComponent :rank="1" :avatar-url="url" :player-name="player.name"></PlayerAvatarComponent>
    </div>
  </div>
</template>

<style scoped>
.enemy {
  cursor: pointer;
}
.enemy-main {
  height: 7vh;
  display: flex;
  justify-content: space-between;
  align-items: end;
  align-content: flex-end;
  transition: all 0.3s;
}
.enemy-main:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  margin-left: -3vh;
  height: 10vh;
}

.bar-section {
  display: flex;
  margin: 1vh 2vh;
  width: 5lh;
}

.selected {
  animation: border-glow 1.5s infinite;
  border: 2px solid cyan;
  border-radius: 8px;
}

@keyframes border-glow {
  0% {
    box-shadow: 0 0 5px cyan;
  }
  50% {
    box-shadow: 0 0 20px cyan;
  }
  100% {
    box-shadow: 0 0 5px cyan;
  }
}


</style>