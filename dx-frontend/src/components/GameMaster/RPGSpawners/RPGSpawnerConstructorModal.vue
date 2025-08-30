<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import RPGCharactersTemplatePresenter from "@/components/GameMaster/RPGCharacterTempaltes/RPGCharactersTemplatePresenter.vue";
import RPGCharactersTemplatesModal from "@/components/GameMaster/RPGCharacterTempaltes/RPGCharactersTemplatesModal.vue";
import { GMWorldNPCSpawnersApi } from '@/api/backendService.js';
import { worldSpawnersService } from '@/services/WorldSpawnersService';
import type {
  NPCSpawnerCreateRequest,
  GenericSpawner,
  NPCGenericSpawnerRequest,
  PatchedNPCGenericSpawnerRequest,
  NPCSpawnerMinimalPreview
} from '@/api/dx-backend';

interface CharacterTemplate {
  id?: string;
  name: string;
  description?: string;
  behavior?: string;
  avatar?: string;
  category?: string;
  level?: number;
  race?: string;
  class?: string;
}

interface Props {
  positionId: string;
  npcSpawnerId?: string;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  spawnerCreated: [spawnerId: string];
  spawnerUpdated: [spawnerId: string];
  close: [];
}>();

// Form state
const selectedTemplate = ref<CharacterTemplate | null>(null);
const dimensionId = ref<number>(1);
const isActive = ref<boolean>(true);
const spawnLimit = ref<number>(1);
const respawnCycles = ref<number>(1);

// Spawner data state
const currentSpawner = ref<GenericSpawner | null>(null);
const spawnerType = ref<string | null>(null);

// UI state
const isTemplateModalOpen = ref(false);
const isLoading = ref(false);
const error = ref<string | null>(null);
const isSubmitting = ref(false);

// Validation
const isFormValid = computed(() => {
  return selectedTemplate.value && selectedTemplate.value.id;
});

// Template selection handlers
const openTemplateModal = () => {
  isTemplateModalOpen.value = true;
};

const closeTemplateModal = () => {
  isTemplateModalOpen.value = false;
};

const onTemplateSelected = (template: CharacterTemplate) => {
  selectedTemplate.value = template;
  closeTemplateModal();
};

const clearSelectedTemplate = () => {
  selectedTemplate.value = null;
};

// Form submission
const createSpawner = async () => {
  if (!isFormValid.value || !selectedTemplate.value?.id) {
    error.value = 'Please select a character template';
    return;
  }

  isSubmitting.value = true;
  error.value = null;

  try {
    const spawnerData = {
      position: props.positionId,
      character_template: selectedTemplate.value.id,
      dimension: dimensionId.value || undefined,
      is_active: isActive.value,
      spawn_limit: spawnLimit.value,
      respawn_cycles: respawnCycles.value
    };

    const newSpawner = await worldSpawnersService.createNPCSpawner(spawnerData);

    if (newSpawner) {
      emit('spawnerCreated', newSpawner.id || 'unknown');
    }
  } catch (err: any) {
    console.error('Error creating NPC spawner:', err);
    error.value = err.response?.data?.message || err.message || 'Failed to create NPC spawner';
  } finally {
    isSubmitting.value = false;
  }
};

const updateSpawner = async () => {
  if (!isFormValid.value || !selectedTemplate.value?.id || !props.npcSpawnerId) {
    error.value = 'Please select a character template';
    return;
  }

  isSubmitting.value = true;
  error.value = null;

  try {
    const updateData: PatchedNPCGenericSpawnerRequest = {
      character_template: selectedTemplate.value.id,
      dimension: dimensionId.value || undefined,
      is_active: isActive.value,
      spawn_limit: spawnLimit.value,
      respawn_cycles: respawnCycles.value
    };

    const updatedSpawner = await worldSpawnersService.updateNPCSpawner(props.npcSpawnerId, updateData);

    if (updatedSpawner) {
      emit('spawnerUpdated', updatedSpawner.id || 'unknown');
    }
  } catch (err: any) {
    console.error('Error updating NPC spawner:', err);
    error.value = err.response?.data?.message || err.message || 'Failed to update NPC spawner';
  } finally {
    isSubmitting.value = false;
  }
};

const handleSubmit = async () => {
  if (props.npcSpawnerId) {
    await updateSpawner();
  } else {
    await createSpawner();
  }
};

// Load existing spawner data if editing
onMounted(async () => {
  if (props.npcSpawnerId) {
    try {
      isLoading.value = true;
      console.log('Loading existing spawner:', props.npcSpawnerId);

      // Initialize the spawners service if needed
      await worldSpawnersService.initialize();

      // Try to find the spawner (could be generic or NPC)
      const spawner = worldSpawnersService.getSpawnerById(props.npcSpawnerId);

      if (spawner) {
        currentSpawner.value = spawner;

        // Check if it's a generic spawner with object_type
        if ('object_type' in spawner && spawner.object_type) {
          spawnerType.value = spawner.object_type.model;

          // If it's an NPC spawner, extract template from real_instance
          if (spawner.real_instance && typeof spawner.real_instance === 'object') {
            const realInstance = spawner.real_instance as any;
            if (realInstance.character_template) {
              // Set the template ID for prefilling
              selectedTemplate.value = {
                id: realInstance.character_template,
                name: 'Loading...' // Will be updated when template loads
              };
            }
          }
        }

        // If it's an NPCGenericSpawner, get template directly
        if ('character_template' in spawner && spawner.character_template) {
          selectedTemplate.value = {
            id: spawner.character_template,
            name: 'Loading...' // Will be updated when template loads
          };
        }

        // Populate form fields
        if (spawner.dimension !== undefined) {
          dimensionId.value = spawner.dimension || 1;
        }
        isActive.value = spawner.is_active ?? true;
        spawnLimit.value = spawner.spawn_limit || 1;
        respawnCycles.value = spawner.respawn_cycles || 1;

        console.log('Loaded spawner data:', spawner);
        console.log('Spawner type:', spawnerType.value);
      } else {
        console.warn('Spawner not found:', props.npcSpawnerId);
        error.value = 'Spawner not found';
      }
    } catch (err) {
      console.error('Failed to load spawner data:', err);
      error.value = 'Failed to load spawner data';
    } finally {
      isLoading.value = false;
    }
  }
});
</script>

<template>
  <RPGContainer class="npc-spawner-constructor">
    <div class="header">
      <div class="header-top">
        <h2 class="title">
          {{ npcSpawnerId ? 'Edit NPC Spawner' : 'Create NPC Spawner' }}
        </h2>
        <button @click="emit('close')" class="close-btn" title="Close Spawner Constructor">
          ×
        </button>
      </div>
      <!-- Spawner Type Display -->
      <div v-if="spawnerType && npcSpawnerId" class="spawner-type-info">
        <span class="spawner-type-label">Spawner Type:</span>
        <span class="spawner-type-value">{{ spawnerType }}</span>
      </div>
    </div>

    <div class="form-content">
      <!-- Error Display -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- 2-Column Layout: Template Image + Form Fields -->
      <div class="main-content-row">
        <!-- Left Column: Character Template Selection -->
        <div class="template-column">
          <label class="section-label">Character Template *</label>
          <div class="template-selection">
            <div v-if="selectedTemplate" class="selected-template">
              <RPGCharactersTemplatePresenter
                :template-id="selectedTemplate.id"
                :selected="true"
                class="template-display"
                @click="openTemplateModal"
              />
              <button
                @click="clearSelectedTemplate"
                class="clear-template-btn"
                title="Clear selected template"
              >
                ×
              </button>
            </div>
            <div v-else class="template-placeholder" @click="openTemplateModal">
              <div class="placeholder-icon">+</div>
              <div class="placeholder-text">Select Character Template</div>
            </div>
          </div>
        </div>

        <!-- Right Column: Form Fields -->
        <div class="form-column">
          <div class="form-fields">
            <!-- Dimension ID -->
            <div class="form-group">
              <label for="dimensionId" class="field-label">Dimension ID</label>
              <input
                id="dimensionId"
                v-model.number="dimensionId"
                type="number"
                min="1"
                max="10"
                class="form-input"
                placeholder="Dimension ID (1-10)"
              />
            </div>

            <!-- Is Active -->
            <div class="form-group checkbox-group">
              <label class="checkbox-label">
                <input
                  v-model="isActive"
                  type="checkbox"
                  class="form-checkbox"
                />
                <span class="checkbox-text">Active Spawner</span>
              </label>
            </div>

            <!-- Spawn Limit -->
            <div class="form-group">
              <label for="spawnLimit" class="field-label">Spawn Limit</label>
              <input
                id="spawnLimit"
                v-model.number="spawnLimit"
                type="number"
                min="0"
                max="2147483647"
                class="form-input"
                placeholder="Maximum spawns (0 = unlimited)"
              />
            </div>

            <!-- Respawn Cycles -->
            <div class="form-group">
              <label for="respawnCycles" class="field-label">Respawn Cycles</label>
              <input
                id="respawnCycles"
                v-model.number="respawnCycles"
                type="number"
                min="1"
                max="50"
                class="form-input"
                placeholder="Number of respawn cycles"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="form-actions">
        <button
          @click="emit('close')"
          class="cancel-btn"
          :disabled="isSubmitting"
        >
          Cancel
        </button>
        <button
          @click="handleSubmit"
          class="submit-btn"
          :disabled="!isFormValid || isSubmitting"
        >
          <span v-if="isSubmitting">
            {{ npcSpawnerId ? 'Updating...' : 'Creating...' }}
          </span>
          <span v-else>
            {{ npcSpawnerId ? 'Update Spawner' : 'Create Spawner' }}
          </span>
        </button>
      </div>
    </div>

    <!-- Template Selection Modal -->
    <div v-if="isTemplateModalOpen" class="modal-overlay" @click="closeTemplateModal">
      <div class="modal-content" @click.stop>
        <RPGCharactersTemplatesModal
          :selectedTemplateId="selectedTemplate?.id"
          @templateSelected="onTemplateSelected"
          @close="closeTemplateModal"
        />
      </div>
    </div>
  </RPGContainer>
</template>

<style scoped>
.npc-spawner-constructor {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 500px;
  max-height: 700px;
}

.header {
  flex-shrink: 0;
  margin-bottom: 1rem;
}

.spawner-type-info {
  margin-top: 0.5rem;
  padding: 0.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  font-size: 0.9rem;
}

.spawner-type-label {
  font-weight: bold;
  color: #ccc;
  margin-right: 0.5rem;
}

.spawner-type-value {
  color: #fff;
  background-color: rgba(0, 123, 255, 0.2);
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
  border: 1px solid rgba(0, 123, 255, 0.3);
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  flex: 1;
  text-align: center;
}

.close-btn {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  line-height: 1;
}

.close-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-50%) scale(1.1);
  color: #7fff16;
}

.form-content {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.error-message {
  padding: 0.7rem;
  margin-bottom: 1rem;
  background: rgba(255, 0, 0, 0.1);
  border: 2px solid rgba(255, 0, 0, 0.3);
  border-radius: 0.525rem;
  color: #ff6b6b;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  text-align: center;
}

.form-section {
  margin-bottom: 1.5rem;
}

/* 2-Column Layout */
.main-content-row {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.template-column {
  flex: 0 0 auto;
  min-width: 220px;
}

.form-column {
  flex: 1;
  min-width: 300px;
}

.section-label {
  display: block;
  margin-bottom: 0.7rem;
  font-size: 1rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
}

.template-selection {
  position: relative;
}

.selected-template {
  position: relative;
  display: inline-block;
  width: 100%;
}

.template-display {
  cursor: pointer;
  transition: all 0.3s ease;
}

.template-display:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(127, 255, 22, 0.2);
}

.clear-template-btn {
  position: absolute;
  top: -0.5rem;
  right: -0.5rem;
  width: 1.5rem;
  height: 1.5rem;
  border: 2px solid rgba(255, 0, 0, 0.3);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.8);
  color: #ff6b6b;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  line-height: 1;
}

.clear-template-btn:hover {
  border-color: #ff6b6b;
  background: rgba(255, 0, 0, 0.1);
  transform: scale(1.1);
}

.template-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 200px;
  height: 140px;
  border: 2px dashed rgba(127, 255, 22, 0.3);
  border-radius: 0.525rem;
  background: rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
}

.template-placeholder:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.05);
  transform: translateY(-2px);
}

.placeholder-icon {
  font-size: 2rem;
  color: rgba(127, 255, 22, 0.6);
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.placeholder-text {
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: rgba(250, 218, 149, 0.7);
  font-size: 0.9rem;
  text-align: center;
}

.form-fields {
  display: grid;
  gap: 1rem;
  margin-bottom: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
}

.field-label {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
}

.form-input {
  padding: 0.7rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.525rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.9rem;
  transition: border-color 0.3s, background-color 0.3s;
}

.form-input::placeholder {
  color: rgba(250, 218, 149, 0.5);
}

.form-input:focus {
  outline: none;
  border-color: #7fff16;
  background: rgba(0, 0, 0, 0.6);
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
}

.form-checkbox {
  margin-right: 0.7rem;
  width: 1.2rem;
  height: 1.2rem;
  accent-color: #7fff16;
}

.checkbox-text {
  font-size: 0.9rem;
  font-weight: 500;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid rgba(127, 255, 22, 0.2);
}

.cancel-btn,
.submit-btn {
  padding: 0.7rem 1.4rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.525rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover:not(:disabled) {
  border-color: rgba(255, 0, 0, 0.5);
  background: rgba(255, 0, 0, 0.1);
  color: #ff6b6b;
}

.submit-btn:hover:not(:disabled) {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-1px);
}

.submit-btn:disabled,
.cancel-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 90%;
  max-width: 1000px;
  height: 80%;
  max-height: 700px;
}

/* Responsive design */
@media (max-width: 768px) {
  .main-content-row {
    flex-direction: column;
    gap: 1rem;
  }

  .template-column {
    min-width: auto;
  }

  .form-column {
    min-width: auto;
  }

  .form-actions {
    flex-direction: column;
  }

  .template-placeholder {
    width: 100%;
  }
}
</style>