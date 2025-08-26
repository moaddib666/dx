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
  color: #fada95;
  font-size: 1rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

.add-btn {
  padding: 0.35rem 0.7rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.add-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  color: #7fff16;
  transform: scale(1.05);
}

.empty-state {
  color: rgba(250, 218, 149, 0.6);
  font-style: italic;
  text-align: center;
  padding: 1rem;
  border: 1px dashed rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.cost-item {
  background: rgba(0, 0, 0, 0.2);
  border: 2px solid rgba(127, 255, 22, 0.2);
  border-radius: 0.263rem;
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
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.9rem;
}

.form-input {
  padding: 0.35rem 0.525rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 400;
  transition: border-color 0.3s, background-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #7fff16;
  background: rgba(0, 0, 0, 0.6);
}

.form-input option {
  background: rgba(0, 0, 0, 0.9);
  color: #fada95;
}

.remove-btn {
  padding: 0.35rem 0.7rem;
  border: 2px solid rgba(244, 67, 54, 0.5);
  border-radius: 0.263rem;
  background: rgba(244, 67, 54, 0.2);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  height: fit-content;
}

.remove-btn:hover {
  border-color: #f44336;
  background: rgba(244, 67, 54, 0.3);
  color: #f44336;
  transform: scale(1.05);
}
</style>