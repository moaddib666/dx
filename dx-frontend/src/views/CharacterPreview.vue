<template>
  <HeroBackground id="background"></HeroBackground>
  <div class="character-preview">
    <!-- Background image via HeroBackground -->

    <div v-if="isLoading" class="loading-overlay">
      <div class="loader">
        <div class="spinner"></div>
        <p class="loading-text">Loading Characters...</p>
      </div>
    </div>

    <div class="cp-layout" v-if="!isLoading">
      <CharacterAvatarPanel :character="selectedCharacter" />
      <CharacterDescriptionPanel :character="selectedCharacter" />
      <CharacterSelectorGrid
        :items="gridItems"
        :selected-id="selectedCharacter?.id || null"
        :loading="gridLoading"
        :has-more="publishedHasMore"
        :loading-more="publishedLoadingMore"
        title="Preview"
        @select="onSelect"
        @load-more="onLoadMore"
      />
    </div>
  </div>

</template>

<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import HeroBackground from "@/components/WhatIsIt/HeroBackground.vue"
import CharacterDescriptionPanel from '@/components/CharacterPreview/CharacterDescriptionPanel.vue'
import CharacterAvatarPanel from '@/components/CharacterPreview/CharacterAvatarPanel.vue'
import CharacterSelectorGrid, { type CharGridItem } from '@/components/CharacterPreview/CharacterSelectorGrid.vue'
import { CharacterGameApi } from '@/api/backendService.js'
import { usePublishedCharacters } from '@/composables/usePublishedCharacters'
import store from '@/store'

interface CharacterDto {
  id: string | number
  name: string
  avatar?: string
  description?: string
  tiktok_link?: string
  youtube_link?: string
  instagram_link?: string
}

// Published characters (public)
const published = usePublishedCharacters()
const publishedItems = published.items
const publishedLoading = published.loading
const publishedHasMore = published.hasMore
const publishedLoadingMore = published.loadingMore

// We show overlay while first published page is loading
const isLoading = computed(() => publishedLoading.value)
const gridLoading = computed(() => publishedLoading.value)

const players = ref<CharGridItem[]>([])
const selectedCharacter = ref<CharacterDto|null>(null)

// Map published items -> right grid as Legendary NPCs
function asPublishedItem(x:any): CharGridItem {
  // Use small_avatar for grid display (x is already normalized PublishedCardItem)
  const gridAvatar = x.small_avatar || x.big_avatar || x.avatar
  return {
    id: x.id,
    name: x.name || 'Unknown',
    avatar: gridAvatar,
    description: x.description || '',
    subtitle: x.subtitle || '',
    tone: 'purple',
    badge: 'NPC',
    kind: 'npcs'
  }
}

const npcs = computed<CharGridItem[]>(() => (publishedItems.value || []).map(asPublishedItem))
// Show only published characters (npcs), not players
const gridItems = computed(() => npcs.value)

function asItem(x:any, kind:'players'|'npcs'): CharGridItem {
  return {
    id: x.id,
    name: x.name || x.title || 'Unknown',
    avatar: x.avatar || x.image || undefined,
    description: x.description || x.bio || x.lore || x.story || x.backstory || '',
    subtitle: x.subtitle || x.class || x.faction || '',
    tone: kind === 'npcs' ? 'purple' : 'blue',
    badge: kind === 'npcs' ? 'NPC' : 'PC',
    kind
  }
}

function toDto(x:any): CharacterDto { return { id: x.id, name: x.name || 'Unknown', avatar: x.avatar, description: x.description } }

function selectFirst() {
  if (selectedCharacter.value) return
  const first = gridItems.value[0]
  if (first) {
    // Find the normalized data to get social media links and big_avatar for preview
    const data = publishedItems.value?.find((x: any) => x.id === first.id)
    const previewAvatar = data?.big_avatar || data?.small_avatar || data?.avatar
    selectedCharacter.value = {
      id: first.id,
      name: first.name,
      avatar: previewAvatar,
      description: first.description || '',
      tiktok_link: data?.tiktok_link,
      youtube_link: data?.youtube_link,
      instagram_link: data?.instagram_link
    }
  }
}

function onSelect(item: CharGridItem) {
  // Find the normalized data to get social media links and big_avatar for preview
  const data = publishedItems.value?.find((x: any) => x.id === item.id)
  const previewAvatar = data?.big_avatar || data?.small_avatar || data?.avatar
  selectedCharacter.value = {
    id: item.id,
    name: item.name,
    avatar: previewAvatar,
    description: item.description || '',
    tiktok_link: data?.tiktok_link,
    youtube_link: data?.youtube_link,
    instagram_link: data?.instagram_link
  }
}

async function loadData() {
  // Kick off published characters first page
  published.init({ pageSize: 24 })

  // Player characters (requires auth; skip silently if not logged in)
  try {
    const authed = store?.getters?.isAuthenticated
    if (authed) {
      const pcResp = await CharacterGameApi.characterPlayerList(false)
      players.value = (pcResp?.data || []).map((x:any) => asItem(x,'players'))
    } else {
      players.value = []
    }
  } catch (e) {
    players.value = []
  }
}

function onLoadMore() {
  if (!publishedLoadingMore.value) published.fetchNextPage()
}

onMounted(() => { loadData() })

// Select first available after any data arrives
watch([publishedItems, players], () => { selectFirst() })
</script>

<style scoped>
.character-preview { position:relative; width:100%; height:100vh; overflow:hidden; }
.cp-layout {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  padding: 1rem;
}

/* Ensure the background component uses the CharactersPreviewPublic image */
#background {
  background-image: url('@/assets/images/backgrounds/CharactersPreviewPublic.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* Reuse loader visuals from world-map preview */
.loading-overlay { position:absolute; inset:0; background:rgba(0,0,0,0.7); display:flex; justify-content:center; align-items:center; z-index:5; }
.loader { text-align:center; color:#fff }
.spinner { width:50px; height:50px; border:4px solid rgba(255,255,255,0.3); border-top:4px solid #ffffff; border-radius:50%; animation: spin 1s linear infinite; margin:0 auto 20px; }
@keyframes spin { 0%{transform:rotate(0)} 100%{transform:rotate(360deg)} }
.loading-text { font-size:18px; font-weight:500; margin:0; opacity:0.9; }

</style>
