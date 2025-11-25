<template>
  <section class="content-section summary-section">
    <h2 class="section-title">{{ title }}</h2>

    <div class="summary-content">
      <!-- Key Features -->
      <div class="summary-block">
        <h3 class="subsection-title">{{ keyFeatures.title }}</h3>
        <div class="features-grid">
          <div class="feature-item" v-for="(feature, index) in keyFeatures.features" :key="index">
            <strong>{{ feature }}</strong>
          </div>
        </div>
      </div>

      <!-- Getting Started -->
      <div class="summary-block">
        <h3 class="subsection-title">{{ gettingStarted.title }}</h3>
        <ol class="getting-started-steps">
          <li v-for="(step, index) in gettingStarted.steps" :key="index">{{ step }}</li>
        </ol>
      </div>

      <!-- Requirements -->
      <div class="summary-block requirements-block">
        <h3 class="subsection-title">{{ requirements.title }}</h3>
        <div class="requirements-grid">
          <div class="requirements-column">
            <h4>{{ requirements.technical.title }}</h4>
            <ul class="requirements-list">
              <li v-for="(req, index) in requirements.technical.items" :key="index">{{ req }}</li>
            </ul>
          </div>
          <div class="requirements-column">
            <h4>{{ requirements.personal.title }}</h4>
            <ul class="requirements-list">
              <li v-for="(req, index) in requirements.personal.items" :key="index">{{ req }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- World Overview -->
      <div class="summary-block world-overview">
        <h3 class="subsection-title">World Overview</h3>
        <div class="world-content">
          <div class="world-section">
            <h4 class="world-subtitle">{{ worldOverview.title }}</h4>
            <p class="world-description">{{ worldOverview.description }}</p>
          </div>

          <div class="world-section">
            <h4 class="world-subtitle">{{ worldOverview.conflict.title }}</h4>
            <p class="world-description">{{ worldOverview.conflict.description }}</p>
            <div class="world-paths">
              <div class="world-path" v-for="(path, index) in worldOverview.conflict.paths" :key="index">
                <strong>{{ path.title }}</strong> - {{ path.description }}
              </div>
            </div>
          </div>

          <div class="world-section">
            <h4 class="world-subtitle">{{ worldOverview.keyPlayers.title }}</h4>
            <div class="key-players">
              <div class="key-player" v-for="(player, index) in worldOverview.keyPlayers.players" :key="index">
                <strong>{{ player.name }}</strong> - {{ player.description }}
              </div>
            </div>
          </div>

          <div class="world-section">
            <h4 class="world-subtitle">{{ worldOverview.worldToday.title }}</h4>
            <p class="world-description">{{ worldOverview.worldToday.description }}</p>
          </div>

          <div class="world-section">
            <h4 class="world-subtitle">{{ worldOverview.yourChoice.title }}</h4>
            <p class="world-description">{{ worldOverview.yourChoice.description }}</p>
            <p class="world-conclusion">{{ worldOverview.conclusion }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
interface ImageData {
  src: string
  alt: string
  caption: string
}

interface KeyFeaturesData {
  title: string
  features: string[]
}

interface GettingStartedData {
  title: string
  steps: string[]
}

interface RequirementsData {
  title: string
  technical: {
    title: string
    items: string[]
  }
  personal: {
    title: string
    items: string[]
  }
}

interface ConflictPath {
  title: string
  description: string
}

interface KeyPlayer {
  name: string
  description: string
}

interface WorldOverviewData {
  title: string
  description: string
  conflict: {
    title: string
    description: string
    paths: ConflictPath[]
  }
  keyPlayers: {
    title: string
    players: KeyPlayer[]
  }
  worldToday: {
    title: string
    description: string
  }
  yourChoice: {
    title: string
    description: string
  }
  conclusion: string
}

defineProps<{
  title: string
  keyFeatures: KeyFeaturesData
  gettingStarted: GettingStartedData
  requirements: RequirementsData
  worldOverview: WorldOverviewData
  inventoryImage: ImageData
}>()

defineEmits<{
  (e: 'toggle-zoom', event: Event): void
}>()
</script>

<style scoped>
.summary-section {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.05), rgba(0, 255, 255, 0.05));
  border: 2px solid rgba(255, 215, 0, 0.2);
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

.subsection-title {
  font-size: 1.5rem;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 1rem;
  font-weight: 600;
}

.summary-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.summary-block {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.feature-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  text-align: center;
  border-left: 3px solid var(--cyber-cyan, #00ffff);
}

.getting-started-steps {
  counter-reset: step-counter;
  list-style: none;
  padding: 0;
}

.getting-started-steps li {
  counter-increment: step-counter;
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border-left: 4px solid var(--cyber-yellow, #ffd700);
  position: relative;
  padding-left: 2.5rem;
}

.getting-started-steps li::before {
  content: counter(step-counter);
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: var(--cyber-yellow, #ffd700);
  color: #000;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
}

.requirements-block {
  margin-top: 2rem;
}

.requirements-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.requirements-column h4 {
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 1rem;
}

.requirements-list {
  list-style: none;
  padding: 0;
}

.requirements-list li {
  margin-bottom: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 6px;
  border-left: 3px solid var(--cyber-cyan, #00ffff);
}

.world-overview {
  margin-top: 2rem;
}

.world-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.world-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  padding: 1rem;
  border-left: 3px solid var(--cyber-yellow, #ffd700);
}

.world-subtitle {
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 0.75rem;
  font-size: 1.2rem;
}

.world-description {
  margin-bottom: 1rem;
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--light-steel-blue, #b0c4de);
}

.world-paths {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1rem;
}

.world-path {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  padding: 0.75rem;
  border-left: 3px solid var(--cyber-cyan, #00ffff);
}

.key-players {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.key-player {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  padding: 0.75rem;
  border-left: 3px solid var(--cyber-cyan, #00ffff);
}

.world-conclusion {
  margin-top: 1rem;
  font-size: 1.1rem;
  font-style: italic;
  color: var(--cyber-yellow, #ffd700);
  text-align: center;
  padding: 0.75rem;
  background: rgba(255, 215, 0, 0.05);
  border-radius: 8px;
}

.inventory-image-container {
  text-align: center;
}

.inventory-image {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
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

.image-caption {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--light-steel-blue, #b0c4de);
  font-style: italic;
}

@keyframes borderPulse {
  0% {
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.3), inset 0 0 15px rgba(255, 215, 0, 0.2);
  }
  100% {
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.6), inset 0 0 20px rgba(255, 215, 0, 0.4);
  }
}

@media (max-width: 768px) {
  .section-title {
    font-size: 1.5rem;
  }

  .subsection-title {
    font-size: 1.3rem;
  }

  .requirements-grid {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1.3rem;
  }

  .subsection-title {
    font-size: 1.1rem;
  }

  .getting-started-steps li {
    padding-left: 2rem;
  }

  .getting-started-steps li::before {
    width: 20px;
    height: 20px;
    font-size: 0.8rem;
    left: 0.5rem;
  }

  .zoomable-image:hover {
    transform: scale(1.02);
  }
}
</style>