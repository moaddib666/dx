<template>
  <div class="effect-configuration">
    <div class="section-header">
      <h4>Skill Effects</h4>
      <button type="button" @click="addEffect" class="add-btn">
        Add Effect
      </button>
    </div>

    <div v-if="effects.length === 0" class="empty-state">
      No effects defined. Click "Add Effect" to add skill effects.
    </div>

    <div v-for="(effect, index) in effects" :key="index" class="effect-item">
      <div class="effect-header">
        <h5>Effect {{ index + 1 }}</h5>
        <button type="button" @click="removeEffect(index)" class="remove-btn">
          Remove Effect
        </button>
      </div>

      <div class="effect-fields">
        <!-- Basic Effect Properties -->
        <div class="form-row">
          <div class="form-group">
            <label>Effect Name</label>
            <select v-model="effect.name" class="form-input">
              <option :value="EffectEnum.None">None</option>
              <option :value="EffectEnum.KnockedOut">Knocked Out</option>
              <option :value="EffectEnum.Coma">Coma</option>
              <option :value="EffectEnum.Burning">Burning</option>
              <option :value="EffectEnum.Poisoned">Poisoned</option>
              <option :value="EffectEnum.Sleeping">Sleeping</option>
              <option :value="EffectEnum.Confused">Confused</option>
              <option :value="EffectEnum.Paralyzed">Paralyzed</option>
              <option :value="EffectEnum.Fear">Fear</option>
              <option :value="EffectEnum.Slowness">Slowness</option>
              <option :value="EffectEnum.Cold">Cold</option>
              <option :value="EffectEnum.Cursed">Cursed</option>
              <option :value="EffectEnum.Blindness">Blindness</option>
              <option :value="EffectEnum.Haste">Haste</option>
              <option :value="EffectEnum.Regeneration">Regeneration</option>
              <option :value="EffectEnum.Blessed">Blessed</option>
              <option :value="EffectEnum.ArcaneSurge">Arcane Surge</option>
              <option :value="EffectEnum.Marked">Marked</option>
            </select>
          </div>

          <div class="form-group">
            <label>Base Chance</label>
            <input
              v-model.number="effect.base_chance"
              type="number"
              min="0"
              max="1"
              step="0.1"
              class="form-input"
              placeholder="1.0"
            />
          </div>
        </div>

        <!-- Impact Configuration (Optional) -->
        <div class="subsection">
          <div class="subsection-header">
            <h6>Effect Impact</h6>
            <label class="checkbox-label">
              <input
                type="checkbox"
                :checked="effect.impact !== null"
                @change="toggleImpact(effect, $event)"
              />
              Enable Impact
            </label>
          </div>

          <div v-if="effect.impact" class="impact-section">
            <div class="form-row">
              <div class="form-group">
                <label>Impact Kind</label>
                <select v-model="effect.impact.kind" class="form-input">
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
                <select v-model="effect.impact.type" class="form-input">
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

            <FormulaBuilder
              v-model="effect.impact.formula"
              :title="`Effect ${index + 1} Impact Formula`"
            />
          </div>
        </div>

        <!-- Duration Modifier -->
        <div class="subsection">
          <h6>Duration Modifier</h6>
          <div class="form-group">
            <label>Label</label>
            <input
              v-model="effect.duration_modifier.label"
              type="text"
              class="form-input"
              placeholder="Duration modifier label"
            />
          </div>

          <FormulaBuilder
            v-model="effect.duration_modifier.formula"
            :title="`Effect ${index + 1} Duration Formula`"
          />
        </div>

        <!-- Stat Modifiers -->
        <div class="subsection">
          <div class="subsection-header">
            <h6>Stat Modifiers</h6>
            <button type="button" @click="addStatModifier(effect)" class="add-btn-small">
              Add Stat Modifier
            </button>
          </div>

          <div v-if="!effect.stat_modifiers || effect.stat_modifiers.length === 0" class="empty-state-small">
            No stat modifiers. Click "Add Stat Modifier" to add modifiers.
          </div>

          <div v-for="(modifier, modIndex) in effect.stat_modifiers" :key="modIndex" class="modifier-item">
            <div class="modifier-header">
              <span>Stat Modifier {{ modIndex + 1 }}</span>
              <button type="button" @click="removeStatModifier(effect, modIndex)" class="remove-btn-small">
                Remove
              </button>
            </div>

            <div class="form-group">
              <label>Label</label>
              <input
                v-model="modifier.label"
                type="text"
                class="form-input"
                placeholder="Stat modifier label"
              />
            </div>

            <FormulaBuilder
              v-model="modifier.formula"
              :title="`Stat Modifier ${modIndex + 1} Formula`"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import {
  EffectEnum,
  ImpactTypeEnum,
  Type82bEnum,
  type AssignableEffectRequest,
  type ImpactRequest,
  type ModifierRequest,
  type FormulaRequest
} from '@/api/dx-backend'
import FormulaBuilder from './FormulaBuilder.vue'

// Props
interface Props {
  modelValue: AssignableEffectRequest[]
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: AssignableEffectRequest[]]
}>()

// Reactive state
const effects = ref<AssignableEffectRequest[]>([...props.modelValue])

// Methods
const addEffect = () => {
  const newEffect: AssignableEffectRequest = {
    name: EffectEnum.None,
    impact: null,
    base_chance: 1,
    duration_modifier: {
      label: '',
      formula: {
        base: 0,
        requires: [],
        scaling: [],
        min_efficiency: null,
        max_efficiency: null
      }
    },
    stat_modifiers: []
  }
  effects.value.push(newEffect)
  emitUpdate()
}

const removeEffect = (index: number) => {
  effects.value.splice(index, 1)
  emitUpdate()
}

const toggleImpact = (effect: AssignableEffectRequest, event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.checked) {
    effect.impact = {
      kind: ImpactTypeEnum.None,
      type: Type82bEnum.None,
      formula: {
        base: 0,
        requires: [],
        scaling: [],
        min_efficiency: null,
        max_efficiency: null
      }
    }
  } else {
    effect.impact = null
  }
  emitUpdate()
}

const addStatModifier = (effect: AssignableEffectRequest) => {
  if (!effect.stat_modifiers) {
    effect.stat_modifiers = []
  }
  effect.stat_modifiers.push({
    label: '',
    formula: {
      base: 0,
      requires: [],
      scaling: [],
      min_efficiency: null,
      max_efficiency: null
    }
  })
  emitUpdate()
}

const removeStatModifier = (effect: AssignableEffectRequest, index: number) => {
  effect.stat_modifiers?.splice(index, 1)
  emitUpdate()
}

const emitUpdate = () => {
  emit('update:modelValue', [...effects.value])
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  effects.value = [...newValue]
}, { deep: true })
</script>

<style scoped>
.effect-configuration {
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

.effect-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.effect-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.effect-header h5 {
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9rem;
}

.effect-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.subsection {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.25rem;
  padding: 0.75rem;
}

.subsection-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.subsection-header h6 {
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.85rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.8rem;
  cursor: pointer;
}

.impact-section {
  margin-top: 0.75rem;
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

.add-btn-small {
  background: #1E90FF;
  color: white;
  border: none;
  padding: 0.3rem 0.6rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.7rem;
}

.add-btn-small:hover {
  background: #1873CC;
}

.empty-state-small {
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
  text-align: center;
  padding: 0.5rem;
  border: 1px dashed rgba(255, 255, 255, 0.2);
  border-radius: 0.25rem;
  font-size: 0.75rem;
}

.modifier-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 0.25rem;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
}

.modifier-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.modifier-header span {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.8rem;
  font-weight: 500;
}

.remove-btn,
.remove-btn-small {
  background: #f44336;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.8rem;
}

.remove-btn-small {
  padding: 0.3rem 0.6rem;
  font-size: 0.7rem;
}

.remove-btn:hover,
.remove-btn-small:hover {
  background: #d32f2f;
}
</style>