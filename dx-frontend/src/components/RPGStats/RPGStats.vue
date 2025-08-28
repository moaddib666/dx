<script setup lang="ts">
import { ref, computed } from 'vue'
import RPGStatPresentor from './RPGStatPresentor.vue'
import SwitchBaseValuesModal from '@/components/Modal/SwitchBaseValuesModal.vue'

interface Stat {
  id: string
  name: string
  dice_rolls: any[]
  additional_value: number
  base_value?: number
}

interface Props {
  stats: Stat[]
  title?: string
  showUpgrades?: boolean
  availableUpgradePoints?: number
  allowResetBaseStats?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Character Stats',
  showUpgrades: true,
  availableUpgradePoints: 0,
  allowResetBaseStats: false
})

const emit = defineEmits<{
  upgradeStat: [statId: string]
  statUpgraded: [statId: string, newValue: number]
  switchBaseStats: [{ fromStatId: string, toStatId: string }]
}>()

const upgradePoints = ref(props.availableUpgradePoints)
const showModal = ref(false)
const preSelectedStat = ref<Stat | null>(null)

const totalStatsValue = computed(() => {
  return props.stats.reduce((total, stat) => {
    const baseValue = stat.base_value || 0
    return total + baseValue + stat.additional_value
  }, 0)
})

// Modal management methods
const requestStatSwitch = (statId: string) => {
  preSelectedStat.value = props.stats.find((stat) => stat.id === statId) || null
  openModal()
}

const openModal = () => {
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const handleSwitch = ({ fromStatId, toStatId }: { fromStatId: string, toStatId: string }) => {
  emit('switchBaseStats', { fromStatId, toStatId })
  closeModal()
}
</script>

<template>
  <div class="rpg-stats-container">
    <div class="stats-header">
      <h3 class="stats-title">{{ title }}</h3>
      <div class="stats-summary" v-if="showUpgrades">
        <div class="upgrade-points">
          <span class="points-label">Upgrade Points:</span>
          <span class="points-value">{{ upgradePoints }}</span>
        </div>
        <div class="total-stats">
          <span class="total-label">Total Stats:</span>
          <span class="total-value">{{ totalStatsValue }}</span>
        </div>
      </div>
    </div>

    <div class="stats-list">
      <RPGStatPresentor
        v-for="stat in stats"
        :key="stat.id"
        :stat="stat"
        :allowResetBaseStats="allowResetBaseStats"
        @switchBaseStats="requestStatSwitch"
        class="stat-item"
      />
    </div>

    <div class="stats-footer" v-if="showUpgrades && upgradePoints === 0">
      <p class="no-points-message">No upgrade points available</p>
    </div>

    <!-- Modal for stat swapping -->
    <SwitchBaseValuesModal
      :stats="stats"
      :isOpen="showModal && allowResetBaseStats"
      :initialFromStatId="preSelectedStat?.id"
      @switchBaseValues="handleSwitch"
      @closeModal="closeModal"
    />
  </div>
</template>

<style scoped>
.rpg-stats-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.7rem;
  padding: 1rem;
  min-height: 200px;
}

.stats-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border-bottom: 1px solid rgba(127, 255, 22, 0.2);
  padding-bottom: 0.7rem;
}

.stats-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  text-align: center;
}

.stats-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
}

.upgrade-points,
.total-stats {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.points-label,
.total-label {
  color: rgba(250, 218, 149, 0.7);
}

.points-value {
  color: #7fff16;
  font-weight: 600;
  background: rgba(127, 255, 22, 0.1);
  padding: 0.2rem 0.5rem;
  border-radius: 0.3rem;
  border: 1px solid rgba(127, 255, 22, 0.3);
}

.total-value {
  color: #fada95;
  font-weight: 600;
  background: rgba(250, 218, 149, 0.1);
  padding: 0.2rem 0.5rem;
  border-radius: 0.3rem;
  border: 1px solid rgba(250, 218, 149, 0.3);
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  flex: 1;
}

.stat-item {
  transition: transform 0.2s ease;
}

.stat-item:hover {
  transform: translateX(0.2rem);
}

.stats-footer {
  text-align: center;
  padding-top: 0.7rem;
  border-top: 1px solid rgba(127, 255, 22, 0.2);
}

.no-points-message {
  margin: 0;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  color: rgba(250, 218, 149, 0.5);
  font-style: italic;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .stats-summary {
    flex-direction: column;
    gap: 0.5rem;
    align-items: stretch;
  }

  .upgrade-points,
  .total-stats {
    justify-content: center;
  }
}
</style>