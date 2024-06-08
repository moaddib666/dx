<template>
  <section class="hero" @mousemove="handleMouseMove">
    <div class="background-layer layer1" :style="layerStyles[0]"></div>
    <div class="background-layer layer2" :style="layerStyles[1]"></div>
    <div class="background-layer layer3" :style="layerStyles[2]"></div>
    <div class="background-layer layer4" :style="layerStyles[3]"></div>
    <div class="login-form">
      <form>
        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />
        <button type="submit" class="primary-btn">Login</button>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const opacity1 = ref(1);
const opacity2 = ref(1);
const opacity3 = ref(1);
const saturation4 = ref(100);

var currentZone = 0;
var currentOpacity = 1;

const getMousePosition = (event) => {
  const { clientX, clientY, currentTarget } = event;
  const { offsetWidth, offsetHeight } = currentTarget;

  const xPercentage = clientX / offsetWidth;
  // const yPercentage = clientY / offsetHeight;
  // const percentage = Math.max(xPercentage, yPercentage);

  return xPercentage
};

const calculateSaturation = (zone, percentage) => {
  if (zone !== 3 ) {
    return 0;
  }
  return percentage * 0.7 * 100;
};

const handleMouseMove = (event) => {
  const percentage = getMousePosition(event);
  const {zone, zone_percentage_value} = getZones(percentage, 4);
  currentZone = zone;
  currentOpacity = zone_percentage_value;
  console.log(currentZone, currentOpacity);
  opacity1.value = calculateZoneOpacity(0, currentZone, currentOpacity);
  opacity2.value = calculateZoneOpacity(1, currentZone, currentOpacity);
  opacity3.value = calculateZoneOpacity(2, currentZone, currentOpacity);
  saturation4.value = calculateSaturation(3, percentage);

};

const getZones = (percentage, zone_count) => {
  const zone_percentage = 1 / zone_count;
  const zone = Math.floor(percentage / zone_percentage);
  const zone_percentage_value = 1 - (percentage - zone * zone_percentage) / zone_percentage;
  return { zone, zone_percentage_value };
};

const calculateZoneOpacity = (zone, currentZone, opacity) => {
  if (zone === currentZone) {
    return opacity;
  } else if (zone > currentZone) {
    return 1
  } else {
    return 0
  }
}

const layerStyles = computed(() => [
  { opacity: opacity1.value, transition: 'opacity 0.5s ease' },
  { opacity: opacity2.value, transition: 'opacity 0.5s ease' },
  { opacity: opacity3.value, transition: 'opacity 0.5s ease' },
  { filter: `saturate(${saturation4.value}%)`, transition: 'filter 0.5s ease' },
]);
</script>

<style scoped>
.hero {
  position: relative;
  text-align: center;
  padding: 150px 0;
  overflow: hidden;
}

.background-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
}

.layer1 {
  background-image: url('@/assets/images/dx-1.webp');
  z-index: 100;
}

.layer2 {
  background-image: url('@/assets/images/dx-2.webp');
  z-index: 90;
}

.layer3 {
  background-image: url('@/assets/images/dx-3.webp');
  z-index: 80;
}

.layer4 {
  background-image: url('@/assets/images/dx-4.webp');
  z-index: 70;
}

.login-form {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.7);
  padding: 20px;
  border-radius: 10px;
  z-index: 5;
}

.login-form form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.login-form input {
  padding: 10px;
  border: none;
  border-radius: 5px;
}

.primary-btn {
  background-color: var(--electric-blue);
  color: #FFFFFF;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 18px;
}

.primary-btn:hover {
  background-color: #1C86EE;
}

.secondary-btn {
  background-color: var(--neon-pink);
  color: #FFFFFF;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 18px;
}

.secondary-btn:hover {
  background-color: #EE1289;
}
</style>
