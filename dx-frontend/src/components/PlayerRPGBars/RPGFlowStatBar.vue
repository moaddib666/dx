<script setup lang="ts">
import {computed} from 'vue'

interface StatBarProps {
  current: number
  max: number
}

const props = withDefaults(defineProps<StatBarProps>(), {})

const percentage = computed(() => (props.current / props.max) * 100)
//
// const barConfig = computed(() => {
//   switch ("sdasd") {
//     case 'health':
//       return {
//         backgroundImage: '/src/assets/rpg_bars/halth_bar_with_border.png',
//         fillImage: '/src/assets/rpg_bars/health_bar_content.png',
//         cssClass: 'health-bar'
//       }
//     case 'flow':
//       return {
//         backgroundImage: '/src/assets/rpg_bars/flow_bar_with_border.png',
//         fillImage: '/src/assets/rpg_bars/flow_bar_content.png',
//         label: props.label || 'FLOW',
//         cssClass: 'flow-bar'
//       }
//     case 'actionPoints':
//       return {
//         backgroundImage: '/src/assets/rpg_bars/action_points_bar_with_border.png',
//         fillImage: '/src/assets/rpg_bars/action_points_content.png',
//         label: props.label || 'AP',
//         cssClass: 'action-points-bar'
//       }
//     default:
//       return {
//         backgroundImage: '',
//         fillImage: '',
//         label: 'STAT',
//         cssClass: 'default-bar'
//       }
//   }
// })
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
  height: 2.12rem;
  width: 15rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: url("@/assets/rpg_bars/flow_bar_with_border.png") no-repeat left top;
  background-size: contain;
  position: relative;
  padding: 0;
  margin: 0;
  pointer-events: none;
}
.rpg-stat-bar__wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  background-size: contain;
  mask: url("@/assets/rpg_bars/flow_bar_with_border_mask_invented.png") no-repeat center;
  mask-size: contain;
}
.rpg-stat-bar__fill {
  background: url("@/assets/rpg_bars/flow_bar_content.png") no-repeat center;
  background-size: cover;
  width: 100%;
  height: 100%;
  transition: width 0.3s ease;
  background-blend-mode: overlay;

  box-shadow: inset 0 0 1.2rem rgb(22, 234, 255);
  border-radius: 3rem;
}
.rpg-stat-bar__label {
  position: absolute;
  top: 52%;
  left: 42%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 0.7rem;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);

}
</style>