<script>
import PlayerAvatarComponent from "@/components/Game/Fight/PlayerAvatarComponent.vue";
import BarGroupComponent from "@/components/Game/Fight/BarGroupComponent.vue";

export default {
  name: "PlayerComponent",
  components: {BarGroupComponent, PlayerAvatarComponent},
  props: {
    player: {
      type: Object,
      required: true
    }
  },
  computed: {
    url: function () {
      // Use Vite's import.meta.glob to dynamically load the image
      const images = import.meta.glob('@/assets/images/player_avatar.png');
      // Extract the key from the object returned by import.meta.glob
      const imagePath = Object.keys(images)[0];
      return imagePath.replace(/^@/, '');
    },
  },
  methods: {
    blink() {
      console.log('Blinking player:', this.player);
    },
    blinkattributes() {
      console.log('Blinking player attributes:', this.player.attributes);
      this.$refs.attributesComponent.blink();
    }
  }
}
</script>

<template>
  <div class="player" v-if="player">
    <div class="player-main horizontal-layout">
      <PlayerAvatarComponent :rank="1" :avatar-url="url" :player-name="player.name"></PlayerAvatarComponent>
      <BarGroupComponent ref="attributesComponent" :attributes="player.attributes"></BarGroupComponent>
    </div>
  </div>
</template>

<style scoped>
.player-main {
  height: 20vh;
  max-width: 60%;
}

</style>