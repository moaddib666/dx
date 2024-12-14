<script>
import BarComponent from "@/components/Game/Fight/BarComponent.vue";

export default {
  name: "BarGroupComponent",
  components: {BarComponent},
  props: {
    attributes: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isBlinking: false
    }
  },
  methods: {
    blink() {
      console.log('Blinking attributes:', this.attributes);
      this.isBlinking = true;
      setTimeout(() => {
        this.isBlinking = false;
      }, 500);
    }
  }
}
</script>

<template>
  <div class="bar-section vertical-layout" :class="isBlinking ? 'blink': ''">
    <BarComponent type="health" :currentValue="attributes.health" :maxValue="attributes.max_health" />
    <BarComponent type="energy" :currentValue="attributes.energy" :maxValue="attributes.max_energy" />
    <BarComponent v-if="attributes.ap" type="ap" :currentValue="attributes.ap" :maxValue="attributes.max_ap" />
  </div>
</template>

<style scoped>
.bar-section {
  display: flex;
  margin: 1vh 2vh;
  width: 20lh;
}
.blink {
  animation: blinker 0.2s linear infinite;
}

@keyframes blinker {
  50% {
    background: rgba(255, 0, 0, 0.5);
    margin-left: 0.1vh;
  }
}

</style>