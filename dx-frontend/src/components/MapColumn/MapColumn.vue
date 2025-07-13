<script setup lang="ts">
import MiniMapComponent from "@/components/Map/MiniMapComponent.vue";
import type {MiniMap} from '@/api/dx-backend/api';

// Define props with default values
const props = withDefaults(defineProps<{
  mapData?: MiniMap
}>(), {
  mapData: () => ({})
});
</script>

<template>
  <div class="container">
    <div class="map--background">
      <div class="map--container">
          <MiniMapComponent :map-data="mapData" width="100%" height="100%"></MiniMapComponent>
      </div>
    </div>
    <div class="map--overlay"></div>
  </div>
</template>

<style scoped>
.map--container {
  aspect-ratio: 1 / 1;
  z-index: 2;
  display: flex;
  justify-content: center;
  align-items: center;
}
.map--background {
  background: url("@/assets/images/RightBar/MapBG.png") no-repeat bottom center;
  background-size: cover;
  padding-bottom: 2rem;
}


</style>