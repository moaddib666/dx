<template>
  <div class="world-editor-items-list">
    <div class="items-list-header">
      <h3>Items</h3>
      <div class="search-container">
        <input
            v-model="searchQuery"
            class="search-input"
            placeholder="Search items..."
            type="text"
        />
        <button class="refresh-btn" title="Refresh Items" @click="refreshItems">
          <span class="icon-refresh"></span>
        </button>
      </div>
    </div>

    <div class="items-filter">
      <select v-model="selectedType" class="type-filter">
        <option value="">All Types</option>
        <option v-for="(value, key) in itemTypes" :key="key" :value="value">
          {{ formatItemType(key) }}
        </option>
      </select>
    </div>

    <div ref="itemsContainer" class="items-container">
      <div v-if="isLoading" class="loading-indicator">
        Loading items...
      </div>

      <div v-else-if="filteredItems.length === 0" class="no-items">
        No items found.
      </div>

      <div
          v-for="item in filteredItems"
          v-else
          :key="item.id"
          class="item-cell"
          draggable="true"
          @click="selectItem(item)"
          @dragstart="onDragStart($event, item)"
      >
        <div class="item-icon">
          <img
              v-if="item.icon"
              :alt="item.name"
              :src="item.icon"
              class="item-image"
          />
          <div v-else class="item-placeholder">
            {{ getItemInitials(item.name) }}
          </div>
        </div>
        <div class="item-info">
          <div class="item-name">{{ item.name }}</div>
          <div v-if="item.type" class="item-type">{{ item.type }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {itemsService} from '@/services/ItemsService.js';
import {dragDropService} from '@/services/DragDropService.js';
import {Type496Enum} from '@/api/dx-backend/api.ts';

export default {
  name: 'WorldEditorItemsList',
  data() {
    return {
      items: [],
      isLoading: true,
      searchQuery: '',
      selectedType: '',
      error: null,
      itemTypes: Type496Enum
    };
  },
  computed: {
    filteredItems() {
      let result = this.items;

      // Filter by type if selected
      if (this.selectedType) {
        result = result.filter(item => item.type === this.selectedType);
      }

      // Filter by search query
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase().trim();
        result = result.filter(item =>
            item.name.toLowerCase().includes(query) ||
            (item.description && item.description.toLowerCase().includes(query))
        );
      }

      return result;
    }
  },
  async mounted() {
    try {
      // Register event listeners
      itemsService.on('loadingStarted', this.onLoadingStarted);
      itemsService.on('itemsLoaded', this.onItemsLoaded);
      itemsService.on('loadingFailed', this.onLoadingFailed);

      // Initialize the service and load items
      await itemsService.initialize();
    } catch (error) {
      console.error('Error initializing items list:', error);
      this.error = error.message || 'Failed to load items';
      this.isLoading = false;
    }
  },
  beforeUnmount() {
    // Clean up event listeners
    itemsService.off('loadingStarted', this.onLoadingStarted);
    itemsService.off('itemsLoaded', this.onItemsLoaded);
    itemsService.off('loadingFailed', this.onLoadingFailed);
  },
  methods: {
    // Event handlers
    onLoadingStarted() {
      this.isLoading = true;
      this.error = null;
    },

    onItemsLoaded(items) {
      this.items = items;
      this.isLoading = false;
    },

    onLoadingFailed(error) {
      console.error('Failed to load items:', error);
      this.error = error.message || 'Failed to load items';
      this.isLoading = false;
    },

    // UI actions
    async refreshItems() {
      try {
        this.isLoading = true;
        await itemsService.refresh();
      } catch (error) {
        console.error('Error refreshing items:', error);
      }
    },

    selectItem(item) {
      // Emit the selected item to parent components
      this.$emit('item-selected', item);
    },

    // Helper methods
    getItemInitials(name) {
      if (!name) return '??';

      // Get first two characters of the name
      return name.substring(0, 2).toUpperCase();
    },

    formatItemType(type) {
      // Convert camelCase or snake_case to Title Case with spaces
      return type
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
    onDragStart(event, item) {
      console.log('Drag start:', item);

      // Set the drag data to the item's JSON string
      const itemJson = JSON.stringify(item);
      event.dataTransfer.setData('text/plain', itemJson);
      // Also set it as application/json for better compatibility
      event.dataTransfer.setData('application/json', itemJson);
      console.log('Set drag data:', itemJson);

      // Set the drag effect to 'copy' to indicate that we're copying the item
      event.dataTransfer.effectAllowed = 'copy';

      // Add a class to the dragged element for visual feedback
      event.target.classList.add('dragging');

      // Create a custom drag image
      const dragImage = this.createDragImage(item);
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
      dragDropService.startDrag(item);

      // Remove the class when the drag ends
      const onDragEnd = () => {
        event.target.classList.remove('dragging');
        event.target.removeEventListener('dragend', onDragEnd);

        // We don't need to call endDrag here, as it will be handled by the DragDropService
        // dragDropService.endDrag();
      };

      event.target.addEventListener('dragend', onDragEnd);
    },

    // Create a custom drag image
    createDragImage(item) {
      // Create a new element for the drag image
      const dragImage = document.createElement('div');
      dragImage.className = 'custom-drag-image';

      // Add item icon
      const iconContainer = document.createElement('div');
      iconContainer.className = 'drag-image-icon';

      if (item.icon) {
        const img = document.createElement('img');
        img.src = item.icon;
        img.alt = item.name;
        iconContainer.appendChild(img);
      } else {
        iconContainer.textContent = this.getItemInitials(item.name);
      }

      // Add item name
      const nameContainer = document.createElement('div');
      nameContainer.className = 'drag-image-name';
      nameContainer.textContent = item.name;

      // Add item type if available
      if (item.type) {
        const typeContainer = document.createElement('div');
        typeContainer.className = 'drag-image-type';
        typeContainer.textContent = item.type;
        dragImage.appendChild(typeContainer);
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
        marginBottom: '5px'
      });

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

      if (dragImage.querySelector('.drag-image-type')) {
        Object.assign(dragImage.querySelector('.drag-image-type').style, {
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
.world-editor-items-list {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #2d2d2d;
  color: #ffffff;
  border-radius: 4px;
  overflow: hidden;
}

.items-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #333;
  border-bottom: 1px solid #444;
}

.items-list-header h3 {
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

.items-filter {
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #444;
}

.type-filter {
  width: 100%;
  padding: 0.25rem;
  background: #444;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  font-size: 0.9rem;
}

.items-container {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
  grid-gap: 0.5rem;
  align-content: start;
}

.loading-indicator, .no-items {
  grid-column: 1 / -1;
  padding: 2rem;
  text-align: center;
  color: #999;
}

.item-cell {
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

.item-cell:hover {
  background: #444;
  border-color: #666;
  transform: translateY(-2px);
}

.item-cell.dragging {
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

.item-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.3rem;
}

.item-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.item-placeholder {
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

.item-info {
  width: 100%;
  text-align: center;
}

.item-name {
  font-size: 0.8rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-type {
  font-size: 0.7rem;
  color: #aaa;
  text-transform: capitalize;
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .items-container {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }
}

@media (max-width: 768px) {
  .items-container {
    grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
  }

  .search-input {
    width: 120px;
  }
}

/* Scrollbar Styling */
.items-container::-webkit-scrollbar {
  width: 6px;
}

.items-container::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.items-container::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}

.items-container::-webkit-scrollbar-thumb:hover {
  background: #666;
}
</style>
