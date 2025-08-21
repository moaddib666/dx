<template>
  <div class="skill-factory">
    <div class="skill-factory-row">
      <h3 class="skill-factory-title">Skill Factory</h3>
      <div class="skill-factory-actions">
        <LandingButton :action="openCreateModal" class="create-skill-btn">
          Create New Skill
        </LandingButton>
      </div>
    </div>

    <!-- Skill Creation Modal -->
    <SkillCreationModal
      :is-open="isCreateModalOpen"
      @close="closeCreateModal"
      @skill-created="onSkillCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import LandingButton from '@/components/btn/LandingButton.vue'
import SkillCreationModal from './SkillCreationModal.vue'

// Reactive state
const isCreateModalOpen = ref(false)

// Methods
const openCreateModal = () => {
  isCreateModalOpen.value = true
}

const closeCreateModal = () => {
  isCreateModalOpen.value = false
}

const onSkillCreated = (skill: any) => {
  console.log('Skill created:', skill)
  closeCreateModal()
  // Emit event to parent component if needed
}
</script>

<style scoped>
.skill-factory {
  width: 100%;
  margin: 0.5rem 0;
}

.skill-factory-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(30, 30, 30, 0.95);
  border: 2px solid #555;
  border-radius: 12px;
  padding: 0.625rem 0.875rem;
  color: #ffffff;
  font-family: 'Inter', sans-serif;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
  transition: all 0.2s ease;
}

.skill-factory-row:hover {
  border-color: #1E90FF;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.7);
}

.skill-factory-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  font-family: 'Cinzel', serif;
  color: #fada95;
}

.skill-factory-actions {
  display: flex;
  gap: 0.5rem;
}

.create-skill-btn {
  background: #1E90FF;
  color: white;
  border: none;
  padding: 0.5rem 0.875rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.create-skill-btn:hover {
  background: #1873CC;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}

.create-skill-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}
</style>