<template>
  <div class="player-profile">
    <!-- Avatar and Path Overlay -->

    <div class="avatar-container">

      <img v-if="player.biography.avatar" :src="player.biography.avatar" alt="Player Avatar" class="avatar"/>
      <img v-else src="@/assets/images/avatar/placeholder.webp" alt="Player Avatar" class="avatar"/>

      <div class="path-overlay" :title="pathTooltip">
        <modificator-holder class="modificator-overlay" :modificators="modificators"/>
        <img :src="player.path.icon" alt="Path Icon" class="path-icon"/>
      </div>
      <h2 class="player-name">{{ player.name }}</h2>
    </div>

    <!-- Details Section -->
    <div class="details-section">
      <RankComponent :rank="player.rank" :experience="player.experience"/>
      <TagsComponent :tags="player.tags"/>
    </div>
  </div>
</template>

<script>
import TagsComponent from "@/components/Player/TagsComponent.vue";
import RankComponent from "@/components/Rank/RankComponent.vue";
import ModificatorHolder from "@/components/Modificator/ModificatorHolder.vue";

export default {
  name: "PlayerProfile",
  components: {
    ModificatorHolder,
    RankComponent,
    TagsComponent,
  },
  props: {
    player: {
      type: Object,
      required: true,
    },
    modificators: {
      type: Array,
      required: true,
    },
  },
  computed: {
    pathTooltip() {
      return `${this.player.path.name}: ${this.player.path.description}`;
    },
  },
};
</script>

<style scoped>
.player-profile {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: rgba(0, 0, 0, 0.8);
  padding: 1rem;
  border-radius: 0.5rem;
  color: white;
  font-family: "Roboto", sans-serif;
  margin: auto;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
}

.avatar-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.avatar {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #00e5ff;
}

.path-overlay {
  position: absolute;
  bottom: 0.2rem;
  right: 0.2rem;
  width: 1.5rem;
  height: 1.5rem;

  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;

  cursor: pointer;
  transition: transform 0.2s;
}

.modificator-overlay {
  font-size: 0.4rem;
  border-radius: 50%;
  border: 2px solid #ffffff;
}

.path-icon {
  width: 1.2rem;
  height: 1.2rem;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #ffffff;
}

.player-name {
  font-size: 1rem;
  font-weight: bold;
  margin-top: 0.5rem;
  color: #ffffff;
}

.details-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
