export interface TimelineItem {
  id: string | number
  category: string
  time: number | string
  beforeAnomalyGlow?: boolean
  title: string
  description?: string
  location?: string
  participants?: number
  tags: TimelineTag[]
  image?: string
  gradient?: string
  metadata?: Record<string, any>
}

export interface TimelineTag {
  label: string
  color?: string
}

export interface TimelineCategory {
  id: string
  label: string
  color: string
  colorGradient: string
  visible: boolean
}

export interface TimelineFilter {
  categories: string[]
  tags: string[]
  timeRange?: { start: string; end: string }
  searchQuery?: string
}

export interface TimelineServiceResponse {
  items: TimelineItem[]
  categories: TimelineCategory[]
  totalCount: number
}
