<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal">
      <h2 class="modal-title">Create New Skill</h2>
      <p class="modal-description">Fill in the details to create a comprehensive skill with all properties.</p>

      <form @submit.prevent="createSkill" class="skill-form">
        <!-- Skill Templates -->
        <div class="form-section">
          <h3>Skill Templates</h3>
          <p class="template-description">Choose a pre-defined template to quickly create balanced skills, or start from scratch.</p>

          <div class="template-buttons">
            <button type="button" @click="applyTemplate('healing')" class="template-btn healing">
              <span class="template-icon">💚</span>
              <div class="template-info">
                <strong>Healing Skill</strong>
                <small>Concentration-based, restores health/energy</small>
              </div>
            </button>

            <button type="button" @click="applyTemplate('physical')" class="template-btn physical">
              <span class="template-icon">⚔️</span>
              <div class="template-info">
                <strong>Physical Damage</strong>
                <small>Physical Strength-based attack</small>
              </div>
            </button>

            <button type="button" @click="applyTemplate('magic')" class="template-btn magic">
              <span class="template-icon">🔮</span>
              <div class="template-info">
                <strong>Magic Damage</strong>
                <small>Flow Manipulation-based spell</small>
              </div>
            </button>

            <button type="button" @click="applyTemplate('forbidden')" class="template-btn forbidden">
              <span class="template-icon">💀</span>
              <div class="template-info">
                <strong>Forbidden Magic</strong>
                <small>High damage, health cost</small>
              </div>
            </button>

            <button type="button" @click="clearForm" class="template-btn clear">
              <span class="template-icon">🗑️</span>
              <div class="template-info">
                <strong>Start Fresh</strong>
                <small>Clear all fields</small>
              </div>
            </button>
          </div>
        </div>

        <!-- Basic Information -->
        <div class="form-section">
          <h3>Basic Information</h3>

          <div class="form-group">
            <label for="skillName">Skill Name *</label>
            <input
              id="skillName"
              v-model="skillData.name"
              type="text"
              required
              class="form-input"
              placeholder="Enter skill name"
            />
          </div>

          <div class="form-group">
            <label for="skillDescription">Description *</label>
            <textarea
              id="skillDescription"
              v-model="skillData.description"
              class="form-textarea"
              placeholder="Enter skill description"
              rows="3"
              required
            ></textarea>
          </div>

          <div class="form-group">
            <label for="skillSchool">School (UUID)</label>
            <input
              id="skillSchool"
              v-model="skillData.school"
              type="text"
              class="form-input"
              placeholder="Enter school UUID (optional)"
            />
          </div>
        </div>

        <!-- Skill Properties -->
        <div class="form-section">
          <h3>Properties</h3>

          <div class="form-row">
            <div class="form-group">
              <label for="skillType">Skill Type *</label>
              <select
                id="skillType"
                v-model="skillData.type"
                class="form-input"
                required
              >
                <option :value="TypeC27Enum.Attack">Attack</option>
                <option :value="TypeC27Enum.Defense">Defense</option>
                <option :value="TypeC27Enum.Heal">Heal</option>
                <option :value="TypeC27Enum.Buff">Buff</option>
                <option :value="TypeC27Enum.Debuff">Debuff</option>
                <option :value="TypeC27Enum.Utility">Utility</option>
                <option :value="TypeC27Enum.Special">Special</option>
              </select>
            </div>

            <div class="form-group">
              <label for="skillGrade">Grade *</label>
              <input
                id="skillGrade"
                v-model.number="skillData.grade"
                type="number"
                min="1"
                max="10"
                class="form-input"
                placeholder="1"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input
                type="checkbox"
                v-model="skillData.multi_target"
              />
              Multi-Target Skill
            </label>
          </div>
        </div>

        <!-- Cost Configuration -->
        <div class="form-section">
          <CostConfiguration v-model="skillData.cost" />
        </div>

        <!-- Effect Configuration -->
        <div class="form-section">
          <EffectConfiguration v-model="skillData.effect" />
        </div>

        <!-- Impact Configuration -->
        <div class="form-section">
          <ImpactConfiguration v-model="skillData.impact" />
        </div>

        <!-- Error Display -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <!-- Action Buttons -->
        <div class="modal-actions">
          <LandingButton :action="closeModal" :disabled="isLoading">
            Cancel
          </LandingButton>
          <LandingButton
            type="submit"
            :disabled="!isFormValid || isLoading"
            class="create-btn"
          >
            {{ isLoading ? 'Creating...' : 'Create Skill' }}
          </LandingButton>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import LandingButton from '@/components/btn/LandingButton.vue'
import CostConfiguration from './CostConfiguration.vue'
import EffectConfiguration from './EffectConfiguration.vue'
import ImpactConfiguration from './ImpactConfiguration.vue'
import { GameMasterApi } from '@/api/backendService.js'
import {
  TypeC27Enum,
  AttributesEnum,
  ImpactTypeEnum,
  Type82bEnum,
  StatEnum,
  type SkillCreateRequest,
  type CostRequest,
  type AssignableEffectRequest,
  type ImpactRequest
} from '@/api/dx-backend'

// Props
interface Props {
  isOpen: boolean
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  close: []
  skillCreated: [skill: any]
}>()

// Reactive state
const isLoading = ref(false)
const error = ref('')

const skillData = ref<SkillCreateRequest>({
  name: '',
  description: '',
  school: '',
  multi_target: false,
  type: TypeC27Enum.Utility,
  grade: 1,
  cost: [],
  effect: [],
  impact: []
})

// Computed
const isFormValid = computed(() => {
  return skillData.value.name.trim().length > 0 &&
         skillData.value.description.trim().length > 0
})

// Methods
const closeModal = () => {
  emit('close')
}

const resetForm = () => {
  skillData.value = {
    name: '',
    description: '',
    school: '',
    multi_target: false,
    type: TypeC27Enum.Utility,
    grade: 1,
    cost: [],
    effect: [],
    impact: []
  }
  error.value = ''
}

const clearForm = () => {
  resetForm()
}

const applyTemplate = (templateType: string) => {
  error.value = ''

  switch (templateType) {
    case 'healing':
      skillData.value = {
        name: 'Healing Touch',
        description: 'A restorative skill that heals wounds and restores energy through concentrated flow manipulation.',
        school: '',
        multi_target: false,
        type: TypeC27Enum.Heal,
        grade: 9,
        cost: [
          {
            kind: AttributesEnum.ActionPoints,
            value: 5
          },
          {
            kind: AttributesEnum.Energy,
            value: 31
          }
        ],
        effect: [],
        impact: [
          {
            kind: ImpactTypeEnum.Heal,
            type: Type82bEnum.Energy,
            formula: {
              base: 13,
              requires: [
                {
                  stat: StatEnum.Concentration,
                  value: 10
                }
              ],
              scaling: [
                {
                  stat: StatEnum.Concentration,
                  value: 0.05
                }
              ],
              min_efficiency: 0.5,
              max_efficiency: 2.0
            }
          }
        ]
      }
      break

    case 'physical':
      skillData.value = {
        name: 'Power Strike',
        description: 'A devastating physical attack that channels raw strength into a focused blow.',
        school: '',
        multi_target: false,
        type: TypeC27Enum.Attack,
        grade: 9,
        cost: [
          {
            kind: AttributesEnum.ActionPoints,
            value: 2
          },
          {
            kind: AttributesEnum.Energy,
            value: 12
          }
        ],
        effect: [],
        impact: [
          {
            kind: ImpactTypeEnum.Damage,
            type: Type82bEnum.Physical,
            formula: {
              base: 6,
              requires: [
                {
                  stat: StatEnum.PhysicalStrength,
                  value: 10
                }
              ],
              scaling: [
                {
                  stat: StatEnum.FlowResonance,
                  value: 0.05
                }
              ],
              min_efficiency: 0.5,
              max_efficiency: 2.0
            }
          }
        ]
      }
      break

    case 'magic':
      skillData.value = {
        name: 'Arcane Bolt',
        description: 'A focused magical projectile that harnesses flow manipulation to deal energy damage.',
        school: '',
        multi_target: false,
        type: TypeC27Enum.Attack,
        grade: 9,
        cost: [
          {
            kind: AttributesEnum.ActionPoints,
            value: 3
          },
          {
            kind: AttributesEnum.Energy,
            value: 25
          }
        ],
        effect: [],
        impact: [
          {
            kind: ImpactTypeEnum.Damage,
            type: Type82bEnum.Energy,
            formula: {
              base: 12,
              requires: [
                {
                  stat: StatEnum.FlowManipulation,
                  value: 10
                }
              ],
              scaling: [
                {
                  stat: StatEnum.FlowManipulation,
                  value: 0.05
                }
              ],
              min_efficiency: 0.5,
              max_efficiency: 2.0
            }
          }
        ]
      }
      break

    case 'forbidden':
      skillData.value = {
        name: 'Soul Rend',
        description: 'A forbidden technique that sacrifices the caster\'s life force to unleash devastating magical damage.',
        school: '',
        multi_target: false,
        type: TypeC27Enum.Attack,
        grade: 9,
        cost: [
          {
            kind: AttributesEnum.ActionPoints,
            value: 3
          },
          {
            kind: AttributesEnum.Energy,
            value: 10
          },
          {
            kind: AttributesEnum.Health,
            value: 9
          }
        ],
        effect: [],
        impact: [
          {
            kind: ImpactTypeEnum.Damage,
            type: Type82bEnum.Energy,
            formula: {
              base: 20,
              requires: [
                {
                  stat: StatEnum.FlowResonance,
                  value: 10
                }
              ],
              scaling: [
                {
                  stat: StatEnum.FlowResonance,
                  value: 0.05
                }
              ],
              min_efficiency: 0.5,
              max_efficiency: 2.0
            }
          }
        ]
      }
      break

    default:
      resetForm()
      break
  }
}

const createSkill = async () => {
  if (!isFormValid.value || isLoading.value) return

  isLoading.value = true
  error.value = ''

  try {
    // Prepare skill data for API according to SkillCreateRequest interface
    const skillPayload: SkillCreateRequest = {
      name: skillData.value.name.trim(),
      description: skillData.value.description.trim(),
      school: skillData.value.school?.trim() || undefined,
      multi_target: skillData.value.multi_target,
      type: skillData.value.type,
      grade: skillData.value.grade,
      cost: skillData.value.cost?.length ? skillData.value.cost : undefined,
      effect: skillData.value.effect?.length ? skillData.value.effect : undefined,
      impact: skillData.value.impact?.length ? skillData.value.impact : undefined
    }

    // Call the GameMaster API to create the skill
    const response = await GameMasterApi.gamemasterSkillFactoryNewSkillCreate(skillPayload)

    // Emit success event
    emit('skillCreated', response.data)

    // Reset form
    resetForm()

  } catch (err: any) {
    console.error('Error creating skill:', err)
    error.value = err.response?.data?.message || 'Failed to create skill. Please try again.'
  } finally {
    isLoading.value = false
  }
}

// Watch for modal open/close to reset form
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    resetForm()
  }
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: rgba(43, 43, 43, 0.95);
  border-radius: 0.5rem;
  padding: 2rem;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  color: white;
  font-family: "Roboto", sans-serif;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
}

.modal-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.modal-description {
  margin: 0 0 1.5rem 0;
  color: rgba(255, 255, 255, 0.8);
}

.skill-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-section h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #4CAF50;
  border-bottom: 1px solid rgba(76, 175, 80, 0.3);
  padding-bottom: 0.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-row .form-group {
  flex: 1;
}

.form-group label {
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
}

.form-input,
.form-textarea {
  padding: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.25rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #4CAF50;
  background: rgba(255, 255, 255, 0.15);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  font-weight: 500;
}

.checkbox-label input[type="checkbox"] {
  margin: 0;
}

.error-message {
  background: rgba(244, 67, 54, 0.2);
  border: 1px solid #f44336;
  border-radius: 0.25rem;
  padding: 0.75rem;
  color: #ffcdd2;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.create-btn {
  background: #4CAF50;
}

.create-btn:hover:not(:disabled) {
  background: #45a049;
}

.create-btn:disabled {
  background: rgba(76, 175, 80, 0.5);
  cursor: not-allowed;
}

.template-description {
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
}

.template-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.template-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
  text-align: left;
}

.template-btn:hover {
  border-color: rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.template-btn.healing:hover {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.1);
}

.template-btn.physical:hover {
  border-color: #FF5722;
  background: rgba(255, 87, 34, 0.1);
}

.template-btn.magic:hover {
  border-color: #9C27B0;
  background: rgba(156, 39, 176, 0.1);
}

.template-btn.forbidden:hover {
  border-color: #F44336;
  background: rgba(244, 67, 54, 0.1);
}

.template-btn.clear:hover {
  border-color: #607D8B;
  background: rgba(96, 125, 139, 0.1);
}

.template-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.template-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.template-info strong {
  font-size: 0.95rem;
  font-weight: 600;
}

.template-info small {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.2;
}
</style>