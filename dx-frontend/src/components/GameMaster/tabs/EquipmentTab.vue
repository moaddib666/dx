<template>
  <div class="equipment-tab">
    <h3>Equipment & Items ({{ template.data.items.length }}/{{ template.validation.max_items_count }})</h3>

    <!-- Current Items Section -->
    <div class="current-items-section">
      <h4>Current Equipment</h4>
      <div class="current-items-container">
        <div v-if="currentItems.length === 0" class="no-items">
          No items equipped
        </div>
        <div v-else class="current-items-grid">
          <div
            v-for="item in currentItems"
            :key="item.id"
            class="current-item-icon"
            @click="removeItem(item.id)"
            :title="`${item.name} - Click to remove`"
          >
            <img v-if="item.icon" :src="item.icon" :alt="item.name" />
            <div v-else class="placeholder-icon">
              <span>{{ item.name?.charAt(0)?.toUpperCase() || '?' }}</span>
            </div>
            <div class="item-name">{{ item.name || `Item ${item.id}` }}</div>
            <div class="remove-indicator">×</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Items Section -->
    <div v-if="template.data.items.length < template.validation.max_items_count" class="add-items-section">
      <h4>Available Items</h4>
      
      <!-- Search and Filter Controls -->
      <div class="controls-row">
        <div class="search-container">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search items..."
            class="search-input"
          />
        </div>
        <div class="filter-container">
          <select v-model="selectedType" class="type-filter">
            <option value="">All Types</option>
            <option v-for="type in availableTypes" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
        </div>
        <button class="refresh-button" @click="refreshItems" :disabled="isLoading" title="Refresh items">
          ↻
        </button>
      </div>

      <!-- Available Items Grid -->
      <div class="available-items-container">
        <div v-if="isLoading" class="loading-message">
          Loading items...
        </div>
        <div v-else-if="filteredItems.length === 0" class="no-results">
          No items found
        </div>
        <div v-else>
          <div class="items-grid">
            <div
              v-for="item in paginatedItems"
              :key="item.id"
              :class="['item-icon', { 'item-selected': isItemSelected(item.id), 'item-disabled': !canAddItem() }]"
              @click="addItem(item)"
              :title="`${item.name} - ${item.type || 'Unknown type'}${isItemSelected(item.id) ? ' (Already selected)' : ''}`"
            >
              <img v-if="item.icon" :src="item.icon" :alt="item.name" />
              <div v-else class="placeholder-icon">
                <span>{{ item.name?.charAt(0)?.toUpperCase() || '?' }}</span>
              </div>
              <div class="item-name">{{ item.name || `Item ${item.id}` }}</div>
              <div v-if="isItemSelected(item.id)" class="selected-indicator">✓</div>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="pagination">
            <button
              @click="currentPage = Math.max(1, currentPage - 1)"
              :disabled="currentPage === 1"
              class="page-button"
            >
              ← Previous
            </button>
            <span class="page-info">
              Page {{ currentPage }} of {{ totalPages }}
            </span>
            <button
              @click="currentPage = Math.min(totalPages, currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="page-button"
            >
              Next →
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Equipment Summary -->
    <div class="equipment-summary">
      <div class="summary-card">
        <h4>Summary</h4>
        <div class="summary-stats">
          <div class="stat-row">
            <span>Items:</span>
            <span>{{ template.data.items.length }}/{{ template.validation.max_items_count }}</span>
          </div>
          <div class="stat-row">
            <span>Remaining Slots:</span>
            <span>{{ template.validation.max_items_count - template.data.items.length }}</span>
          </div>
          <div v-if="itemTypesSummary" class="stat-row">
            <span>Types:</span>
            <span class="types-summary">{{ itemTypesSummary }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { itemsService } from '@/services/ItemsService.js';

export default {
  name: 'EquipmentTab',
  props: {
    template: {
      type: Object,
      required: true
    },
    service: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      itemsService: itemsService,
      allItems: [],
      isLoading: false,
      searchQuery: '',
      selectedType: '',
      currentPage: 1,
      itemsPerPage: 12
    };
  },
  computed: {
    currentItems() {
      return this.template.data.items
        .map(itemId => this.allItems.find(item => item.id === itemId))
        .filter(item => item !== undefined);
    },
    availableTypes() {
      const types = [...new Set(this.allItems.map(item => item.type).filter(Boolean))];
      return types.sort();
    },
    filteredItems() {
      let items = this.allItems;

      // Filter by search query
      if (this.searchQuery.trim()) {
        items = this.itemsService.searchItems(this.searchQuery);
      }

      // Filter by type
      if (this.selectedType) {
        items = items.filter(item => item.type === this.selectedType);
      }

      return items;
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredItems.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    itemTypesSummary() {
      const typeCounts = {};
      this.currentItems.forEach(item => {
        const type = item.type || 'Unknown';
        typeCounts[type] = (typeCounts[type] || 0) + 1;
      });
      
      return Object.entries(typeCounts)
        .map(([type, count]) => `${type} (${count})`)
        .join(', ') || 'None';
    }
  },
  async created() {
    await this.loadItems();
    
    // Set up event listeners for items service
    this.itemsService.on('itemsLoaded', this.onItemsLoaded);
    this.itemsService.on('loadingStarted', this.onLoadingStarted);
    this.itemsService.on('loadingFailed', this.onLoadingFailed);
  },
  beforeUnmount() {
    // Clean up event listeners
    this.itemsService.off('itemsLoaded', this.onItemsLoaded);
    this.itemsService.off('loadingStarted', this.onLoadingStarted);
    this.itemsService.off('loadingFailed', this.onLoadingFailed);
  },
  watch: {
    searchQuery() {
      this.currentPage = 1; // Reset to first page when searching
    },
    selectedType() {
      this.currentPage = 1; // Reset to first page when filtering
    }
  },
  methods: {
    async loadItems() {
      try {
        this.isLoading = true;
        await this.itemsService.initialize();
        this.allItems = this.itemsService.getItems();
      } catch (error) {
        console.error('Failed to load items:', error);
      } finally {
        this.isLoading = false;
      }
    },
    async refreshItems() {
      try {
        this.isLoading = true;
        await this.itemsService.refresh();
        this.allItems = this.itemsService.getItems();
      } catch (error) {
        console.error('Failed to refresh items:', error);
      } finally {
        this.isLoading = false;
      }
    },
    addItem(item) {
      if (this.template.data.items.length >= this.template.validation.max_items_count) {
        return;
      }
      
      if (this.isItemSelected(item.id)) {
        return; // Already selected
      }
      
      this.service.addItem(item.id);
      this.$emit('update');
    },
    canAddItem() {
      return this.template.data.items.length < this.template.validation.max_items_count;
    },
    removeItem(itemId) {
      this.service.removeItem(itemId);
      this.$emit('update');
    },
    isItemSelected(itemId) {
      return this.template.data.items.includes(itemId);
    },
    // Event handlers
    onItemsLoaded(items) {
      this.allItems = items;
      this.isLoading = false;
    },
    onLoadingStarted() {
      this.isLoading = true;
    },
    onLoadingFailed(error) {
      console.error('Items loading failed:', error);
      this.isLoading = false;
    }
  }
};
</script>

<style scoped>
.equipment-tab {
  padding: 20px 0;
}

/* Current Items Section */
.current-items-section {
  margin-bottom: 30px;
}

.current-items-section h4 {
  color: #1E90FF;
  margin-bottom: 15px;
}

.current-items-container {
  background: #333;
  border-radius: 4px;
  padding: 15px;
  border: 1px solid #444;
  min-height: 80px;
}

.no-items {
  color: #888;
  text-align: center;
  padding: 20px;
  font-style: italic;
}

.current-items-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.current-item-icon {
  position: relative;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #1a1a2e, #16213e);
  border: 2px solid #9e9e9e;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  overflow: hidden;
}

.current-item-icon:hover {
  transform: scale(1.05);
  box-shadow: 0 0 12px rgba(255, 255, 255, 0.5);
  border-color: #f44336;
}

.current-item-icon img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 4px;
}

.placeholder-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #555, #666);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
  font-weight: bold;
  font-size: 18px;
  border-radius: 4px;
}

.current-item-icon .item-name {
  position: absolute;
  bottom: 2px;
  left: 2px;
  right: 2px;
  font-size: 8px;
  color: #00e5ff;
  text-shadow: 0 0 3px #00e5ff;
  background: rgba(0, 0, 0, 0.8);
  padding: 1px 2px;
  text-align: center;
  text-transform: uppercase;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.remove-indicator {
  position: absolute;
  top: 2px;
  right: 2px;
  background: rgba(244, 67, 54, 0.8);
  color: white;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: none;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.current-item-icon:hover .remove-indicator {
  display: flex;
}

/* Add Items Section */
.add-items-section {
  margin-bottom: 30px;
}

.add-items-section h4 {
  color: #1E90FF;
  margin-bottom: 15px;
}

/* Controls Row */
.controls-row {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  align-items: center;
}

.search-container {
  flex: 1;
}

.search-input {
  width: 100%;
  padding: 10px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #1E90FF;
  outline: none;
}

.filter-container {
  min-width: 150px;
}

.type-filter {
  width: 100%;
  padding: 10px;
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  cursor: pointer;
}

.type-filter:focus {
  border-color: #1E90FF;
  outline: none;
}

.refresh-button {
  padding: 10px 12px;
  background: #666;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 16px;
}

.refresh-button:hover:not(:disabled) {
  background: #777;
}

.refresh-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Available Items Grid */
.available-items-container {
  background: #2d2d2d;
  border-radius: 6px;
  padding: 20px;
  border: 1px solid #444;
}

.loading-message, .no-results {
  text-align: center;
  color: #888;
  padding: 40px;
  font-style: italic;
}

.items-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.item-icon {
  position: relative;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #1a1a2e, #16213e);
  border: 2px solid #9e9e9e;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  overflow: hidden;
}

.item-icon:hover {
  transform: scale(1.05);
  box-shadow: 0 0 12px rgba(255, 255, 255, 0.5);
  border-color: #1E90FF;
}

.item-icon.item-selected {
  border-color: #4CAF50;
  box-shadow: 0 0 12px rgba(76, 175, 80, 0.5);
}

.item-icon.item-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.item-icon.item-disabled:hover {
  transform: none;
  box-shadow: none;
  border-color: #9e9e9e;
}

.item-icon img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 4px;
}

.item-icon .item-name {
  position: absolute;
  bottom: 2px;
  left: 2px;
  right: 2px;
  font-size: 8px;
  color: #00e5ff;
  text-shadow: 0 0 3px #00e5ff;
  background: rgba(0, 0, 0, 0.8);
  padding: 1px 2px;
  text-align: center;
  text-transform: uppercase;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.selected-indicator {
  position: absolute;
  top: 2px;
  right: 2px;
  background: #4CAF50;
  color: white;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

/* Item Image */
.item-image {
  width: 48px;
  height: 48px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
  background: #444;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-image {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #555, #666);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
  font-weight: bold;
  font-size: 18px;
}

/* Item Details */
.item-details {
  flex: 1;
  min-width: 0;
}

.item-info {
  flex: 1;
  padding-top: 8px;
}

.item-name {
  font-weight: bold;
  color: #fff;
  margin-bottom: 4px;
  font-size: 14px;
  line-height: 1.2;
}

.item-type {
  color: #1E90FF;
  font-size: 12px;
  margin-bottom: 4px;
  text-transform: uppercase;
  font-weight: 500;
}

.item-description {
  color: #ccc;
  font-size: 12px;
  line-height: 1.3;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* Remove Button */
.item-remove {
  background: none;
  border: none;
  color: #f44336;
  cursor: pointer;
  font-size: 20px;
  padding: 4px;
  margin: 0;
  transition: color 0.3s ease;
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.item-remove:hover {
  color: #fff;
  background: #f44336;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
}

.page-button {
  padding: 8px 16px;
  background: #444;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.page-button:hover:not(:disabled) {
  background: #555;
}

.page-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #ccc;
  font-size: 14px;
}

/* Equipment Summary */
.equipment-summary {
  margin-top: 30px;
}

.summary-card {
  background: #2d2d2d;
  padding: 20px;
  border-radius: 4px;
  border: 1px solid #444;
}

.summary-card h4 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 15px;
}

.summary-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  color: #ccc;
}

.stat-row span:last-child {
  font-weight: bold;
  color: #fff;
}

h3 {
  color: #1E90FF;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.2rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .controls-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 12px;
  }
  
  .current-item-card {
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
  }
}
</style>