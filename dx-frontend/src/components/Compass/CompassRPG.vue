<script setup lang="ts">
// TODO: Implement the logic for the compass component
// Arrow must dynamically rotate based on the current direction hovered
// If center section is hovered, and the stairs exists we must show the stairs instead of the arrow
// If stairs are locked, we must show the locked stairs
// If direction is active, it must show the active section
// If direction is unavailable, it must show the unavailable section
// If direction is dangerous, it must show the danger section
// if direction is locked, it must show the locked section
// The pressed section must be emitted to the parent component
import {WorldPosition} from "@/api/dx-backend";

const props = defineProps({
  position: WorldPosition
});

const emit = defineEmits(
    ['move']
);

</script>

<template>
  <div class="compass--holder">
    <div class="compass--container">
      <div class="compass--background">
        <div class="compass--background--real-center arrow arrow-up-right" v-if="true">
        </div>
        <div class="compass--background--stairs stairs stairs--locked" v-if="false">
          <div class="stairs-arrow stairs-arrow-down"></div>
          <div class="stairs-arrow stairs-arrow-up"></div>
        </div>
      </div>
      <div class="compass--outer--mask">
        <div class="compass--outer">
          <div class="compass--outer--section--top--left compass--outer--section active"></div>
          <div class="compass--outer--section--top--center compass--outer--section danger"></div>
          <div class="compass--outer--section--top--right compass--outer--section"></div>
          <div class="compass--outer--section--middle--left compass--outer--section"></div>
          <div class="compass--outer--section--middle--center compass--outer--section"></div>
          <div class="compass--outer--section--middle--right compass--outer--section"></div>
          <div class="compass--outer--section--bottom--left compass--outer--section"></div>
          <div class="compass--outer--section--bottom--center compass--outer--section"></div>
          <div class="compass--outer--section--bottom--right compass--outer--section locked"></div>
        </div>
      </div>
      <div class="compass--inner--mask">
        <div class="compass--inner danger">
        </div>
      </div>

    </div>
  </div>

</template>

<style scoped>
.compass--holder {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.compass--container {
  min-width: 15rem;
  min-height: 15rem;
  background-image: url('@/assets/images/compass/compass.png');
  background-size: cover;
  background-position: center;
  position: relative;
}

.compass--outer--mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  mask-image: url('@/assets/images/compass/compass-mask.png');
  mask-size: cover;
  mask-position: center;
  -webkit-mask-position: center;
  -webkit-mask-image: url('@/assets/images/compass/compass-mask-selectors.png');
  -webkit-mask-size: cover;
}

.compass--outer {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);

}

.compass--outer--section--middle--center {
  margin: 0.5rem auto;
}

.compass--outer--section {
  transition: opacity 0.3s ease, transform 0.3s ease;
  mix-blend-mode: multiply;
}

.compass--outer--section:hover {
  opacity: 1;
  transform: scale(1.05);

}

.active {
  cursor: pointer;
  background: linear-gradient(90deg, rgba(22, 234, 255, 1) 0%, rgba(0, 212, 255, 1) 100%);
}

.locked {
  cursor: pointer;
  background: linear-gradient(90deg, rgba(255, 255, 0, 1) 0%, rgba(255, 165, 0, 1) 100%);
}

.unavailable {
  background: linear-gradient(90deg, rgba(128, 128, 128, 1) 0%, rgba(192, 192, 192, 1) 100%);
}

.danger {
  cursor: pointer;
  background: linear-gradient(90deg, rgba(255, 0, 0, 1) 0%, rgba(255, 69, 0, 1) 100%);
}

.compass--inner--mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  mask-image: url('@/assets/images/compass/compass-mask-circle.png');
  mask-size: cover;
  mask-position: center;
  -webkit-mask-image: url('@/assets/images/compass/compass-mask-circle.png');
  -webkit-mask-size: cover;
}

.compass--inner {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  opacity: 0.5;
  mix-blend-mode: multiply;
}

.compass--background {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 45%;
  height: 45%;
  transform: translate(-50%, -50%);
  z-index: -1; /* Ensure it stays behind other elements */
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
}

.compass--background--real-center {
  width: 50%;
  height: 50%;
  border-radius: 50%;
}

.compass--background--stairs {
  width: 100%;
  height: 100%;
  background-size: cover;
  position: relative;
}

.arrow {
  background: url('@/assets/images/compass/compass-arrow.png') no-repeat center center;
  background-size: contain;
  transition: transform 0.3s ease;
}

.arrow-up {
  transform: rotate(0deg);
}

.arrow-up-left {
  transform: rotate(45deg);
}

.arrow-up-right {
  transform: rotate(-45deg);
}

.arrow-down {
  transform: rotate(180deg);
}

.arrow-down-left {
  transform: rotate(135deg);
}

.arrow-left {
  transform: rotate(90deg);
}

.arrow-down-right {
  transform: rotate(-135deg);
}

.arrow-right {
  transform: rotate(-90deg);
}

.arrow:hover {
  cursor: pointer;
  transform: scale(1.1);
}


.stairs {
  background: url('@/assets/images/compass/compass-stairs.png') no-repeat center center;
  background-size: 50% 50%;
}

.stairs-arrow {

}

.stairs--locked {
  filter: grayscale(100%);
}

.stairs-arrow-down {
  background: url('@/assets/images/compass/compass-stairs-arrow-down.png') no-repeat center center;
  transform: rotate(0deg);
  background-size: contain;
  width: 20%;
  height: 20%;
  position: absolute;
  top: 50%;
  left: 20%;
}

.stairs-arrow-up {
  background: url('@/assets/images/compass/compass-stairs-arrow-down.png') no-repeat center center;
  transform: rotate(180deg);
  background-size: contain;
  width: 20%;
  height: 20%;
  position: absolute;
  top: 20%;
  right: 20%;
}


</style>