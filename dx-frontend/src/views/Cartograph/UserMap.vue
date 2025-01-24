<template>
  <CurrentTurnComponent
      class="current-turn-component"
      @turnChanged="refreshMap"
  />
  <RoomInfoPanel
      :roomLabels="roomLabels"
      :roomTypes="roomTypes"
      :selectedRoom="selectedRoom"
      class="room-info-panel"
      @update-room="onRoomUpdated"
      @delete-room="onRoomDeleted"
      @unset-room="selectedRoom = null"
  />
  <MapComponent v-if="mapData" :mapData="mapData" :use-clip="false" @syncMap="refreshMap" @select-room="onRoomSelected"
                @create-room="onRoomCreated"/>
</template>

<script>
import {RoomLabel, RoomType} from "@/utils/mapData.js";

import MapComponent from "@/components/Map/MapComponent.vue";
import {WorldGameApi} from "@/api/backendService.js";
import RoomInfoPanel from "@/views/Cartograph/RoomInfoPanel.vue";
import CurrentTurnComponent from "@/components/Game/CurrentTurnComponent.vue";

export default {
  components: {CurrentTurnComponent, RoomInfoPanel, MapComponent},
  async mounted() {
    this.mapData = (await WorldGameApi.worldMapsWorldMapRetrieve()).data;
  },
  data() {
    return {
      // * Map data Object
      mapData: null,
      roomTypes: Object.values(RoomType),
      roomLabels: Object.values(RoomLabel),
      selectedRoom: null,
    };
  },
  methods: {
    async refreshMap() {
      this.mapData = (await WorldGameApi.worldMapsWorldMapRetrieve()).data;

    },
    async onRoomSelected(room) {
      console.log("Room selected", room);
      this.selectedRoom = room;
    },
    async onRoomUpdated(room) {
      this.mapData = (await WorldGameApi.worldMapsPositionUpdateCreate({
        position_id: room.position.id,
        labels: room.labels
      })).data;
      // await this.refreshMap();
    },
    async onRoomDeleted(roomId) {
      await WorldGameApi.worldMapsPositionRemoveCreate({id: roomId});
      await this.refreshMap();
    },
    async onRoomCreated(room) {
      await this.refreshMap();
    },
  },
}
</script>

<style scoped>
.current-turn-component {
  position: absolute;
  top: 5rem;
  right: 5rem;
  z-index: 100;
}

.room-info-panel {
  position: absolute;
  top: 10rem;
  left: 3rem;
  z-index: 100;
}

</style>
