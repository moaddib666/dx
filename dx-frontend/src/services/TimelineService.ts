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
            { id: 'locations', label: 'Locations', color: 'bg-amber-500', colorGradient: 'from-amber-600/50 to-amber-700/50', visible: true }
        ]
    }

    private getMockItemsByCategory(categoryId: string, offset: number = 0, limit: number = 10): TimelineItem[] {
        const mockData: Record<string, TimelineItem[]> = {
            events: [
                {
                    id: 1,
                    category: 'events',
                    time: 0,
                    beforeAnomalyGlow: true,
                    title: 'The Beginning',
                    description: 'Nothing exists except pure energy - the Flow. The primordial state before reality itself.',
                    location: 'Pre-Reality',
                    participants: 0,
                    tags: [{ label: 'BAG', color: 'purple' }, { label: 'Origin', color: 'gold' }],
                    gradient: 'linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 100%)'
                },
                {
                    id: 2,
                    category: 'events',
                    time: 10000,
                    beforeAnomalyGlow: true,
                    title: 'Flow Concentration Begins',
                    description: 'The Flow starts to concentrate, and the pressure of pure energy increases exponentially, setting the stage for material reality.',
                    location: 'Pre-Reality',
                    participants: 0,
                    tags: [{ label: 'BAG', color: 'purple' }, { label: 'Formation', color: 'cyan' }],
                    gradient: 'linear-gradient(135deg, #1a0a2e 0%, #2e0a1a 100%)'
                },
                {
                    id: 3,
                    category: 'events',
                    time: 50000,
                    beforeAnomalyGlow: true,
                    title: 'First Matter Forms',
                    description: 'The Flow begins forming physical reality. Matter starts connecting into shapes, creating the primordial mega-sphere.',
                    location: 'Forming Reality',
                    participants: 0,
                    tags: [{ label: 'BAG', color: 'purple' }, { label: 'Matter', color: 'blue' }],
                    gradient: 'linear-gradient(135deg, #1a1a2e 0%, #2e1a2e 100%)'
                },
                {
                    id: 4,
                    category: 'events',
                    time: 75000,
                    beforeAnomalyGlow: true,
                    title: 'The Great Explosion',
                    description: 'The mega-sphere explodes with tremendous force, freeing material and splitting reality into ten dimensions. Energy flows from the borders toward the middle.',
                    location: 'All Dimensions',
                    participants: 0,
                    tags: [{ label: 'BAG', color: 'purple' }, { label: 'Dimensional', color: 'cyan' }, { label: 'Catastrophic', color: 'red' }],
                    gradient: 'linear-gradient(135deg, #2e1a4e 0%, #4e1a2e 100%)'
                },
                {
                    id: 5,
                    category: 'events',
                    time: 76000,
                    beforeAnomalyGlow: true,
                    title: 'Dimensional Stabilization',
                    description: 'The ten dimensions stabilize and energy flows begin to establish consistent patterns. The laws of physics take their final form.',
                    location: 'All Dimensions',
                    participants: 0,
                    tags: [{ label: 'BAG', color: 'purple' }, { label: 'Stability', color: 'blue' }],
                    gradient: 'linear-gradient(135deg, #1a2e4e 0%, #2e1a4e 100%)'
                },
                {
                    id: 6,
                    category: 'events',
                    time: 85000,
                    beforeAnomalyGlow: true,
                    title: 'Birth of the Stars',
                    description: 'Pressure of energy in the 1st dimension increases dramatically. Stars ignite and begin spreading energy throughout the universe.',
                    location: '1st Dimension',
                    participants: 0,
                    tags: [{ label: 'BAG', color: 'purple' }, { label: 'Cosmic', color: 'blue' }, { label: 'Light', color: 'gold' }],
                    gradient: 'linear-gradient(135deg, #1a1a4e 0%, #2e2a1a 100%)'
                },
                {
                    id: 7,
                    category: 'events',
                    time: 87000,
                    beforeAnomalyGlow: true,
                    title: 'Star System Formation',
                    description: 'Early star systems begin to form across the universe, setting the stage for planetary creation.',
                    location: '1st Dimension',
                    participants: 0,
                    tags: [{ label: 'BAG', color: 'purple' }, { label: 'Stellar', color: 'blue' }],
                    gradient: 'linear-gradient(135deg, #2e2a4e 0%, #1a2e2e 100%)'
                },
                {
                    id: 8,
                    category: 'events',
                    time: 95000,
                    beforeAnomalyGlow: true,
                    title: 'First Planets',
                    description: 'The first planets form from exploded stars, accumulating matter through gravitational spin and arranging into solar systems.',
                    location: '1st Dimension',
                    participants: 0,
                    tags: [{ label: 'BAG', color: 'purple' }, { label: 'Planetary', color: 'green' }],
                    gradient: 'linear-gradient(135deg, #1a4e2e 0%, #2e2a1a 100%)'
                },
                {
                    id: 9,
                    category: 'events',
                    time: 120000,
                    beforeAnomalyGlow: true,
                    title: 'Primitive Life Emerges',
                    description: 'The first primitive forms of life begin to develop on isolated planets, separated by billions of solar systems.',
                    location: 'Various Planets',
                    participants: 0,
                    tags: [{ label: 'BAG', color: 'purple' }, { label: 'Life', color: 'green' }, { label: 'Origin', color: 'gold' }],
                    gradient: 'linear-gradient(135deg, #1a2e1a 0%, #2e4e1a 100%)'
                },
                {
                    id: 10,
                    category: 'events',
                    time: 145000,
                    beforeAnomalyGlow: true,
                    title: 'Early Ecosystems',
                    description: 'Basic ecosystems start to develop with simple plant and animal life emerging on habitable worlds.',
                    location: 'Habitable Planets',
                    participants: 0,
                    tags: [{ label: 'BAG', color: 'purple' }, { label: 'Evolution', color: 'green' }],
                    gradient: 'linear-gradient(135deg, #2e4e1a 0%, #1a4e2e 100%)'
                },
                {
                    id: 11,
                    category: 'events',
                    time: 200000,
                    beforeAnomalyGlow: false,
                    title: 'The Anomaly Glow',
                    description: 'All stars suddenly change their energy from type A to type B as dimensions 1 and 10 shift energy patterns. This triggers rapid evolution of life across all worlds, marking the beginning of a new era.',
                    location: 'All Dimensions',
                    participants: 0,
                    tags: [{ label: 'AG', color: 'cyan' }, { label: 'Transformation', color: 'gold' }, { label: 'Historic', color: 'amber' }],
                    gradient: 'linear-gradient(135deg, #1a4e4e 0%, #4e4e1a 100%)'
                },
                {
                    id: 12,
                    category: 'events',
                    time: 205000,
                    beforeAnomalyGlow: false,
                    title: 'Multicellular Revolution',
                    description: 'Simple multicellular organisms rapidly appear across inhabited worlds, beginning the diversification of complex life.',
                    location: 'Habitable Planets',
                    participants: 0,
                    tags: [{ label: 'Post-AG', color: 'cyan' }, { label: 'Evolution', color: 'green' }],
                    gradient: 'linear-gradient(135deg, #1a4e2e 0%, #2e4e1a 100%)'
                },
                {
                    id: 13,
                    category: 'events',
                    time: 215000,
                    beforeAnomalyGlow: false,
                    title: 'Humanoid Life Appears',
                    description: 'Humanoid carbon-based life appears on numerous planets across the universe, beginning the path toward sentient civilization.',
                    location: 'Multiple Planets',
                    participants: 0,
                    tags: [{ label: 'Post-AG', color: 'cyan' }, { label: 'Humanoid', color: 'amber' }],
                    gradient: 'linear-gradient(135deg, #2e2a1a 0%, #1a2e4e 100%)'
                },
                {
                    id: 14,
                    category: 'events',
                    time: 230000,
                    beforeAnomalyGlow: false,
                    title: 'First Civilizations',
                    description: 'Early civilizations begin to form with rudimentary tools, social structures, and proto-languages.',
                    location: 'Mainland Primus',
                    participants: 1000,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Civilization', color: 'gold' }],
                    gradient: 'linear-gradient(135deg, #2e1a1a 0%, #1a2e2e 100%)'
                },
                {
                    id: 15,
                    category: 'events',
                    time: 235000,
                    beforeAnomalyGlow: false,
                    title: 'Agricultural Revolution',
                    description: 'Humanoid societies develop agriculture and permanent settlements, leading to population growth and cultural development.',
                    location: 'Mainland Primus',
                    participants: 5000,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Development', color: 'amber' }],
                    gradient: 'linear-gradient(135deg, #1a2e1a 0%, #2e2a1a 100%)'
                },
                {
                    id: 16,
                    category: 'events',
                    time: 240000,
                    beforeAnomalyGlow: false,
                    title: 'Emergence of Complex Societies',
                    description: 'Advanced societies develop with trade networks, writing systems, and organized religions spreading across continents.',
                    location: 'Multiple Continents',
                    participants: 50000,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Culture', color: 'purple' }],
                    gradient: 'linear-gradient(135deg, #2e1a4e 0%, #1a2e2e 100%)'
                },
                {
                    id: 17,
                    category: 'events',
                    time: 250000,
                    beforeAnomalyGlow: false,
                    title: 'Evolution of the Differs',
                    description: 'Due to complex energy flow patterns, some creatures become "Differs" - beings who can see the Flow and accumulate energy. This gift appears randomly across species.',
                    location: 'Mainland Primus',
                    participants: 1000,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Evolution', color: 'purple' }, { label: 'Flow', color: 'blue' }],
                    gradient: 'linear-gradient(135deg, #1a2e4e 0%, #2e1a4e 100%)'
                },
                {
                    id: 18,
                    category: 'events',
                    time: 251000,
                    beforeAnomalyGlow: false,
                    title: 'First Energy Manipulators',
                    description: 'Early discoveries of intentional energy manipulation by gifted Differs mark the beginning of structured Flow control.',
                    location: 'Various Locations',
                    participants: 50,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Flow', color: 'blue' }, { label: 'Discovery', color: 'gold' }],
                    gradient: 'linear-gradient(135deg, #1a2e4e 0%, #4e2e1a 100%)'
                },
                {
                    id: 19,
                    category: 'events',
                    time: 255000,
                    beforeAnomalyGlow: false,
                    title: 'Founding of Flow Schools',
                    description: 'The first schools are established to train gifted individuals in controlling and harnessing the Flow, creating structured magical education.',
                    location: 'Mystory Heaven',
                    participants: 500,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Education', color: 'blue' }, { label: 'Magic', color: 'purple' }],
                    gradient: 'linear-gradient(135deg, #2e1a4e 0%, #1a2e4e 100%)'
                },
                {
                    id: 20,
                    category: 'events',
                    time: 256000,
                    beforeAnomalyGlow: false,
                    title: 'Birth of The Chosen One',
                    description: 'JSon is born with unprecedented ability to accumulate enormous amounts of energy and travel through dimensions. His top dimension is the 3rd one - a feat unmatched in history.',
                    location: 'City of Memories',
                    participants: 1,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Chosen', color: 'gold' }, { label: 'Legendary', color: 'purple' }],
                    gradient: 'linear-gradient(135deg, #4e2a1a 0%, #2a1a4e 100%)'
                },
                {
                    id: 21,
                    category: 'events',
                    time: 256200,
                    beforeAnomalyGlow: false,
                    title: 'Scientific Boom',
                    description: 'Jonathan Casey invents the dimensional suit - revolutionary gear that covers creatures with energy flow, allowing non-gifted individuals to travel between dimensions for the first time.',
                    location: 'TechnoEdge',
                    participants: 100,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Technology', color: 'cyan' }, { label: 'Revolution', color: 'orange' }],
                    gradient: 'linear-gradient(135deg, #1a4e2e 0%, #2e4e1a 100%)'
                },
                {
                    id: 22,
                    category: 'events',
                    time: 256300,
                    beforeAnomalyGlow: false,
                    title: 'Dimensional Travel Experiments',
                    description: 'Early experiments with dimension travel begin, leading to breakthrough technological advancements and new understanding of reality.',
                    location: 'TechnoEdge',
                    participants: 200,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Science', color: 'cyan' }, { label: 'Experimental', color: 'orange' }],
                    gradient: 'linear-gradient(135deg, #2e4e4e 0%, #1a2e4e 100%)'
                },
                {
                    id: 23,
                    category: 'events',
                    time: 256500,
                    beforeAnomalyGlow: false,
                    title: 'The Gear Control Crisis',
                    description: 'The Chosen demand control over dimensional gear manufacture, claiming it unnatural and dangerous. Jonathan Casey fights to democratize dimensional travel, sparking political conflict.',
                    location: 'City of Memories',
                    participants: 10000,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Political', color: 'gold' }, { label: 'Conflict', color: 'red' }],
                    gradient: 'linear-gradient(135deg, #4e2e1a 0%, #2e1a4e 100%)'
                },
                {
                    id: 24,
                    category: 'events',
                    time: 256600,
                    beforeAnomalyGlow: false,
                    title: 'The First Conflict',
                    description: 'John invents a powerful weapon to challenge JSon. They meet in the dangerous 3rd dimension for an epic battle that reshapes the balance of power between tech and magic.',
                    location: '3rd Dimension',
                    participants: 2,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'War', color: 'red' }, { label: 'Dimensional', color: 'cyan' }, { label: 'Epic', color: 'gold' }],
                    gradient: 'linear-gradient(135deg, #4e1a1a 0%, #1a1a4e 100%)'
                },
                {
                    id: 25,
                    category: 'events',
                    time: 256800,
                    beforeAnomalyGlow: false,
                    title: 'The Great Mall Opening',
                    description: 'The Great Mall opens in the City of Memories, becoming the central hub for trade, culture, and dimensional commerce. It symbolizes peace between factions.',
                    location: 'City of Memories',
                    participants: 50000,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Economic', color: 'gold' }, { label: 'Cultural', color: 'cyan' }, { label: 'Peace', color: 'blue' }],
                    gradient: 'linear-gradient(135deg, #2e4e1a 0%, #4e2e1a 100%)'
                },
                {
                    id: 26,
                    category: 'events',
                    time: 257000,
                    beforeAnomalyGlow: false,
                    title: 'Eva Chan\'s Rampage',
                    description: 'Enhanced mercenary Eva Chan attacks the City of Memories in a cybernetic rage caused by mental instability from over-augmentation. After a brief confrontation in the 4th dimension, she mysteriously disappears.',
                    location: 'City of Memories',
                    participants: 1000,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Attack', color: 'red' }, { label: 'Technology', color: 'cyan' }, { label: 'Mystery', color: 'purple' }],
                    gradient: 'linear-gradient(135deg, #4e1a1a 0%, #1a4e4e 100%)'
                },
                {
                    id: 27,
                    category: 'events',
                    time: 257000,
                    beforeAnomalyGlow: false,
                    title: 'Dead Spider Arrests',
                    description: 'Following Eva\'s attack, Dead Spider mercenaries are arrested. Their leader is imprisoned and all dangerous artifacts and enhancements are confiscated by authorities.',
                    location: 'City of Memories',
                    participants: 50,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Justice', color: 'blue' }, { label: 'Law', color: 'gold' }],
                    gradient: 'linear-gradient(135deg, #2e2e2e 0%, #1a2e4e 100%)'
                },
                {
                    id: 28,
                    category: 'events',
                    time: 257100,
                    beforeAnomalyGlow: false,
                    title: 'Present Day',
                    description: 'The current era where magic and technology coexist in uneasy balance. Mysteries remain unsolved, including Eva Chan\'s fate and the nature of the blue-eyed shadows in the 4th dimension.',
                    location: 'Dimension-X',
                    participants: 1000000,
                    tags: [{ label: 'HE', color: 'green' }, { label: 'Modern', color: 'cyan' }, { label: 'Active', color: 'orange' }],
                    gradient: 'linear-gradient(135deg, #1a2e4e 0%, #2e1a4e 100%)'
                }
            ],
            characters: [
                {
                    id: 29,
                    category: 'characters',
                    time: 256000,
                    beforeAnomalyGlow: false,
                    title: 'JSon - The Chosen One',
                    description: 'Born with unprecedented ability to accumulate energy and traverse dimensions. Can reach the 3rd dimension - a feat unmatched by any other being in history.',
                    location: 'City of Memories',
                    participants: 1,
                    tags: [{ label: 'Legendary', color: 'gold' }, { label: 'Flow Master', color: 'blue' }, { label: 'Dimensional', color: 'cyan' }],
                    gradient: 'linear-gradient(135deg, #2a1a4e 0%, #4e2a1a 100%)'
                },
                {
                    id: 30,
                    category: 'characters',
                    time: 254000,
                    beforeAnomalyGlow: false,
                    title: 'Jonathan Casey - The Inventor',
                    description: 'Brilliant scientist who invented the dimensional suit, enabling non-gifted individuals to travel between dimensions and challenging the monopoly of the Chosen.',
                    location: 'TechnoEdge',
                    participants: 1,
                    tags: [{ label: 'Genius', color: 'cyan' }, { label: 'Revolutionary', color: 'orange' }, { label: 'Tech', color: 'green' }],
                    gradient: 'linear-gradient(135deg, #1a4e2e 0%, #2e1a4e 100%)'
                },
                {
                    id: 31,
                    category: 'characters',
                    time: 254500,
                    beforeAnomalyGlow: false,
                    title: 'Eva Chan - The Fallen Mercenary',
                    description: 'Once a skilled fighter, Eva\'s over-reliance on cybernetic enhancements led to severe mental instability. Her attack on the City and mysterious disappearance into the 4th dimension remains unsolved.',
                    location: 'TechnoEdge',
                    participants: 1,
                    tags: [{ label: 'Tragic', color: 'purple' }, { label: 'Enhanced', color: 'cyan' }, { label: 'Mercenary', color: 'red' }],
                    gradient: 'linear-gradient(135deg, #4e1a2e 0%, #2e4e1a 100%)'
                },
                {
                    id: 32,
                    category: 'characters',
                    time: 253000,
                    beforeAnomalyGlow: false,
                    title: 'Valid Arbiter - The Mysterious Guide',
                    description: 'An enigmatic figure who appears to travelers at the Monument of Memories, sharing cryptic knowledge about the world\'s true nature before vanishing without explanation.',
                    location: 'Monument of Memories',
                    participants: 1,
                    tags: [{ label: 'Mysterious', color: 'purple' }, { label: 'Guide', color: 'blue' }, { label: 'Enigmatic', color: 'cyan' }],
                    gradient: 'linear-gradient(135deg, #1a1a4e 0%, #4e1a4e 100%)'
                },
                {
                    id: 33,
                    category: 'characters',
                    time: 255500,
                    beforeAnomalyGlow: false,
                    title: 'Punk - The Informant',
                    description: 'A streetwise character who operates in the shadows of the City of Memories. Claims to know the location of the legendary Ale of Eternity, though his true motives remain unclear.',
                    location: 'City of Memories',
                    participants: 1,
                    tags: [{ label: 'Informant', color: 'orange' }, { label: 'Mysterious', color: 'purple' }, { label: 'Urban', color: 'gray' }],
                    gradient: 'linear-gradient(135deg, #2e2e1a 0%, #1a2e2e 100%)'
                },
                {
                    id: 34,
                    category: 'characters',
                    time: 252000,
                    beforeAnomalyGlow: false,
                    title: 'The Council of Elders',
                    description: 'Ancient Flow masters who govern Mystory Heaven and maintain the delicate balance between magical and technological forces. Their wisdom spans centuries.',
                    location: 'Mystory Heaven',
                    participants: 12,
                    tags: [{ label: 'Leadership', color: 'gold' }, { label: 'Ancient', color: 'amber' }, { label: 'Wisdom', color: 'blue' }],
                    gradient: 'linear-gradient(135deg, #2e1a4e 0%, #4e2e1a 100%)'
                },
                {
                    id: 35,
                    category: 'characters',
                    time: 256500,
                    beforeAnomalyGlow: false,
                    title: 'Dead Spider Clan Leader',
                    description: 'Leader of the notorious Dead Spider mercenary organization. Imprisoned after Eva Chan\'s rampage, his network was dismantled but some members remain at large.',
                    location: 'TechnoEdge',
                    participants: 1,
                    tags: [{ label: 'Criminal', color: 'red' }, { label: 'Mercenary', color: 'orange' }, { label: 'Captured', color: 'gray' }],
                    gradient: 'linear-gradient(135deg, #4e1a1a 0%, #2e2e2e 100%)'
                },
                {
                    id: 36,
                    category: 'characters',
                    time: 251000,
                    beforeAnomalyGlow: false,
                    title: 'First Flow Seers',
                    description: 'The original individuals to manifest the ability to see and manipulate the Flow. They became the ancestors and teachers of all modern magic users and Flow schools.',
                    location: 'Mainland Primus',
                    participants: 50,
                    tags: [{ label: 'Origin', color: 'gold' }, { label: 'Flow', color: 'blue' }, { label: 'Historic', color: 'amber' }],
                    gradient: 'linear-gradient(135deg, #1a2e4e 0%, #4e2e1a 100%)'
                }
            ],
            locations: [
                {
                    id: 37,
                    category: 'locations',
                    time: 250000,
                    beforeAnomalyGlow: false,
                    title: 'City of Memories',
                    description: 'The neutral ground and political center of Dimension-X. Home to the Great Mall and the Monument of Memories, where past and present converge in harmony.',
                    location: 'Mainland Primus',
                    participants: 0,
                    tags: [{ label: 'Capital', color: 'gold' }, { label: 'Neutral', color: 'blue' }, { label: 'Historic', color: 'amber' }],
                    gradient: 'linear-gradient(135deg, #2e2a1a 0%, #1a2e4e 100%)'
                },
                {
                    id: 38,
                    category: 'locations',
                    time: 252000,
                    beforeAnomalyGlow: false,
                    title: 'TechnoEdge',
                    description: 'The industrial powerhouse where technology and innovation flourish. Governed by corporate oligarchy, it\'s the birthplace of dimensional gear and advanced tech.',
                    location: 'TechnoEdge Continent',
                    participants: 0,
                    tags: [{ label: 'Industrial', color: 'cyan' }, { label: 'Technology', color: 'green' }, { label: 'Innovation', color: 'orange' }],
                    gradient: 'linear-gradient(135deg, #1a4e2e 0%, #2e4e4e 100%)'
                },
                {
                    id: 39,
                    category: 'locations',
                    time: 251000,
                    beforeAnomalyGlow: false,
                    title: 'Mystory Heaven',
                    description: 'The magical authority ruled by the Council of Elders. Ancient temples dot the landscape where Flow masters train and mystical knowledge is preserved through generations.',
                    location: 'Mystory Heaven Continent',
                    participants: 0,
                    tags: [{ label: 'Magical', color: 'purple' }, { label: 'Ancient', color: 'amber' }, { label: 'Sacred', color: 'blue' }],
                    gradient: 'linear-gradient(135deg, #2e1a4e 0%, #1a2e4e 100%)'
                },
                {
                    id: 40,
                    category: 'locations',
                    time: 256800,
                    beforeAnomalyGlow: false,
                    title: 'The Great Mall',
                    description: 'Central hub of commerce in the City of Memories. A massive marketplace where dimensional traders exchange goods, knowledge, and artifacts from across all accessible dimensions.',
                    location: 'City of Memories',
                    participants: 0,
                    tags: [{ label: 'Commerce', color: 'gold' }, { label: 'Cultural', color: 'cyan' }, { label: 'Trading', color: 'green' }],
                    gradient: 'linear-gradient(135deg, #4e2e1a 0%, #2e4e1a 100%)'
                },
                {
                    id: 41,
                    category: 'locations',
                    time: 253000,
                    beforeAnomalyGlow: false,
                    title: 'Monument of Memories',
                    description: 'An ancient and mysterious structure where Valid Arbiter often appears. Said to be a powerful convergence point of dimensional energy and historical significance.',
                    location: 'City of Memories',
                    participants: 0,
                    tags: [{ label: 'Historic', color: 'amber' }, { label: 'Mysterious', color: 'purple' }, { label: 'Sacred', color: 'blue' }],
                    gradient: 'linear-gradient(135deg, #1a1a4e 0%, #4e2e1a 100%)'
                },
                {
                    id: 42,
                    category: 'locations',
                    time: 254000,
                    beforeAnomalyGlow: false,
                    title: 'The Eternal Grove',
                    description: 'Scattered settlements living in perfect harmony with the Flow and nature. Advanced eco-tech is subtly integrated into the natural environment.',
                    location: 'Mainland Primus',
                    participants: 0,
                    tags: [{ label: 'Natural', color: 'green' }, { label: 'Peaceful', color: 'blue' }, { label: 'Eco-Tech', color: 'cyan' }],
                    gradient: 'linear-gradient(135deg, #1a4e2e 0%, #2e4e1a 100%)'
                },
                {
                    id: 43,
                    category: 'locations',
                    time: 251500,
                    beforeAnomalyGlow: false,
                    title: 'Flow Peaks Mountains',
                    description: 'Mountain range with extraordinary Flow convergence. Home to ancient temples and meditation sites where Flow masters achieve dimensional enlightenment and profound power.',
                    location: 'Mystory Heaven',
                    participants: 0,
                    tags: [{ label: 'Flow Nexus', color: 'blue' }, { label: 'Sacred', color: 'purple' }, { label: 'Ancient', color: 'amber' }],
                    gradient: 'linear-gradient(135deg, #2e2a4e 0%, #1a4e4e 100%)'
                },
                {
                    id: 44,
                    category: 'locations',
                    time: 75000,
                    beforeAnomalyGlow: true,
                    title: '2nd Dimension',
                    description: 'A realm where time flows slower and visibility is limited. Used by experienced travelers as shortcuts between continents. Energy drains over time, requiring careful planning.',
                    location: '2nd Dimension',
                    participants: 0,
                    tags: [{ label: 'Dimensional', color: 'cyan' }, { label: 'Transit', color: 'orange' }, { label: 'Dangerous', color: 'red' }],
                    gradient: 'linear-gradient(135deg, #1a1a2e 0%, #2e2e4e 100%)'
                },
                {
                    id: 45,
                    category: 'locations',
                    time: 75000,
                    beforeAnomalyGlow: true,
                    title: '3rd Dimension',
                    description: 'A desolate zone with powerful storms obscuring vision. Only JSon can reliably access this dimension. Used as a battleground by the most powerful beings in existence.',
                    location: '3rd Dimension',
                    participants: 0,
                    tags: [{ label: 'Dimensional', color: 'cyan' }, { label: 'Extreme', color: 'red' }, { label: 'Elite Only', color: 'purple' }],
                    gradient: 'linear-gradient(135deg, #2e1a1a 0%, #1a1a2e 100%)'
                },
                {
                    id: 46,
                    category: 'locations',
                    time: 75000,
                    beforeAnomalyGlow: true,
                    title: '4th Dimension',
                    description: 'A realm where time flows faster, allowing more actions in the same period. Sharp shadows of humanoid creatures with glowing blue eyes occasionally appear. Extremely hazardous to navigate.',
                    location: '4th Dimension',
                    participants: 0,
                    tags: [{ label: 'Dimensional', color: 'cyan' }, { label: 'Time Distortion', color: 'orange' }, { label: 'Deadly', color: 'red' }],
                    gradient: 'linear-gradient(135deg, #1a2e4e 0%, #4e1a2e 100%)'
                },
                {
                    id: 47,
                    category: 'locations',
                    time: 75000,
                    beforeAnomalyGlow: true,
                    title: '5th-10th Dimensions',
                    description: 'Largely unknown realms beyond mortal reach. Everyone who has attempted to pass the barrier has been forcibly returned to the 1st dimension completely drained of energy.',
                    location: 'Unknown Dimensions',
                    participants: 0,
                    tags: [{ label: 'Dimensional', color: 'cyan' }, { label: 'Unknown', color: 'purple' }, { label: 'Forbidden', color: 'red' }],
                    gradient: 'linear-gradient(135deg, #1a1a1a 0%, #2e1a2e 100%)'
                }
            ]
        }

        const items = mockData[categoryId] || []
        return items.slice(offset, offset + limit)
    }
}

export default new TimelineService()