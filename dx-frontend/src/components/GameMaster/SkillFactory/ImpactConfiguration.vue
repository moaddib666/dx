<template>
  <div class="impact-configuration">
    <div class="section-header">
      <h4>Skill Impacts</h4>
      <button type="button" @click="addImpact" class="add-btn">
        Add Impact
      </button>
    </div>

    <div v-if="impacts.length === 0" class="empty-state">
      No impacts defined. Click "Add Impact" to add skill impacts.
    </div>

    <div v-for="(impact, index) in impacts" :key="index" class="impact-item">
      <div class="impact-header">
        <h5>Impact {{ index + 1 }}</h5>
        <button type="button" @click="removeImpact(index)" class="remove-btn">
          Remove Impact
        </button>
      </div>

      <div class="impact-fields">
        <div class="form-row">
          <div class="form-group">
            <label>Impact Kind</label>
            <select v-model="impact.kind" class="form-input">
              <option :value="ImpactTypeEnum.None">None</option>
              <option :value="ImpactTypeEnum.KnockOut">Knock Out</option>
              <option :value="ImpactTypeEnum.Damage">Damage</option>
              <option :value="ImpactTypeEnum.Heal">Heal</option>
              <option :value="ImpactTypeEnum.Shield">Shield</option>
              <option :value="ImpactTypeEnum.Buff">Buff</option>
              <option :value="ImpactTypeEnum.Debuff">Debuff</option>
              <option :value="ImpactTypeEnum.Stun">Stun</option>
              <option :value="ImpactTypeEnum.Sleep">Sleep</option>
              <option :value="ImpactTypeEnum.Confusion">Confusion</option>
              <option :value="ImpactTypeEnum.Paralysis">Paralysis</option>
              <option :value="ImpactTypeEnum.Fear">Fear</option>
              <option :value="ImpactTypeEnum.Freeze">Freeze</option>
              <option :value="ImpactTypeEnum.Burn">Burn</option>
              <option :value="ImpactTypeEnum.Poison">Poison</option>
              <option :value="ImpactTypeEnum.Slow">Slow</option>
              <option :value="ImpactTypeEnum.Haste">Haste</option>
              <option :value="ImpactTypeEnum.Blind">Blind</option>
              <option :value="ImpactTypeEnum.Silence">Silence</option>
              <option :value="ImpactTypeEnum.Bleed">Bleed</option>
              <option :value="ImpactTypeEnum.Disarm">Disarm</option>
              <option :value="ImpactTypeEnum.Root">Root</option>
              <option :value="ImpactTypeEnum.EnergyDecrease">Energy Decrease</option>
              <option :value="ImpactTypeEnum.Reflect">Reflect</option>
              <option :value="ImpactTypeEnum.Absorb">Absorb</option>
              <option :value="ImpactTypeEnum.Dodge">Dodge</option>
              <option :value="ImpactTypeEnum.Resist">Resist</option>
              <option :value="ImpactTypeEnum.Immunity">Immunity</option>
              <option :value="ImpactTypeEnum.Regeneration">Regeneration</option>
              <option :value="ImpactTypeEnum.Lifesteal">Lifesteal</option>
            </select>
          </div>

          <div class="form-group">
            <label>Violation Type</label>
            <select v-model="impact.type" class="form-input">
              <option :value="Type82bEnum.None">None</option>
              <option :value="Type82bEnum.Physical">Physical</option>
              <option :value="Type82bEnum.Mental">Mental</option>
              <option :value="Type82bEnum.Energy">Energy</option>
              <option :value="Type82bEnum.Heat">Heat</option>
              <option :value="Type82bEnum.Cold">Cold</option>
              <option :value="Type82bEnum.Light">Light</option>
              <option :value="Type82bEnum.Darkness">Darkness</option>
            </select>
          </div>
        </div>

        <!-- Formula Configuration -->
        <FormulaBuilder
          v-model="impact.formula"
          :title="`Impact ${index + 1} Formula`"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ImpactTypeEnum, Type82bEnum, IdEa2Enum, type ImpactRequest, type FormulaRequest } from '@/api/dx-backend'
import FormulaBuilder from './FormulaBuilder.vue'

// Props
interface Props {
  modelValue: ImpactRequest[]
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: ImpactRequest[]]
}>()

// Reactive state
const impacts = ref<ImpactRequest[]>([...props.modelValue])

// Methods
const addImpact = () => {
  const isFirstImpact = impacts.value.length === 0

  const newImpact: ImpactRequest = {
    kind: isFirstImpact ? ImpactTypeEnum.Damage : ImpactTypeEnum.None,
    type: isFirstImpact ? Type82bEnum.Physical : Type82bEnum.None,
    formula: {
      base: isFirstImpact ? 10 : 0,
      requires: isFirstImpact ? [{
        stat: IdEa2Enum.PhysicalStrength,
        value: 5
      }] : [],
      scaling: isFirstImpact ? [{
        stat: IdEa2Enum.PhysicalStrength,
        value: 1.0
      }] : [],
      min_efficiency: isFirstImpact ? 0.5 : null,
      max_efficiency: isFirstImpact ? 2.0 : null
    }
  }
  impacts.value.push(newImpact)
  emitUpdate()
}

const removeImpact = (index: number) => {
  impacts.value.splice(index, 1)
  emitUpdate()
}

const emitUpdate = () => {
  emit('update:modelValue', [...impacts.value])
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  impacts.value = [...newValue]
}, { deep: true })
</script>

<style scoped>
.impact-configuration {
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

.impact-item {
  background: rgba(0, 0, 0, 0.2);
  border: 2px solid rgba(127, 255, 22, 0.2);
  border-radius: 0.263rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.impact-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.impact-header h5 {
  margin: 0;
  color: #fada95;
  font-size: 0.9rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

.impact-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: flex;
  gap: 1rem;
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
}

.remove-btn:hover {
  border-color: #f44336;
  background: rgba(244, 67, 54, 0.3);
  color: #f44336;
  transform: scale(1.05);
}
</style>