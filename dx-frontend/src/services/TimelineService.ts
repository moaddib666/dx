import type { TimelineItem, TimelineCategory, TimelineServiceResponse, TimelineFilter } from '@/models/TimelineModels'
import { KnowledgeBaseTimelineEventsGameApi } from '@/api/backendService'
import type { TimeLineEvent, PaginatedTimeLineEventList } from '@/api/dx-backend/api'
import { CategoriesEnum } from '@/api/dx-backend/api'

interface CacheEntry {
  data: TimelineItem[]
  timestamp: number
  count: number
  next: string | null
}

class TimelineService {
  private cache: Map<string, CacheEntry> = new Map()
  private readonly CACHE_DURATION = 5 * 60 * 1000 // 5 minutes in milliseconds

  /**
   * Convert backend TimeLineEvent to frontend TimelineItem
   */
  private mapTimeLineEventToTimelineItem(event: TimeLineEvent): TimelineItem {
    const { document, date_time } = event

    // Calculate time value from date_time (solar_year:sol format)
    const timeValue = date_time.solar_year !== undefined && date_time.sol !== undefined
      ? `${date_time.solar_year}:${date_time.sol}`
      : '0:0'

    // Extract category from document categories (use first category or 'other')
    const category = document.categories && document.categories.length > 0
      ? document.categories[0].toLowerCase()
      : 'other'

    // Parse tags from document content or metadata
    const tags: { label: string; color?: string }[] = []

    return {
      id: event.id,
      category,
      time: timeValue,
      beforeAnomalyGlow: date_time.active_glow || false,
      title: document.title,
      description: document.content,
      tags,
      image: document.image || undefined,
      metadata: {
        documentId: document.id,
        dateTimeId: date_time.id,
        solarYear: date_time.solar_year,
        sol: date_time.sol,
        categories: document.categories
      }
    }
  }

  /**
   * Generate cache key for request parameters
   */
  private getCacheKey(category: string, page: number, pageSize: number, filter?: TimelineFilter): string {
    const filterKey = filter
      ? `_${filter.searchQuery || ''}_${filter.categories.join(',')}_${filter.tags.join(',')}`
      : ''
    return `${category}_${page}_${pageSize}${filterKey}`
  }

  /**
   * Check if cache entry is still valid
   */
  private isCacheValid(entry: CacheEntry): boolean {
    return Date.now() - entry.timestamp < this.CACHE_DURATION
  }

  /**
   * Fetch timeline items by category with pagination
   */
  async fetchItemsByCategory(
    category: string,
    page: number = 1,
    pageSize: number = 100
  ): Promise<{ items: TimelineItem[]; count: number; next: string | null }> {
    const cacheKey = this.getCacheKey(category, page, pageSize)

    // Check cache first
    const cachedEntry = this.cache.get(cacheKey)
    if (cachedEntry && this.isCacheValid(cachedEntry)) {
      console.log(`Cache hit for key: ${cacheKey}`)
      return {
        items: cachedEntry.data,
        count: cachedEntry.count,
        next: cachedEntry.next
      }
    }

    // Validate page boundaries using cached count from previous requests
    // Check if we have any cached entry for this category to get total count
    const firstPageKey = this.getCacheKey(category, 1, pageSize)
    const firstPageCache = this.cache.get(firstPageKey)

    if (firstPageCache && this.isCacheValid(firstPageCache)) {
      const totalCount = firstPageCache.count
      const maxPage = Math.ceil(totalCount / pageSize)

      if (page > maxPage) {
        console.warn(`Attempted to fetch page ${page} but max page is ${maxPage} (total: ${totalCount}, pageSize: ${pageSize})`)
        // Return empty result instead of making unnecessary API call
        return {
          items: [],
          count: totalCount,
          next: null
        }
      }
    }

    try {
      // Fetch from backend
      const response = await KnowledgeBaseTimelineEventsGameApi.knowledgeBaseTimelineEventsList(
        undefined, // activeGlow
        undefined, // dateTime
        undefined, // document
        undefined, // ordering (default is by timeline)
        page,
        pageSize,
        undefined, // search
        undefined, // sol
        undefined, // solGte
        undefined, // solLte
        undefined, // solarYear
        undefined, // solarYearGte
        undefined  // solarYearLte
      )

      const paginatedList: PaginatedTimeLineEventList = response.data

      // Map backend events to frontend items
      const items = paginatedList.results.map(event => this.mapTimeLineEventToTimelineItem(event))

      // Cache the result
      const cacheEntry: CacheEntry = {
        data: items,
        timestamp: Date.now(),
        count: paginatedList.count,
        next: paginatedList.next || null
      }
      this.cache.set(cacheKey, cacheEntry)

      console.log(`Fetched ${items.length} items from backend (page ${page}, total: ${paginatedList.count})`)

      return {
        items,
        count: paginatedList.count,
        next: paginatedList.next || null
      }
    } catch (error) {
      console.error('Error fetching timeline items:', error)
      throw error
    }
  }

  /**
   * Fetch filtered timeline items based on search query and filters
   */
  async fetchFilteredItems(filter: TimelineFilter): Promise<TimelineItem[]> {
    try {
      // Build filter parameters
      const searchQuery = filter.searchQuery?.trim() || undefined

      // For now, fetch all matching items (could be paginated in the future)
      const response = await KnowledgeBaseTimelineEventsGameApi.knowledgeBaseTimelineEventsList(
        undefined, // activeGlow
        undefined, // dateTime
        undefined, // document
        undefined, // ordering
        1, // page
        1000, // pageSize - fetch more items for filtering
        searchQuery, // search
        undefined, // sol
        undefined, // solGte
        undefined, // solLte
        undefined, // solarYear
        undefined, // solarYearGte
        undefined  // solarYearLte
      )

      const paginatedList: PaginatedTimeLineEventList = response.data

      // Map backend events to frontend items
      let items = paginatedList.results.map(event => this.mapTimeLineEventToTimelineItem(event))

      // Apply client-side category filtering if specified
      if (filter.categories && filter.categories.length > 0) {
        items = items.filter(item => filter.categories.includes(item.category))
      }

      // Apply client-side tag filtering if specified
      if (filter.tags && filter.tags.length > 0) {
        items = items.filter(item =>
          item.tags.some(tag => filter.tags.includes(tag.label))
        )
      }

      console.log(`Filtered ${items.length} items (search: "${searchQuery}")`)

      return items
    } catch (error) {
      console.error('Error fetching filtered items:', error)
      throw error
    }
  }

  /**
   * Clear all cached data
   */
  clearCache(): void {
    this.cache.clear()
    console.log('Timeline cache cleared')
  }

  /**
   * Clear specific cache entry
   */
  clearCacheEntry(category: string, page: number, pageSize: number): void {
    const cacheKey = this.getCacheKey(category, page, pageSize)
    this.cache.delete(cacheKey)
    console.log(`Cache entry cleared: ${cacheKey}`)
  }

  /**
   * Fetch available categories based on CategoriesEnum
   */
  fetchCategories(): TimelineCategory[] {
    // Define color mappings for each category with actual CSS gradient values
    const categoryColors: Record<string, { color: string; colorGradient: string }> = {
      events: { color: 'bg-purple-500', colorGradient: 'linear-gradient(to bottom, rgba(147, 51, 234, 0.5), rgba(126, 34, 206, 0.5))' },
      rules: { color: 'bg-red-500', colorGradient: 'linear-gradient(to bottom, rgba(220, 38, 38, 0.5), rgba(185, 28, 28, 0.5))' },
      lore: { color: 'bg-indigo-500', colorGradient: 'linear-gradient(to bottom, rgba(99, 102, 241, 0.5), rgba(79, 70, 229, 0.5))' },
      stories: { color: 'bg-pink-500', colorGradient: 'linear-gradient(to bottom, rgba(236, 72, 153, 0.5), rgba(219, 39, 119, 0.5))' },
      guides: { color: 'bg-yellow-500', colorGradient: 'linear-gradient(to bottom, rgba(234, 179, 8, 0.5), rgba(202, 138, 4, 0.5))' },
      items: { color: 'bg-orange-500', colorGradient: 'linear-gradient(to bottom, rgba(249, 115, 22, 0.5), rgba(234, 88, 12, 0.5))' },
      characters: { color: 'bg-green-500', colorGradient: 'linear-gradient(to bottom, rgba(34, 197, 94, 0.5), rgba(22, 163, 74, 0.5))' },
      locations: { color: 'bg-teal-500', colorGradient: 'linear-gradient(to bottom, rgba(20, 184, 166, 0.5), rgba(13, 148, 136, 0.5))' },
      places: { color: 'bg-cyan-500', colorGradient: 'linear-gradient(to bottom, rgba(6, 182, 212, 0.5), rgba(8, 145, 178, 0.5))' },
      factions: { color: 'bg-blue-500', colorGradient: 'linear-gradient(to bottom, rgba(59, 130, 246, 0.5), rgba(37, 99, 235, 0.5))' },
      creatures: { color: 'bg-lime-500', colorGradient: 'linear-gradient(to bottom, rgba(132, 204, 22, 0.5), rgba(101, 163, 13, 0.5))' },
      skills: { color: 'bg-emerald-500', colorGradient: 'linear-gradient(to bottom, rgba(16, 185, 129, 0.5), rgba(5, 150, 105, 0.5))' },
      spells: { color: 'bg-violet-500', colorGradient: 'linear-gradient(to bottom, rgba(139, 92, 246, 0.5), rgba(124, 58, 237, 0.5))' },
      abilities: { color: 'bg-fuchsia-500', colorGradient: 'linear-gradient(to bottom, rgba(217, 70, 239, 0.5), rgba(192, 38, 211, 0.5))' },
      other: { color: 'bg-gray-500', colorGradient: 'linear-gradient(to bottom, rgba(107, 114, 128, 0.5), rgba(75, 85, 99, 0.5))' }
    }

    // Start with 'all' category
    const categories: TimelineCategory[] = [
      {
        id: 'all',
        label: 'All Events',
        color: 'bg-blue-500',
        colorGradient: 'linear-gradient(to bottom, rgba(59, 130, 246, 0.5), rgba(37, 99, 235, 0.5))',
        visible: true
      }
    ]

    // Convert CategoriesEnum values to TimelineCategory objects
    Object.values(CategoriesEnum).forEach(categoryValue => {
      const colorConfig = categoryColors[categoryValue] || {
        color: 'bg-gray-500',
        colorGradient: 'linear-gradient(to bottom, rgba(107, 114, 128, 0.5), rgba(75, 85, 99, 0.5))'
      }

      // Capitalize first letter for label
      const label = categoryValue.charAt(0).toUpperCase() + categoryValue.slice(1)

      categories.push({
        id: categoryValue,
        label,
        color: colorConfig.color,
        colorGradient: colorConfig.colorGradient,
        visible: false // Categories are hidden by default except 'all'
      })
    })

    return categories
  }
}

export default new TimelineService()