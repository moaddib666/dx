<template>
  <div class="page-container">
    <ZoomModal
      :is-visible="isZoomed"
      :image-url="currentZoomedImage"
      @close="closeZoom"
    />
    <HeroBackground @toggle-zoom="toggleZoom" id="background"/>

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

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import TitleComponent from '@/components/TitleComponent.vue'
import HeroBackground from '@/components/WhatIsIt/HeroBackground.vue'
import ZoomModal from '@/components/WhatIsIt/ZoomModal.vue'

const { t } = useI18n()

const isZoomed = ref(false)
const currentZoomedImage = ref('')
const scrollPosition = ref(0)

const immediateExamples = computed(() => [
  t('playerCheatSheet.actionTypes.immediate.examples.0'),
  t('playerCheatSheet.actionTypes.immediate.examples.1')
])

const scheduledExamples = computed(() => [
  t('playerCheatSheet.actionTypes.scheduled.examples.0'),
  t('playerCheatSheet.actionTypes.scheduled.examples.1'),
  t('playerCheatSheet.actionTypes.scheduled.examples.2')
])

const finiteExamples = computed(() => [
  t('playerCheatSheet.actionTypes.finite.examples.0')
])

function toggleZoom(event: Event) {
  const target = event.target as HTMLElement
  const imgElement = target.tagName === 'IMG' ? target as HTMLImageElement : target.querySelector('img')

  if (imgElement) {
    currentZoomedImage.value = imgElement.src
    isZoomed.value = true
    scrollPosition.value = window.pageYOffset || document.documentElement.scrollTop
    document.body.style.overflow = 'hidden'
  } else if (target.classList.contains('hero-background')) {
    const style = getComputedStyle(target)
    const bgImage = style.backgroundImage
    const url = bgImage.replace(/^url\(['"]?/, '').replace(/['"]?\)$/, '')
    currentZoomedImage.value = url
    isZoomed.value = true
    scrollPosition.value = window.pageYOffset || document.documentElement.scrollTop
    document.body.style.overflow = 'hidden'
  }
}

function closeZoom() {
  isZoomed.value = false
  document.body.style.overflow = ''
  window.scrollTo(0, scrollPosition.value)
}
</script>

<style scoped>
.page-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
  display: flex;
  justify-content: center;
}

/* Ensure the background component uses a custom image from common directory */
#background {
  background-image: url('@/assets/images/backgrounds/common/moaddib_Desolate_corrupted_wasteland_with_twisted_terrain_jag_072aff1a-d29b-4f13-a8a6-57bab975d17b_1.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.cheatsheet {
  max-width: 1200px;
  width: 100%;
  padding: 3rem 2rem;
  color: #e0f7fa;
  position: relative;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(2px);
  margin: 0 auto;
  border-radius: 12px;
}

.subtitle {
  font-size: 1.2rem;
  line-height: 1.7;
  color: #b0e7f0;
  font-style: italic;
  text-align: center;
  margin-bottom: 2.5rem;
  margin-top: 1rem;
  font-weight: 400;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.print-hint {
  display: inline-block;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #9feaff;
  opacity: 0.9;
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
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border-left: 3px solid #22d3ee;
  transition: all 0.3s ease;
}

.content-section:hover {
  background: rgba(0, 0, 0, 0.4);
  border-left-color: #06b6d4;
  transform: translateX(4px);
}

.section-title {
  font-size: 1.5rem;
  color: #22d3ee;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 600;
  letter-spacing: 0.3px;
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
  background: rgba(10, 18, 32, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.step-number {
  width: 30px;
  height: 30px;
  background: rgba(99, 247, 255, 0.8);
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
  color: #bdf9ff;
  margin-bottom: 0.25rem;
}

.step-content p {
  font-size: 0.9rem;
  color: #9feaff;
}

/* Action Types */
.action-types {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.5rem;
}

.action-card {
  padding: 0.75rem;
  background: rgba(6, 14, 24, 0.55);
  border-radius: 8px;
  text-align: center;
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.action-card h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #bdf9ff;
}

.action-card p {
  font-size: 0.9rem;
  color: #9feaff;
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
  background: rgba(10, 18, 32, 0.6);
  border: 1px solid rgba(99, 247, 255, 0.3);
  border-radius: 15px;
  font-size: 0.8rem;
  color: #b7f9ff;
}

/* Resource Management */
.resources {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

.resource-item {
  padding: 0.75rem;
  background: rgba(10, 18, 32, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.resource-item h3 {
  font-size: 1.1rem;
  color: #bdf9ff;
  margin-bottom: 0.75rem;
  text-align: center;
}

.progress-container {
  margin-bottom: 0.75rem;
}

.progress-bar {
  height: 20px;
  background: rgba(10, 18, 32, 0.6);
  border: 1px solid rgba(99, 247, 255, 0.3);
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 10px;
  background: linear-gradient(90deg, rgba(99, 247, 255, 0.6), rgba(34, 211, 238, 0.8));
}

.resource-formula {
  text-align: center;
  font-size: 0.9rem;
  color: #9feaff;
  font-style: italic;
  opacity: 0.9;
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
  background: rgba(10, 18, 32, 0.6);
  border: 1px solid rgba(99, 247, 255, 0.3);
  border-radius: 8px;
  text-align: center;
}

.interaction-number {
  width: 30px;
  height: 30px;
  background: rgba(99, 247, 255, 0.8);
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
  color: #bdf9ff;
  margin-bottom: 0.25rem;
}

.interaction-content p {
  font-size: 0.85rem;
  color: #9feaff;
}

.interaction-arrow {
  font-size: 1.5rem;
  color: #9feaff;
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
  background: rgba(10, 18, 32, 0.6);
  border: 1px solid rgba(99, 247, 255, 0.3);
  border-radius: 8px;
  text-align: center;
}

.dimension-card h3 {
  font-size: 1.1rem;
  color: #bdf9ff;
  margin-bottom: 0.5rem;
}

.dimension-card p {
  font-size: 0.9rem;
  color: #b7f9ff;
  margin-bottom: 0.75rem;
}

.dimension-effect {
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
  background: rgba(10, 18, 32, 0.4);
  color: #9feaff;
  border: 1px solid rgba(99, 247, 255, 0.2);
}

/* Quick Actions */
.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 0.5rem;
}

.quick-action {
  padding: 0.75rem 0.5rem;
  background: rgba(10, 18, 32, 0.6);
  border: 1px solid rgba(99, 247, 255, 0.3);
  border-radius: 8px;
  text-align: center;
  font-size: 0.9rem;
  color: #b7f9ff;
  transition: all 0.3s ease;
}

.quick-action:hover {
  background: rgba(34, 211, 238, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(34, 211, 238, 0.2);
  border-color: rgba(99, 247, 255, 0.5);
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
  background: rgba(10, 18, 32, 0.6);
  border: 1px solid rgba(99, 247, 255, 0.3);
  border-radius: 8px;
}

.rule-marker {
  width: 12px;
  height: 12px;
  background: rgba(99, 247, 255, 0.8);
  border-radius: 2px;
  flex-shrink: 0;
}

.rule-item p {
  font-size: 0.95rem;
  color: #b7f9ff;
}

/* Dice Modifiers */
.dice-modifiers {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.modifier-card {
  padding: 1rem;
  background: rgba(10, 18, 32, 0.6);
  border: 1px solid rgba(99, 247, 255, 0.3);
  border-radius: 8px;
}

.modifier-card h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #bdf9ff;
}

.modifier-card p {
  font-size: 0.9rem;
  color: #9feaff;
  font-style: italic;
  opacity: 0.9;
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
  color: #9feaff;
  opacity: 0.95;
}

.discord-link {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: linear-gradient(45deg, rgba(99, 247, 255, 0.8), rgba(34, 211, 238, 0.8));
  color: #000;
  text-decoration: none;
  border-radius: 25px;
  font-weight: bold;
  transition: transform 0.3s ease;
  border: 1px solid rgba(99, 247, 255, 0.6);
}

.discord-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.4);
}

/* Additional Links */
.additional-links {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.additional-link {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background: rgba(10, 18, 32, 0.6);
  color: #bdf9ff;
  text-decoration: none;
  border-radius: 20px;
  font-weight: bold;
  transition: all 0.3s ease;
  border: 1px solid rgba(99, 247, 255, 0.4);
}

.additional-link:hover {
  background: rgba(34, 211, 238, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(34, 211, 238, 0.3);
  color: #e8fdff;
  text-decoration: none;
  border-color: rgba(99, 247, 255, 0.6);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .cheatsheet {
    max-width: 100%;
    padding: 2.5rem 1.5rem;
    padding-top: 80px;
  }

  .subtitle {
    font-size: 1.15rem;
    margin-bottom: 2rem;
  }

  .content-section {
    padding: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .section-title {
    font-size: 1.35rem;
  }
}

@media (max-width: 768px) {
  .cheatsheet {
    padding: 2rem 1.25rem;
    padding-top: 70px;
  }

  .subtitle {
    font-size: 1.1rem;
    margin-bottom: 1.75rem;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .content-section {
    padding: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .section-title {
    font-size: 1.35rem;
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

  .additional-links {
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .cheatsheet {
    padding: 1.5rem 1rem;
    padding-top: 60px;
  }

  .subtitle {
    font-size: 1.05rem;
    margin-bottom: 1.5rem;
  }

  .print-hint {
    font-size: 0.8rem;
  }

  .content-section {
    padding: 1rem;
    margin-bottom: 1.25rem;
  }

  .section-title {
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
  }

  .step-item,
  .rule-item,
  .interaction-step {
    padding: 0.6rem;
  }

  .step-number,
  .interaction-number {
    width: 25px;
    height: 25px;
    font-size: 0.85rem;
  }

  .step-content h3,
  .interaction-content h3,
  .dimension-card h3,
  .resource-item h3,
  .action-card h3,
  .modifier-card h3 {
    font-size: 0.95rem;
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
    font-size: 0.85rem;
    padding: 0.6rem 0.4rem;
  }

  .progress-bar {
    height: 15px;
  }

  .quick-actions-grid {
    grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
  }

  .discord-link {
    padding: 0.6rem 1.5rem;
    font-size: 0.9rem;
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