<template>
  <div class="info-section">
    <h4>Basic Information</h4>
    <div class="info-grid">
      <div class="info-item">
        <label>Room ID:</label>
        <span>{{ room.id }}</span>
      </div>
      <div class="info-item">
        <label>Position:</label>
        <span>({{ room.position.grid_x }}, {{ room.position.grid_y }}, {{ room.position.grid_z }})</span>
      </div>
      <div class="info-item">
        <label>Type:</label>
        <select v-model="localRoomType" :disabled="!editable" @change="onTypeChange">
          <option value="default">Default</option>
          <option value="special">Special</option>
          <option value="secret">Secret</option>
          <option value="dangerous">Dangerous</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BasicInformation',
  props: {
    room: {
      type: Object,
      required: true
    },
    editable: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      localRoomType: this.room.type || 'default'
    };
  },
  watch: {
    'room.type': {
      handler(newType) {
        this.localRoomType = newType || 'default';
      },
      immediate: true
    }
  },
  methods: {
    onTypeChange() {
      this.$emit('update:room-type', this.localRoomType);
    }
  }
};
</script>

<style scoped>
.info-section {

}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 0.5rem;
}

.info-item label {
  font-size: 0.8rem;
  color: #aaa;
  margin-bottom: 0.25rem;
}

.info-item span {
  font-size: 0.9rem;
  color: #fff;
}

.info-item select {
  background: #444;
  border: 1px solid #555;
  color: #fff;
  padding: 0.25rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.info-item select:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>