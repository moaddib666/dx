<template>
  <div class="chapter-timeline">
    <div class="timeline-header">
      <h3>Story Timeline</h3>
      <button
        v-if="editMode"
        @click="$emit('create')"
        class="btn-create-chapter"
      >
        <span class="icon">+</span> Add Chapter
      </button>
    </div>

    <div class="timeline-container">
      <div
        v-for="(chapter, index) in chapters"
        :key="chapter.id"
        :class="[
          'timeline-item',
          { 'timeline-item--selected': selectedChapter?.id === chapter.id }
        ]"
        @click="$emit('select', chapter)"
      >
        <!-- Chapter marker -->
        <div class="timeline-marker">
          <span class="chapter-number">{{ index + 1 }}</span>
        </div>

        <!-- Chapter content -->
        <div class="timeline-content">
          <h4>{{ chapter.title }}</h4>
          <p class="chapter-description">{{ chapter.description }}</p>

          <!-- Quest count indicator -->
          <div class="quest-count">
            <span class="icon">📜</span>
            {{ chapter.quests?.length || 0 }} quests
          </div>

          <!-- Edit actions -->
          <div v-if="editMode" class="chapter-actions">
            <button @click.stop="$emit('edit', chapter)" class="action-button">
              <span class="icon">✏️</span>
            </button>
            <button @click.stop="$emit('delete', chapter.id)" class="action-button">
              <span class="icon">🗑️</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import { Chapter } from '@/api/dx-backend';

const props = defineProps<{
  chapters: Chapter[];
  selectedChapter: Chapter | null;
  editMode: boolean;
}>();

defineEmits<{
  (e: 'select', chapter: Chapter): void;
  (e: 'create'): void;
  (e: 'edit', chapter: Chapter): void;
  (e: 'delete', chapterId: string): void;
}>();
</script>

<style scoped>
.chapter-timeline {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.timeline-header h3 {
  font-size: 1.2rem;
  color: var(--cyber-yellow, #ffd700);
  margin: 0;
}

.btn-create-chapter {
  background: rgba(255, 215, 0, 0.2);
  color: var(--cyber-yellow, #ffd700);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

.btn-create-chapter:hover {
  background: rgba(255, 215, 0, 0.3);
  transform: translateY(-2px);
}

.timeline-container {
  position: relative;
}

.timeline-container::before {
  content: '';
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--cyber-yellow, #ffd700);
}

.timeline-item {
  position: relative;
  margin-left: 40px;
  padding: 15px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s ease;
  margin-bottom: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.timeline-item:hover {
  background: rgba(255, 215, 0, 0.1);
  transform: translateY(-2px);
}

.timeline-item--selected {
  background: rgba(255, 215, 0, 0.15);
  border-left: 3px solid var(--cyber-yellow, #ffd700);
}

.timeline-marker {
  position: absolute;
  left: -30px;
  top: 15px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--cyber-yellow, #ffd700);
  display: flex;
  align-items: center;
  justify-content: center;
  color: black;
  font-weight: bold;
}

.timeline-content h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: white;
}

.chapter-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.5rem;
}

.quest-count {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  display: flex;
  align-items: center;
}

.quest-count .icon {
  margin-right: 5px;
}

.chapter-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
}

.action-button {
  background: rgba(0, 0, 0, 0.3);
  border: none;
  border-radius: 4px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover {
  background: rgba(0, 0, 0, 0.5);
}

.icon {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .timeline-item {
    margin-left: 30px;
    padding: 10px;
  }

  .timeline-marker {
    left: -25px;
    width: 25px;
    height: 25px;
  }

  .timeline-container::before {
    left: 15px;
  }
}
</style>