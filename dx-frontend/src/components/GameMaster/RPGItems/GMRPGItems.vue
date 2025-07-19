<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import RPGGridWithScroller from "@/components/RPGGrid/RPGGridWithScroller.vue";
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import ItemCell from "@/components/Item/ItemCell.vue";
import { itemsService } from '@/services/ItemsService.js';
import { dragDropService } from '@/services/DragDropService.js';
import { Type496Enum } from '@/api/dx-backend';

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
  isItemsDraggable: {
    type: Boolean,
    default: false
  }
});

// Emit events
const emit = defineEmits(['itemSelected']);

// State
const items = ref([]);
const isLoading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const selectedType = ref('');
const itemTypes = Type496Enum;

// Dragging state
const position = ref({ x: 0, y: 0 });
const isDragging = ref(false);
const dragOffset = ref({ x: 0, y: 0 });

// Computed properties
const filteredItems = computed(() => {
  let result = items.value;

  // Filter by type if selected
  if (selectedType.value) {
    result = result.filter(item => item.type === selectedType.value);
  }

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    result = result.filter(item =>
      item.name.toLowerCase().includes(query) ||
      (item.description && item.description.toLowerCase().includes(query))
    );
  }

  return result;
});

// Event handlers
const onLoadingStarted = () => {
  isLoading.value = true;
  error.value = null;
};

const onItemsLoaded = (loadedItems) => {
  items.value = loadedItems;
  isLoading.value = false;
};

const onLoadingFailed = (err) => {
  console.error('Failed to load items:', err);
  error.value = err.message || 'Failed to load items';
  isLoading.value = false;
};

// UI actions
const refreshItems = async () => {
  try {
    isLoading.value = true;
    await itemsService.refresh();
  } catch (err) {
    console.error('Error refreshing items:', err);
  }
};

const selectItem = (item) => {
  // Emit the selected item to parent components
  emit('itemSelected', item);
};

// Helper methods
const getItemInitials = (name) => {
  if (!name) return '??';
  return name.substring(0, 2).toUpperCase();
};

const formatItemType = (type) => {
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
};

// Handle drag start event
const onDragStart = (event, item) => {
  if (!props.isItemsDraggable) return;

  console.log('Drag start:', item);

  // Set the drag data to the item's JSON string
  const itemJson = JSON.stringify(item);
  event.dataTransfer.setData('text/plain', itemJson);
  // Also set it as application/json for better compatibility
  event.dataTransfer.setData('application/json', itemJson);

  // Set the drag effect to 'copy' to indicate that we're copying the item
  event.dataTransfer.effectAllowed = 'copy';

  // Add a class to the dragged element for visual feedback
  event.target.classList.add('dragging');

  // Create a custom drag image
  const dragImage = createDragImage(item);
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
  };

  event.target.addEventListener('dragend', onDragEnd);
};

// Create a custom drag image
const createDragImage = (item) => {
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
    iconContainer.textContent = getItemInitials(item.name);
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
  // Use the RPGContainer element (first element with gm-rpg-items class)
  const container = document.querySelector('.gm-rpg-items');
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
  const container = document.querySelector('.gm-rpg-items');
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

// Lifecycle hooks
onMounted(async () => {
  try {
    // Register event listeners
    itemsService.on('loadingStarted', onLoadingStarted);
    itemsService.on('itemsLoaded', onItemsLoaded);
    itemsService.on('loadingFailed', onLoadingFailed);

    // Initialize the service and load items
    await itemsService.initialize();
  } catch (err) {
    console.error('Error initializing items list:', err);
    error.value = err.message || 'Failed to load items';
    isLoading.value = false;
  }
});

onBeforeUnmount(() => {
  // Clean up event listeners
  itemsService.off('loadingStarted', onLoadingStarted);
  itemsService.off('itemsLoaded', onItemsLoaded);
  itemsService.off('loadingFailed', onLoadingFailed);

  // Clean up drag event listeners if they're still active
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', endDrag);
});
</script>

<template>
  <RPGContainer
    class="gm-rpg-items"
    :class="{ 'draggable': isDraggable }"
    :style="isDraggable ? { position: 'absolute', left: position.x + 'px', top: position.y + 'px', zIndex: isDragging ? 1000 : 10 } : {}"
    @mousedown="startDrag"
  >
    <div class="items-list-header">
      <h3>Items</h3>
      <div class="items-filter">
        <select v-model="selectedType" class="type-filter">
          <option value="">All Types</option>
          <option v-for="(value, key) in itemTypes" :key="key" :value="value">
            {{ formatItemType(key) }}
          </option>
        </select>
      </div>
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
    <div class="items-grid-container">
      <div v-if="isLoading" class="loading-indicator">
        Loading items...
      </div>

      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-else-if="filteredItems.length === 0" class="no-items">
        No items found.
      </div>

      <RPGGridWithScroller
        v-else
        :row-count="rows"
        :col-count="cols"
        :cell-size="cellSize"
        :items="filteredItems"
        class="items-grid"
        @grid-item-picked="selectItem"
      >
        <template #default="{ item }">
          <div
            class="item-wrapper"
            :draggable="isItemsDraggable"
            @dragstart="onDragStart($event, item)"
            @click="selectItem(item)"
          >
            <ItemCell
              v-if="item"
              :itemData="{ item: item }"
              class="item-cell"
            />
          </div>
        </template>
      </RPGGridWithScroller>
    </div>
  </RPGContainer>
</template>

<style scoped>
.gm-rpg-items {
  display: flex;
  flex-direction: column;
  color: #ffffff;
  border-radius: 4px;
  overflow: hidden;
}

.gm-rpg-items.draggable {
  cursor: move;
}

.items-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
}

.items-list-header h3 {
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

.items-grid-container {
  flex: 1;
  overflow: hidden;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
}

.loading-indicator, .no-items, .error-message {
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

.items-grid {
  flex: 1;
}

.item-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;
}

.item-wrapper:hover {
  transform: scale(1.05);
}

.item-wrapper.dragging {
  opacity: 0.9;
  background: #444;
  border: 2px solid #1E90FF;
  box-shadow: 0 0 12px rgba(30, 144, 255, 0.7);
  transform: scale(1.1);
  z-index: 1000;
  position: relative;
  cursor: grabbing;
}

.item-cell {
  width: 90%;
  height: 90%;
}

</style>