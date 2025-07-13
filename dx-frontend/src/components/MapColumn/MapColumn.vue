<script setup lang="ts">
import MiniMapComponent from "@/components/Map/MiniMapComponent.vue";
import type {MiniMap, Coordinate} from '@/api/dx-backend/api';

// Define props with default values
const props = withDefaults(defineProps<{
  mapData?: MiniMap
  coordinates?: Coordinate
}>(), {
  mapData: () => ({})
});
</script>

<template>
  <div class="container">
    <div class="map--background">
      <div class="map--container">
          <MiniMapComponent :map-data="mapData" width="100%" height="100%"></MiniMapComponent>
          <div v-if="coordinates" class="coordinates">
            x:{{ coordinates.x }}
            y:{{ coordinates.y }}
            z:{{ coordinates.z}}
            </div>
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
  position: relative;
  pointer-events: none;
}
.map--background {
  background: url("@/assets/images/RightBar/MapBG.png") no-repeat bottom center;
  background-size: cover;
  padding-bottom: 2rem;
}

.coordinates {
  position: absolute;
  bottom: 0;
  left: 0;
  padding: 0.3rem 0.5rem;
  font-size: 0.7rem;
  background-color: rgba(0, 0, 0, 0.7);
  border: 0.15rem solid rgba(22, 234, 255, 0.9);
  border-radius: 0.5rem;
  color: rgba(22, 234, 255, 0.9);
  font-weight: bold;
  display: flex;
  gap: 0.5rem;
  box-shadow: 0 0 0.5rem rgba(22, 234, 255, 0.7),
              inset 0 0 0.5rem rgba(22, 234, 255, 0.4);
  text-shadow: 0 0 0.3rem rgba(22, 234, 255, 0.7);

}


</style>