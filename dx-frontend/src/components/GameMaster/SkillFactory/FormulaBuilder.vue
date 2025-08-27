<template>
  <div class="formula-builder">
    <div class="section-header">
      <h4>{{ title || 'Formula Configuration' }}</h4>
    </div>

    <!-- Base Value -->
    <div class="form-group">
      <label>Base Value</label>
      <input
        v-model.number="formula.base"
        type="number"
        class="form-input"
        placeholder="0"
      />
    </div>

    <!-- Stat Requirements -->
    <div class="subsection">
      <div class="subsection-header">
        <h5>Stat Requirements</h5>
        <button type="button" @click="addRequirement" class="add-btn">
          Add Requirement
        </button>
      </div>

      <div v-if="formula.requires.length === 0" class="empty-state">
        No stat requirements. Click "Add Requirement" to add requirements.
      </div>

      <div v-for="(req, index) in formula.requires" :key="index" class="requirement-item">
        <div class="requirement-fields">
          <div class="form-group">
            <label>Stat</label>
            <select v-model="req.stat" class="form-input">
              <option :value="IdEa2Enum.PhysicalStrength">Physical Strength</option>
              <option :value="IdEa2Enum.MentalStrength">Mental Strength</option>
              <option :value="IdEa2Enum.FlowResonance">Flow Resonance</option>
              <option :value="IdEa2Enum.Concentration">Concentration</option>
              <option :value="IdEa2Enum.FlowManipulation">Flow Manipulation</option>
              <option :value="IdEa2Enum.FlowConnection">Flow Connection</option>
              <option :value="IdEa2Enum.Knowledge">Knowledge</option>
              <option :value="IdEa2Enum.Speed">Speed</option>
              <option :value="IdEa2Enum.Luck">Luck</option>
              <option :value="IdEa2Enum.Charisma">Charisma</option>
            </select>
          </div>

          <div class="form-group">
            <label>Required Value</label>
            <input
              v-model.number="req.value"
              type="number"
              min="0"
              class="form-input"
              placeholder="0"
            />
          </div>

          <button type="button" @click="removeRequirement(index)" class="remove-btn">
            Remove
          </button>
        </div>
      </div>
    </div>

    <!-- Scaling Factors -->
    <div class="subsection">
      <div class="subsection-header">
        <h5>Scaling Factors</h5>
        <button type="button" @click="addScaling" class="add-btn">
          Add Scaling
        </button>
      </div>

      <div v-if="formula.scaling.length === 0" class="empty-state">
        No scaling factors. Click "Add Scaling" to add stat scaling.
      </div>

      <div v-for="(scaling, index) in formula.scaling" :key="index" class="scaling-item">
        <div class="scaling-fields">
          <div class="form-group">
            <label>Stat</label>
            <select v-model="scaling.stat" class="form-input">
              <option :value="IdEa2Enum.PhysicalStrength">Physical Strength</option>
              <option :value="IdEa2Enum.MentalStrength">Mental Strength</option>
              <option :value="IdEa2Enum.FlowResonance">Flow Resonance</option>
              <option :value="IdEa2Enum.Concentration">Concentration</option>
              <option :value="IdEa2Enum.FlowManipulation">Flow Manipulation</option>
              <option :value="IdEa2Enum.FlowConnection">Flow Connection</option>
              <option :value="IdEa2Enum.Knowledge">Knowledge</option>
              <option :value="IdEa2Enum.Speed">Speed</option>
              <option :value="IdEa2Enum.Luck">Luck</option>
              <option :value="IdEa2Enum.Charisma">Charisma</option>
            </select>
          </div>

          <div class="form-group">
            <label>Scaling Value</label>
            <input
              v-model.number="scaling.value"
              type="number"
              step="0.1"
              class="form-input"
              placeholder="0.0"
            />
          </div>

          <button type="button" @click="removeScaling(index)" class="remove-btn">
            Remove
          </button>
        </div>
      </div>
    </div>

    <!-- Efficiency Settings -->
    <div class="efficiency-section">
      <h5>Efficiency Limits</h5>
      <div class="efficiency-fields">
        <div class="form-group">
          <label>Min Efficiency</label>
          <input
            v-model.number="formula.min_efficiency"
            type="number"
            step="0.1"
            class="form-input"
            placeholder="Optional"
          />
        </div>

        <div class="form-group">
          <label>Max Efficiency</label>
          <input
            v-model.number="formula.max_efficiency"
            type="number"
            step="0.1"
            class="form-input"
            placeholder="Optional"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { IdEa2Enum, type FormulaRequest, type StatRequirementRequest, type ScalingRequest } from '@/api/dx-backend'

// Props
interface Props {
  modelValue: FormulaRequest
  title?: string
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: FormulaRequest]
}>()

// Reactive state
const formula = ref<FormulaRequest>({
  base: props.modelValue.base || 0,
  requires: props.modelValue.requires || [],
  scaling: props.modelValue.scaling || [],
  min_efficiency: props.modelValue.min_efficiency || null,
  max_efficiency: props.modelValue.max_efficiency || null
})

// Methods
const addRequirement = () => {
  formula.value.requires = formula.value.requires || []
  formula.value.requires.push({
    stat: IdEa2Enum.PhysicalStrength,
    value: 0
  })
  emitUpdate()
}

const removeRequirement = (index: number) => {
  formula.value.requires?.splice(index, 1)
  emitUpdate()
}

const addScaling = () => {
  formula.value.scaling = formula.value.scaling || []
  formula.value.scaling.push({
    stat: IdEa2Enum.PhysicalStrength,
    value: 0
  })
  emitUpdate()
}

const removeScaling = (index: number) => {
  formula.value.scaling?.splice(index, 1)
  emitUpdate()
}

const emitUpdate = () => {
  emit('update:modelValue', { ...formula.value })
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  formula.value = {
    base: newValue.base || 0,
    requires: newValue.requires || [],
    scaling: newValue.scaling || [],
    min_efficiency: newValue.min_efficiency || null,
    max_efficiency: newValue.max_efficiency || null
  }
}, { deep: true })

// Watch for internal changes
watch(formula, () => {
  emitUpdate()
}, { deep: true })
</script>

<style scoped>
.formula-builder {
  background: rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(127, 255, 22, 0.2);
  border-radius: 0.263rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.section-header {
  margin-bottom: 1rem;
}

.section-header h4 {
  margin: 0;
  color: #fada95;
  font-size: 1rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

.subsection {
  margin-bottom: 1.5rem;
}

.subsection-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.subsection-header h5 {
  margin: 0;
  color: #fada95;
  font-size: 0.9rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 500;
}

.efficiency-section h5 {
  margin: 0 0 0.5rem 0;
  color: #fada95;
  font-size: 0.9rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 500;
}

.add-btn {
  padding: 0.25rem 0.5rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.7rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  color: #7fff16;
  transform: scale(1.05);
}

.empty-state {
  color: rgba(250, 218, 149, 0.5);
  font-style: italic;
  text-align: center;
  padding: 0.5rem;
  border: 1px dashed rgba(127, 255, 22, 0.2);
  border-radius: 0.263rem;
  font-size: 0.75rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.requirement-item,
.scaling-item {
  background: rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(127, 255, 22, 0.15);
  border-radius: 0.263rem;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
}

.requirement-fields,
.scaling-fields,
.efficiency-fields {
  display: flex;
  gap: 1rem;
  align-items: end;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.form-group label {
  font-weight: 500;
  color: #fada95;
  font-size: 0.8rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
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
  padding: 0.25rem 0.5rem;
  border: 2px solid rgba(244, 67, 54, 0.5);
  border-radius: 0.263rem;
  background: rgba(244, 67, 54, 0.2);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.7rem;
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