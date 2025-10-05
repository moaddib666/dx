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

  async fetchItemsByCategory(categoryId: string, offset: number = 0, limit: number = 10): Promise<TimelineItem[]> {
    // Don't use cache for paginated requests
    const cacheKey = `category_${categoryId}_${offset}_${limit}`

    try {
      const response = await fetch(`${this.baseUrl}/items?category=${categoryId}&offset=${offset}&limit=${limit}`)
      if (!response.ok) throw new Error(`Failed to fetch items for category ${categoryId}`)
      const items = await response.json()
      return items
    } catch (error) {
      console.error(`Error fetching items for category ${categoryId}:`, error)
      return this.getMockItemsByCategory(categoryId, offset, limit)
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

  private getMockItemsByCategory(categoryId: string, offset: number = 0, limit: number = 10): TimelineItem[] {
    const mockData: Record<string, TimelineItem[]> = {
      events: [
        {
          id: 1,
          category: 'events',
          time: '10050',
          title: 'Battle of Arrakeen',
          description: 'The decisive battle for control of Arrakis',
          location: 'Arrakeen',
          participants: 10000,
          tags: [{ label: 'War', color: 'red' }, { label: 'Historic', color: 'amber' }],
          gradient: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)'
        },
        {
          id: 2,
          category: 'events',
          time: '10140',
          title: 'Spice Monopoly Established',
          description: 'House Atreides gains control of spice production',
          location: 'Arrakis',
          participants: 500,
          tags: [{ label: 'Economic', color: 'gold' }, { label: 'Political', color: 'purple' }],
          gradient: 'linear-gradient(135deg, #2a1a4e 0%, #3e1646 100%)'
        }
      ],
      characters: [
        {
          id: 3,
          category: 'characters',
          time: '10025',
          title: 'Paul Atreides Born',
          description: 'Birth of the future Muad\'Dib',
          location: 'Caladan',
          participants: 1,
          tags: [{ label: 'Kwisatz Haderach', color: 'blue' }, { label: 'Atreides', color: 'gold' }],
          gradient: 'linear-gradient(135deg, #1a2e4e 0%, #16463e 100%)'
        },
        {
          id: 4,
          category: 'characters',
          time: '10175',
          title: 'Leto II Ascends',
          description: 'The God Emperor begins his reign',
          location: 'Arrakis',
          participants: 1,
          tags: [{ label: 'Emperor', color: 'purple' }, { label: 'Transformation', color: 'cyan' }],
          gradient: 'linear-gradient(135deg, #2e1a4e 0%, #46163e 100%)'
        }
      ],
      locations: [
        {
          id: 5,
          category: 'locations',
          time: '10080',
          title: 'Sietch Tabr Discovered',
          description: 'Hidden Fremen stronghold revealed',
          location: 'Deep Desert',
          participants: 0,
          tags: [{ label: 'Fremen', color: 'brown' }, { label: 'Secret', color: 'purple' }],
          gradient: 'linear-gradient(135deg, #1a4e2e 0%, #163e46 100%)'
        },
        {
          id: 6,
          category: 'locations',
          time: '10190',
          title: 'Water of Life Source',
          description: 'Sacred pool of the Water of Life found',
          location: 'Southern Pole',
          participants: 0,
          tags: [{ label: 'Sacred', color: 'green' }, { label: 'Mystical', color: 'cyan' }],
          gradient: 'linear-gradient(135deg, #1a2e4e 0%, #16463e 100%)'
        }
      ],
      quests: [
        {
          id: 7,
          category: 'quests',
          time: '10100',
          title: 'Retrieve the Crysknife',
          description: 'Obtain the sacred blade of the Fremen',
          location: 'Sietch Tabr',
          participants: 5,
          tags: [{ label: 'Sacred', color: 'red' }, { label: 'Weapon', color: 'gold' }],
          gradient: 'linear-gradient(135deg, #4e1a1a 0%, #3e1616 100%)'
        },
        {
          id: 8,
          category: 'quests',
          time: '10160',
          title: 'Spice Harvesting Mission',
          description: 'Secure spice from the deep desert',
          location: 'Coriolis Storm Region',
          participants: 50,
          tags: [{ label: 'Dangerous', color: 'orange' }, { label: 'Spice', color: 'purple' }],
          gradient: 'linear-gradient(135deg, #4e2e1a 0%, #3e2616 100%)'
        }
      ]
    }

    const items = mockData[categoryId] || []
    // Apply pagination: slice array based on offset and limit
    return items.slice(offset, offset + limit)
  }
}

export default new TimelineService()
