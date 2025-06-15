<template>
  <div class="glitch-container">
    <slot></slot>
    <GlitchEffect
        :appearChance="appearChance"
        :containerSelector="containerSelector"
        :maxSize="maxSize"
        :minSize="minSize"
        :onGlitchClick="handleGlitchClick"
    />
  </div>
</template>

<script>
import GlitchEffect from './GlitchEffect.vue';

export default {
  name: "GlitchContainer",
  components: {
    GlitchEffect
  },
  props: {
    containerSelector: {
      type: String,
      default: ".glitch-container"
    },
    minSize: {
      type: Number,
      default: 2
    },
    maxSize: {
      type: Number,
      default: 15
    },
    appearChance: {
      type: Number,
      default: 0.3
    },
    onGlitchFound: {
      type: Function,
      default: null
    }
  },
  data() {
    return {
      glitchesFound: 0
    };
  },
  methods: {
    handleGlitchClick() {
      this.glitchesFound++;

      // Emit an event that can be listened to by parent components
      this.$emit('glitch-found', this.glitchesFound);

      // Call the callback function if provided
      if (this.onGlitchFound) {
        this.onGlitchFound(this.glitchesFound);
      }
    }
  }
};
</script>

<style scoped>
.glitch-container {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>