<script setup lang="ts">
import {computed} from 'vue'

interface StatBarProps {
  current: number
  max: number
}

const props = withDefaults(defineProps<StatBarProps>(), {})

const percentage = computed(() => (props.current / props.max) * 100)
</script>

<template>
  <div class="rpg-stat-bar">
    <div class="rpg-stat-bar__wrapper">
      <div class="rpg-stat-bar__fill" :style="{ width: percentage + '%' }">
        <span class="rpg-stat-bar__label">{{ props.current }} / {{ props.max }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rpg-stat-bar {
  height: 2.8rem;
  width: 15rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: url("@/assets/rpg_bars/halth_bar_with_border.png") no-repeat left top;
  position: relative;
  background-size: contain;
  padding: 0;
  margin: 0;
}

.rpg-stat-bar__wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  background-size: contain;
  mask: url("@/assets/rpg_bars/halth_bar_with_border_mask_invented.png") no-repeat center;
  mask-size: contain;
}
.rpg-stat-bar__fill {
  background: url("@/assets/rpg_bars/health_bar_content.png") no-repeat center;
  background-size: cover;
  width: 100%;
  height: 100%;
  transition: width 0.3s ease;
  background-blend-mode: overlay;
}
.rpg-stat-bar__label {
  position: absolute;
  top: 72%;
  left: 45%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 0.7rem;
  font-weight: bold;
}
</style>