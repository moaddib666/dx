import { ref, computed, shallowRef } from 'vue'
import { PublishedCharactersPublicApi } from '@/api/backendService.js'
import type { PublishedCharacter } from '@/api/dx-backend'

// Normalized item used by the view/composables
export interface PublishedCardItem {
  id: string
  name: string
  avatar?: string
  small_avatar?: string
  big_avatar?: string
  description?: string
  subtitle?: string
  tiktok_link?: string
  youtube_link?: string
  instagram_link?: string
}

type QueryKey = string // e.g. `${search}|${ordering}` — reserved for future use

interface PageCache {
  items: PublishedCardItem[]
  fetchedAt: number
}

export function createPublishedCharactersService() {
  // Reactive state
  const items = ref<PublishedCardItem[]>([])
  const page = ref(1)
  const pageSize = ref(24)
  const total = ref<number | null>(null) // unknown by API; best‑effort via pages length
  const loading = ref(false)
  const loadingMore = ref(false)
  const error = shallowRef<unknown | null>(null)

  // Config
  const ttlMs = ref(5 * 60_000)
  const query = ref<{ search?: string; ordering?: string }>({})

  // Caches per query key
  const cache = new Map<QueryKey, Map<number, PageCache>>()
  const inflight = new Map<string, Promise<PublishedCardItem[]>>() // key: `${key}:${page}`

  const keyOf = (q = query.value): QueryKey => `${q.search ?? ''}|${q.ordering ?? ''}`

  const hasMore = computed(() => {
    // We don't get `count` from API. Heuristic: if the last fetched page had < pageSize, no more.
    const key = keyOf()
    const pCache = cache.get(key)
    if (!pCache) return false
    const last = pCache.get(page.value)
    if (!last) return false
    return last.items.length === pageSize.value
  })

  function normalize(x: PublishedCharacter): PublishedCardItem {
    const bio = x.biography as any
    // Use small_avatar for grid display, fallback to big_avatar if not available
    const avatar = x.small_avatar || x.big_avatar || bio?.avatar
    const desc = bio?.background || bio?.appearance || ''
    // Use character_name from API as primary source
    const fallbackName = `Character ${x.id.slice(0, 8)}`
    const maybeName = (x.character_name || bio?.name || '') as string
    return {
      id: x.id,
      name: maybeName && typeof maybeName === 'string' ? maybeName : fallbackName,
      avatar: avatar || undefined,
      small_avatar: x.small_avatar || undefined,
      big_avatar: x.big_avatar || undefined,
      description: desc || undefined,
      subtitle: bio?.gender ? `Age ${bio?.age ?? ''} • ${String(bio.gender)}`.trim() : (bio?.age ? `Age ${bio.age}` : undefined),
      tiktok_link: x.tiktok_link || undefined,
      youtube_link: x.youtube_link || undefined,
      instagram_link: x.instagram_link || undefined,
    }
  }

  function getPageFromCache(key: QueryKey, p: number): PublishedCardItem[] | null {
    const pages = cache.get(key)
    if (!pages) return null
    const entry = pages.get(p)
    if (!entry) return null
    if (Date.now() - entry.fetchedAt > ttlMs.value) return null
    return entry.items
  }

  function setPageCache(key: QueryKey, p: number, data: PublishedCardItem[]) {
    let pages = cache.get(key)
    if (!pages) {
      pages = new Map()
      cache.set(key, pages)
    }
    pages.set(p, { items: data, fetchedAt: Date.now() })
  }

  async function fetchPage(p = 1, opts?: { force?: boolean }) {
    const key = keyOf()
    const inflightKey = `${key}:${p}`
    const cached = !opts?.force ? getPageFromCache(key, p) : null
    if (cached) return cached

    if (inflight.has(inflightKey)) return inflight.get(inflightKey)!

    const request = (async () => {
      const params: any = { page: p, page_size: pageSize.value }
      if (query.value.search) params.search = query.value.search
      if (query.value.ordering) params.ordering = query.value.ordering

      const isFirst = p === 1
      if (isFirst) { loading.value = true } else { loadingMore.value = true }
      error.value = null
      try {
        const resp = await PublishedCharactersPublicApi.characterPublishedList({ params })
        const array = Array.isArray(resp.data) ? resp.data as PublishedCharacter[] : []
        const normalized = array.map(normalize)
        setPageCache(key, p, normalized)
        // Merge into items if requesting current query
        if (key === keyOf()) {
          if (isFirst) {
            items.value = normalized.slice()
            page.value = 1
            total.value = normalized.length // unknown overall, track first page length
          } else {
            // append if page increments
            if (p === page.value + 1) {
              items.value = items.value.concat(normalized)
              page.value = p
            }
          }
        }
        return normalized
      } catch (e) {
        // retry once quickly
        try {
          await new Promise(r => setTimeout(r, 250))
          const resp2 = await PublishedCharactersPublicApi.characterPublishedList({ params })
          const array2 = Array.isArray(resp2.data) ? resp2.data as PublishedCharacter[] : []
          const normalized2 = array2.map(normalize)
          setPageCache(key, p, normalized2)
          if (p === 1) { items.value = normalized2.slice(); page.value = 1 } else if (p === page.value + 1) { items.value = items.value.concat(normalized2); page.value = p }
          return normalized2
        } catch (e2) {
          error.value = e2
          throw e2
        }
      } finally {
        inflight.delete(inflightKey)
        if (p === 1) loading.value = false; else loadingMore.value = false
      }
    })()

    inflight.set(inflightKey, request)
    return request
  }

  async function fetchNextPage() {
    const next = page.value + 1
    return fetchPage(next)
  }

  function setQuery(q: { search?: string; ordering?: string }) {
    const prevKey = keyOf()
    query.value = { ...q }
    const nextKey = keyOf()
    if (prevKey !== nextKey) {
      // abort in‑flight for previous key (best effort)
      inflight.clear()
      // try cache for page 1
      const cached = getPageFromCache(nextKey, 1)
      if (cached) {
        items.value = cached.slice()
        page.value = 1
      } else {
        // trigger fresh load
        fetchPage(1)
      }
    }
  }

  function init(opts?: { ttlMs?: number; pageSize?: number }) {
    if (opts?.ttlMs) ttlMs.value = opts.ttlMs
    if (opts?.pageSize) pageSize.value = opts.pageSize
    // Preload first page if empty and not loading
    if (!items.value.length && !loading.value) fetchPage(1)
  }

  function reset() {
    items.value = []
    page.value = 1
    total.value = null
    loading.value = false
    loadingMore.value = false
    error.value = null
  }

  return {
    // state
    items, page, pageSize, total, loading, loadingMore, error, hasMore,
    // ops
    init, fetchPage, fetchNextPage, setQuery, reset,
    // internals (for tests)
    _cache: cache,
  }
}

// Default singleton used by the app
export const PublishedCharactersService = createPublishedCharactersService()
