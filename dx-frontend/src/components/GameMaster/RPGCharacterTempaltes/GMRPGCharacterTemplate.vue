<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import RPGGridWithScroller from "@/components/RPGGrid/RPGGridWithScroller.vue";
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import { characterTemplatesService } from '@/services/CharacterTemplatesService.ts';
import { dragDropService } from '@/services/DragDropService.js';

// Props definition
const props = defineProps({
  // Grid configuration
  rows: {
    type: Number,
    default: 3
  },
  cols: {
    type: Number,
    default: 5
  },
  cellSize: {
    type: Number,
    default: 6 // Size in rem
  },
  // Drag configuration
  isDraggable: {
    type: Boolean,
    default: false
  },
  isTemplatesDraggable: {
    type: Boolean,
    default: false
  }
});

// Emit events
const emit = defineEmits(['templateSelected']);

// State
const templates = ref([]);
const isLoading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const selectedBehavior = ref('');
const behaviors = ref([]);

// Dragging state
const position = ref({ x: 0, y: 0 });
const isDragging = ref(false);
const dragOffset = ref({ x: 0, y: 0 });

// Computed properties
const filteredTemplates = computed(() => {
  let result = templates.value;

  // Filter by behavior if selected
  if (selectedBehavior.value) {
    result = result.filter(template => template.behavior === selectedBehavior.value);
  }

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    result = result.filter(template =>
      template.name.toLowerCase().includes(query) ||
      (template.description && template.description.toLowerCase().includes(query))
    );
  }

  return result;
});

// Event handlers
const onLoadingStarted = () => {
  isLoading.value = true;
  error.value = null;
};

const onTemplatesLoaded = (loadedTemplates) => {
  templates.value = loadedTemplates;
  isLoading.value = false;

  // Extract unique behaviors for the filter
  const behaviorSet = new Set();
  loadedTemplates.forEach(template => {
    if (template.behavior) {
      behaviorSet.add(template.behavior);
    }
  });
  behaviors.value = Array.from(behaviorSet);
};

const onLoadingFailed = (err) => {
  console.error('Failed to load templates:', err);
  error.value = err.message || 'Failed to load templates';
  isLoading.value = false;
};

// UI actions
const refreshTemplates = async () => {
  try {
    isLoading.value = true;
    await characterTemplatesService.refresh();
  } catch (err) {
    console.error('Error refreshing templates:', err);
  }
};

const selectTemplate = (template) => {
  // Emit the selected template to parent components
  emit('templateSelected', template);
};

// Helper methods
const getTemplateInitials = (name) => {
  if (!name) return '??';
  return name.substring(0, 2).toUpperCase();
};

const formatBehavior = (behavior) => {
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

// Handle drag start event
const onDragStart = (event, template) => {
  if (!props.isTemplatesDraggable) return;

  console.log('Drag start:', template);

  // Set the drag data to the template's JSON string
  const templateJson = JSON.stringify(template);
  event.dataTransfer.setData('text/plain', templateJson);
  // Also set it as application/json for better compatibility
  event.dataTransfer.setData('application/json', templateJson);
  // Set a custom type to identify this as an NPC template
  event.dataTransfer.setData('application/npc-template', templateJson);

  // Set the drag effect to 'copy' to indicate that we're copying the template
  event.dataTransfer.effectAllowed = 'copy';

  // Add a class to the dragged element for visual feedback
  event.target.classList.add('dragging');

  // Create a custom drag image
  const dragImage = createDragImage(template);
  if (dragImage) {
    // Use the custom drag image
    event.dataTransfer.setDragImage(dragImage, dragImage.width / 2, dragImage.height / 2);

    // Clean up the drag image after a short delay
    setTimeout(() => {
      if (dragImage.parentNode) {
        document.body.removeChild(dragImage);
      }
    }, 100);
  }

  // Notify the drag drop service that we've started dragging
  dragDropService.startDrag({
    type: 'npc-template',
    data: template
  });

  // Remove the class when the drag ends
  const onDragEnd = () => {
    event.target.classList.remove('dragging');
    event.target.removeEventListener('dragend', onDragEnd);
  };

  event.target.addEventListener('dragend', onDragEnd);
};

// Create a custom drag image
const createDragImage = (template) => {
  // Create a new element for the drag image
  const dragImage = document.createElement('div');
  dragImage.className = 'custom-drag-image';

  // Add template icon
  const iconContainer = document.createElement('div');
  iconContainer.className = 'drag-image-icon';

  if (template.avatar) {
    const img = document.createElement('img');
    img.src = template.avatar;
    img.alt = template.name;

    // Handle image load errors
    img.onerror = () => {
      // Create fancy placeholder instead
      iconContainer.classList.add('fancy-placeholder');
      iconContainer.innerHTML = '';

      const initials = document.createElement('span');
      initials.className = 'initials';
      initials.textContent = getTemplateInitials(template.name);
      iconContainer.appendChild(initials);
    };

    iconContainer.appendChild(img);
  } else {
    // Create fancy placeholder
    iconContainer.classList.add('fancy-placeholder');

    const initials = document.createElement('span');
    initials.className = 'initials';
    initials.textContent = getTemplateInitials(template.name);
    iconContainer.appendChild(initials);
  }

  // Add template name
  const nameContainer = document.createElement('div');
  nameContainer.className = 'drag-image-name';
  nameContainer.textContent = template.name;

  // Add template behavior if available
  if (template.behavior) {
    const behaviorContainer = document.createElement('div');
    behaviorContainer.className = 'drag-image-behavior';
    behaviorContainer.textContent = template.behavior;
    dragImage.appendChild(behaviorContainer);
  }

  // Assemble the drag image
  dragImage.appendChild(iconContainer);
  dragImage.appendChild(nameContainer);

  // Add styles
  Object.assign(dragImage.style, {
    position: 'absolute',
    top: '-1000px', // Position off-screen
    padding: '10px',
    background: '#444',
    border: '2px solid #1E90FF',
    borderRadius: '6px',
    boxShadow: '0 0 15px rgba(30, 144, 255, 0.8)',
    color: 'white',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '5px',
    zIndex: '9999',
    pointerEvents: 'none'
  });

  Object.assign(iconContainer.style, {
    width: '40px',
    height: '40px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#555',
    borderRadius: '4px',
    marginBottom: '5px',
    position: 'relative',
    overflow: 'hidden'
  });

  // Apply additional styles for fancy placeholder
  if (iconContainer.classList.contains('fancy-placeholder')) {
    Object.assign(iconContainer.style, {
      background: 'linear-gradient(135deg, #3a3a3a 0%, #2d2d2d 100%)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)'
    });

    // Add the glow effect
    const glowEffect = document.createElement('div');
    Object.assign(glowEffect.style, {
      position: 'absolute',
      top: '-50%',
      left: '-50%',
      width: '200%',
      height: '200%',
      background: 'radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 60%)',
      animation: 'pulse 3s ease-in-out infinite',
      zIndex: '1'
    });
    iconContainer.appendChild(glowEffect);

    // Style the initials
    if (iconContainer.querySelector('.initials')) {
      Object.assign(iconContainer.querySelector('.initials').style, {
        position: 'relative',
        zIndex: '2',
        fontSize: '1rem',
        fontWeight: 'bold',
        textShadow: '0 1px 3px rgba(0, 0, 0, 0.5)',
        color: '#ffffff'
      });
    }
  }

  if (iconContainer.querySelector('img')) {
    Object.assign(iconContainer.querySelector('img').style, {
      maxWidth: '100%',
      maxHeight: '100%',
      objectFit: 'contain'
    });
  }

  Object.assign(nameContainer.style, {
    fontWeight: 'bold',
    fontSize: '12px',
    textAlign: 'center',
    maxWidth: '100px',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap'
  });

  if (dragImage.querySelector('.drag-image-behavior')) {
    Object.assign(dragImage.querySelector('.drag-image-behavior').style, {
      fontSize: '10px',
      color: '#aaa',
      textTransform: 'capitalize'
    });
  }

  // Add to the document
  document.body.appendChild(dragImage);

  return dragImage;
};

// Dragging functionality
const startDrag = (event) => {
  if (!props.isDraggable) return;

  // Don't start drag if we're clicking on an interactive element
  const interactiveElements = ['INPUT', 'SELECT', 'BUTTON', 'A'];
  if (interactiveElements.includes(event.target.tagName)) {
    return;
  }

  isDragging.value = true;

  // Calculate the offset between mouse position and element's top-left corner
  // Use the RPGContainer element (first element with gm-rpg-character-templates class)
  const container = document.querySelector('.gm-rpg-character-templates');
  const rect = container ? container.getBoundingClientRect() : event.currentTarget.getBoundingClientRect();

  dragOffset.value = {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  };

  // Set initial position if not already set
  if (position.value.x === 0 && position.value.y === 0) {
    position.value = {
      x: rect.left,
      y: rect.top
    };
  }

  // Add event listeners for drag and end drag
  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', endDrag);

  // Prevent default behavior
  event.preventDefault();
};

const onDrag = (event) => {
  if (!isDragging.value) return;

  // Get the container element to calculate its dimensions
  const container = document.querySelector('.gm-rpg-character-templates');
  const containerWidth = container ? container.offsetWidth : 300; // Default fallback width
  const containerHeight = container ? container.offsetHeight : 400; // Default fallback height

  // Get viewport dimensions
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  // Calculate new position based on mouse movement and offset
  let newX = event.clientX - dragOffset.value.x;
  let newY = event.clientY - dragOffset.value.y;

  // Apply boundary constraints to keep the component within the viewport
  // Left boundary
  newX = Math.max(0, newX);
  // Right boundary (subtract container width to prevent it from going off-screen)
  newX = Math.min(viewportWidth - containerWidth, newX);
  // Top boundary
  newY = Math.max(0, newY);
  // Bottom boundary (subtract container height to prevent it from going off-screen)
  newY = Math.min(viewportHeight - containerHeight, newY);

  // Update position
  position.value = {
    x: newX,
    y: newY
  };

  // Prevent default behavior
  event.preventDefault();
};

const endDrag = () => {
  isDragging.value = false;

  // Remove event listeners
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', endDrag);
};

// Handle image load errors
const handleImageError = (event, template) => {
  // Replace the image with a fancy placeholder
  const img = event.target;
  const parent = img.parentNode;

  // Create fancy placeholder
  const placeholder = document.createElement('div');
  placeholder.className = 'template-placeholder fancy-placeholder';

  // Add initials
  const initials = document.createElement('span');
  initials.className = 'initials';
  initials.textContent = getTemplateInitials(template.name);
  placeholder.appendChild(initials);

  // Replace the image with the placeholder
  parent.replaceChild(placeholder, img);
};

// Lifecycle hooks
onMounted(async () => {
  try {
    // Register event listeners
    characterTemplatesService.on('loadingStarted', onLoadingStarted);
    characterTemplatesService.on('templatesLoaded', onTemplatesLoaded);
    characterTemplatesService.on('loadingFailed', onLoadingFailed);

    // Initialize the service and load templates
    await characterTemplatesService.initialize();
  } catch (err) {
    console.error('Error initializing templates list:', err);
    error.value = err.message || 'Failed to load templates';
    isLoading.value = false;
  }
});

onBeforeUnmount(() => {
  // Clean up event listeners
  characterTemplatesService.off('loadingStarted', onLoadingStarted);
  characterTemplatesService.off('templatesLoaded', onTemplatesLoaded);
  characterTemplatesService.off('loadingFailed', onLoadingFailed);

  // Clean up drag event listeners if they're still active
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', endDrag);
});
</script>

<template>
  <RPGContainer
    class="gm-rpg-character-templates"
    :class="{ 'draggable': isDraggable }"
    :style="isDraggable ? { position: 'absolute', left: position.x + 'px', top: position.y + 'px', zIndex: isDragging ? 1000 : 10 } : {}"
    @mousedown="startDrag"
  >
    <div class="templates-list-header">
      <h3>Character Templates</h3>
      <div class="templates-filter">
        <select v-model="selectedBehavior" class="behavior-filter">
          <option value="">All Behaviors</option>
          <option v-for="behavior in behaviors" :key="behavior" :value="behavior">
            {{ formatBehavior(behavior) }}
          </option>
        </select>
      </div>
      <div class="search-container">
        <input
          v-model="searchQuery"
          class="search-input"
          placeholder="Search templates..."
          type="text"
        />
        <button class="refresh-btn" title="Refresh Templates" @click="refreshTemplates">
          <span class="icon-refresh"></span>
        </button>
      </div>
    </div>
    <div class="templates-grid-container">
      <div v-if="isLoading" class="loading-indicator">
        Loading templates...
      </div>

      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-else-if="filteredTemplates.length === 0" class="no-templates">
        No templates found.
      </div>

      <RPGGridWithScroller
        v-else
        :row-count="rows"
        :col-count="cols"
        :cell-size="cellSize"
        :items="filteredTemplates"
        class="templates-grid"
        @grid-item-picked="selectTemplate"
      >
        <template #default="{ item }">
          <div
            class="template-wrapper"
            :draggable="isTemplatesDraggable"
            @dragstart="onDragStart($event, item)"
            @click="selectTemplate(item)"
          >
            <div class="template-cell">
              <div class="template-icon">
                <img
                  v-if="item.avatar"
                  :alt="item.name"
                  :src="item.avatar"
                  class="template-image"
                  @error="handleImageError($event, item)"
                />
                <div v-else class="template-placeholder fancy-placeholder">
                  <span class="initials">{{ getTemplateInitials(item.name) }}</span>
                </div>
              </div>
              <div class="template-info">
                <div class="template-name">{{ item.name }}</div>
                <div v-if="item.behavior" class="template-behavior">{{ item.behavior }}</div>
              </div>
            </div>
          </div>
        </template>
      </RPGGridWithScroller>
    </div>
  </RPGContainer>
</template>

<style scoped>
.gm-rpg-character-templates {
  display: flex;
  flex-direction: column;
  color: #ffffff;
  border-radius: 4px;
  overflow: hidden;
}

.gm-rpg-character-templates.draggable {
  cursor: move;
}

.templates-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
}

.templates-list-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.search-container {
  display: flex;
  align-items: center;
}

.search-input {
  padding: 0.25rem 0.5rem;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  font-size: 0.9rem;
  width: 150px;
}

.refresh-btn {
  padding: 0.25rem;
  background: #444;
  color: #ccc;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.refresh-btn:hover {
  background: #555;
  color: #fff;
}

.icon-refresh::before {
  content: '↻';
}

.templates-filter {
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #444;
}

.behavior-filter {
  width: 100%;
  padding: 0.25rem;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  font-size: 0.9rem;
}

.templates-grid-container {
  flex: 1;
  overflow: hidden;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
}

.loading-indicator, .no-templates, .error-message {
  padding: 2rem;
  text-align: center;
  color: #999;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-message {
  color: #ff6b6b;
}

.templates-grid {
  flex: 1;
}

.template-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;
}

.template-wrapper:hover {
  transform: scale(1.05);
}

.template-wrapper.dragging {
  opacity: 0.9;
  background: #444;
  border: 2px solid #1E90FF;
  box-shadow: 0 0 12px rgba(30, 144, 255, 0.7);
  transform: scale(1.1);
  z-index: 1000;
  position: relative;
  cursor: grabbing;
}

.template-cell {
  width: 90%;
  height: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 4px;
  padding: 0.3rem;
}

.template-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.3rem;
}

.template-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.template-placeholder {
  width: 100%;
  height: 100%;
  background: #555;
  color: #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border-radius: 4px;
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

.fancy-placeholder::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 30%;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.2), transparent);
}

.fancy-placeholder .initials {
  position: relative;
  z-index: 2;
  font-size: 1rem;
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
  width: 100%;
  text-align: center;
}

.template-name {
  font-size: 0.8rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.template-behavior {
  font-size: 0.7rem;
  color: #aaa;
  text-transform: capitalize;
}
</style>