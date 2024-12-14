<template>
  <div class="button-container" @click="cast">
    <div class="outer-square">
      <div class="inner-square">
        <slot name="icon">
            {{ spell.skill.icon }}
        </slot>
      </div>
    </div>
    <div class="action-label">
      <slot name="label">
        {{ spell.skill.name }}
      </slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SpellButtonComponent',
  props: {
    spell: {
      type: Object,
      required: true
    }
  },
  methods: {
    cast() {
      console.debug('Casting spell:', this.spell.skill.id)
      this.$emit('cast', this.spell.skill);
    }
  }
}
</script>

<style scoped>
.button-container {
  aspect-ratio: 1 / 1;
  min-width: 3vh;
  min-height: 3vh;
  width: 100%;
  position: relative;
  cursor: pointer;
  background: rgba(46, 42, 42, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(65, 66, 66, 0.5);
  transition: all 0.3s ease-in-out;
  z-index: 1;
  text-align: center;
  margin-left: 1vh;
}

.button-container:hover {
  border: 1px solid rgba(0, 191, 255, 0.8); /* DeepSkyBlue on hover */
}

.outer-square {
  z-index: 1;
  width: 100%;
  height: 100%;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease-in-out;
}

.button-container:hover .outer-square {
  box-shadow: 0 0 15px rgba(0, 191, 255, 0.5), 0 0 30px rgba(0, 191, 255, 0.4), inset 0 0 15px rgba(0, 191, 255, 0.5); /* DeepSkyBlue on hover */
}

.inner-square {
  z-index: 1;
  width: 80%;
  height: 80%;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease-in-out;
}

.button-container:hover .inner-square {
  background: rgba(0, 191, 255, 0.4); /* DeepSkyBlue on hover */
}

.icon {
  font-size: 3rem;
  color: whitesmoke;
  text-shadow: 0 0 10px rgba(255, 255, 255, 1);
  z-index: -1;
  font-family: 'Orbitron', sans-serif;
}

.action-label {
  font-size: 0.7rem;
  color: white;
  text-align: center;
  font-family: 'Orbitron', sans-serif;
  text-shadow: 0 0 10px rgba(0, 191, 255, 0.8); /* DeepSkyBlue */
}
</style>
