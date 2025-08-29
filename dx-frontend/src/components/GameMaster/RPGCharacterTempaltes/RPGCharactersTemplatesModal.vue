<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue";
import RpgCharactersTemplatePresenter from "./RPGCharactersTemplatePresenter.vue";
import { characterTemplatesService } from '@/services/CharacterTemplatesService.ts';

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

interface Filter {
  name?: string;
  id?: string;
  behavior?: string;
  category?: string;
}

interface Props {
  selectedTemplateId?: string;
}

const props = withDefaults(defineProps<Props>(), {
  selectedTemplateId: undefined,
});

const emit = defineEmits<{
  templateSelected: [template: CharacterTemplate];
  close: [];
}>();

// State
const templates = ref<CharacterTemplate[]>([]);
const isLoading = ref(true);
const error = ref<string | null>(null);

// Filter state
const searchQuery = ref('');
const selectedBehavior = ref('');
const selectedCategory = ref('');
const sortBy = ref('name');
const sortOrder = ref<'asc' | 'desc'>('asc');

// Computed properties for filter options
const behaviors = ref<string[]>([]);
const categories = ref<string[]>([]);

// Filtered and sorted templates
const filteredTemplates = computed(() => {
  let result = templates.value;

  // Apply search query (name, description, behavior, category)
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    result = result.filter(template =>
      template.name.toLowerCase().includes(query) ||
      (template.description && template.description.toLowerCase().includes(query)) ||
      (template.behavior && template.behavior.toLowerCase().includes(query)) ||
      (template.category && template.category.toLowerCase().includes(query)) ||
      (template.race && template.race.toLowerCase().includes(query)) ||
      (template.class && template.class.toLowerCase().includes(query))
    );
  }

  // Apply behavior filter
  if (selectedBehavior.value) {
    result = result.filter(template => template.behavior === selectedBehavior.value);
  }

  // Apply category filter
  if (selectedCategory.value) {
    result = result.filter(template => template.category === selectedCategory.value);
  }

  // Apply sorting
  result = [...result].sort((a, b) => {
    let aValue: any, bValue: any;

    switch (sortBy.value) {
      case 'name':
        aValue = a.name.toLowerCase();
        bValue = b.name.toLowerCase();
        break;
      case 'behavior':
        aValue = a.behavior?.toLowerCase() || '';
        bValue = b.behavior?.toLowerCase() || '';
        break;
      case 'category':
        aValue = a.category?.toLowerCase() || '';
        bValue = b.category?.toLowerCase() || '';
        break;
      case 'level':
        aValue = a.level || 0;
        bValue = b.level || 0;
        break;
      default:
        aValue = a.name.toLowerCase();
        bValue = b.name.toLowerCase();
    }

    if (aValue < bValue) return sortOrder.value === 'asc' ? -1 : 1;
    if (aValue > bValue) return sortOrder.value === 'asc' ? 1 : -1;
    return 0;
  });

  return result;
});

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

  if (selectedBehavior.value) {
    filters.push({
      type: 'behavior',
      label: `Behavior: ${formatBehavior(selectedBehavior.value)}`,
      value: selectedBehavior.value
    });
  }

  if (selectedCategory.value) {
    filters.push({
      type: 'category',
      label: `Category: ${selectedCategory.value}`,
      value: selectedCategory.value
    });
  }

  return filters;
});

// Event handlers
const onLoadingStarted = () => {
  isLoading.value = true;
  error.value = null;
};

const onTemplatesLoaded = (loadedTemplates: CharacterTemplate[]) => {
  templates.value = loadedTemplates;
  isLoading.value = false;

  // Extract unique behaviors for the filter
  const behaviorSet = new Set<string>();
  const categorySet = new Set<string>();

  loadedTemplates.forEach(template => {
    if (template.behavior) {
      behaviorSet.add(template.behavior);
    }
    if (template.category) {
      categorySet.add(template.category);
    }
  });

  behaviors.value = Array.from(behaviorSet);
  categories.value = Array.from(categorySet);
};

const onLoadingFailed = (err) => {
  console.error('Failed to load templates:', err);
  error.value = err.message || 'Failed to load templates';
  isLoading.value = false;
};

// Filter management functions
const clearAllFilters = () => {
  searchQuery.value = '';
  selectedBehavior.value = '';
  selectedCategory.value = '';
};

const removeFilter = (filterType: string) => {
  switch (filterType) {
    case 'search':
      searchQuery.value = '';
      break;
    case 'behavior':
      selectedBehavior.value = '';
      break;
    case 'category':
      selectedCategory.value = '';
      break;
  }
};

// Template selection handlers
const selectTemplate = (template: CharacterTemplate) => {
  emit('templateSelected', template);
};

const copyTemplateId = (templateId: string) => {
  navigator.clipboard.writeText(templateId);
};

const filterByCategory = (template: CharacterTemplate) => {
  if (template.category) {
    selectedCategory.value = template.category;
  }
};

const filterByBehavior = (template: CharacterTemplate) => {
  if (template.behavior) {
    selectedBehavior.value = template.behavior;
  }
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

// Helper methods
const getTemplateInitials = (name) => {
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
  <RPGContainer class="templates-modal-container">
    <div class="header">
      <div class="header-top">
        <h2 class="title">Character Templates</h2>
        <button @click="emit('close')" class="close-btn" title="Close Templates Modal">
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
            placeholder="Search templates..."
            class="search-input"
          />
        </div>

        <!-- Category Filter -->
        <div class="filter-group">
          <select v-model="selectedCategory" class="filter-select">
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>

        <!-- Behavior Filter -->
        <div class="filter-group">
          <select v-model="selectedBehavior" class="filter-select">
            <option value="">All Behaviors</option>
            <option v-for="behavior in behaviors" :key="behavior" :value="behavior">
              {{ formatBehavior(behavior) }}
            </option>
          </select>
        </div>

        <!-- Sort Options -->
        <div class="filter-group">
          <select v-model="sortBy" class="filter-select">
            <option value="name">Sort by Name</option>
            <option value="behavior">Sort by Behavior</option>
            <option value="category">Sort by Category</option>
            <option value="level">Sort by Level</option>
          </select>
        </div>

        <!-- Sort Order -->
        <div class="filter-group sort-order-group">
          <button
            @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'"
            class="sort-order-btn"
            :title="`Sort ${sortOrder === 'asc' ? 'Descending' : 'Ascending'}`"
          >
            {{ sortOrder === 'asc' ? '↑' : '↓' }}
          </button>
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

        <!-- Refresh Button -->
        <div class="filter-group refresh-button-group">
          <button
            @click="refreshTemplates"
            class="refresh-btn"
            title="Refresh Templates"
          >
            ↻
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

    <div class="templates-content">
      <div v-if="isLoading" class="loading-indicator">
        Loading templates...
      </div>

      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-else-if="filteredTemplates.length === 0" class="no-templates">
        No templates found matching your criteria.
      </div>

      <div v-else class="templates-grid">
        <RpgCharactersTemplatePresenter
          v-for="template in filteredTemplates"
          :key="template.id || template.name"
          :template="template"
          :selected="template.id === props.selectedTemplateId"
          class="template-card"
          @click="selectTemplate(template)"
          @copy-id="copyTemplateId"
          @filter-by-category="filterByCategory"
          @filter-by-behavior="filterByBehavior"
        />
      </div>
    </div>
  </RPGContainer>
</template>

<style scoped>
.templates-modal-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 500px;
  max-height: 700px;
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

.close-btn {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  line-height: 1;
}

.close-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-50%) scale(1.1);
  color: #7fff16;
}

.close-btn:active {
  transform: translateY(-50%) scale(0.95);
}

.filters {
  display: flex;
  gap: 0.525rem;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.filter-group {
  flex: 1;
  min-width: 140px;
}

.sort-order-group,
.clear-button-group,
.refresh-button-group {
  flex: 0 0 auto;
  min-width: auto;
}

.search-input,
.filter-select {
  width: 100%;
  padding: 0.35rem 0.525rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.263rem;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 400;
  transition: border-color 0.3s, background-color 0.3s;
}

.search-input::placeholder {
  color: rgba(250, 218, 149, 0.5);
}

.search-input:focus,
.filter-select:focus {
  outline: none;
  border-color: #7fff16;
  background: rgba(0, 0, 0, 0.6);
}

.filter-select option {
  background: rgba(0, 0, 0, 0.9);
  color: #fada95;
}

.sort-order-btn,
.clear-all-btn,
.refresh-btn {
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

.sort-order-btn {
  width: 2.5rem;
  height: 2.5rem;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.refresh-btn {
  width: 2.5rem;
  height: 2.5rem;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.sort-order-btn:hover:not(:disabled),
.clear-all-btn:hover:not(:disabled),
.refresh-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-1px);
}

.sort-order-btn:active:not(:disabled),
.clear-all-btn:active:not(:disabled),
.refresh-btn:active {
  transform: translateY(0);
}

.clear-all-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border-color: rgba(127, 255, 22, 0.1);
}

/* Filter Tags */
.filter-tags {
  margin-top: 0.525rem;
  padding-top: 0.525rem;
  border-top: 1px solid rgba(127, 255, 22, 0.2);
}

.filter-tags-label {
  font-size: 0.75rem;
  font-weight: 500;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: rgba(250, 218, 149, 0.8);
  margin-bottom: 0.35rem;
  text-align: center;
}

.filter-tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  justify-content: center;
}

.filter-tag {
  display: flex;
  align-items: center;
  background: rgba(127, 255, 22, 0.1);
  border: 1px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.875rem;
  padding: 0.175rem 0.35rem;
  font-size: 0.75rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  backdrop-filter: blur(2px);
  transition: all 0.2s ease;
}

.filter-tag:hover {
  background: rgba(127, 255, 22, 0.15);
  border-color: rgba(127, 255, 22, 0.5);
}

.filter-tag-label {
  margin-right: 0.25rem;
  font-weight: 400;
}

.filter-tag-remove {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1rem;
  height: 1rem;
  border: none;
  border-radius: 50%;
  background: rgba(255, 0, 0, 0.2);
  color: #fada95;
  font-size: 0.75rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  line-height: 1;
}

.filter-tag-remove:hover {
  background: rgba(255, 0, 0, 0.4);
  transform: scale(1.1);
}

.filter-tag-remove:active {
  transform: scale(0.9);
}

.templates-content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.loading-indicator,
.no-templates,
.error-message {
  padding: 2rem;
  text-align: center;
  color: rgba(250, 218, 149, 0.7);
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
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
  overflow-y: auto;
  padding: 0.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  align-content: start;
}

.template-card {
  width: 100%;
}

/* Responsive filters */
@media (max-width: 768px) {
  .filters {
    flex-direction: column;
    gap: 0.5rem;
  }

  .filter-group {
    min-width: 100%;
  }

  .sort-order-group,
  .clear-button-group,
  .refresh-button-group {
    min-width: 100%;
  }

  .templates-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .templates-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 0.5rem;
  }
}
</style>