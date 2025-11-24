<template>
  <section class="cp-left">
    <header class="cp-left__header">
      <h2 class="cp-left__title">{{ character?.name || 'Unknown' }}</h2>
    </header>

    <div class="cp-left__scroll">
      <p v-if="hasLore" class="cp-lore">{{ character?.description }}</p>
      <p v-else class="cp-lore cp-lore--muted">No lore yet.</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface CharPreviewItem {
  id: string | number
  name: string
  description?: string
}

const props = defineProps<{ character: CharPreviewItem | null }>()

const hasLore = computed(() => !!props.character?.description && props.character.description.trim().length > 0)
</script>

<style scoped>
.cp-left { display:flex; flex-direction:column; min-width:300px; max-width:360px; max-height:78vh; }
.cp-left__header { padding:8px 10px; background:rgba(9,16,28,0.55); border:1px solid rgba(99,247,255,0.4); box-shadow:0 0 12px rgba(34,211,238,0.2); }
.cp-left__title { color:#c7f5ff; letter-spacing:0.3em; font-weight:600; font-size:18px; margin:0; text-transform:uppercase; }

.cp-left__scroll { flex:1; margin-top:12px; padding:12px; background:rgba(10,18,32,0.6); border:1px solid rgba(99,247,255,0.4); box-shadow:0 0 12px rgba(34,211,238,0.18); overflow-y:auto; -webkit-overflow-scrolling: touch; }

.cp-lore { color:#b7f9ff; opacity:.95; font-size:13px; line-height:1.7; margin:0; white-space:pre-wrap; overflow-wrap:anywhere; word-break:break-word; hyphens:auto; }
.cp-lore--muted { opacity:.65; font-style:italic; }
</style>
