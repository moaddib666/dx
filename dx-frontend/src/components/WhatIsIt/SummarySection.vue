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
  background: linear-gradient(135deg, rgba(99, 247, 255, 0.08), rgba(34, 211, 238, 0.05));
  border: 1px solid rgba(99, 247, 255, 0.3);
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

.subsection-title {
  font-size: 1.5rem;
  color: #bdf9ff;
  margin-bottom: 1rem;
  font-weight: 600;
  letter-spacing: 0.15em;
}

.summary-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.summary-block {
  padding: 1rem;
  background: rgba(10, 18, 32, 0.5);
  border-radius: 10px;
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.feature-item {
  padding: 0.75rem;
  background: rgba(6, 14, 24, 0.55);
  border-radius: 8px;
  text-align: center;
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.getting-started-steps {
  counter-reset: step-counter;
  list-style: none;
  padding: 0;
}

.getting-started-steps li {
  counter-increment: step-counter;
  margin-bottom: 0.75rem;
  padding: 0.75rem;
  background: rgba(10, 18, 32, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(99, 247, 255, 0.3);
  position: relative;
  padding-left: 2.5rem;
}

.getting-started-steps li::before {
  content: counter(step-counter);
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(99, 247, 255, 0.8);
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
  color: #bdf9ff;
  margin-bottom: 1rem;
  letter-spacing: 0.1em;
}

.requirements-list {
  list-style: none;
  padding: 0;
}

.requirements-list li {
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: rgba(10, 18, 32, 0.6);
  border-radius: 6px;
  border: 1px solid rgba(99, 247, 255, 0.3);
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
  background: rgba(10, 18, 32, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  border: none;
}

.world-subtitle {
  color: #bdf9ff;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  letter-spacing: 0.1em;
}

.world-description {
  margin-bottom: 0.75rem;
  font-size: 1.1rem;
  line-height: 1.6;
  color: #9feaff;
  opacity: 0.95;
}

.world-paths {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.world-path {
  background: rgba(6, 14, 24, 0.3);
  border-radius: 6px;
  padding: 0.5rem;
  border: none;
}

.key-players {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.key-player {
  background: rgba(6, 14, 24, 0.3);
  border-radius: 6px;
  padding: 0.5rem;
  border: none;
}

.world-conclusion {
  margin-top: 0.75rem;
  font-size: 1.1rem;
  font-style: italic;
  color: #bdf9ff;
  text-align: center;
  padding: 0.5rem;
  background: rgba(10, 18, 32, 0.4);
  border-radius: 8px;
  border: none;
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
  border: 1px solid rgba(99, 247, 255, 0.3);
  position: relative;
}

.zoomable-image:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.3);
  border-color: rgba(99, 247, 255, 0.5);
}

.image-caption {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #9feaff;
  font-style: italic;
  opacity: 0.9;
}

@media (max-width: 1024px) {
  .content-section {
    padding: 1.5rem;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .subsection-title {
    font-size: 1.4rem;
  }

  .summary-block {
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

  .subsection-title {
    font-size: 1.3rem;
    letter-spacing: 0.1em;
  }

  .summary-content {
    gap: 1.25rem;
  }

  .summary-block {
    padding: 1rem;
  }

  .requirements-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .world-description {
    font-size: 1rem;
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

  .subsection-title {
    font-size: 1.1rem;
    letter-spacing: 0.08em;
  }

  .summary-content {
    gap: 1rem;
  }

  .summary-block {
    padding: 0.75rem;
  }

  .feature-item {
    padding: 0.75rem;
    font-size: 0.9rem;
  }

  .getting-started-steps li {
    padding-left: 2rem;
    padding-right: 0.75rem;
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
    font-size: 0.9rem;
    margin-bottom: 0.75rem;
  }

  .getting-started-steps li::before {
    width: 20px;
    height: 20px;
    font-size: 0.8rem;
    left: 0.5rem;
  }

  .requirements-list li {
    padding: 0.6rem;
    font-size: 0.9rem;
    margin-bottom: 0.6rem;
  }

  .requirements-column h4 {
    font-size: 1rem;
  }

  .world-section {
    padding: 0.75rem;
  }

  .world-subtitle {
    font-size: 1.1rem;
  }

  .world-description {
    font-size: 0.95rem;
  }

  .world-path,
  .key-player {
    padding: 0.6rem;
    font-size: 0.9rem;
  }

  .world-conclusion {
    font-size: 1rem;
    padding: 0.6rem;
  }

  .zoomable-image:hover {
    transform: scale(1.02);
  }
}
</style>