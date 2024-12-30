<template>
  <div class="effects-holder">
    <EffectItem
        v-for="(effectData, index) in effects"
        :key="index"
        :effectData="effectData"
    />
  </div>
</template>

<script>
import EffectItem from "./EffectItem.vue"; // Import the EffectItem component

export default {
  name: "EffectsHolder",
  components: {
    EffectItem,
  },
  props: {
    effects: {
      type: Array,
      required: true, // Expects an array of effect objects
    },
  },
};
</script>

<style scoped>
.effects-holder {
  display: flex;
  gap: 0.5rem; /* Space between effects */
  font-family: "Roboto", sans-serif;
  font-size: 1rem;
  flex: 1;
  height: 4rem;
  background: rgba(0, 0, 0, 0.2); /* Subtle background */
  padding: 0.5rem;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.9); /* Bright text for visibility */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow-x: auto; /* Allow horizontal scrolling if effects overflow */
}

.effects-holder::-webkit-scrollbar {
  width: 1rem;
}

.effects-holder::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.effects-holder::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.4);
}
</style>
