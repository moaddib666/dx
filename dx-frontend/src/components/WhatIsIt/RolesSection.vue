<template>
  <section class="content-section roles-section">
    <h2 class="section-title">{{ title }}</h2>
    <div class="roles-grid">
      <!-- Player Column -->
      <div class="role-column player-column">
        <h3 class="role-title">{{ player.title }}</h3>
        <p class="role-description">{{ player.description }}</p>

        <div class="role-details">
          <div class="role-detail-item">
            <h4>{{ player.characterCreation.title }}</h4>
            <div class="paths-list">
              <div class="path-item" v-for="(path, index) in player.characterCreation.paths" :key="index">
                <strong>{{ path }}</strong>
              </div>
            </div>
          </div>

          <div class="role-detail-item">
            <h4>{{ player.responsibilities }}</h4>
          </div>

          <div class="role-detail-item">
            <h4>{{ player.timeCommitment }}</h4>
          </div>

          <div class="role-detail-item">
            <h4>{{ player.gameplay }}</h4>
          </div>

          <div class="role-detail-item">
            <h4>{{ player.progression }}</h4>
          </div>
        </div>

        <div class="role-image-container">
          <img
            :src="player.image.src"
            :alt="player.image.alt"
            class="role-image zoomable-image"
            @click="$emit('toggle-zoom', $event)"
          />
        </div>
      </div>

      <!-- Game Master Column -->
      <div class="role-column gm-column">
        <h3 class="role-title">{{ gameMaster.title }}</h3>
        <p class="role-description">{{ gameMaster.description }}</p>

        <div class="role-details">
          <div class="role-detail-item">
            <h4>{{ gameMaster.responsibilities }}</h4>
          </div>

          <div class="role-detail-item">
            <h4>{{ gameMaster.digitalTools.title }}</h4>
            <ul class="tools-list">
              <li v-for="(tool, index) in gameMaster.digitalTools.tools" :key="index">{{ tool }}</li>
            </ul>
          </div>

          <div class="role-detail-item">
            <h4>{{ gameMaster.skillsDeveloped }}</h4>
          </div>

          <div class="role-detail-item">
            <h4>{{ gameMaster.timeCommitment }}</h4>
          </div>

          <div class="role-detail-item">
            <h4>{{ gameMaster.uniqueAspects }}</h4>
          </div>
        </div>

        <div class="role-image-container">
          <img
            :src="gameMaster.image.src"
            :alt="gameMaster.image.alt"
            class="role-image zoomable-image"
            @click="$emit('toggle-zoom', $event)"
          />
        </div>
      </div>
    </div>

    <!-- Game Master Tools Gallery -->
    <ImageGallery
      :items="toolsGalleryItems"
      @toggle-zoom="$emit('toggle-zoom', $event)"
      class="gm-tools-gallery"
    />
  </section>
</template>

<script setup lang="ts">
import ImageGallery from './ImageGallery.vue'

interface ImageData {
  src: string
  alt: string
  caption: string
}

interface CharacterCreation {
  title: string
  paths: string[]
}

interface DigitalTools {
  title: string
  tools: string[]
}

interface PlayerData {
  title: string
  description: string
  responsibilities: string
  timeCommitment: string
  gameplay: string
  progression: string
  characterCreation: CharacterCreation
  image: {
    src: string
    alt: string
  }
}

interface GameMasterData {
  title: string
  description: string
  responsibilities: string
  skillsDeveloped: string
  timeCommitment: string
  uniqueAspects: string
  digitalTools: DigitalTools
  image: {
    src: string
    alt: string
  }
}

defineProps<{
  title: string
  player: PlayerData
  gameMaster: GameMasterData
  toolsGalleryItems: ImageData[]
}>()

defineEmits<{
  (e: 'toggle-zoom', event: Event): void
}>()
</script>

<style scoped>
.roles-section {
  margin-top: 3rem;
}

.content-section {
  margin-bottom: 4rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.section-title {
  font-size: 2rem;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 600;
}

.roles-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  margin-bottom: 2rem;
}

.role-column {
  padding: 1.5rem;
  border-radius: 10px;
}

.player-column {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 255, 255, 0.05));
  border: 2px solid rgba(0, 255, 255, 0.4);
}

.gm-column {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 215, 0, 0.05));
  border: 2px solid rgba(255, 215, 0, 0.4);
}

.role-title {
  font-size: 1.8rem;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 1rem;
  text-align: center;
}

.role-description {
  margin-bottom: 1.5rem;
  font-size: 1rem;
  text-align: center;
}

.role-details {
  margin-bottom: 1.5rem;
}

.role-detail-item {
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.role-detail-item h4 {
  color: var(--cyber-yellow, #ffd700);
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.paths-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.5rem;
}

.path-item {
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 4px;
}

.tools-list {
  list-style: none;
  padding-left: 0.5rem;
}

.tools-list li {
  margin-bottom: 0.5rem;
  position: relative;
  padding-left: 1.5rem;
}

.tools-list li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: var(--cyber-cyan, #00ffff);
}

.role-image-container {
  text-align: center;
}

.role-image {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.gm-tools-gallery {
  margin-top: 2rem;
}

.zoomable-image {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 3px solid transparent;
  position: relative;
}

.zoomable-image::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.5), inset 0 0 15px rgba(255, 215, 0, 0.3);
  z-index: 1;
  pointer-events: none;
  animation: borderPulse 3s infinite alternate;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.zoomable-image:hover {
  transform: scale(1.03);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
}

.zoomable-image:hover::before {
  opacity: 1;
}

@keyframes borderPulse {
  0% {
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.3), inset 0 0 15px rgba(255, 215, 0, 0.2);
  }
  100% {
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.6), inset 0 0 20px rgba(255, 215, 0, 0.4);
  }
}

@media (min-width: 1024px) {
  .roles-grid {
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
  }
}

@media (max-width: 1024px) {
  .roles-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .role-title {
    font-size: 1.6rem;
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 1.5rem;
  }

  .role-title {
    font-size: 1.4rem;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1.3rem;
  }

  .role-title {
    font-size: 1.2rem;
  }

  .zoomable-image:hover {
    transform: scale(1.02);
  }
}
</style>