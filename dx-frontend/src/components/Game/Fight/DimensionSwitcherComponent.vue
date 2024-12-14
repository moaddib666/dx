<template>
  <div class="dimension-switcher horizontal-layout" v-if="dimension && activated">
    <div class="dimension-overlay prev" @click="switchDimension(prevDimensionNumber)" v-if="hasPrevDimension">
      <span class="label">Prev</span>
    </div>
    <div class="dimension-overlay current" @click="cancelMovement" >
        <span class="label">Cancel</span>
    </div>
    <div class="dimension-overlay next" @click="switchDimension(nextDimensionNumber)" v-if="hasNextDimension" >
      <span class="label">Next</span>
    </div>
  </div>
</template>

<script >
export default {
  name: 'DimensionSwitcherComponent',
  props: {
    dimension: {
      type: Object,
    },
    activated: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    dimensionNumber() {
      return this.dimension ? this.dimension : 1;
    },
    nextDimensionNumber() {
      return this.dimensionNumber + 1;
    },
    prevDimensionNumber() {
      return this.dimensionNumber - 1;
    },
    hasPrevDimension() {
      return this.prevDimensionNumber > 0;
    },
    hasNextDimension() {
      return this.nextDimensionNumber < 11;
    }
  },
  methods: {
    switchDimension(direction) {
      this.$emit('switch', direction);
    },
    cancelMovement() {
      this.$emit('abort');
    }
  }
}
</script>

<style scoped>
.dimension-switcher {
  position: absolute;
  z-index: 10;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
  font-family: 'Orbitron', sans-serif;
}

.dimension-overlay {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2em;
  color: #fff;
  cursor: pointer;
  height: 100%;

  backdrop-filter: blur(0.2rem);
  box-shadow: 5vh 5vh 10vh rgba(0, 0, 0, 0.5);
  transition: flex 0.3s ease-in-out;
}

.label {
  text-shadow: 0 0 10px rgb(22, 234, 255);
  font-size: 2rem;
}
.dimension-overlay:hover {
  backdrop-filter: blur(0rem);
  flex: 5;
}

.prev {
  background: rgba(255, 255, 255, 0.3); /* Light background for previous dimension */
  opacity: 0.8;
}

.prev:hover {
  filter: brightness(1.1) saturate(1.5);
  opacity: 1;
  background: linear-gradient(45deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0));
}

.current {
}

.current:hover {
}

.next {
  filter: saturate(0.5); /* Less brightness and less saturation */
  opacity: 0.8;
}

.next:hover {
  background: linear-gradient(45deg, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 1));
  opacity: 1;
}

</style>
