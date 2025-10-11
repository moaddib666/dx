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
const categories = ref<TimelineCategory[]>([
  {
    id: 'all',
    label: 'All Events',
    color: 'bg-blue-500',
    colorGradient: 'from-blue-600/50 to-blue-700/50',
    visible: true
  }
])
const loading = ref(false)
const currentFilter = ref<TimelineFilter>({
  categories: [],
  tags: [],
  searchQuery: ''
})
const currentPage = ref(1)
const pageSize = 100
const hasMore = ref(true)
const totalCount = ref(0)

const timeSlots = computed(() => {
  // Generate time slots ONLY from actual item times (skip empty timeframes)
  if (timelineItems.value.length === 0) {
    // Default fallback if no items loaded yet
    return [0]
  }

  // Extract all unique time values from items
  const uniqueTimes = new Set<number>()

  timelineItems.value.forEach(item => {
    let timeValue: number
    if (typeof item.time === 'number') {
      timeValue = item.time
    } else if (typeof item.time === 'string' && item.time.includes(':')) {
      timeValue = parseFloat(item.time.replace(':', '.'))
    } else {
      timeValue = parseInt(item.time as string)
    }
    uniqueTimes.add(timeValue)
  })

  // Convert to sorted array (oldest to newest for proper ordering)
  const slots = Array.from(uniqueTimes).sort((a, b) => a - b)

  return slots
})

onMounted(async () => {
  await loadInitialData()
})

const loadInitialData = async () => {
  loading.value = true
  try {
    // Fetch all timeline items (page 1)
    const response = await TimelineService.fetchItemsByCategory('all', currentPage.value, pageSize)

    timelineItems.value = response.items
    totalCount.value = response.count
    hasMore.value = response.next !== null

    console.log(`Loaded ${response.items.length} items (total: ${response.count})`)
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
    // Reload all data when toggling category visibility
    loading.value = true
    try {
      const response = await TimelineService.fetchItemsByCategory(categoryId, 1, pageSize)
      // Add items that don't already exist
      const existingIds = new Set(timelineItems.value.map(item => item.id))
      const newItems = response.items.filter(item => !existingIds.has(item.id))
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
      // Reset pagination when filtering
      hasMore.value = false
    } catch (error) {
      console.error('Error fetching filtered items:', error)
    } finally {
      loading.value = false
    }
  } else {
    // If search is cleared, reload initial data
    currentPage.value = 1
    await loadInitialData()
  }
}

const handleLoadMore = async () => {
  if (loading.value || !hasMore.value) return

  loading.value = true
  try {
    // Increment page for next batch
    currentPage.value += 1

    // Fetch more items
    const response = await TimelineService.fetchItemsByCategory('all', currentPage.value, pageSize)

    // If no new items returned, we've reached the end
    if (response.items.length === 0) {
      hasMore.value = false
    } else {
      // Add new items that don't already exist
      const existingIds = new Set(timelineItems.value.map(item => item.id))
      const uniqueNewItems = response.items.filter(item => !existingIds.has(item.id))
      timelineItems.value.push(...uniqueNewItems)

      // Update hasMore based on next field
      hasMore.value = response.next !== null
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
