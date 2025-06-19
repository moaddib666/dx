<template>
  <div class="inventory-grid-container">
    <!-- Filters and pagination controls -->
    <div class="inventory-controls">
      <div class="filter-controls">
        <select v-model="selectedType" class="type-filter">
          <option value="">All Types</option>
          <option v-for="type in uniqueItemTypes" :key="type" :value="type">
            {{ formatItemType(type) }}
          </option>
        </select>
        <button class="page-button refresh-button" title="Refresh inventory" @click="refreshInventory">
          ↻
        </button>
      </div>
      <div class="pagination-controls">
        <button
            :disabled="currentPage === 1"
            class="page-button"
            @click="prevPage"
        >
          ◀
        </button>
        <span class="page-indicator">{{ currentPage }} / {{ totalPages }}</span>
        <button
            :disabled="currentPage === totalPages"
            class="page-button"
            @click="nextPage"
        >
          ▶
        </button>
      </div>
    </div>

    <!-- Inventory grid -->
    <div class="inventory-grid">
      <div
          v-for="(cell, index) in currentPageCells"
          :key="index"
          :class="{ 'has-item': cell.item }"
          class="inventory-cell"
          @click="cell.item && selectItem(cell.item)"
      >
        <template v-if="cell.item">
          <div class="item-icon">
            <img
                v-if="getItemIcon(cell.item)"
                :alt="getItemName(cell.item)"
                :src="getItemIcon(cell.item)"
                class="item-image"
            />
            <div v-else class="item-placeholder">
              {{ getItemInitials(getItemName(cell.item)) }}
            </div>
          </div>
          <div class="item-info">
            <div class="item-name">{{ getItemName(cell.item) }}</div>
          </div>
        </template>
        <div v-else class="empty-cell"></div>
      </div>
    </div>
  </div>
</template>

<script>
import {gameMasterCharacterService} from '@/services/GameMasterCharacterService.js';

export default {
  name: 'GameMasterInventoryGrid',
  props: {
    items: {
      type: Array,
      required: true,
      default: () => []
    },
    characterId: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 24, // 4 columns x 6 rows
      selectedType: ''
    };
  },
  computed: {
    // Filter items by type
    filteredItems() {
      if (!this.selectedType) {
        return this.items;
      }
      return this.items.filter(item => this.getItemType(item) === this.selectedType);
    },

    // Calculate total pages
    totalPages() {
      return Math.max(1, Math.ceil(this.filteredItems.length / this.itemsPerPage));
    },

    // Get items for current page
    currentPageItems() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredItems.slice(startIndex, startIndex + this.itemsPerPage);
    },

    // Create a 4x6 grid with items or empty cells
    currentPageCells() {
      const cells = Array(this.itemsPerPage).fill().map(() => ({item: null}));

      this.currentPageItems.forEach((item, index) => {
        if (index < cells.length) {
          cells[index].item = item;
        }
      });

      return cells;
    },

    // Get unique item types for filter dropdown
    uniqueItemTypes() {
      const types = new Set();
      this.items.forEach(item => {
        const type = this.getItemType(item);
        if (type) {
          types.add(type);
        }
      });
      return Array.from(types).sort();
    }
  },
  watch: {
    // Reset to first page when filter changes
    selectedType() {
      this.currentPage = 1;
    },

    // Reset to first page when items change
    items() {
      this.currentPage = 1;
    }
  },
  methods: {
    // Refresh inventory
    async refreshInventory() {
      try {
        // Emit event for backward compatibility
        this.$emit('refresh-inventory');

        // If characterId is provided, use the service to refresh the character data
        if (this.characterId) {
          console.log(`Refreshing character inventory for ${this.characterId}`);
          await gameMasterCharacterService.refreshCharacter(this.characterId);
        } else {
          console.warn('Cannot refresh inventory: No characterId provided');
        }
      } catch (error) {
        console.error('Error refreshing inventory:', error);
      }
    },

    // Pagination methods
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },

    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },

    // Item selection
    selectItem(item) {
      this.$emit('world-item-selected', this.getWorldItemId(item));
    },

    // Helper methods for accessing item properties
    getItemName(item) {
      return item.world_item?.item?.name || item.name || 'Unknown Item';
    },

    getItemType(item) {
      return item.world_item?.item?.type || item.type || '';
    },

    getItemIcon(item) {
      return item.world_item?.item?.icon || item.icon || null;
    },

    getWorldItemId(item) {
      return item.world_item?.id || item.id || null;
    },

    getItemInitials(name) {
      if (!name) return '??';
      return name.substring(0, 2).toUpperCase();
    },

    formatItemType(type) {
      if (!type) return 'Item';

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
    }
  }
};
</script>

<style scoped>
.inventory-grid-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  background: rgba(20, 20, 20, 0.5);
  border-radius: 4px;
  padding: 0.25rem;
  border: 1px solid rgba(30, 144, 255, 0.2);
}

/* Controls section */
.inventory-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
}

.filter-controls {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.refresh-button {
  font-size: 0.8rem;
  padding: 0;
}

.type-filter {
  width: 100%;
  max-width: 120px;
  padding: 0.15rem;
  background: rgba(40, 40, 40, 0.8);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  font-size: 0.7rem;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.page-button {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(40, 40, 40, 0.8);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.7rem;
}

.page-button:hover:not(:disabled) {
  background: rgba(30, 144, 255, 0.3);
}

.page-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-indicator {
  font-size: 0.7rem;
  color: #ccc;
}

/* Inventory grid */
.inventory-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  grid-template-rows: repeat(6, minmax(0, 1fr));
  gap: 0.2rem;
  height: 220px; /* Reduced fixed height for 6 rows */
  width: 100%;
}

.inventory-cell {
  background: rgba(30, 30, 30, 0.7);
  border-radius: 3px;
  border: 1px solid rgba(30, 144, 255, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.15rem;
  min-height: 36px;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

.inventory-cell.has-item {
  cursor: pointer;
}

.inventory-cell.has-item:hover {
  background: rgba(40, 40, 40, 0.8);
  border-color: rgba(30, 144, 255, 0.6);
}

.empty-cell {
  width: 100%;
  height: 100%;
  border: 1px dashed rgba(30, 144, 255, 0.2);
  border-radius: 3px;
}

/* Item styling */
.item-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.1rem;
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
  font-size: 0.6rem;
  border-radius: 2px;
}

.item-info {
  width: 100%;
  text-align: center;
  max-width: 100%;
  overflow: hidden;
  max-height: 24px;
}

.item-name {
  font-weight: bold;
  font-size: 0.55rem;
  overflow: hidden;
  text-overflow: ellipsis;
  color: rgba(255, 255, 255, 0.9);
  width: 100%;
  max-width: 100%;
  word-break: break-word;
}


/* Responsive adjustments */
@media (max-width: 768px) {
  .inventory-grid {
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(6, 1fr);
    height: 220px; /* Keep the same compact height */
  }
}
</style>
