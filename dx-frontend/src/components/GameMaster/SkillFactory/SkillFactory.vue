<template>
  <RPGContainer class="skill-factory-container">
    <div class="header">
      <div class="header-top">
        <h2 class="title">Skill Factory</h2>
        <div class="skill-factory-actions">
          <button @click="openCreateModal" class="create-skill-btn">
            Create New Skill
          </button>
        </div>
      </div>
    </div>

    <!-- Skill Creation Modal -->
    <SkillCreationModal
      :is-open="isCreateModalOpen"
      @close="closeCreateModal"
      @skill-created="onSkillCreated"
    />
  </RPGContainer>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import RPGContainer from '@/components/RPGContainer/RPGContainer.vue'
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
.skill-factory-container {
  display: flex;
  flex-direction: column;
  min-height: 200px;
}

.header {
  flex-shrink: 0;
  margin-bottom: 0.7rem;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.7rem;
  position: relative;
}

.title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  flex: 1;
  text-align: center;
}

.skill-factory-actions {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

.create-skill-btn {
  padding: 0.35rem 0.7rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.create-skill-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  color: #7fff16;
  transform: translateY(-50%) scale(1.05);
}

.create-skill-btn:active {
  transform: translateY(-50%) scale(0.95);
}
</style>