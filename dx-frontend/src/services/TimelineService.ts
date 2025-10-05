import type { TimelineItem, TimelineCategory, TimelineServiceResponse, TimelineFilter } from '@/models/TimelineModels'

class TimelineService {
  private baseUrl = '/api/timeline'
  private cache: Map<string, TimelineItem[]> = new Map()

  async fetchCategories(): Promise<TimelineCategory[]> {
    try {
      const response = await fetch(`${this.baseUrl}/categories`)
      if (!response.ok) throw new Error('Failed to fetch categories')
      return await response.json()
    } catch (error) {
      console.error('Error fetching categories:', error)
      return this.getDefaultCategories()
    }
  }

  async fetchItemsByCategory(categoryId: string): Promise<TimelineItem[]> {
    const cacheKey = `category_${categoryId}`
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey)!
    }

    try {
      const response = await fetch(`${this.baseUrl}/items?category=${categoryId}`)
      if (!response.ok) throw new Error(`Failed to fetch items for category ${categoryId}`)
      const items = await response.json()
      this.cache.set(cacheKey, items)
      return items
    } catch (error) {
      console.error(`Error fetching items for category ${categoryId}:`, error)
      return this.getMockItemsByCategory(categoryId)
    }
  }

  async fetchFilteredItems(filter: TimelineFilter): Promise<TimelineItem[]> {
    try {
      const queryParams = new URLSearchParams()
      if (filter.categories.length > 0) {
        queryParams.append('categories', filter.categories.join(','))
      }
      if (filter.tags.length > 0) {
        queryParams.append('tags', filter.tags.join(','))
      }
      if (filter.searchQuery) {
        queryParams.append('search', filter.searchQuery)
      }
      if (filter.timeRange) {
        queryParams.append('start', filter.timeRange.start)
        queryParams.append('end', filter.timeRange.end)
      }

      const response = await fetch(`${this.baseUrl}/items?${queryParams.toString()}`)
      if (!response.ok) throw new Error('Failed to fetch filtered items')
      return await response.json()
    } catch (error) {
      console.error('Error fetching filtered items:', error)
      return []
    }
  }

  clearCache(): void {
    this.cache.clear()
  }

  private getDefaultCategories(): TimelineCategory[] {
    return [
      { id: 'events', label: 'Events', color: 'bg-blue-500', colorGradient: 'from-blue-600/50 to-blue-700/50', visible: true },
      { id: 'characters', label: 'Characters', color: 'bg-cyan-500', colorGradient: 'from-cyan-600/50 to-cyan-700/50', visible: true },
      { id: 'locations', label: 'Locations', color: 'bg-amber-500', colorGradient: 'from-amber-600/50 to-amber-700/50', visible: true },
      { id: 'quests', label: 'Quests', color: 'bg-emerald-500', colorGradient: 'from-emerald-600/50 to-emerald-700/50', visible: true }
    ]
  }

  private getMockItemsByCategory(categoryId: string): TimelineItem[] {
    const mockData: Record<string, TimelineItem[]> = {
      events: [
        {
          id: 1,
          category: 'events',
          time: '09:00',
          title: 'The Great Battle',
          description: 'A legendary battle that changed the course of history',
          location: 'Ancient Battlefield',
          participants: 1000,
          tags: [{ label: 'War', color: 'red' }, { label: 'Historic', color: 'amber' }],
          gradient: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)'
        },
        {
          id: 2,
          category: 'events',
          time: '14:00',
          title: 'Royal Coronation',
          description: 'The crowning of the new monarch',
          location: 'Royal Palace',
          participants: 500,
          tags: [{ label: 'Ceremony', color: 'gold' }, { label: 'Royal', color: 'purple' }],
          gradient: 'linear-gradient(135deg, #2a1a4e 0%, #3e1646 100%)'
        }
      ],
      characters: [
        {
          id: 3,
          category: 'characters',
          time: '10:30',
          title: 'Sir Aldric the Brave',
          description: 'A legendary knight known for his valor',
          location: 'Kingdom of Valor',
          participants: 1,
          tags: [{ label: 'Knight', color: 'blue' }, { label: 'Hero', color: 'gold' }],
          gradient: 'linear-gradient(135deg, #1a2e4e 0%, #16463e 100%)'
        },
        {
          id: 4,
          category: 'characters',
          time: '15:30',
          title: 'Elara the Wise',
          description: 'A powerful mage and advisor to the crown',
          location: 'Arcane Tower',
          participants: 1,
          tags: [{ label: 'Mage', color: 'purple' }, { label: 'Advisor', color: 'cyan' }],
          gradient: 'linear-gradient(135deg, #2e1a4e 0%, #46163e 100%)'
        }
      ],
      locations: [
        {
          id: 5,
          category: 'locations',
          time: '12:00',
          title: 'The Forgotten Temple',
          description: 'An ancient temple lost to time',
          location: 'Deep Forest',
          participants: 0,
          tags: [{ label: 'Ancient', color: 'brown' }, { label: 'Mystery', color: 'purple' }],
          gradient: 'linear-gradient(135deg, #1a4e2e 0%, #163e46 100%)'
        },
        {
          id: 6,
          category: 'locations',
          time: '17:00',
          title: 'Crystal Caverns',
          description: 'Magnificent caves filled with glowing crystals',
          location: 'Northern Mountains',
          participants: 0,
          tags: [{ label: 'Natural', color: 'green' }, { label: 'Beautiful', color: 'cyan' }],
          gradient: 'linear-gradient(135deg, #1a2e4e 0%, #16463e 100%)'
        }
      ],
      quests: [
        {
          id: 7,
          category: 'quests',
          time: '16:00',
          title: 'The Dragon\'s Hoard',
          description: 'Retrieve the legendary treasure from the dragon\'s lair',
          location: 'Dragon Peak',
          participants: 5,
          tags: [{ label: 'Epic', color: 'red' }, { label: 'Treasure', color: 'gold' }],
          gradient: 'linear-gradient(135deg, #4e1a1a 0%, #3e1616 100%)'
        },
        {
          id: 8,
          category: 'quests',
          time: '18:00',
          title: 'The Lost Artifact',
          description: 'Find the ancient artifact before it falls into the wrong hands',
          location: 'Ruins of Eldoria',
          participants: 3,
          tags: [{ label: 'Adventure', color: 'orange' }, { label: 'Artifact', color: 'purple' }],
          gradient: 'linear-gradient(135deg, #4e2e1a 0%, #3e2616 100%)'
        }
      ]
    }

    return mockData[categoryId] || []
  }
}

export default new TimelineService()
