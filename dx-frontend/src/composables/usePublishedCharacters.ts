import { computed } from 'vue'
import { PublishedCharactersService } from '@/services/publishedCharactersService'

export function usePublishedCharacters() {
  const svc = PublishedCharactersService

  // expose as readonly where appropriate via computed wrappers
  return {
    items: svc.items,
    page: svc.page,
    pageSize: svc.pageSize,
    total: svc.total,
    loading: svc.loading,
    loadingMore: svc.loadingMore,
    hasMore: svc.hasMore,
    error: svc.error,
    // operations
    init: svc.init,
    fetchPage: svc.fetchPage,
    fetchNextPage: svc.fetchNextPage,
    setQuery: svc.setQuery,
    reset: svc.reset,
    // helpers
    empty: computed(() => !svc.loading.value && svc.items.value.length === 0),
  }
}
