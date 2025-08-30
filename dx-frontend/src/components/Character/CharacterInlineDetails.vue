<script setup lang="ts">

import {ref, computed, onMounted, watch} from 'vue'
import {CharacterInfoGameService} from "@/services/characterInfoService.js"
import {OpenaiCharacter} from "@/api/dx-backend";

const props = defineProps<{
  charId: string;
  gmMode: boolean;
}>()
const characterData = ref<OpenaiCharacter>(null);
const loading = ref(true);
const fetchInfo = async () => {
  loading.value = true;
  characterData.value = await CharacterInfoGameService.getCharacterInfo(props.charId, props.gmMode);
  loading.value = false;
};
onMounted(fetchInfo);
watch(() => props.charId, fetchInfo);
watch(() => props.gmMode, fetchInfo);

</script>

<template>
  <div class="char-info">
      <span>{{ characterData?.name  || "Unknown Character" }}</span>
  </div>
</template>

<style scoped>
.char-info {
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  text-shadow: 1px 1px 2px #000;
}
</style>