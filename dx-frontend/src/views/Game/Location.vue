<template>
  <div class="location-view">
    <!-- Background View -->
    <BackgroundView :key="position.id" :background="position.image" style="display: flex; position: fixed; z-index: -1">
    </BackgroundView>
    <!-- Compass Component -->
    <CompassComponent
        :connections="this.activeConnections"
        centerAction="true"
        centerLabel="Up"
        @move="handleMove"
    />

    <CharacterCardHolder
        :characters="activeCharacters"
        :selectedCharacterId="selectedCharacterId"
        @characterSelected="handleCharacterSelected"
    />

    <PlayerComponent
        :player="playerInfo"
        :playerImage="playerGeneralInfo.biography.avatar"
    />
  </div>

</template>

<script>
import CompassComponent from '@/components/Game/Location/Compass.vue';
import {CharacterGameApi, WorldGameApi} from "@/api/backendService.js";
import CharacterCardHolder from "@/components/Game/Location/CharacterCardHolder.vue";
import PlayerComponent from "@/components/Game/Location/PlayerComponent.vue";
import BackgroundView from "@/components/Game/Location/BackgroundView.vue";

export default {
  name: 'LocationView',
  components: {
    BackgroundView,
    PlayerComponent,
    CharacterCardHolder,
    CompassComponent
  },
  data() {
    return {
      position: null,
      connections: null,
      playerInfo: null,
      playerGeneralInfo: null,
      characters: [],
      selectedCharacterId: 'f3c4216f-cbaa-4792-b6e6-1cedd502deae',
    };
  },
  computed: {
    activeCharacters() {
      return this.characters
    },
    activeConnections() {
      if (!this.connections) return [];
      console.log(this.connections);
      // this.connections is an object, so we need to convert it to an array
      return Object.values(this.connections);
    },
  },
  async created() {
    await this.getCurrentPositionInfo();
    await this.getPlayerInfo();
  },
  methods: {
    async handleMove(direction) {
      const move_direction = this.connections[direction]
      const new_postion_id = move_direction.to_position;
      await WorldGameApi.worldPositionMoveToPositionCreate(new_postion_id);
      await this.getCurrentPositionInfo();
    },
    async resolveCharacter(characterId) {
      const data = await CharacterGameApi.characterRetrieve(characterId);
      this.characters.push(data.data);
    },
    async getCurrentPositionInfo() {
      this.position = (await WorldGameApi.worldPositionCurrentRetrieve()).data;
      this.connections = {}
      this.position.connections.forEach((conn) => {
        this.connections[conn.direction] = conn;
      });
      this.characters = [];
      this.position.characters.forEach((char) => {
        this.resolveCharacter(char);
      });
    },
    async getPlayerInfo() {
      this.playerInfo = (await CharacterGameApi.characterCharacterInfoRetrieve()).data;
      if (this.playerGeneralInfo === null) {
        this.playerGeneralInfo = (await CharacterGameApi.characterRetrieve(this.playerInfo.id)).data;
      }
    }
  },
};
</script>

<style scoped>
</style>