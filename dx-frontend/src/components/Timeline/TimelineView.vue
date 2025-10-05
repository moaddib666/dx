<template>
  <div class="timeline-view">
    <VerticalTimeline
      :items="timelineItems"
      :categories="categories"
      :loading="loading"
      :time-slots="timeSlots"
      @category-toggle="handleCategoryToggle"
      @category-add="handleCategoryAdd"
      @item-click="handleItemClick"
      @filter-change="handleFilterChange"
      @load-more="handleLoadMore"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import VerticalTimeline from './VerticalTimeline.vue'
import TimelineService from '@/services/TimelineService'
import type { TimelineItem, TimelineCategory, TimelineFilter } from '@/models/TimelineModels'

const timelineItems = ref<TimelineItem[]>([])
const categories = ref<TimelineCategory[]>([])
const loading = ref(false)
const currentFilter = ref<TimelineFilter>({
  categories: [],
  tags: [],
  searchQuery: ''
})
const offset = ref(0)
const limit = 10
const hasMore = ref(true)

const timeSlots = computed(() => {
  // Generate year-based time slots for timeline spanning years
  // Starting from year 10000 AG, with 20-year intervals, for 200 years
  const startYear = 10000
  const interval = 20
  const count = 11
  return Array.from({ length: count }, (_, i) => startYear + (i * interval))
})

onMounted(async () => {
  await loadInitialData()
})

const loadInitialData = async () => {
  loading.value = true
  try {
    // Load categories first
    categories.value = await TimelineService.fetchCategories()

    // Load items for all visible categories
    const visibleCategories = categories.value.filter(c => c.visible)
    const itemPromises = visibleCategories.map(cat =>
      TimelineService.fetchItemsByCategory(cat.id)
    )

    const itemsArrays = await Promise.all(itemPromises)
    timelineItems.value = itemsArrays.flat()
  } catch (error) {
    console.error('Error loading timeline data:', error)
  } finally {
    loading.value = false
  }
}

const handleCategoryToggle = async (categoryId: string) => {
  const category = categories.value.find(c => c.id === categoryId)
  if (!category) return

  category.visible = !category.visible

  if (category.visible) {
    // Load items for this category if not already loaded
    loading.value = true
    try {
      const items = await TimelineService.fetchItemsByCategory(categoryId)
      // Add items that don't already exist
      const existingIds = new Set(timelineItems.value.map(item => item.id))
      const newItems = items.filter(item => !existingIds.has(item.id))
      timelineItems.value.push(...newItems)
    } catch (error) {
      console.error(`Error loading items for category ${categoryId}:`, error)
    } finally {
      loading.value = false
    }
  }
}

const handleCategoryAdd = (label: string) => {
  const newCategory: TimelineCategory = {
    id: `category_${Date.now()}`,
    label,
    color: 'bg-gray-500',
    colorGradient: 'from-gray-600/50 to-gray-700/50',
    visible: true
  }
  categories.value.push(newCategory)
}

const handleItemClick = (item: TimelineItem) => {
  console.log('Item clicked:', item)
  // Handle item click - could open detail modal, navigate, etc.
}

const handleFilterChange = async (filter: { search: string; categories: string[] }) => {
  currentFilter.value.searchQuery = filter.search
  currentFilter.value.categories = filter.categories

  // If search query is provided, fetch filtered results from server
  if (filter.search.trim()) {
    loading.value = true
    try {
      const filteredItems = await TimelineService.fetchFilteredItems(currentFilter.value)
      timelineItems.value = filteredItems
    } catch (error) {
      console.error('Error fetching filtered items:', error)
    } finally {
      loading.value = false
    }
  }
}

const handleLoadMore = async () => {
  if (loading.value || !hasMore.value) return

  loading.value = true
  try {
    // Increment offset for next batch
    offset.value += limit

    // Fetch more items for all visible categories
    const visibleCategories = categories.value.filter(c => c.visible)
    const itemPromises = visibleCategories.map(cat =>
      TimelineService.fetchItemsByCategory(cat.id, offset.value, limit)
    )

    const itemsArrays = await Promise.all(itemPromises)
    const newItems = itemsArrays.flat()

    // If no new items returned, we've reached the end
    if (newItems.length === 0) {
      hasMore.value = false
    } else {
      // Add new items that don't already exist
      const existingIds = new Set(timelineItems.value.map(item => item.id))
      const uniqueNewItems = newItems.filter(item => !existingIds.has(item.id))
      timelineItems.value.push(...uniqueNewItems)
    }
  } catch (error) {
    console.error('Error loading more items:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.timeline-view {
  width: 100%;
  min-height: 100vh;
}
</style>
