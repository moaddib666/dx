<template>
  <div class="page-container">
    <ZoomModal
      :is-visible="isZoomed"
      :image-url="currentZoomedImage"
      @close="closeZoom"
    />
    <div class="hero-background" @click="toggleZoom($event)"></div>
    <main class="cheatsheet">
      <TitleComponent>{{ t('playerCheatSheet.title') }}</TitleComponent>
      <p class="subtitle">{{ t('playerCheatSheet.subtitle') }}</p>

      <!-- Main Content Grid -->
      <div class="content-grid">
        <!-- Turn Cycle Flow -->
        <section class="content-section">
          <h2 class="section-title">{{ t('playerCheatSheet.turnCycleFlow.title') }}</h2>
          <div class="turn-cycle">
            <div class="step-item">
              <div class="step-number">1</div>
              <div class="step-content">
                <h3>{{ t('playerCheatSheet.turnCycleFlow.steps.step1.title') }}</h3>
                <p>{{ t('playerCheatSheet.turnCycleFlow.steps.step1.description') }}</p>
              </div>
            </div>
            <div class="step-item">
              <div class="step-number">2</div>
              <div class="step-content">
                <h3>{{ t('playerCheatSheet.turnCycleFlow.steps.step2.title') }}</h3>
                <p>{{ t('playerCheatSheet.turnCycleFlow.steps.step2.description') }}</p>
              </div>
            </div>
            <div class="step-item">
              <div class="step-number">3</div>
              <div class="step-content">
                <h3>{{ t('playerCheatSheet.turnCycleFlow.steps.step3.title') }}</h3>
                <p>{{ t('playerCheatSheet.turnCycleFlow.steps.step3.description') }}</p>
              </div>
            </div>
            <div class="step-item">
              <div class="step-number">4</div>
              <div class="step-content">
                <h3>{{ t('playerCheatSheet.turnCycleFlow.steps.step4.title') }}</h3>
                <p>{{ t('playerCheatSheet.turnCycleFlow.steps.step4.description') }}</p>
              </div>
            </div>
            <div class="step-item">
              <div class="step-number">5</div>
              <div class="step-content">
                <h3>{{ t('playerCheatSheet.turnCycleFlow.steps.step5.title') }}</h3>
                <p>{{ t('playerCheatSheet.turnCycleFlow.steps.step5.description') }}</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Action Types -->
        <section class="content-section">
          <h2 class="section-title">{{ t('playerCheatSheet.actionTypes.title') }}</h2>
          <div class="action-types">
            <div class="action-card immediate">
              <h3>{{ t('playerCheatSheet.actionTypes.immediate.title') }}</h3>
              <p>{{ t('playerCheatSheet.actionTypes.immediate.description') }}</p>
              <div class="action-examples">
                <span v-for="(example, index) in immediateExamples" :key="index" class="action-pill">{{ example }}</span>
              </div>
            </div>
            <div class="action-card scheduled">
              <h3>{{ t('playerCheatSheet.actionTypes.scheduled.title') }}</h3>
              <p>{{ t('playerCheatSheet.actionTypes.scheduled.description') }}</p>
              <div class="action-examples">
                <span v-for="(example, index) in scheduledExamples" :key="index" class="action-pill">{{ example }}</span>
              </div>
            </div>
            <div class="action-card finite">
              <h3>{{ t('playerCheatSheet.actionTypes.finite.title') }}</h3>
              <p>{{ t('playerCheatSheet.actionTypes.finite.description') }}</p>
              <div class="action-examples">
                <span v-for="(example, index) in finiteExamples" :key="index" class="action-pill">{{ example }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Resource Management -->
        <section class="content-section">
          <h2 class="section-title">{{ t('playerCheatSheet.resourceManagement.title') }}</h2>
          <div class="resources">
            <div class="resource-item">
              <h3>{{ t('playerCheatSheet.resourceManagement.actionPoints.title') }}</h3>
              <div class="progress-container">
                <div class="progress-bar ap-bar">
                  <div class="progress-fill" style="width: 70%"></div>
                </div>
              </div>
              <p class="resource-formula">{{ t('playerCheatSheet.resourceManagement.actionPoints.description') }}</p>
            </div>
            <div class="resource-item">
              <h3>{{ t('playerCheatSheet.resourceManagement.energyFlow.title') }}</h3>
              <div class="progress-container">
                <div class="progress-bar energy-bar">
                  <div class="progress-fill" style="width: 50%"></div>
                </div>
              </div>
              <p class="resource-formula">{{ t('playerCheatSheet.resourceManagement.energyFlow.description') }}</p>
            </div>
            <div class="resource-item">
              <h3>{{ t('playerCheatSheet.resourceManagement.healthPoints.title') }}</h3>
              <div class="progress-container">
                <div class="progress-bar hp-bar">
                  <div class="progress-fill" style="width: 85%"></div>
                </div>
              </div>
              <p class="resource-formula">{{ t('playerCheatSheet.resourceManagement.healthPoints.description') }}</p>
            </div>
          </div>
        </section>

        <!-- Player-GM Interaction -->
        <section class="content-section">
          <h2 class="section-title">{{ t('playerCheatSheet.playerGMInteraction.title') }}</h2>
          <div class="interaction-flow">
            <div class="interaction-step">
              <div class="interaction-number">1</div>
              <div class="interaction-content">
                <h3>{{ t('playerCheatSheet.playerGMInteraction.steps.step1.title') }}</h3>
                <p>{{ t('playerCheatSheet.playerGMInteraction.steps.step1.description') }}</p>
              </div>
            </div>
            <div class="interaction-arrow">→</div>
            <div class="interaction-step">
              <div class="interaction-number">2</div>
              <div class="interaction-content">
                <h3>{{ t('playerCheatSheet.playerGMInteraction.steps.step2.title') }}</h3>
                <p>{{ t('playerCheatSheet.playerGMInteraction.steps.step2.description') }}</p>
              </div>
            </div>
            <div class="interaction-arrow">→</div>
            <div class="interaction-step">
              <div class="interaction-number">3</div>
              <div class="interaction-content">
                <h3>{{ t('playerCheatSheet.playerGMInteraction.steps.step3.title') }}</h3>
                <p>{{ t('playerCheatSheet.playerGMInteraction.steps.step3.description') }}</p>
              </div>
            </div>
            <div class="interaction-arrow">→</div>
            <div class="interaction-step">
              <div class="interaction-number">4</div>
              <div class="interaction-content">
                <h3>{{ t('playerCheatSheet.playerGMInteraction.steps.step4.title') }}</h3>
                <p>{{ t('playerCheatSheet.playerGMInteraction.steps.step4.description') }}</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Quick Actions -->
        <section class="content-section">
          <h2 class="section-title">{{ t('playerCheatSheet.quickActions.title') }}</h2>
          <div class="quick-actions-grid">
            <div class="quick-action">{{ t('playerCheatSheet.quickActions.actions.move') }}</div>
            <div class="quick-action">{{ t('playerCheatSheet.quickActions.actions.attack') }}</div>
            <div class="quick-action">{{ t('playerCheatSheet.quickActions.actions.defend') }}</div>
            <div class="quick-action">{{ t('playerCheatSheet.quickActions.actions.castSpell') }}</div>
            <div class="quick-action">{{ t('playerCheatSheet.quickActions.actions.useItem') }}</div>
            <div class="quick-action">{{ t('playerCheatSheet.quickActions.actions.inspect') }}</div>
            <div class="quick-action">{{ t('playerCheatSheet.quickActions.actions.communicate') }}</div>
            <div class="quick-action">{{ t('playerCheatSheet.quickActions.actions.teleport') }}</div>
          </div>
        </section>

        <!-- Key Rules -->
        <section class="content-section">
          <h2 class="section-title">{{ t('playerCheatSheet.keyRules.title') }}</h2>
          <div class="key-rules">
            <div class="rule-item">
              <div class="rule-marker"></div>
              <p>{{ t('playerCheatSheet.keyRules.rules.rule1') }}</p>
            </div>
            <div class="rule-item">
              <div class="rule-marker"></div>
              <p>{{ t('playerCheatSheet.keyRules.rules.rule2') }}</p>
            </div>
            <div class="rule-item">
              <div class="rule-marker"></div>
              <p>{{ t('playerCheatSheet.keyRules.rules.rule3') }}</p>
            </div>
            <div class="rule-item">
              <div class="rule-marker"></div>
              <p>{{ t('playerCheatSheet.keyRules.rules.rule4') }}</p>
            </div>
          </div>
        </section>
      </div>

      <!-- Footer -->
      <div class="footer-section">
        <p>{{ t('playerCheatSheet.footer.readyToBegin') }}</p>
        <a href="https://discord.gg/vC3TvVzK" target="_blank" class="discord-link">
          {{ t('playerCheatSheet.footer.joinDiscord') }}
        </a>
        <div class="additional-links">
          <router-link to="/faq/newcomers-guide" class="additional-link">{{ t('playerCheatSheet.footer.newcomersGuide') }}</router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import TitleComponent from '@/components/TitleComponent.vue';
import { useI18n } from 'vue-i18n';
import ZoomModal from '@/components/WhatIsIt/ZoomModal.vue';

export default {
  name: 'PlayerCheatSheet',
  components: {
    TitleComponent,
    ZoomModal
  },
  setup() {
    const { t } = useI18n();
    return { t };
  },
  data() {
    return {
      isZoomed: false,
      currentZoomedImage: ''
    };
  },
  computed: {
    zoomedImageStyle() {
      return {
        backgroundImage: `url(${this.currentZoomedImage})`
      };
    },
    immediateExamples() {
      return [this.t('playerCheatSheet.actionTypes.immediate.examples.0'), this.t('playerCheatSheet.actionTypes.immediate.examples.1')];
    },
    scheduledExamples() {
      return [this.t('playerCheatSheet.actionTypes.scheduled.examples.0'), this.t('playerCheatSheet.actionTypes.scheduled.examples.1'), this.t('playerCheatSheet.actionTypes.scheduled.examples.2')];
    },
    finiteExamples() {
      return [this.t('playerCheatSheet.actionTypes.finite.examples.0')];
    }
  },
  methods: {
    toggleZoom(event) {
      // Get the image element from the event
      const imgElement = event.target.tagName === 'IMG' ? event.target : event.target.querySelector('img');

      if (imgElement) {
        // Use the actual resolved src from the DOM
        this.currentZoomedImage = imgElement.src;
      } else if (event.target.classList.contains('hero-background')) {
        // Special case for hero background which is a fixed background
        // Get computed style to extract the actual URL
        const style = getComputedStyle(event.target);
        const bgImage = style.backgroundImage;
        // Extract URL from the "url('...')" format
        const url = bgImage.replace(/^url\(['"]?/, '').replace(/['"]?\)$/, '');
        this.currentZoomedImage = url;
      }

      this.isZoomed = !this.isZoomed;
    },
    closeZoom() {
      if (this.isZoomed) {
        this.isZoomed = false;
      }
    }
  }
};
</script>

<style scoped>
.cheatsheet {
  padding: 60px;
  color: white;
  position: relative;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(1px);
  margin-top: 60px;
}

.subtitle {
  font-size: 1.2rem;
  color: var(--light-steel-blue, #b0c4de);
  font-style: italic;
  text-align: center;
  margin-bottom: 2rem;
}

.print-hint {
  display: inline-block;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--cyber-yellow, #ffd700);
}

/* Hero Background */
.page-container {
  position: relative;
  min-height: 100vh;
}

.hero-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/images/faq/faq-hero-2.1-section.png');
  background-size: cover;
  background-position: center 10%;
  background-attachment: fixed;
  z-index: -1;
}

.hero-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7));
}

/* Animation Keyframes */

@keyframes zoomIn {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* Main Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.75rem;
  margin-top: 1.5rem;
}

/* Content Sections */
.content-section {
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.section-title {
  font-size: 1.3rem;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 0.75rem;
  text-align: center;
  font-weight: 600;
}

/* Turn Cycle Flow */
.turn-cycle {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border-left: 4px solid var(--cyber-yellow, #ffd700);
}

.step-number {
  width: 30px;
  height: 30px;
  background: var(--cyber-yellow, #ffd700);
  color: #000;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content h3 {
  font-size: 1.1rem;
  color: white;
  margin-bottom: 0.25rem;
}

.step-content p {
  font-size: 0.9rem;
  color: var(--light-steel-blue, #b0c4de);
}

/* Action Types */
.action-types {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.5rem;
}

.action-card {
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  text-align: center;
}

.action-card.immediate {
  border-left: 4px solid #4CAF50;
}

.action-card.scheduled {
  border-left: 4px solid #FF9800;
}

.action-card.finite {
  border-left: 4px solid #2196F3;
}

.action-card h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.action-card.immediate h3 {
  color: #4CAF50;
}

.action-card.scheduled h3 {
  color: #FF9800;
}

.action-card.finite h3 {
  color: #2196F3;
}

.action-card p {
  font-size: 0.9rem;
  color: var(--light-steel-blue, #b0c4de);
  margin-bottom: 1rem;
}

.action-examples {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.action-pill {
  padding: 0.25rem 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  font-size: 0.8rem;
  color: white;
}

/* Resource Management */
.resources {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

.resource-item {
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.resource-item h3 {
  font-size: 1.1rem;
  color: white;
  margin-bottom: 0.75rem;
  text-align: center;
}

.progress-container {
  margin-bottom: 0.75rem;
}

.progress-bar {
  height: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 10px;
}

.ap-bar .progress-fill {
  background: linear-gradient(90deg, #4CAF50, #2E7D32);
}

.energy-bar .progress-fill {
  background: linear-gradient(90deg, #00bfff, #1e90ff);
}

.hp-bar .progress-fill {
  background: linear-gradient(90deg, #ff4500, #8b0000);
}

.resource-formula {
  text-align: center;
  font-size: 0.9rem;
  color: var(--light-steel-blue, #b0c4de);
  font-style: italic;
}

/* Player-GM Interaction */
.interaction-flow {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.interaction-step {
  flex: 1;
  min-width: 130px;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  text-align: center;
}

.interaction-number {
  width: 30px;
  height: 30px;
  background: var(--cyber-yellow, #ffd700);
  color: #000;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin: 0 auto 0.5rem;
}

.interaction-content h3 {
  font-size: 1rem;
  color: white;
  margin-bottom: 0.25rem;
}

.interaction-content p {
  font-size: 0.85rem;
  color: var(--light-steel-blue, #b0c4de);
}

.interaction-arrow {
  font-size: 1.5rem;
  color: var(--cyber-yellow, #ffd700);
  margin: 0 0.25rem;
}

/* Dimension Effects */
.dimensions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.dimension-card {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  text-align: center;
}

.dimension-card h3 {
  font-size: 1.1rem;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 0.5rem;
}

.dimension-card p {
  font-size: 0.9rem;
  color: white;
  margin-bottom: 0.75rem;
}

.dimension-effect {
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
}

.dimension-effect.positive {
  background: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
}

.dimension-effect.negative {
  background: rgba(244, 67, 54, 0.2);
  color: #F44336;
}

/* Quick Actions */
.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 0.5rem;
}

.quick-action {
  padding: 0.75rem 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 8px;
  text-align: center;
  font-size: 0.9rem;
  color: white;
  transition: all 0.3s ease;
}

.quick-action:hover {
  background: rgba(255, 215, 0, 0.1);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Key Rules */
.key-rules {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.rule-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.rule-marker {
  width: 12px;
  height: 12px;
  background: var(--action-green, #4CAF50);
  border-radius: 2px;
  flex-shrink: 0;
}

.rule-item p {
  font-size: 0.95rem;
  color: white;
}

/* Dice Modifiers */
.dice-modifiers {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.modifier-card {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.modifier-card.positive {
  border-left: 4px solid #4CAF50;
}

.modifier-card.negative {
  border-left: 4px solid #F44336;
}

.modifier-card h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.modifier-card.positive h3 {
  color: #4CAF50;
}

.modifier-card.negative h3 {
  color: #F44336;
}

.modifier-card p {
  font-size: 0.9rem;
  color: var(--light-steel-blue, #b0c4de);
  font-style: italic;
}

/* Footer */
.footer-section {
  text-align: center;
  padding: 2rem;
  margin-top: 2rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
}

.footer-section p {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: var(--light-steel-blue, #b0c4de);
}

.discord-link {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: linear-gradient(45deg, var(--cyber-yellow, #ffd700), #00ffff);
  color: #000;
  text-decoration: none;
  border-radius: 25px;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.discord-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
}

/* Additional Links */
.additional-links {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

.additional-link {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  color: var(--cyber-yellow, #ffd700);
  text-decoration: none;
  border-radius: 20px;
  font-weight: bold;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.additional-link:hover {
  background: rgba(255, 215, 0, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 215, 0, 0.3);
  color: white;
  text-decoration: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  .cheatsheet {
    padding: 30px;
    margin-top: 40px;
  }

  .hero-background {
    background-attachment: scroll; /* Fixed attachment can cause issues on mobile */
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .zoomed-image {
    width: 95%;
    height: 80%;
  }

  .dice-modifiers {
    grid-template-columns: 1fr;
  }

  .interaction-flow {
    flex-direction: column;
  }

  .interaction-arrow {
    transform: rotate(90deg);
    margin: 0.5rem 0;
  }

  .interaction-step {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .cheatsheet {
    padding: 20px;
    margin-top: 30px;
  }

  .subtitle {
    font-size: 1rem;
  }

  .print-hint {
    font-size: 0.8rem;
  }

  .content-section {
    padding: 1rem;
  }

  .section-title {
    font-size: 1.3rem;
  }

  .step-item,
  .rule-item,
  .interaction-step {
    padding: 0.75rem;
  }

  .step-number,
  .interaction-number {
    width: 25px;
    height: 25px;
    font-size: 0.9rem;
  }

  .step-content h3,
  .interaction-content h3,
  .dimension-card h3,
  .resource-item h3,
  .action-card h3,
  .modifier-card h3 {
    font-size: 1rem;
  }

  .step-content p,
  .interaction-content p,
  .dimension-card p,
  .resource-formula,
  .action-card p,
  .modifier-card p,
  .rule-item p {
    font-size: 0.85rem;
  }

  .action-pill {
    font-size: 0.75rem;
    padding: 0.2rem 0.6rem;
  }

  .quick-action {
    font-size: 0.9rem;
    padding: 0.75rem 0.5rem;
  }

  .progress-bar {
    height: 15px;
  }

  .zoomed-image {
    width: 98%;
    height: 70%;
  }

  .quick-actions-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }
}

/* Print Styles */
@media print {
  .page-container {
    background: white;
  }

  .hero-background,
  .footer-section,
  .discord-link {
    display: none;
  }

  .cheatsheet {
    padding: 0.5cm;
    margin: 0;
    background: white;
    color: black;
    box-shadow: none;
    backdrop-filter: none;
  }

  .subtitle {
    color: #333;
  }

  .print-hint {
    display: none;
  }

  .content-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5cm;
  }

  .content-section {
    page-break-inside: avoid;
    background: white;
    border: 1px solid #ccc;
    box-shadow: none;
    margin-bottom: 0.5cm;
  }

  .section-title {
    color: black;
    border-bottom: 2px solid #ffd700;
    padding-bottom: 0.2cm;
  }

  .step-item,
  .rule-item,
  .interaction-step,
  .action-card,
  .dimension-card,
  .resource-item,
  .modifier-card,
  .quick-action {
    background: white;
    border: 1px solid #ddd;
    color: black;
  }

  .step-content p,
  .interaction-content p,
  .dimension-card p,
  .resource-formula,
  .action-card p,
  .modifier-card p,
  .rule-item p {
    color: #333;
  }

  .step-number,
  .interaction-number,
  .rule-marker {
    background: #ffd700;
    color: black;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  .action-card.immediate {
    border-left: 4px solid #4CAF50;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  .action-card.scheduled {
    border-left: 4px solid #FF9800;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  .action-card.finite {
    border-left: 4px solid #2196F3;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  .action-card.immediate h3 {
    color: #4CAF50;
  }

  .action-card.scheduled h3 {
    color: #FF9800;
  }

  .action-card.finite h3 {
    color: #2196F3;
  }

  .dimension-card h3,
  .resource-item h3 {
    color: black;
  }

  .dimension-effect.positive {
    background: rgba(76, 175, 80, 0.2);
    color: #4CAF50;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  .dimension-effect.negative {
    background: rgba(244, 67, 54, 0.2);
    color: #F44336;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  .progress-bar {
    border: 1px solid #ccc;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  .progress-fill {
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  .ap-bar .progress-fill {
    background: #ffd700;
  }

  .energy-bar .progress-fill {
    background: #1e90ff;
  }

  .hp-bar .progress-fill {
    background: #ff4500;
  }

  .interaction-arrow {
    color: #ffd700;
  }

  /* Ensure page breaks don't occur in the middle of important elements */
  .step-item,
  .rule-item,
  .interaction-step,
  .action-card,
  .dimension-card,
  .resource-item,
  .modifier-card {
    page-break-inside: avoid;
  }

  /* Add a note about printing at the top */
  .cheatsheet::before {
    content: "Dimension-X Player Cheat Sheet - Print Reference";
    display: block;
    text-align: center;
    font-size: 0.8rem;
    color: #666;
    margin-bottom: 0.5cm;
  }
}
</style>