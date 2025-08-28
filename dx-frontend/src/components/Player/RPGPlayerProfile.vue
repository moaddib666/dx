<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import RPGContainer from "@/components/RPGContainer/RPGContainer.vue"
import RPGStats from "@/components/RPGStats/RPGStats.vue"
import { CharacterGameApi } from "@/api/backendService.js"

interface Player {
  id: string
  name: string
  biography: {
    avatar?: string
  }
  path: {
    id: string
    name: string
    description: string
    icon: string
  }
  rank: {
    name: string
    level: number
  }
  experience: number
  tags: string[]
}

interface Stat {
  id: string
  name: string
  dice_rolls: any[]
  additional_value: number
  base_value?: number
}

interface Props {
  isOpen?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isOpen: false
})

const emit = defineEmits<{
  close: []
  upgradeStat: [statId: string]
}>()

const loading = ref(true)
const playerInfo = ref<Player | null>(null)
const playerStats = ref<Stat[]>([])
const upgradePoints = ref(5) // Example starting upgrade points

const isModalOpen = computed(() => props.isOpen)

const handleClose = () => {
  emit('close')
}

const handleUpgradeStat = (statId: string) => {
  const stat = playerStats.value.find(s => s.id === statId)
  if (stat && upgradePoints.value > 0) {
    stat.additional_value++
    upgradePoints.value--
    emit('upgradeStat', statId)
  }
}

const syncPlayerData = async () => {
  try {
    loading.value = true

    // Fetch player info
    const playerResponse = await CharacterGameApi.characterPlayerCharacterDetailsRetrieve()
    playerInfo.value = playerResponse.data

    // Fetch player stats
    const statsResponse = await CharacterGameApi.characterStatsList()
    playerStats.value = statsResponse.data

  } catch (error) {
    console.error("Failed to fetch player data:", error)
    // Fallback mock data for development
    playerInfo.value = {
      id: "player-1",
      name: "Adventurer",
      biography: {
        avatar: "/src/assets/images/avatar/placeholder.webp"
      },
      path: {
        id: "path-1",
        name: "Warrior",
        description: "A brave warrior on the path of strength",
        icon: "/src/assets/images/paths/warrior.webp"
      },
      rank: {
        name: "Novice",
        level: 1
      },
      experience: 150,
      tags: ["Brave", "Strong"]
    }

    playerStats.value = [
      { id: "str", name: "Strength", dice_rolls: [], additional_value: 2, base_value: 10 },
      { id: "dex", name: "Dexterity", dice_rolls: [], additional_value: 1, base_value: 8 },
      { id: "int", name: "Intelligence", dice_rolls: [], additional_value: 0, base_value: 12 },
      { id: "wis", name: "Wisdom", dice_rolls: [], additional_value: 1, base_value: 9 },
      { id: "con", name: "Constitution", dice_rolls: [], additional_value: 3, base_value: 11 },
      { id: "cha", name: "Charisma", dice_rolls: [], additional_value: 0, base_value: 7 }
    ]
  } finally {
    loading.value = false
  }
}

// Watch for modal opening to fetch data
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    syncPlayerData()
  }
}, { immediate: true })
</script>

<template>
  <div v-if="isModalOpen" class="modal-overlay" @click.self="handleClose">
    <RPGContainer class="player-profile-modal">
      <div class="modal-header">
        <div class="header-top">
          <h2 class="modal-title">Player Profile</h2>
          <button @click="handleClose" class="close-btn" title="Close Player Profile">
            ×
          </button>
        </div>
      </div>

      <div class="modal-content" v-if="!loading && playerInfo">
        <!-- Player Info Section -->
        <div class="player-info-section">
          <div class="avatar-container">
            <img
              v-if="playerInfo.biography.avatar"
              :src="playerInfo.biography.avatar"
              alt="Player Avatar"
              class="player-avatar"
            />
            <img
              v-else
              src="@/assets/images/avatar/placeholder.webp"
              alt="Player Avatar"
              class="player-avatar"
            />

            <div class="path-overlay" :title="`${playerInfo.path.name}: ${playerInfo.path.description}`">
              <img :src="playerInfo.path.icon" alt="Path Icon" class="path-icon"/>
            </div>
          </div>

          <div class="player-details">
            <h3 class="player-name">{{ playerInfo.name }}</h3>
            <div class="player-meta">
              <div class="rank-info">
                <span class="rank-label">Rank:</span>
                <span class="rank-value">{{ playerInfo.rank.name }} (Level {{ playerInfo.rank.level }})</span>
              </div>
              <div class="experience-info">
                <span class="exp-label">Experience:</span>
                <span class="exp-value">{{ playerInfo.experience }} XP</span>
              </div>
            </div>

            <div class="player-tags" v-if="playerInfo.tags && playerInfo.tags.length > 0">
              <span class="tag" v-for="tag in playerInfo.tags" :key="tag">{{ tag }}</span>
            </div>
          </div>
        </div>

        <!-- Stats Section -->
        <div class="stats-section">
          <RPGStats
            :stats="playerStats"
            title="Character Statistics"
            :show-upgrades="true"
            :available-upgrade-points="upgradePoints"
            @upgrade-stat="handleUpgradeStat"
          />
        </div>
      </div>

      <div class="loading-content" v-else-if="loading">
        <div class="loading-spinner"></div>
        <p class="loading-text">Loading player data...</p>
      </div>
    </RPGContainer>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.player-profile-modal {
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  flex-shrink: 0;
  margin-bottom: 1rem;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.modal-title {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  flex: 1;
  text-align: center;
}

.close-btn {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.4);
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  line-height: 1;
}

.close-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  transform: translateY(-50%) scale(1.1);
  color: #7fff16;
}

.modal-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  flex: 1;
}

.player-info-section {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(127, 255, 22, 0.2);
  border-radius: 0.5rem;
}

.avatar-container {
  position: relative;
  flex-shrink: 0;
}

.player-avatar {
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(127, 255, 22, 0.3);
}

.path-overlay {
  position: absolute;
  bottom: -0.2rem;
  right: -0.2rem;
  width: 1.5rem;
  height: 1.5rem;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 2px solid rgba(127, 255, 22, 0.3);
}

.path-icon {
  width: 1.2rem;
  height: 1.2rem;
  object-fit: cover;
  border-radius: 50%;
}

.player-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.player-name {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
}

.player-meta {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
}

.rank-info,
.experience-info {
  display: flex;
  gap: 0.5rem;
}

.rank-label,
.exp-label {
  color: rgba(250, 218, 149, 0.7);
}

.rank-value,
.exp-value {
  color: #fada95;
  font-weight: 600;
}

.player-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  margin-top: 0.5rem;
}

.tag {
  background: rgba(127, 255, 22, 0.1);
  color: #7fff16;
  padding: 0.2rem 0.5rem;
  border-radius: 0.3rem;
  font-size: 0.75rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  border: 1px solid rgba(127, 255, 22, 0.3);
}

.stats-section {
  flex: 1;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
}

.loading-spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid rgba(127, 255, 22, 0.3);
  border-top: 3px solid #7fff16;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin: 0;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  color: #fada95;
  font-size: 0.875rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .player-info-section {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .player-meta {
    align-items: center;
  }

  .rank-info,
  .experience-info {
    justify-content: center;
  }
}
</style>