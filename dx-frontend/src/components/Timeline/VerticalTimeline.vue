<template>
  <div class="vertical-timeline">
    <!-- Fixed parallax background -->
    <div class="timeline-background"></div>
    <div class="timeline-background-overlay"></div>

    <!-- Header with filters -->
    <div class="timeline-header">
      <div class="header-title">
        <h1>Timeline View</h1>
        <p>{{ formattedDate }}</p>
      </div>

      <div class="header-controls">
        <!-- Search -->
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search timeline..."
            @input="handleSearchChange"
          />
        </div>

        <!-- Category toggles -->
        <div class="category-toggles">
          <button
            v-for="category in categories"
            :key="category.id"
            class="category-toggle"
            :class="{ active: category.visible }"
            @click="toggleCategory(category.id)"
          >
            <span class="toggle-indicator" :class="category.color"></span>
            <span class="toggle-label">{{ category.label }}</span>
          </button>
        </div>

        <!-- Add category button -->
        <button class="add-category-btn" @click="showAddCategoryDialog = true">
          <i class="fas fa-plus"></i>
          Add Category
        </button>
      </div>
    </div>

    <!-- Timeline container -->
    <div class="timeline-container" ref="timelineContainer" :style="{ height: `${timelineHeight}px`, paddingLeft: '350px' }">
      <!-- Time labels -->
      <div class="time-labels">
        <div
          v-for="timeSlot in timeSlots"
          :key="timeSlot"
          class="time-label"
          :style="{ top: `${getTimePosition(timeSlot)}px` }"
        >
          {{ formatTime(timeSlot) }}
        </div>
      </div>

      <!-- Vertical lane lines -->
      <div class="lane-lines">
        <div
          v-for="category in visibleCategories"
          :key="category.id"
          class="lane-line"
          :style="{ left: `${getLanePosition(category.id)}px` }"
        >
          <div class="line-gradient" :class="category.colorGradient"></div>
          <div class="line-glow" :class="category.colorGradient"></div>
        </div>
      </div>

      <!-- Horizontal time grid lines -->
      <div class="time-grid-lines">
        <div
          v-for="timeSlot in timeSlots"
          :key="timeSlot"
          class="time-grid-line"
          :style="{ top: `${getTimePosition(timeSlot)}px` }"
        ></div>
      </div>

      <!-- Timeline items -->
      <div class="timeline-items">
        <div
          v-for="item in filteredItems"
          :key="item.id"
          class="timeline-item-wrapper"
          :style="getItemPosition(item)"
        >
          <!-- Connection line to lane -->
          <div
            class="connection-line"
            :style="getConnectionStyle(item)"
          ></div>

          <!-- Connection dot -->
          <div
            class="connection-dot"
            :class="getCategoryColor(item.category)"
            :style="getConnectionDotStyle(item)"
          ></div>

          <!-- Mini card -->
          <TimelineMiniCard
            :item="item"
            :is-selected="selectedItemId === item.id"
            :loading="loadingItems.has(item.id)"
            @click="handleItemClick"
          />
        </div>
      </div>

      <!-- Infinite scroll loading indicator at bottom -->
      <div v-if="loading && filteredItems.length > 0" class="infinite-scroll-loading">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Loading more items...</p>
      </div>

      <!-- Loading overlay (initial load) -->
      <div v-if="loading && filteredItems.length === 0" class="timeline-loading">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Loading timeline...</p>
      </div>
    </div>

    <!-- Timeline Detail Card - Fixed position on right -->
    <TimelineDetailCard
      :visible="selectedItem !== null"
      :item="selectedItem"
      :categories="categories"
      :loading="loadingItems.has(selectedItemId)"
      @close="clearSelection"
    />

    <!-- Add category dialog -->
    <div v-if="showAddCategoryDialog" class="dialog-overlay" @click.self="showAddCategoryDialog = false">
      <div class="dialog-content">
        <h3>Add New Category</h3>
        <input
          v-model="newCategoryLabel"
          type="text"
          placeholder="Category name"
          class="dialog-input"
        />
        <div class="dialog-actions">
          <button class="dialog-btn cancel" @click="showAddCategoryDialog = false">Cancel</button>
          <button class="dialog-btn confirm" @click="addCategory">Add</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import TimelineMiniCard from './TimelineMiniCard.vue'
import TimelineDetailCard from './TimelineDetailCard.vue'
import type { TimelineItem, TimelineCategory } from '@/models/TimelineModels'

interface Props {
  items: TimelineItem[]
  categories: TimelineCategory[]
  loading?: boolean
  timeSlots?: number[]
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  timeSlots: () => Array.from({ length: 12 }, (_, i) => 9 + i)
})

const emit = defineEmits<{
  categoryToggle: [categoryId: string]
  categoryAdd: [label: string]
  itemClick: [item: TimelineItem]
  filterChange: [filter: { search: string; categories: string[] }]
  loadMore: []
}>()

const timelineContainer = ref<HTMLElement | null>(null)
const searchQuery = ref('')
const selectedItemId = ref<string | number | null>(null)
const loadingItems = ref(new Set<string | number>())
const showAddCategoryDialog = ref(false)
const newCategoryLabel = ref('')

const LANE_START_OFFSET = 350
const LANE_SPACING = 25
const TIME_START_OFFSET = 80
const TIME_SLOT_HEIGHT = 120
const CARD_WIDTH = 224
const CONNECTION_LENGTH = 80

const formattedDate = computed(() => {
  const date = new Date()
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
})

const visibleCategories = computed(() => {
  return props.categories.filter(cat => cat.visible)
})

const filteredItems = computed(() => {
  let items = props.items

  // Filter by visible categories
  const visibleCategoryIds = visibleCategories.value.map(c => c.id)
  items = items.filter(item => visibleCategoryIds.includes(item.category))

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    items = items.filter(item =>
      item.title.toLowerCase().includes(query) ||
      item.description?.toLowerCase().includes(query) ||
      item.tags.some(tag => tag.label.toLowerCase().includes(query))
    )
  }

  return items
})

const selectedItem = computed(() => {
  if (!selectedItemId.value) return null
  return props.items.find(item => item.id === selectedItemId.value) || null
})

const timelineHeight = computed(() => {
  if (filteredItems.value.length === 0) {
    return 1200 // Default minimum height
  }

  // Find the maximum time position among all items
  let maxTimePos = 0
  filteredItems.value.forEach(item => {
    let timeValue: number
    if (item.time.includes(':')) {
      timeValue = parseFloat(item.time.replace(':', '.'))
    } else {
      timeValue = parseInt(item.time)
    }
    const timePos = getTimePosition(timeValue)
    if (timePos > maxTimePos) {
      maxTimePos = timePos
    }
  })

  // Add buffer for card height (96px) and extra space (300px) for infinite scroll
  return Math.max(1200, maxTimePos + 96 + 300)
})

const getLanePosition = (categoryId: string): number => {
  const index = visibleCategories.value.findIndex(c => c.id === categoryId)
  return LANE_START_OFFSET + (index * LANE_SPACING)
}

const getTimePosition = (timeSlot: number): number => {
  const minTime = Math.min(...props.timeSlots)
  const maxTime = Math.max(...props.timeSlots)
  const timeRange = maxTime - minTime

  // Use exponential scale for large time ranges (years)
  // INVERTED: newest (maxTime) at top, oldest (minTime) at bottom
  if (timeRange > 100) {
    const normalizedTime = (maxTime - timeSlot) / timeRange // Inverted: maxTime - timeSlot
    const exponentialPosition = Math.pow(normalizedTime, 0.7) // 0.7 exponent for better distribution
    return TIME_START_OFFSET + (exponentialPosition * timeRange * TIME_SLOT_HEIGHT / 10)
  }

  // Linear scale for small ranges - also inverted
  return TIME_START_OFFSET + ((maxTime - timeSlot) * TIME_SLOT_HEIGHT)
}

const getItemPosition = (item: TimelineItem) => {
  const laneIndex = visibleCategories.value.findIndex(c => c.id === item.category)
  const lanePos = getLanePosition(item.category)

  // Parse time value - handle both year format (e.g., "10191") and time format (e.g., "09:00")
  let timeValue: number
  if (item.time.includes(':')) {
    // Time format: convert "09:00" to 9.0
    timeValue = parseFloat(item.time.replace(':', '.'))
  } else {
    // Year format: parse as integer
    timeValue = parseInt(item.time)
  }

  const timePos = getTimePosition(timeValue)

  const isLeftSide = laneIndex % 2 === 0
  const cardOffset = isLeftSide ? -(CARD_WIDTH + CONNECTION_LENGTH) : CONNECTION_LENGTH

  return {
    left: `${lanePos + cardOffset}px`,
    top: `${timePos}px`
  }
}

const getConnectionStyle = (item: TimelineItem) => {
  const laneIndex = visibleCategories.value.findIndex(c => c.id === item.category)
  const isLeftSide = laneIndex % 2 === 0
  const CARD_HEIGHT = 96 // 6rem = 96px
  const cardCenter = CARD_HEIGHT / 2 // 48px - center of the card

  return {
    left: isLeftSide ? `${CARD_WIDTH}px` : `-${CONNECTION_LENGTH}px`,
    top: `${cardCenter}px`,
    width: `${CONNECTION_LENGTH}px`
  }
}

const getConnectionDotStyle = (item: TimelineItem) => {
  const laneIndex = visibleCategories.value.findIndex(c => c.id === item.category)
  const isLeftSide = laneIndex % 2 === 0
  const CARD_HEIGHT = 96 // 6rem = 96px
  const cardCenter = CARD_HEIGHT / 2 // 48px - center of the card

  return {
    left: isLeftSide ? `${CARD_WIDTH + CONNECTION_LENGTH}px` : `-${CONNECTION_LENGTH}px`,
    top: `${cardCenter}px`
  }
}

const getCategoryColor = (categoryId: string): string => {
  const category = props.categories.find(c => c.id === categoryId)
  return category?.color || 'bg-gray-500'
}

const formatTime = (timeSlot: number): string => {
  const minTime = Math.min(...props.timeSlots)
  const maxTime = Math.max(...props.timeSlots)
  const timeRange = maxTime - minTime

  // For large ranges (years), display as year
  if (timeRange > 100) {
    return `${Math.floor(timeSlot)} AG`
  }

  // For small ranges (hours), display as time
  const hour = Math.floor(timeSlot)
  const isPM = hour >= 12
  const displayHour = hour > 12 ? hour - 12 : hour
  return `${displayHour}:00 ${isPM ? 'PM' : 'AM'}`
}

const toggleCategory = (categoryId: string) => {
  emit('categoryToggle', categoryId)
}

const addCategory = () => {
  if (newCategoryLabel.value.trim()) {
    emit('categoryAdd', newCategoryLabel.value.trim())
    newCategoryLabel.value = ''
    showAddCategoryDialog.value = false
  }
}

const handleItemClick = (item: TimelineItem) => {
  selectedItemId.value = selectedItemId.value === item.id ? null : item.id
  emit('itemClick', item)
}

const clearSelection = () => {
  selectedItemId.value = null
}

const handleSearchChange = () => {
  const visibleCategoryIds = visibleCategories.value.map(c => c.id)
  emit('filterChange', {
    search: searchQuery.value,
    categories: visibleCategoryIds
  })
}

watch(() => props.categories, () => {
  const visibleCategoryIds = visibleCategories.value.map(c => c.id)
  emit('filterChange', {
    search: searchQuery.value,
    categories: visibleCategoryIds
  })
}, { deep: true })

// Infinite scroll implementation
const handleScroll = () => {
  if (!timelineContainer.value || props.loading) return

  const container = timelineContainer.value
  const scrollTop = container.scrollTop
  const scrollHeight = container.scrollHeight
  const clientHeight = container.clientHeight

  // Trigger loadMore when within 200px of bottom
  const threshold = 200
  if (scrollTop + clientHeight >= scrollHeight - threshold) {
    emit('loadMore')
  }
}

onMounted(() => {
  if (timelineContainer.value) {
    timelineContainer.value.addEventListener('scroll', handleScroll)
  }
})

onUnmounted(() => {
  if (timelineContainer.value) {
    timelineContainer.value.removeEventListener('scroll', handleScroll)
  }
})
</script>

<style scoped>
.vertical-timeline {
  min-height: 100vh;
  background: #000;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', serif;
  padding: 3rem 2rem;
  position: relative;
  overflow: hidden;
}

/* Fixed parallax background */
.timeline-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/images/backgrounds/TimeLine.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  z-index: 0;
}

/* Semi-transparent overlay for content readability */
.timeline-background-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  z-index: 1;
}

.timeline-header {
  position: relative;
  z-index: 2;
  border-bottom: 1px solid rgba(250, 218, 149, 0.3);
  padding-bottom: 2rem;
  margin-bottom: 3rem;
}

.header-title h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #fada95;
  margin: 0 0 0.5rem 0;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.header-title p {
  color: rgba(250, 218, 149, 0.6);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-weight: bold;
  margin: 0;
}

.header-controls {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(250, 218, 149, 0.1);
  border: 1px solid rgba(250, 218, 149, 0.3);
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  flex: 1;
  min-width: 200px;
}

.search-box i {
  color: rgba(250, 218, 149, 0.6);
}

.search-box input {
  background: transparent;
  border: none;
  outline: none;
  color: #fada95;
  flex: 1;
  font-size: 0.875rem;
}

.search-box input::placeholder {
  color: rgba(250, 218, 149, 0.4);
}

.category-toggles {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.category-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid rgba(250, 218, 149, 0.3);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: bold;
}

.category-toggle.active {
  background: rgba(250, 218, 149, 0.1);
  box-shadow: 0 0 12px rgba(250, 218, 149, 0.4);
}

.category-toggle:hover {
  transform: scale(1.05);
}

.toggle-indicator {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.toggle-label {
  color: rgba(250, 218, 149, 0.6);
  transition: all 0.3s ease;
}

.category-toggle.active .toggle-label {
  color: #fada95;
}

.category-toggle:not(.active) .toggle-indicator {
  opacity: 0.4;
}

/* Dynamic colored borders for active state */
.category-toggle.active:has(.bg-blue-500) {
  border-color: rgb(59, 130, 246);
}

.category-toggle.active:has(.bg-cyan-500) {
  border-color: rgb(6, 182, 212);
}

.category-toggle.active:has(.bg-amber-500) {
  border-color: rgb(245, 158, 11);
}

.category-toggle.active:has(.bg-emerald-500) {
  border-color: rgb(16, 185, 129);
}

.category-toggle.active:has(.bg-gray-500) {
  border-color: rgb(107, 114, 128);
}

.add-category-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, rgba(250, 218, 149, 0.2), rgba(250, 218, 149, 0.1));
  border: 1px solid #fada95;
  border-radius: 0.5rem;
  color: #fada95;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: bold;
}

.add-category-btn:hover {
  background: linear-gradient(135deg, rgba(250, 218, 149, 0.3), rgba(250, 218, 149, 0.2));
  transform: scale(1.05);
}

.timeline-container {
  position: relative;
  z-index: 2;
  overflow-x: auto;
  overflow-y: auto;
}

.time-labels {
  position: absolute;
  left: 0;
  top: 80px;
  width: 100px;
}

.time-label {
  position: absolute;
  right: 20px;
  color: rgba(250, 218, 149, 0.6);
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  text-align: right;
}

.lane-lines {
  position: absolute;
  left: 100px;
  top: 80px;
  right: 0;
  bottom: 0;
}

.lane-line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 1px;
}

.line-gradient {
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, var(--tw-gradient-stops));
  opacity: 0.5;
}

.line-glow {
  position: absolute;
  left: 0;
  top: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(to bottom, var(--tw-gradient-stops));
  filter: blur(4px);
  opacity: 0.3;
}

.time-grid-lines {
  position: absolute;
  left: 100px;
  top: 80px;
  right: 0;
}

.time-grid-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 1px;
  border-top: 1px solid rgba(250, 218, 149, 0.1);
}

.timeline-items {
  position: absolute;
  left: 100px;
  top: 80px;
  right: 0;
}

.timeline-item-wrapper {
  position: absolute;
}

.connection-line {
  position: absolute;
  height: 1px;
  background: linear-gradient(to right, rgba(250, 218, 149, 0.2), rgba(250, 218, 149, 0.4), rgba(250, 218, 149, 0.2));
  transform: translateY(-50%);
}

.connection-dot {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid #000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  transform: translate(-50%, -50%);
}

.timeline-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  z-index: 100;
}

.timeline-loading i {
  font-size: 3rem;
  color: #fada95;
}

.timeline-loading p {
  color: rgba(250, 218, 149, 0.8);
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
}

.infinite-scroll-loading {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: rgba(0, 0, 0, 0.9);
  border: 1px solid rgba(250, 218, 149, 0.3);
  border-radius: 0.5rem;
  backdrop-filter: blur(10px);
  z-index: 50;
}

.infinite-scroll-loading i {
  font-size: 1.5rem;
  color: #fada95;
}

.infinite-scroll-loading p {
  color: rgba(250, 218, 149, 0.8);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin: 0;
}

.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.dialog-content {
  background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
  border: 1px solid #fada95;
  border-radius: 0.75rem;
  padding: 2rem;
  min-width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
}

.dialog-content h3 {
  color: #fada95;
  font-size: 1.5rem;
  margin: 0 0 1.5rem 0;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.dialog-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(250, 218, 149, 0.1);
  border: 1px solid rgba(250, 218, 149, 0.3);
  border-radius: 0.5rem;
  color: #fada95;
  font-size: 1rem;
  margin-bottom: 1.5rem;
  outline: none;
  transition: all 0.3s ease;
}

.dialog-input:focus {
  border-color: #fada95;
  background: rgba(250, 218, 149, 0.15);
}

.dialog-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.dialog-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.dialog-btn.cancel {
  background: transparent;
  border: 1px solid rgba(250, 218, 149, 0.3);
  color: rgba(250, 218, 149, 0.6);
}

.dialog-btn.cancel:hover {
  border-color: rgba(250, 218, 149, 0.6);
  color: #fada95;
}

.dialog-btn.confirm {
  background: linear-gradient(135deg, rgba(250, 218, 149, 0.3), rgba(250, 218, 149, 0.2));
  border: 1px solid #fada95;
  color: #fada95;
}

.dialog-btn.confirm:hover {
  background: linear-gradient(135deg, rgba(250, 218, 149, 0.4), rgba(250, 218, 149, 0.3));
  transform: scale(1.05);
}

/* Tailwind color classes */
.bg-blue-500 { background-color: rgb(59, 130, 246); }
.bg-cyan-500 { background-color: rgb(6, 182, 212); }
.bg-amber-500 { background-color: rgb(245, 158, 11); }
.bg-emerald-500 { background-color: rgb(16, 185, 129); }
.bg-gray-500 { background-color: rgb(107, 114, 128); }

.from-blue-600\/50 { --tw-gradient-from: rgba(37, 99, 235, 0.5); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgba(37, 99, 235, 0)); }
.to-blue-700\/50 { --tw-gradient-to: rgba(29, 78, 216, 0.5); }
.from-cyan-600\/50 { --tw-gradient-from: rgba(8, 145, 178, 0.5); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgba(8, 145, 178, 0)); }
.to-cyan-700\/50 { --tw-gradient-to: rgba(14, 116, 144, 0.5); }
.from-amber-600\/50 { --tw-gradient-from: rgba(217, 119, 6, 0.5); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgba(217, 119, 6, 0)); }
.to-amber-700\/50 { --tw-gradient-to: rgba(180, 83, 9, 0.5); }
.from-emerald-600\/50 { --tw-gradient-from: rgba(5, 150, 105, 0.5); --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgba(5, 150, 105, 0)); }
.to-emerald-700\/50 { --tw-gradient-to: rgba(4, 120, 87, 0.5); }
</style>
