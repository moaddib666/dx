<template>
  <div class="cost-configuration">
    <div class="section-header">
      <h4>Skill Costs</h4>
      <button type="button" @click="addCost" class="add-btn">
        Add Cost
      </button>
    </div>

    <div v-if="costs.length === 0" class="empty-state">
      No costs defined. Click "Add Cost" to add skill costs.
    </div>

    <div v-for="(cost, index) in costs" :key="index" class="cost-item">
      <div class="cost-fields">
        <div class="form-group">
          <label>Cost Type</label>
          <select v-model="cost.kind" class="form-input">
            <option :value="AttributesEnum.Health">Health</option>
            <option :value="AttributesEnum.Energy">Energy</option>
            <option :value="AttributesEnum.ActionPoints">Action Points</option>
          </select>
        </div>

        <div class="form-group">
          <label>Value</label>
          <input
            v-model.number="cost.value"
            type="number"
            min="0"
            class="form-input"
            placeholder="0"
          />
        </div>

        <button type="button" @click="removeCost(index)" class="remove-btn">
          Remove
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { AttributesEnum, type CostRequest } from '@/api/dx-backend'

// Props
interface Props {
  modelValue: CostRequest[]
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: CostRequest[]]
}>()

// Reactive state
const costs = ref<CostRequest[]>([...props.modelValue])

// Methods
const addCost = () => {
  costs.value.push({
    kind: AttributesEnum.Health,
    value: 0
  })
  emitUpdate()
}

const removeCost = (index: number) => {
  costs.value.splice(index, 1)
  emitUpdate()
}

const emitUpdate = () => {
  emit('update:modelValue', [...costs.value])
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  costs.value = [...newValue]
}, { deep: true })
</script>

<style scoped>
.cost-configuration {
  margin-bottom: 1.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h4 {
  margin: 0;
  color: #1E90FF;
  font-size: 1rem;
}

.add-btn {
  background: #1E90FF;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.8rem;
}

.add-btn:hover {
  background: #1873CC;
}

.empty-state {
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
  text-align: center;
  padding: 1rem;
  border: 1px dashed rgba(255, 255, 255, 0.3);
  border-radius: 0.25rem;
}

.cost-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 0.5rem;
}

.cost-fields {
  display: flex;
  gap: 1rem;
  align-items: end;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
}

.form-input {
  padding: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.25rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #1E90FF;
  background: rgba(255, 255, 255, 0.15);
}

.remove-btn {
  background: #f44336;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.8rem;
  height: fit-content;
}

.remove-btn:hover {
  background: #d32f2f;
}
</style>