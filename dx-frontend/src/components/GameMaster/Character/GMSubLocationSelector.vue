<script setup lang="ts">

import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import {SubLocation} from "@/api/dx-backend";
import GMSubLocationSelectorCard from "@/components/GameMaster/Character/GMSubLocationSelectorCard.vue";
import {ref, computed, watch} from "vue";

interface Filter {
  name?: string;
  id?: string;
  location?: string;
  isActive?: boolean;
}

interface Props {
  subLocations: SubLocation[];
  selectedSubLocationId?: string;
}

const props = withDefaults(defineProps<Props>(), {
  selectedSubLocationId: undefined,
});
const emit = defineEmits<{
  select: [subLocation: SubLocation];
  filterByLocation: [location: string];
  close: [];
}>();

// Filter state
const searchQuery = ref('');
const selectedLocation = ref('');
const selectedActiveFilter = ref('');

// Get unique locations from subLocations
const locations = computed(() => {
  const locs = new Set<string>();
  props.subLocations.forEach(subLoc => {
    if (subLoc.location) {
      locs.add(subLoc.location);
    }
  });
  return Array.from(locs).sort();
});

// Filtered subLocations based on search and filters
const filteredSubLocations = computed(() => {
  let filtered = props.subLocations;

  // Apply search query (name, id, description, or location)
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    filtered = filtered.filter(subLoc =>
      subLoc.name.toLowerCase().includes(query) ||
      subLoc.id.toLowerCase().includes(query) ||
      subLoc.description?.toLowerCase().includes(query) ||
      subLoc.location?.toLowerCase().includes(query)
    );
  }

  // Apply location filter
  if (selectedLocation.value) {
    filtered = filtered.filter(subLoc => subLoc.location === selectedLocation.value);
  }

  // Apply active filter
  if (selectedActiveFilter.value !== '') {
    const isActive = selectedActiveFilter.value === 'true';
    filtered = filtered.filter(subLoc => subLoc.is_active === isActive);
  }

  return filtered;
});

// Fast action handlers
const copySubLocationId = (subLocationId: string) => {
  navigator.clipboard.writeText(subLocationId);
};

const filterBySubLocationLocation = (subLocation: SubLocation) => {
  if (subLocation.location) {
    selectedLocation.value = subLocation.location;
    emit('filterByLocation', subLocation.location);
  }
};

// Active filters computed property
const activeFilters = computed(() => {
  const filters = [];

  if (searchQuery.value.trim()) {
    filters.push({
      type: 'search',
      label: `Search: "${searchQuery.value}"`,
      value: searchQuery.value
    });
  }

  if (selectedLocation.value) {
    filters.push({
      type: 'location',
      label: `Location: ${selectedLocation.value}`,
      value: selectedLocation.value
    });
  }

  if (selectedActiveFilter.value !== '') {
    const label = selectedActiveFilter.value === 'true' ? 'Active Only' : 'Inactive Only';
    filters.push({
      type: 'active',
      label: label,
      value: selectedActiveFilter.value
    });
  }

  return filters;
});

// Clear all filters function
const clearAllFilters = () => {
  searchQuery.value = '';
  selectedLocation.value = '';
  selectedActiveFilter.value = '';
};

// Individual filter removal functions
const removeFilter = (filterType: string) => {
  switch (filterType) {
    case 'search':
      searchQuery.value = '';
      break;
    case 'location':
      selectedLocation.value = '';
      break;
    case 'active':
      selectedActiveFilter.value = '';
      break;
  }
};

// Handle SubLocation selection
const handleSubLocationSelect = (subLocation: SubLocation) => {
  emit('select', subLocation);
};
</script>

<template>
  <RPGContainer class="sublocation-selector-container">
    <div class="header">
      <div class="header-top">
        <h2 class="title">SubLocation Selector</h2>
        <button @click="emit('close')" class="close-btn" title="Close SubLocation Selector">
          ×
        </button>
      </div>

      <!-- Filter Controls -->
      <div class="filters">
        <!-- Search Input -->
        <div class="filter-group">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by name, ID, description, location..."
            class="search-input"
          />
        </div>

        <!-- Location Filter -->
        <div class="filter-group">
          <select v-model="selectedLocation" class="filter-select">
            <option value="">All Locations</option>
            <option v-for="location in locations" :key="location" :value="location">
              {{ location }}
            </option>
          </select>
        </div>

        <!-- Active Filter -->
        <div class="filter-group">
          <select v-model="selectedActiveFilter" class="filter-select">
            <option value="">All SubLocations</option>
            <option value="true">Active Only</option>
            <option value="false">Inactive Only</option>
          </select>
        </div>

        <!-- Clear All Filters Button -->
        <div class="filter-group clear-button-group">
          <button
            @click="clearAllFilters"
            class="clear-all-btn"
            :disabled="activeFilters.length === 0"
            title="Clear all active filters"
          >
            Clear All
          </button>
        </div>
      </div>

      <!-- Active Filter Tags -->
      <div v-if="activeFilters.length > 0" class="filter-tags">
        <div class="filter-tags-label">Active Filters:</div>
        <div class="filter-tags-list">
          <div
            v-for="filter in activeFilters"
            :key="filter.type"
            class="filter-tag"
          >
            <span class="filter-tag-label">{{ filter.label }}</span>
            <button
              @click="removeFilter(filter.type)"
              class="filter-tag-remove"
              title="Remove this filter"
            >
              ×
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="sublocations-grid-wrapper">
      <div class="sublocations-grid">
        <GMSubLocationSelectorCard
          v-for="subLocation in filteredSubLocations"
          :key="subLocation.id"
          :subLocation="subLocation"
          :selected="subLocation.id === props.selectedSubLocationId"
          class="sublocation-card"
          @click="handleSubLocationSelect(subLocation)"
          @copy-id="copySubLocationId"
          @filter-by-location="filterBySubLocationLocation"
        />
      </div>

      <!-- No Results Message -->
      <div v-if="filteredSubLocations.length === 0" class="no-results">
        <p>No SubLocations found matching your criteria.</p>
        <button @click="clearAllFilters" class="clear-filters-btn">Clear Filters</button>
      </div>
    </div>
  </RPGContainer>
</template>

<style scoped>
.sublocation-selector-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 400px;
  max-height: 600px;
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
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #fada95;
  cursor: pointer;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background: rgba(250, 218, 149, 0.1);
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.7rem;
}

.filter-group {
  flex: 1;
  min-width: 120px;
}

.clear-button-group {
  flex: 0 0 auto;
  min-width: auto;
}

.search-input,
.filter-select {
  width: 100%;
  padding: 0.4rem 0.6rem;
  border: 1px solid #444;
  border-radius: 0.25rem;
  background: rgba(0, 0, 0, 0.3);
  color: #fada95;
  font-size: 0.8rem;
  transition: border-color 0.3s ease;
}

.search-input:focus,
.filter-select:focus {
  outline: none;
  border-color: #7fff16;
}

.clear-all-btn {
  padding: 0.4rem 0.8rem;
  border: 1px solid #666;
  border-radius: 0.25rem;
  background: rgba(0, 0, 0, 0.3);
  color: #fada95;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-all-btn:hover:not(:disabled) {
  background: rgba(250, 218, 149, 0.1);
  border-color: #fada95;
}

.clear-all-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.7rem;
}

.filter-tags-label {
  font-size: 0.8rem;
  color: #fada95;
  font-weight: 500;
}

.filter-tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.filter-tag {
  display: flex;
  align-items: center;
  background: rgba(127, 255, 22, 0.2);
  border: 1px solid #7fff16;
  border-radius: 1rem;
  padding: 0.2rem 0.5rem;
  font-size: 0.7rem;
  color: #7fff16;
}

.filter-tag-label {
  margin-right: 0.3rem;
}

.filter-tag-remove {
  background: none;
  border: none;
  color: #7fff16;
  cursor: pointer;
  font-size: 0.8rem;
  padding: 0;
  width: 1rem;
  height: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.filter-tag-remove:hover {
  background: rgba(127, 255, 22, 0.3);
}

.sublocations-grid-wrapper {
  flex: 1;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.sublocations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
  padding-bottom: 1rem;
  align-items: start;
}

.sublocation-card {
  transition: transform 0.2s ease;
}

.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
  color: #fada95;
}

.no-results p {
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
}

.clear-filters-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #7fff16;
  border-radius: 0.25rem;
  background: rgba(127, 255, 22, 0.1);
  color: #7fff16;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-filters-btn:hover {
  background: rgba(127, 255, 22, 0.2);
}

/* Scrollbar styling */
.sublocations-grid-wrapper::-webkit-scrollbar {
  width: 0.5rem;
}

.sublocations-grid-wrapper::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 0.25rem;
}

.sublocations-grid-wrapper::-webkit-scrollbar-thumb {
  background: rgba(250, 218, 149, 0.3);
  border-radius: 0.25rem;
}

.sublocations-grid-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(250, 218, 149, 0.5);
}
</style>