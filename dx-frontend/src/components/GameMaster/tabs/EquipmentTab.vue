<template>
  <div class="equipment-tab">
    <h3>Equipment & Items</h3>

    <div class="form-group">
      <label>Items ({{ template.data.items.length }}/{{ template.validation.max_items_count }})</label>
      <div class="items-list">
        <div v-for="(itemId, index) in template.data.items" :key="index" class="item">
          <span class="item-id">{{ itemId }}</span>
          <button class="item-remove" @click="removeItem(itemId)">×</button>
        </div>
        <div v-if="template.data.items.length < template.validation.max_items_count" class="add-item">
          <input
            type="text"
            placeholder="Add item ID"
            v-model="newItemId"
            @keydown.enter="addItem"
          />
          <button class="add-button" @click="addItem">Add</button>
        </div>
      </div>
    </div>

    <div class="equipment-summary">
      <div class="summary-card">
        <h4>Equipment Summary</h4>
        <div class="summary-stats">
          <div class="stat-row">
            <span>Total Items:</span>
            <span>{{ template.data.items.length }}</span>
          </div>
          <div class="stat-row">
            <span>Max Items:</span>
            <span>{{ template.validation.max_items_count }}</span>
          </div>
          <div class="stat-row">
            <span>Remaining Slots:</span>
            <span>{{ template.validation.max_items_count - template.data.items.length }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EquipmentTab',
  props: {
    template: {
      type: Object,
      required: true
    },
    service: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      newItemId: ''
    };
  },
  methods: {
    addItem() {
      if (this.newItemId.trim()) {
        this.service.addItem(this.newItemId.trim());
        this.newItemId = '';
        this.$emit('update');
      }
    },
    removeItem(itemId) {
      this.service.removeItem(itemId);
      this.$emit('update');
    }
  }
};
</script>

<style scoped>
.equipment-tab {
  padding: 20px 0;
}

.form-group {
  margin-bottom: 30px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: #ccc;
}

.items-list {
  background: #333;
  border-radius: 4px;
  padding: 15px;
  margin-top: 10px;
  border: 1px solid #444;
}

.item {
  background: #444;
  color: #fff;
  padding: 10px 15px;
  border-radius: 4px;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-id {
  font-family: monospace;
  font-size: 0.9rem;
}

.item-remove {
  background: none;
  border: none;
  color: #f44336;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0;
  margin: 0;
  transition: color 0.3s ease;
}

.item-remove:hover {
  color: #ff5252;
}

.add-item {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.add-item input {
  flex: 1;
  padding: 8px;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
}

.add-item input:focus {
  border-color: #1E90FF;
  outline: none;
}

.add-button {
  padding: 8px 16px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-button:hover {
  background: #45a049;
}

.equipment-summary {
  margin-top: 30px;
}

.summary-card {
  background: #2d2d2d;
  padding: 20px;
  border-radius: 4px;
  border: 1px solid #444;
}

.summary-card h4 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 15px;
}

.summary-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  color: #ccc;
}

.stat-row span:last-child {
  font-weight: bold;
  color: #fff;
}

h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.2rem;
}
</style>