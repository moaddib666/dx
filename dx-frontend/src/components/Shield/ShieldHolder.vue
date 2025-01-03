<template>
  <div class="shield-holder">
    <ShieldVisualizer
        v-for="(shieldData, index) in shields"
        :key="index"
        :shield="shieldData.shield"
        :level="shieldData.level"
        :cyclesLeft="shieldData.cycles_left"
    />
  </div>
</template>

<script>
import ShieldVisualizer from "@/components/Shield/ShieldVisualizer.vue";

export default {
  name: "ShieldHolder",
  components: {
    ShieldVisualizer,
  },
  props: {
    shields: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.shield-holder {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  align-items: center;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
}
</style>
