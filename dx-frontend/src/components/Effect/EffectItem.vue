<template>
  <div class="effect-item">
    <div class="icon-container" @mouseenter="showDescription" @mouseleave="hideDescription">
      <img :src="effectData.effect.icon" alt="Effect Icon" class="effect-icon" />
      <div class="counter">{{ timeLeft }}</div>
      <div class="description" :class="{ visible: showingDescription }">{{ effectData.effect.id }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "EffectItem",
  props: {
    effectData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showingDescription: false,
    };
  },
  computed: {
    timeLeft() {

      return this.effectData.effect.ends_in - this.effectData.duration
    },
  },
  methods: {
    showDescription() {
      this.showingDescription = true;
    },
    hideDescription() {
      this.showingDescription = false;
    },
  },
};
</script>

<style scoped>
.effect-item {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50px;
}

.icon-container {
  position: relative;
  width: 40px;
  height: 40px;
}

.effect-icon {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  transition: transform 0.2s ease-in-out;
}

.icon-container:hover .effect-icon {
  transform: scale(1.1); /* Slightly enlarge on hover */
}

.counter {
  position: absolute;
  bottom: 2px;
  right: 2px;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  font-size: 0.6rem;
  font-weight: bold;
  padding: 0.2rem;
  border-radius: 50%;
  line-height: 1;
  text-align: center;
}

.description {
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 0.3rem;
  white-space: nowrap;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  visibility: hidden; /* Hidden by default */
  opacity: 0; /* Transparent by default */
  transition: opacity 0.2s ease-in-out, visibility 0.2s ease-in-out;
}

.description.visible {
  visibility: visible; /* Make visible */
  opacity: 1; /* Fade in */
}
</style>
