<script setup lang="ts">
import { computed } from 'vue';

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
  template: CharacterTemplate;
  selected?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  selected: false,
});

const emit = defineEmits<{
  click: [];
  copyId: [templateId: string];
  filterByCategory: [template: CharacterTemplate];
  filterByBehavior: [template: CharacterTemplate];
}>();

// Helper methods
const getTemplateInitials = (name: string) => {
  if (!name) return '??';
  return name.substring(0, 2).toUpperCase();
};

const formatBehavior = (behavior?: string) => {
  if (!behavior) return '';

  // Convert camelCase or snake_case to Title Case with spaces
  return behavior
    // Insert a space before all uppercase letters
    .replace(/([A-Z])/g, ' $1')
    // Replace underscores with spaces
    .replace(/_/g, ' ')
    // Capitalize first letter
    .replace(/^./, str => str.toUpperCase())
    // Trim any extra spaces
    .trim();
};

const handleClick = () => {
  emit('click');
};

const handleCopyId = (event: Event) => {
  event.stopPropagation();
  if (props.template.id) {
    emit('copyId', props.template.id);
  }
};

const handleFilterByCategory = (event: Event) => {
  event.stopPropagation();
  emit('filterByCategory', props.template);
};

const handleFilterByBehavior = (event: Event) => {
  event.stopPropagation();
  emit('filterByBehavior', props.template);
};

// Handle image load errors
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement;
  const parent = img.parentNode as HTMLElement;

  // Create fancy placeholder
  const placeholder = document.createElement('div');
  placeholder.className = 'template-placeholder fancy-placeholder';

  // Add initials
  const initials = document.createElement('span');
  initials.className = 'initials';
  initials.textContent = getTemplateInitials(props.template.name);
  placeholder.appendChild(initials);

  // Replace the image with the placeholder
  parent.replaceChild(placeholder, img);
};
</script>

<template>
  <div
    class="template-card"
    :class="{ 'selected': selected }"
    @click="handleClick"
  >
    <div class="template-avatar">
      <img
        v-if="template.avatar"
        :src="template.avatar"
        :alt="template.name"
        class="template-image"
        @error="handleImageError"
      />
      <div v-else class="template-placeholder fancy-placeholder">
        <span class="initials">{{ getTemplateInitials(template.name) }}</span>
      </div>
    </div>

    <div class="template-info">
      <div class="template-name" :title="template.name">
        {{ template.name }}
      </div>

      <div v-if="template.behavior" class="template-behavior">
        {{ formatBehavior(template.behavior) }}
      </div>

      <div v-if="template.category" class="template-category">
        {{ template.category }}
      </div>

      <div v-if="template.level" class="template-level">
        Level {{ template.level }}
      </div>

      <div class="template-details">
        <span v-if="template.race" class="template-race">{{ template.race }}</span>
        <span v-if="template.class" class="template-class">{{ template.class }}</span>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="template-actions">
      <button
        v-if="template.id"
        @click="handleCopyId"
        class="action-btn copy-btn"
        title="Copy Template ID"
      >
        📋
      </button>

      <button
        v-if="template.category"
        @click="handleFilterByCategory"
        class="action-btn filter-btn"
        title="Filter by Category"
      >
        🏷️
      </button>

      <button
        v-if="template.behavior"
        @click="handleFilterByBehavior"
        class="action-btn filter-btn"
        title="Filter by Behavior"
      >
        🎭
      </button>
    </div>
  </div>
</template>

<style scoped>
.template-card {
  display: flex;
  flex-direction: column;
  padding: 0.7rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.525rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  min-height: 140px;
  backdrop-filter: blur(2px);
}

.template-card:hover {
  border-color: #7fff16;
  background: rgba(0, 0, 0, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(127, 255, 22, 0.2);
}

.template-card.selected {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  box-shadow: 0 0 15px rgba(127, 255, 22, 0.3);
}

.template-avatar {
  width: 60px;
  height: 60px;
  margin: 0 auto 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(127, 255, 22, 0.3);
}

.template-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.template-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border-radius: 50%;
}

.fancy-placeholder {
  background: linear-gradient(135deg, #3a3a3a 0%, #2d2d2d 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  position: relative;
}

.fancy-placeholder::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 60%);
  animation: pulse 3s ease-in-out infinite;
}

.fancy-placeholder .initials {
  position: relative;
  z-index: 2;
  font-size: 1.2rem;
  font-weight: bold;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
  background: linear-gradient(to bottom, #ffffff, #cccccc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: float 2s ease-in-out infinite;
}

@keyframes pulse {
  0% {
    transform: rotate(0deg);
    opacity: 0.5;
  }
  50% {
    opacity: 0.7;
  }
  100% {
    transform: rotate(360deg);
    opacity: 0.5;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

.template-info {
  flex: 1;
  text-align: center;
}

.template-name {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #fada95;
}

.template-behavior {
  font-size: 0.75rem;
  color: rgba(250, 218, 149, 0.8);
  margin-bottom: 0.25rem;
  font-style: italic;
}

.template-category {
  font-size: 0.7rem;
  color: rgba(127, 255, 22, 0.8);
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.template-level {
  font-size: 0.7rem;
  color: rgba(250, 218, 149, 0.7);
  margin-bottom: 0.25rem;
}

.template-details {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.65rem;
  color: rgba(250, 218, 149, 0.6);
}

.template-race,
.template-class {
  padding: 0.1rem 0.3rem;
  background: rgba(127, 255, 22, 0.1);
  border-radius: 0.2rem;
  border: 1px solid rgba(127, 255, 22, 0.2);
}

.template-actions {
  position: absolute;
  top: 0.35rem;
  right: 0.35rem;
  display: flex;
  gap: 0.25rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.template-card:hover .template-actions {
  opacity: 1;
}

.action-btn {
  width: 1.5rem;
  height: 1.5rem;
  border: 1px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.2rem;
  background: rgba(0, 0, 0, 0.7);
  color: #fada95;
  font-size: 0.7rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  backdrop-filter: blur(4px);
}

.action-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: scale(1.1);
}

.action-btn:active {
  transform: scale(0.9);
}

/* Responsive design */
@media (max-width: 640px) {
  .template-card {
    min-height: 120px;
    padding: 0.5rem;
  }

  .template-avatar {
    width: 50px;
    height: 50px;
  }

  .template-name {
    font-size: 0.8rem;
  }

  .template-behavior,
  .template-category,
  .template-level {
    font-size: 0.65rem;
  }

  .template-details {
    font-size: 0.6rem;
  }
}
</style>