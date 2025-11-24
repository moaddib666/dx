<template>
  <section class="cp-panel cp-panel--right">
    <div class="cp-card cp-card--toolbar">
      <div class="cp-toolbar">
        <div class="cp-title-sm">{{ title }}</div>
        <div class="cp-search">
          <input v-model="q" class="cp-input" placeholder="Search characters..." />
        </div>
        <div class="cp-toggle">
          <button class="cp-tab" :class="{active: filter==='players'}" @click="setFilter('players')">Players</button>
          <button class="cp-tab" :class="{active: filter==='npcs'}" @click="setFilter('npcs')">Legendary NPCs</button>
        </div>
      </div>
    </div>

    <div class="cp-grid" ref="gridEl">
      <div v-if="isLoading" class="cp-loading">Loading...</div>
      <div v-else-if="filteredItems.length===0" class="cp-empty">No characters found.</div>
      <button
        v-for="item in filteredItems"
        :key="item.id"
        class="cp-tile"
        :class="{selected: selectedId===item.id}"
        @click="$emit('select', item)"
      >
        <div class="cp-tile__head">
          <div class="cp-tile__name" :title="item.name">{{ item.name }}</div>
          <span class="cp-badge" :data-tone="item.tone || 'blue'">{{ item.badge || 'CHAR' }}</span>
        </div>
        <div class="cp-tile__art">
          <img v-if="item.avatar" :src="item.avatar" :alt="item.name" @error="hide($event)"/>
          <div v-else class="cp-tile__ph">{{ initials(item.name) }}</div>
        </div>
        <div class="cp-tile__sub" :title="item.subtitle">{{ item.subtitle || ' ' }}</div>
      </button>

      <!-- Load more tile -->
      <button v-if="showLoadMore" class="cp-more" :disabled="loadingMore" @click="$emit('load-more')">
        <span v-if="!loadingMore">Load more</span>
        <span v-else class="cp-spinner-sm"></span>
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

export interface CharGridItem {
  id: string | number
  name: string
  avatar?: string
  description?: string
  subtitle?: string
  tone?: 'blue'|'green'|'purple'|'red'
  badge?: string
  kind?: 'players'|'npcs'
}

const props = defineProps<{
  items: CharGridItem[]
  selectedId?: string|number|null
  loading?: boolean
  title?: string
  hasMore?: boolean
  loadingMore?: boolean
}>()
const emit = defineEmits<{ (e:'select', item:CharGridItem): void, (e:'load-more'): void }>()

const q = ref('')
const filter = ref<'players'|'npcs'>('players')
const isLoading = computed(() => !!props.loading)
const hasMore = computed(() => !!props.hasMore)
const loadingMore = computed(() => !!props.loadingMore)
const gridEl = ref<HTMLElement|null>(null)
const showLoadMore = computed(() => hasMore.value && !isLoading.value && filter.value === 'npcs')

const filteredItems = computed(() => {
  const list = props.items?.filter(i => i.kind === filter.value) ?? []
  if (!q.value.trim()) return list
  const s = q.value.toLowerCase()
  return list.filter(i => i.name.toLowerCase().includes(s))
})

function setFilter(v:'players'|'npcs') { filter.value = v }
function initials(name:string) { return name.split(' ').map(p=>p[0]).slice(0,2).join('').toUpperCase() }
function hide(ev: Event) { const el = ev.target as HTMLElement; if (el) (el as any).style.display='none' }

onMounted(() => {
  // ensure grid scroll starts at top
  if (gridEl.value) gridEl.value.scrollTop = 0
})
</script>

<style scoped>
.cp-panel { display:flex; flex-direction:column; gap:12px; min-width:360px; max-width:520px; max-height:78vh; overflow:auto; -webkit-overflow-scrolling: touch; }
.cp-card { background:rgba(9,16,28,0.55); border:1px solid rgba(99,247,255,0.4); padding:10px; box-shadow:0 0 12px rgba(34,211,238,0.2); }
.cp-card--toolbar { position:sticky; top:0; z-index:1; backdrop-filter: blur(2px); }
.cp-toolbar { display:flex; gap:10px; align-items:center; justify-content:space-between; }
.cp-title-sm { color:#baf6ff; letter-spacing:.3em; font-size:12px; font-weight:600; }
.cp-search { flex:1; display:flex; }
.cp-input { flex:1; background:rgba(2,8,18,0.6); border:1px solid rgba(99,247,255,0.25); color:#e8fdff; padding:6px 10px; font-size:12px; }
.cp-toggle { display:flex; gap:6px; }
.cp-tab { padding:6px 8px; border:1px solid rgba(99,247,255,0.35); background:rgba(3,12,22,0.5); color:#b9faff; font-size:10px; letter-spacing:.15em; }
.cp-tab.active { background:rgba(10,170,200,0.15); color:#e8fdff; }

.cp-grid { position:relative; display:grid; grid-template-columns:repeat(2, minmax(160px, 1fr)); gap:10px; padding:2px; flex:1 1 auto; min-height:0; }
.cp-loading, .cp-empty { color:#a3f1ff; opacity:.8; padding:20px; grid-column:1 / -1; text-align:center; }

.cp-tile { text-align:left; border:1px solid rgba(99,247,255,0.35); background:rgba(6,14,24,0.55); color:#ccfcff; padding:8px; display:flex; flex-direction:column; gap:6px; cursor:pointer; box-shadow:0 0 8px rgba(34,211,238,0.18); }
.cp-tile.selected { outline:2px solid rgba(99,247,255,0.8); }
.cp-tile__head { display:flex; align-items:center; justify-content:space-between; }
.cp-tile__name { font-size:10px; letter-spacing:.18em; color:#bdf9ff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:160px; }
.cp-badge { border:1px solid currentColor; font-size:9px; padding:1px 4px; letter-spacing:.15em; }
.cp-badge[data-tone='blue']{ color:#97f0ff }
.cp-badge[data-tone='green']{ color:#9ef4c1 }
.cp-badge[data-tone='purple']{ color:#c9b3ff }
.cp-badge[data-tone='red']{ color:#ffb3c3 }
.cp-tile__art { position:relative; border:1px solid rgba(99,247,255,0.2); background:rgba(2,8,18,0.5); height:120px; display:flex; align-items:center; justify-content:center; overflow:hidden; }
.cp-tile__art img { width:100%; height:100%; object-fit:cover; display:block; opacity:0.9 }
.cp-tile__ph { color:#87eeff; letter-spacing:.2em; font-weight:600; }
.cp-tile__sub { font-size:10px; color:#9feaff; opacity:.75; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

/* Load more tile */
.cp-more { grid-column: 1 / -1; border:1px dashed rgba(99,247,255,0.35); background:rgba(6,14,24,0.35); color:#bdf9ff; padding:10px; letter-spacing:.2em; text-transform:uppercase; cursor:pointer; display:flex; align-items:center; justify-content:center; }
.cp-more[disabled] { opacity:.6; cursor:default }
.cp-spinner-sm { width:18px; height:18px; border:2px solid rgba(255,255,255,0.3); border-top:2px solid #ffffff; border-radius:50%; animation: spin 1s linear infinite; }
@keyframes spin { 0%{transform:rotate(0)} 100%{transform:rotate(360deg)} }

@media (min-width: 1280px){
  .cp-grid{ grid-template-columns:repeat(3, minmax(160px, 1fr)); }
}
</style>
