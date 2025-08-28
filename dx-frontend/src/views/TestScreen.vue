<template>
  <div class="test-screen">
    <HeroBackground></HeroBackground>

    <!-- Player Profile Button -->
    <div class="player-controls">
      <button
        @click="openPlayerProfile"
        class="player-profile-btn"
        title="Open Player Profile"
      >
        <span class="btn-icon">👤</span>
        <span class="btn-text">Player Profile</span>
      </button>
    </div>

    <!-- Player Profile Modal -->
    <RPGPlayerProfile
      :is-open="isPlayerProfileOpen"
      @close="closePlayerProfile"
      @upgrade-stat="handleStatUpgrade"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import HeroBackground from "@/components/WhatIsIt/HeroBackground.vue"
import RPGPlayerProfile from "@/components/Player/RPGPlayerProfile.vue"

const isPlayerProfileOpen = ref(false)

const openPlayerProfile = () => {
  isPlayerProfileOpen.value = true
}

const closePlayerProfile = () => {
  isPlayerProfileOpen.value = false
}

const handleStatUpgrade = (statId: string) => {
  console.log(`Stat upgraded: ${statId}`)
  // Here you could add API calls to save the stat upgrade
}
</script>

<style scoped>
.test-screen {
  position: relative;
  width: 100%;
  height: 100vh;
}

.player-controls {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 100;
}

.player-profile-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.7rem 1rem;
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.5rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.player-profile-btn:hover {
  border-color: #7fff16;
  background: rgba(127, 255, 22, 0.1);
  color: #7fff16;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(127, 255, 22, 0.2);
}

.player-profile-btn:active {
  transform: translateY(0);
}

.btn-icon {
  font-size: 1rem;
  filter: grayscale(1) brightness(1.2);
}

.btn-text {
  white-space: nowrap;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .player-controls {
    top: 1rem;
    right: 1rem;
  }

  .player-profile-btn {
    padding: 0.5rem 0.7rem;
    font-size: 0.75rem;
  }

  .btn-text {
    display: none;
  }

  .btn-icon {
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .player-controls {
    top: 0.5rem;
    right: 0.5rem;
  }
}
</style>