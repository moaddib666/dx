<template>
  <div class="layer-selector">
    <h3 class="layer-selector-title">Dimensional Layers</h3>
    <div class="layers-list">
      <div
        v-for="layer in layers"
        :key="layer.id"
        :class="['layer-item', {
          'active': layer.id === currentLayer,
          'inactive-dimension': !layer.active
        }]"
        @click="selectLayer(layer.id)"
      >
        <div class="layer-header">
          <span class="layer-number">{{ layer.id }}</span>
          <span class="layer-name">{{ layer.name }}</span>
        </div>
        <div class="layer-info">
          <span class="layer-description">{{ layer.description }}</span>
          <span class="layer-energy">Energy: {{ layer.energyCost }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'LayerSelector',
  computed: {
    ...mapGetters('tabletopEditor', [
      'currentMap',
      'currentLayer'
    ]),
    layers() {
      return this.currentMap?.layers || [];
    }
  },
  methods: {
    ...mapActions('tabletopEditor', [
      'setCurrentLayer'
    ]),
    selectLayer(layerId) {
      this.setCurrentLayer(layerId);
    }
  }
};
</script>

<style scoped>
.layer-selector {
  background: rgba(20, 20, 30, 0.95);
  border: 1px solid rgba(100, 100, 150, 0.3);
  border-radius: 8px;
  padding: 15px;
  color: #e0e0e0;
  max-height: 600px;
  overflow-y: auto;
}

.layer-selector-title {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: bold;
  color: #00d4ff;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.layers-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.layer-item {
  background: rgba(40, 40, 60, 0.6);
  border: 2px solid rgba(100, 100, 150, 0.3);
  border-radius: 6px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.layer-item:hover {
  background: rgba(60, 60, 80, 0.8);
  border-color: rgba(0, 212, 255, 0.5);
  transform: translateX(3px);
}

.layer-item.active {
  background: rgba(0, 212, 255, 0.2);
  border-color: #00d4ff;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

.layer-item.inactive-dimension {
  opacity: 0.5;
}

.layer-item.inactive-dimension .layer-name::after {
  content: ' (Locked)';
  font-size: 11px;
  color: #ff6b6b;
}

.layer-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.layer-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: rgba(0, 212, 255, 0.2);
  border: 1px solid #00d4ff;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
  color: #00d4ff;
}

.layer-item.active .layer-number {
  background: #00d4ff;
  color: #000;
}

.layer-name {
  font-weight: bold;
  font-size: 14px;
  color: #fff;
}

.layer-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
  font-size: 11px;
  color: #aaa;
  padding-left: 38px;
}

.layer-description {
  font-style: italic;
}

.layer-energy {
  color: #ffa500;
  font-weight: 500;
}

/* Scrollbar styling */
.layer-selector::-webkit-scrollbar {
  width: 6px;
}

.layer-selector::-webkit-scrollbar-track {
  background: rgba(20, 20, 30, 0.5);
  border-radius: 3px;
}

.layer-selector::-webkit-scrollbar-thumb {
  background: rgba(0, 212, 255, 0.3);
  border-radius: 3px;
}

.layer-selector::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 212, 255, 0.5);
}
</style>
