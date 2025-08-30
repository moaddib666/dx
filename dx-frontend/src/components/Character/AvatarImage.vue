<script setup lang="ts">

import {ref, computed, onMounted, watch} from 'vue'
import {CharacterInfoGameService} from "@/services/characterInfoService.js"
import avatarPlaceholder from "@/assets/images/avatar/placeholder.webp"

const props = defineProps<{
  charId: string;
  gmMode: boolean;
}>()
const avatarUrl = ref<string>(avatarPlaceholder);
const loading = ref(true);
const fetchAvatar = async () => {
  loading.value = true;
  avatarUrl.value = await CharacterInfoGameService.getAvatarUrl(props.charId, props.gmMode) || avatarPlaceholder;
  loading.value = false;
};
onMounted(fetchAvatar);
watch(() => props.charId, fetchAvatar);
watch(() => props.gmMode, fetchAvatar);

</script>

<template>
  <img :src="avatarUrl" alt="Character Avatar" class="char-avatar-img"/>
</template>

<style scoped>

</style>