<template>
  <section class="hero" @mousemove="handleMouseMove">
    <div class="background-layer layer-glow"></div>
    <div class="background-layer layer-characters"></div>
    <div class="background-layer layer1 blending" :style="layerStyles[0]"></div>
    <div class="background-layer layer2 blending" :style="layerStyles[1]"></div>
    <div class="background-layer layer3 blending" :style="layerStyles[2]"></div>
    <div class="background-layer layer4 blending" :style="layerStyles[3]"></div>
    <div class="content">
      <TitleComponent>Dimension-X</TitleComponent>
      <LandingButtonGroup>
        <LandingButton :action="signInAction">Register</LandingButton>
        <LandingButton :action="logInAction">Log In</LandingButton>
        <LandingButton :action="chatAction">Chat with AI</LandingButton>
      </LandingButtonGroup>
      <!--      <LoginForm :layer="currentLayer" />-->
    </div>
  </section>
</template>

<script setup lang="ts">
import {ref, computed} from 'vue';
import TitleComponent from "@/components/TitleComponent.vue";
import LandingButton from "@/components/btn/LandingButton.vue";
import LandingButtonGroup from "@/components/btn/LandingButtonGroup.vue";
import {useRouter} from "vue-router";

const opacity1 = ref(1);
const opacity2 = ref(1);
const opacity3 = ref(1);
const saturation4 = ref(100);
const currentLayer = ref(0);
const router = useRouter();
const chatAction = () => {
  window.open('https://chatgpt.com/g/g-VIcO0L3rg-dimension-x-game-architect', '_blank');
};
const signInAction = () => {
  // FIXME: Redirect to register page

  router.push({name: 'Register'});
};
const logInAction = () => {
  // FIXME: Redirect to login page
  router.push({name: 'Login'});
}
const getMousePosition = (event) => {
  const {clientX, currentTarget} = event;
  const {offsetWidth} = currentTarget;
  return clientX / offsetWidth;
};

const calculateSaturation = (zone, percentage) => {
  if (zone !== 3) return 100;
  return 100 - percentage * 70;
};

const handleMouseMove = (event) => {
  const percentage = getMousePosition(event);
  const {zone, zonePercentageValue} = getZones(percentage, 4);

  opacity1.value = calculateZoneOpacity(0, zone, zonePercentageValue);
  opacity2.value = calculateZoneOpacity(1, zone, zonePercentageValue);
  opacity3.value = calculateZoneOpacity(2, zone, zonePercentageValue);
  saturation4.value = calculateSaturation(zone, percentage);
  currentLayer.value = zone;
};

const getZones = (percentage, zoneCount) => {
  const zonePercentage = 1 / zoneCount;
  const zone = Math.floor(percentage / zonePercentage);
  const zonePercentageValue = 1 - (percentage - zone * zonePercentage) / zonePercentage;
  return {zone, zonePercentageValue};
};

const calculateZoneOpacity = (zone, currentZone, opacity) => {
  if (zone === currentZone) return opacity;
  return zone > currentZone ? 1 : 0;
};

const layerStyles = computed(() => [
  {opacity: opacity1.value, transition: 'opacity 1s ease'},
  {opacity: opacity2.value, transition: 'opacity 1s ease'},
  {opacity: opacity3.value, transition: 'opacity 1s ease'},
  {filter: `saturate(${saturation4.value}%)`, transition: 'filter 1s ease'},
]);
</script>

<style scoped>
html, body {
  height: 100%;
  margin: 0;
  display: flex;
  flex-direction: column;
}

.hero {
  position: relative;
  width: 100%;
  height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  overflow: hidden;
}

.content {
  z-index: 1; /* Ensure the content is above the background layers */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.background-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: top center;
  transition: opacity 1s ease, filter 1s ease;
}

.blending {
  background-blend-mode: multiply;
  isolation: isolate;
}

.layer-characters {
  background-image: url('@/assets/images/dx-chars.webp'), url('@/assets/images/dx-chars.webp');
  opacity: 0.2;
  z-index: -1;
  background-blend-mode: soft-light;
}

.layer-glow {
  background-image: url('@/assets/images/dx-chars.webp'), url('@/assets/images/dx-chars.webp');
  opacity: 0.3;
  z-index: 0;
  background-blend-mode: multiply;
  filter: saturate(400%) brightness(1.1);
}

.layer1 {
  background-image: url('@/assets/images/dx-chars.webp'), url('@/assets/images/dx-1.webp');
  z-index: -2;
}

.layer2 {
  background-image: url('@/assets/images/dx-chars.webp'), url('@/assets/images/dx-2.webp');
  z-index: -3;
}

.layer3 {
  background-image: url('@/assets/images/dx-chars.webp'), url('@/assets/images/dx-3.webp');
  z-index: -4;
}

.layer4 {
  background-image: url('@/assets/images/dx-chars.webp'), url('@/assets/images/dx-4.webp');
  z-index: -5;
}
</style>
