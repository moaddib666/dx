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
  margin-top: 0;
}

.content-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(9, 16, 28, 0.55);
  border-radius: 12px;
  border: 1px solid rgba(99, 247, 255, 0.4);
  box-shadow: 0 0 8px rgba(34, 211, 238, 0.15);
}

.section-title {
  font-size: 2rem;
  color: #c7f5ff;
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 600;
  letter-spacing: 0.2em;
}

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.role-column {
  padding: 1rem;
  border-radius: 10px;
  max-width: 100%;
}

.player-column {
  background: linear-gradient(135deg, rgba(99, 247, 255, 0.1), rgba(34, 211, 238, 0.05));
  border: 1px solid rgba(99, 247, 255, 0.4);
}

.gm-column {
  background: linear-gradient(135deg, rgba(99, 247, 255, 0.12), rgba(34, 211, 238, 0.06));
  border: 1px solid rgba(99, 247, 255, 0.45);
}

.role-title {
  font-size: 1.8rem;
  color: #bdf9ff;
  margin-bottom: 1rem;
  text-align: center;
  letter-spacing: 0.15em;
}

.role-description {
  margin-bottom: 1rem;
  font-size: 1rem;
  text-align: center;
}

.role-details {
  margin-bottom: 1rem;
}

.role-detail-item {
  margin-bottom: 0.75rem;
  padding: 0.75rem;
  background: rgba(10, 18, 32, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.role-detail-item h4 {
  color: #bdf9ff;
  margin-top: 0;
  margin-bottom: 0.5rem;
  letter-spacing: 0.1em;
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
  color: #97f0ff;
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
  border: 1px solid rgba(99, 247, 255, 0.3);
  position: relative;
}

.zoomable-image:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.3);
  border-color: rgba(99, 247, 255, 0.5);
}

@media (max-width: 1024px) {
  .content-section {
    padding: 1.5rem;
  }

  .roles-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .role-title {
    font-size: 1.6rem;
  }

  .role-column {
    padding: 1.25rem;
  }
}

@media (max-width: 768px) {
  .content-section {
    padding: 1.25rem;
  }

  .section-title {
    font-size: 1.5rem;
    letter-spacing: 0.15em;
  }

  .role-title {
    font-size: 1.4rem;
    letter-spacing: 0.12em;
  }

  .role-description {
    font-size: 0.95rem;
  }

  .role-column {
    padding: 1rem;
  }

  .role-detail-item {
    padding: 0.65rem;
  }
}

@media (max-width: 480px) {
  .content-section {
    padding: 1rem;
    margin-bottom: 2rem;
  }

  .section-title {
    font-size: 1.3rem;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
  }

  .role-title {
    font-size: 1.2rem;
    letter-spacing: 0.1em;
  }

  .role-description {
    font-size: 0.9rem;
    margin-bottom: 1rem;
  }

  .role-column {
    padding: 0.75rem;
  }

  .role-detail-item {
    padding: 0.6rem;
    margin-bottom: 0.75rem;
  }

  .role-detail-item h4 {
    font-size: 0.9rem;
  }

  .paths-list {
    gap: 0.4rem;
  }

  .path-item {
    padding: 0.4rem;
  }

  .tools-list li {
    margin-bottom: 0.4rem;
    font-size: 0.9rem;
  }

  .zoomable-image:hover {
    transform: scale(1.02);
  }
}
</style>