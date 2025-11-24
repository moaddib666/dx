<template>
  <section class="cp-left">
    <header class="cp-left__header">
      <h2 class="cp-left__title">{{ character?.name || 'Unknown' }}</h2>
    </header>

    <div class="cp-left__scroll">
      <p v-if="hasLore" class="cp-lore">{{ character?.description }}</p>
      <p v-else class="cp-lore cp-lore--muted">No lore yet.</p>

      <div v-if="hasSocialLinks" class="cp-social">
        <div class="cp-social__title">Social Media</div>
        <div class="cp-social__links">
          <a v-if="character?.tiktok_link" :href="character.tiktok_link" target="_blank" rel="noopener noreferrer" class="cp-social__link" title="TikTok">
            <i class="fab fa-tiktok cp-social__icon"></i>
            <span class="cp-social__label">TikTok</span>
          </a>
          <a v-if="character?.youtube_link" :href="character.youtube_link" target="_blank" rel="noopener noreferrer" class="cp-social__link" title="YouTube">
            <i class="fab fa-youtube cp-social__icon"></i>
            <span class="cp-social__label">YouTube</span>
          </a>
          <a v-if="character?.instagram_link" :href="character.instagram_link" target="_blank" rel="noopener noreferrer" class="cp-social__link" title="Instagram">
            <i class="fab fa-instagram cp-social__icon"></i>
            <span class="cp-social__label">Instagram</span>
          </a>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface CharPreviewItem {
  id: string | number
  name: string
  description?: string
  tiktok_link?: string
  youtube_link?: string
  instagram_link?: string
}

const props = defineProps<{ character: CharPreviewItem | null }>()

const hasLore = computed(() => !!props.character?.description && props.character.description.trim().length > 0)
const hasSocialLinks = computed(() => !!(props.character?.tiktok_link || props.character?.youtube_link || props.character?.instagram_link))
</script>

<style scoped>
.cp-left { display:flex; flex-direction:column; min-width:300px; max-width:360px; max-height:78vh; }
.cp-left__header { padding:8px 10px; background:rgba(9,16,28,0.55); border:1px solid rgba(99,247,255,0.4); box-shadow:0 0 12px rgba(34,211,238,0.2); }
.cp-left__title { color:#c7f5ff; letter-spacing:0.3em; font-weight:600; font-size:18px; margin:0; text-transform:uppercase; }

.cp-left__scroll { flex:1; margin-top:12px; padding:12px; background:rgba(10,18,32,0.6); border:1px solid rgba(99,247,255,0.4); box-shadow:0 0 12px rgba(34,211,238,0.18); overflow-y:auto; -webkit-overflow-scrolling: touch; }

.cp-lore { color:#b7f9ff; opacity:.95; font-size:13px; line-height:1.7; margin:0; white-space:pre-wrap; overflow-wrap:anywhere; word-break:break-word; hyphens:auto; }
.cp-lore--muted { opacity:.65; font-style:italic; }

.cp-social { margin-top:20px; padding-top:16px; border-top:1px solid rgba(99,247,255,0.25); }
.cp-social__title { color:#c7f5ff; font-size:12px; font-weight:600; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:10px; opacity:0.9; }
.cp-social__links { display:flex; flex-direction:column; gap:8px; }
.cp-social__link { display:flex; align-items:center; gap:8px; padding:8px 10px; background:rgba(9,16,28,0.4); border:1px solid rgba(99,247,255,0.3); border-radius:4px; color:#b7f9ff; text-decoration:none; font-size:13px; transition:all 0.2s ease; }
.cp-social__link:hover { background:rgba(34,211,238,0.15); border-color:rgba(99,247,255,0.6); box-shadow:0 0 8px rgba(34,211,238,0.3); transform:translateX(2px); }
.cp-social__icon { font-size:16px; line-height:1; }
.cp-social__label { flex:1; font-weight:500; }
</style>
