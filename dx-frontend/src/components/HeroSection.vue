<template>
  <section class="hero" @mousemove="handleMouseMove">
    <div class="background-layer layer-glow"></div>
    <div class="background-layer layer-characters" :style="charactersLayerStyle"></div>
    <div class="background-layer layer1 blending" :style="layerStyles[0]"></div>
    <div class="background-layer layer2 blending" :style="layerStyles[1]"></div>
    <div class="background-layer layer3 blending" :style="layerStyles[2]"></div>
    <div class="background-layer layer4 blending" :style="layerStyles[3]"></div>
    <div class="content">
      <TitleComponent>Dimension-X <span class="alpha-tag">alpha</span></TitleComponent>
      <LandingButtonGroup>
        <LandingButton :action="signInAction">{{ t('navigation.register') }}</LandingButton>
        <LandingButton :action="logInAction">{{ t('navigation.login') }}</LandingButton>
        <LandingButton :action="chatAction">{{ t('navigation.chatWithAI') }}</LandingButton>
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
import {useI18n} from "vue-i18n";
import {useRandomHeroBackground} from "@/composables/useRandomHeroBackground";

const opacity1 = ref(1);
const opacity2 = ref(1);
const opacity3 = ref(1);
const saturation4 = ref(100);
const currentLayer = ref(0);
const router = useRouter();
const { t } = useI18n();
const { backgroundUrl } = useRandomHeroBackground();
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

const charactersLayerStyle = computed(() => ({
  backgroundImage: backgroundUrl.value ? `url(${backgroundUrl.value})` : 'none'
}));
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
  min-height: 0;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  overflow: hidden;
  padding: 1rem;
  box-sizing: border-box;
}

.content {
  z-index: 1; /* Ensure the content is above the background layers */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  max-width: 90vw;
  width: 100%;
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
  z-index: -1;
  background-attachment: fixed;
  background-size: cover;
  background-position: center top;
  mask: radial-gradient(circle at center, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 1) 40%, rgba(0, 0, 0, 0.1) 100%);
}


.alpha-tag {
  font-size: 0.2em;
  position: absolute;
  top: -0.3em;
  right: -5em;
  background-color: rgba(0, 255, 255, 0.2);
  border: 1px solid rgba(0, 255, 255, 0.6);
  border-radius: 4px;
  padding: 2px 6px;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 0 8px rgba(0, 255, 255, 0.4);
  animation: float 3s ease-in-out infinite;
  z-index: 1;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-5px);
  }
  100% {
    transform: translateY(0px);
  }
}

/* Mobile optimizations */
@media (max-width: 479px) {
  .hero {
    padding: 1rem 0.5rem;
  }

  .content {
    gap: 1.5rem;
    max-width: 95vw;
  }

  .alpha-tag {
    font-size: 0.15em;
    top: -0.2em;
    right: -3em;
    padding: 1px 4px;
  }

  .background-layer {
    background-attachment: scroll; /* Better performance on mobile */
  }
}

/* Tablet optimizations */
@media (min-width: 480px) and (max-width: 767px) {
  .hero {
    padding: 1.5rem 1rem;
  }

  .content {
    gap: 1.75rem;
    max-width: 85vw;
  }

  .alpha-tag {
    font-size: 0.18em;
    top: -0.25em;
    right: -4em;
  }
}

/* Large screen optimizations */
@media (min-width: 1200px) {
  .hero {
    padding: 3rem 2rem;
  }

  .content {
    gap: 2.5rem;
    max-width: 80vw;
  }
}

/* Extra large screens */
@media (min-width: 1600px) {
  .hero {
    padding: 4rem 3rem;
  }

  .content {
    gap: 3rem;
    max-width: 70vw;
  }

  .alpha-tag {
    font-size: 0.25em;
    top: -0.35em;
    right: -6em;
    padding: 3px 8px;
  }
}
</style>
