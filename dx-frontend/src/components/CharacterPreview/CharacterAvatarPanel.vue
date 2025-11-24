<template>
  <section class="cp-center">
    <div class="cp-center__frame">
      <img v-if="character?.avatar" class="cp-center__img" :src="character.avatar" :alt="character?.name" @error="onImgError"/>
      <div v-else class="cp-center__placeholder">
        <div class="cp-center__sigil">{{ initials }}</div>
      </div>
      <div class="cp-center__name">{{ character?.name || 'Unknown' }}</div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface CharPreviewItem {
  id: string | number
  name: string
  avatar?: string
}

const props = defineProps<{ character: CharPreviewItem | null }>()

const initials = computed(() => {
  if (!props.character?.name) return '??'
  return props.character.name.split(' ').map(p=>p[0]).slice(0,2).join('').toUpperCase()
})

function onImgError(ev: Event) {
  const img = ev.target as HTMLImageElement
  if (img) img.style.display = 'none'
}
</script>

<style scoped>
.cp-center { display:flex; align-items:center; justify-content:center; }
.cp-center__frame { position:relative; width:min(520px, 70vw, calc(78vh * 0.75)); max-height:78vh; aspect-ratio:3/4; border:1px solid rgba(99,247,255,0.45); background:radial-gradient(ellipse at center, rgba(20,40,60,0.7), rgba(6,12,20,0.7)); box-shadow:0 0 18px rgba(34,211,238,0.25); overflow:hidden; }
.cp-center__img { width:100%; height:100%; object-fit:cover; display:block; filter:saturate(1.1) contrast(1.02); }
.cp-center__placeholder { width:100%; height:100%; display:flex; align-items:center; justify-content:center; background:linear-gradient(180deg, rgba(4,12,20,0.7), rgba(10,26,36,0.7)); }
.cp-center__sigil { font-size:56px; letter-spacing:.2em; color:#9df6ff; text-shadow:0 0 16px rgba(34,211,238,0.35); }
.cp-center__name { position:absolute; bottom:8px; left:0; right:0; text-align:center; color:#c8fbff; letter-spacing:.25em; font-weight:600; font-size:14px; background:linear-gradient(180deg, transparent, rgba(0,0,0,0.35)); padding:8px 0; }
</style>
