<template>
  <div class="floor-switcher">
    <button class="floor-btn up-btn" title="Go to upper floor" @click="floorUp">
      <span class="arrow">&#9650;</span>
    </button>
    <div class="floor-display">
      <span class="floor-label">{{ currentFloor }}</span>
    </div>
    <button class="floor-btn down-btn" title="Go to lower floor" @click="floorDown">
      <span class="arrow">&#9660;</span>
    </button>
  </div>
</template>

<script>
export default {
  name: 'WorldEditorFloorSwitcher',
  props: {
    currentFloor: {
      type: Number,
      required: true
    }
  },
  emits: ['floor-up', 'floor-down'],
  methods: {
    floorUp() {
      this.$emit('floor-up');
    },
    floorDown() {
      this.$emit('floor-down');
    }
  }
}
</script>

<style scoped>
.floor-switcher {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(45, 45, 45, 0.9);
  border: 1px solid #555;
  border-radius: 4px;
  padding: 8px 4px;
  z-index: 10;
}

.floor-btn {
  background: transparent;
  border: none;
  color: #1E90FF;
  cursor: pointer;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.floor-btn:hover {
  background: rgba(30, 144, 255, 0.2);
}

.floor-display {
  margin: 8px 0;
  font-weight: bold;
  color: #fff;
  font-size: 1.1rem;
  text-align: center;
}

.arrow {
  font-size: 14px;
}
</style>