<template>
  <div class="npc-templates-list">
    <div class="templates-list-header">
      <h3>NPC Templates</h3>
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

    <div class="templates-filter">
      <select v-model="selectedBehavior" class="behavior-filter">
        <option value="">All Behaviors</option>
        <option v-for="behavior in behaviors" :key="behavior" :value="behavior">
          {{ formatBehavior(behavior) }}
        </option>
      </select>
    </div>

    <div ref="templatesContainer" class="templates-container">
      <div v-if="isLoading" class="loading-indicator">
        Loading templates...
      </div>

      <div v-else-if="filteredTemplates.length === 0" class="no-templates">
        No templates found.
      </div>

      <div
          v-for="template in filteredTemplates"
          v-else
          :key="template.id"
          class="template-cell"
          draggable="true"
          @click="selectTemplate(template)"
          @dragstart="onDragStart($event, template)"
      >
        <div class="template-icon">
          <img
              v-if="template.avatar"
              :alt="template.name"
              :src="template.avatar"
              class="template-image"
              @error="handleImageError($event, template)"
          />
          <div v-else class="template-placeholder fancy-placeholder">
            <span class="initials">{{ getTemplateInitials(template.name) }}</span>
          </div>
        </div>
        <div class="template-info">
          <div class="template-name">{{ template.name }}</div>
          <div v-if="template.behavior" class="template-behavior">{{ template.behavior }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {characterTemplatesService} from '@/services/CharacterTemplatesService.js';
import {dragDropService} from '@/services/DragDropService.js';

export default {
  name: 'NPCTemplatesList',
  props: {
    // Optional title for the component
    title: {
      type: String,
      default: 'NPC Templates'
    }
  },
  data() {
    return {
      templates: [],
      isLoading: true,
      searchQuery: '',
      selectedBehavior: '',
      error: null,
      behaviors: [] // Will be populated from templates
    };
  },
  computed: {
    filteredTemplates() {
      let result = this.templates;

      // Filter by behavior if selected
      if (this.selectedBehavior) {
        result = result.filter(template => template.behavior === this.selectedBehavior);
      }

      // Filter by search query
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase().trim();
        result = result.filter(template =>
            template.name.toLowerCase().includes(query) ||
            (template.description && template.description.toLowerCase().includes(query))
        );
      }

      return result;
    }
  },
  async mounted() {
    try {
      // Register event listeners
      characterTemplatesService.on('loadingStarted', this.onLoadingStarted);
      characterTemplatesService.on('templatesLoaded', this.onTemplatesLoaded);
      characterTemplatesService.on('loadingFailed', this.onLoadingFailed);

      // Initialize the service and load templates
      await characterTemplatesService.initialize();
    } catch (error) {
      console.error('Error initializing templates list:', error);
      this.error = error.message || 'Failed to load templates';
      this.isLoading = false;
    }
  },
  beforeUnmount() {
    // Clean up event listeners
    characterTemplatesService.off('loadingStarted', this.onLoadingStarted);
    characterTemplatesService.off('templatesLoaded', this.onTemplatesLoaded);
    characterTemplatesService.off('loadingFailed', this.onLoadingFailed);
  },
  methods: {
    // Event handlers
    onLoadingStarted() {
      this.isLoading = true;
      this.error = null;
    },

    onTemplatesLoaded(templates) {
      this.templates = templates;
      this.isLoading = false;

      // Extract unique behaviors for the filter
      const behaviorSet = new Set();
      templates.forEach(template => {
        if (template.behavior) {
          behaviorSet.add(template.behavior);
        }
      });
      this.behaviors = Array.from(behaviorSet);
    },

    onLoadingFailed(error) {
      console.error('Failed to load templates:', error);
      this.error = error.message || 'Failed to load templates';
      this.isLoading = false;
    },

    // UI actions
    async refreshTemplates() {
      try {
        this.isLoading = true;
        await characterTemplatesService.refresh();
      } catch (error) {
        console.error('Error refreshing templates:', error);
      }
    },

    selectTemplate(template) {
      // Emit the selected template to parent components
      this.$emit('template-selected', template);
    },

    // Helper methods
    getTemplateInitials(name) {
      if (!name) return '??';

      // Get first two characters of the name
      return name.substring(0, 2).toUpperCase();
    },

    // Handle image load errors
    handleImageError(event, template) {
      // Replace the image with a fancy placeholder
      const img = event.target;
      const parent = img.parentNode;

      // Create fancy placeholder
      const placeholder = document.createElement('div');
      placeholder.className = 'template-placeholder fancy-placeholder';

      // Add initials
      const initials = document.createElement('span');
      initials.className = 'initials';
      initials.textContent = this.getTemplateInitials(template.name);
      placeholder.appendChild(initials);

      // Replace the image with the placeholder
      parent.replaceChild(placeholder, img);
    },

    formatBehavior(behavior) {
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
    },

    // Handle drag start event
    onDragStart(event, template) {
      console.log('Drag start:', template);

      // Set the drag data to the template's JSON string
      const templateJson = JSON.stringify(template);
      event.dataTransfer.setData('text/plain', templateJson);
      // Also set it as application/json for better compatibility
      event.dataTransfer.setData('application/json', templateJson);
      // Set a custom type to identify this as an NPC template
      event.dataTransfer.setData('application/npc-template', templateJson);
      console.log('Set drag data:', templateJson);

      // Set the drag effect to 'copy' to indicate that we're copying the template
      event.dataTransfer.effectAllowed = 'copy';

      // Add a class to the dragged element for visual feedback
      event.target.classList.add('dragging');

      // Create a custom drag image
      const dragImage = this.createDragImage(template);
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
    },

    // Create a custom drag image
    createDragImage(template) {
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
          initials.textContent = this.getTemplateInitials(template.name);
          iconContainer.appendChild(initials);
        };

        iconContainer.appendChild(img);
      } else {
        // Create fancy placeholder
        iconContainer.classList.add('fancy-placeholder');

        const initials = document.createElement('span');
        initials.className = 'initials';
        initials.textContent = this.getTemplateInitials(template.name);
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
    }
  }
};
</script>

<style scoped>
.npc-templates-list {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #2d2d2d;
  color: #ffffff;
  border-radius: 4px;
  overflow: hidden;
}

.templates-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #333;
  border-bottom: 1px solid #444;
}

.templates-list-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.search-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.templates-container {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
  grid-gap: 0.5rem;
  align-content: start;
}

.loading-indicator, .no-templates {
  grid-column: 1 / -1;
  padding: 2rem;
  text-align: center;
  color: #999;
}

.template-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.3rem;
  background: #3a3a3a;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.template-cell:hover {
  background: #444;
  border-color: #666;
  transform: translateY(-2px);
}

.template-cell.dragging {
  opacity: 0.9;
  background: #444;
  border: 2px solid #1E90FF;
  box-shadow: 0 0 12px rgba(30, 144, 255, 0.7);
  transform: scale(1.1);
  z-index: 1000;
  position: relative;
  /* Add a custom cursor to make it clear this is being dragged */
  cursor: grabbing;
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

/* Responsive adjustments */
@media (max-width: 1200px) {
  .templates-container {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }
}

@media (max-width: 768px) {
  .templates-container {
    grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
  }

  .search-input {
    width: 120px;
  }
}

/* Scrollbar Styling */
.templates-container::-webkit-scrollbar {
  width: 6px;
}

.templates-container::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.templates-container::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}

.templates-container::-webkit-scrollbar-thumb:hover {
  background: #666;
}
</style>