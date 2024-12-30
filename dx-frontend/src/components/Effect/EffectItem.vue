<template>
  <div :class="{ inactive: !effectData.active }" class="effect-item">
    <div class="icon-container">
      <img :src="effectData.effect.icon" alt="Effect Icon" class="effect-icon"/>
    </div>
    <div class="info-container">
      <div class="effect-name">{{ effectData.effect.id }}</div>
      <div class="effect-details">
        <span v-if="effectData.effect.permanent">Permanent</span>
        <span v-else>
          {{ timeLeft }} Turns Left
        </span>
      </div>
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
  computed: {
    timeLeft() {
      const {ends_in, duration} = this.effectData.effect;
      return ends_in - duration;
    },
  },
};
</script>

<style scoped>
.effect-item {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #1a1a2e, #16213e);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  padding: 0.5rem;
  width: 200px;
  gap: 0.5rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  color: #ffffff;
  font-family: "Roboto", sans-serif;
  font-size: 0.9rem;
  transition: transform 0.3s, box-shadow 0.3s;
}

.effect-item:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(255, 255, 255, 0.2);
}

.effect-item.inactive {
  opacity: 0.5;
}

.icon-container {
  flex-shrink: 0;
}

.effect-icon {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
}

.info-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.effect-name {
  font-weight: bold;
  font-size: 1rem;
  margin-bottom: 0.2rem;
}

.effect-details {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
}
</style>
