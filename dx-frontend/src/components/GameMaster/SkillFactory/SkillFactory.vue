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
  margin: 1rem 0;
}

.skill-factory-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(43, 43, 43, 0.8);
  border-radius: 0.5rem;
  padding: 1rem;
  color: white;
  font-family: "Roboto", sans-serif;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.skill-factory-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 500;
}

.skill-factory-actions {
  display: flex;
  gap: 0.5rem;
}

.create-skill-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.create-skill-btn:hover {
  background: #45a049;
}
</style>