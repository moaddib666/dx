<template>
  <MiniMapComponent v-if="mapData" :mapData="mapData"/>
</template>

<script>

import MiniMapComponent from "@/components/Map/MiniMapComponent.vue";
import {WorldGameApi} from "@/api/backendService.js";

export default {
  components: {MiniMapComponent},
  async mounted() {
    this.mapData = (await WorldGameApi.worldMapsMiniMapRetrieve()).data;
  },
  data() {
    return {
      mapData: null,
    }
  },
}
</script>
