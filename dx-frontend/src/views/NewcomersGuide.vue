<template>
  <div class="page-container">
    <ZoomModal
      :is-visible="isZoomed"
      :image-url="currentZoomedImage"
      @close="closeZoom"
    />
    <HeroBackground id="background" @toggle-zoom="toggleZoom" />

    <main class="newcomers-guide">
      <TitleComponent>{{ t('newcomersGuide.title') }}</TitleComponent>
      <p class="subtitle">{{ t('newcomersGuide.subtitle') }}</p>

      <!-- How To Start -->
      <section class="content-section">
        <h2 class="section-title">{{ t('newcomersGuide.howToStart.title') }}</h2>
        <div class="content-grid">
          <div class="text-content">
            <ol class="step-list">
              <li v-html="t('newcomersGuide.howToStart.steps.step1')"></li>
              <li>{{ t('newcomersGuide.howToStart.steps.step2') }}</li>
              <li>{{ t('newcomersGuide.howToStart.steps.step3') }}</li>
              <li>{{ t('newcomersGuide.howToStart.steps.step4') }}</li>
              <li>{{ t('newcomersGuide.howToStart.steps.step5') }}</li>
            </ol>
          </div>
          <div class="image-content">
            <img
                src="@/assets/images/faq/faq-creation-path.png"
                alt="Character creation interface"
                class="section-image zoomable-image"
                @click="toggleZoom($event)"
            />
            <p class="image-caption">{{ t('newcomersGuide.howToStart.imageCaption') }}</p>
          </div>
        </div>
      </section>

      <!-- How To Play (For Player) -->
      <section class="content-section">
        <h2 class="section-title">{{ t('newcomersGuide.howToPlay.title') }}</h2>
        <div class="content-grid">
          <div class="image-content">
            <img
                src="@/assets/images/faq/faq-gameplay-example.png"
                alt="Game interface showing combat and character stats"
                class="section-image zoomable-image"
                @click="toggleZoom($event)"
            />
            <p class="image-caption">{{ t('newcomersGuide.howToPlay.imageCaption') }}</p>
          </div>
          <div class="text-content">
            <ul class="info-list">
              <li>{{ t('newcomersGuide.howToPlay.infoList.item1') }}</li>
              <li>{{ t('newcomersGuide.howToPlay.infoList.item2') }}</li>
              <li>{{ t('newcomersGuide.howToPlay.infoList.item3') }}</li>
              <li>{{ t('newcomersGuide.howToPlay.infoList.item4') }}</li>
              <li>{{ t('newcomersGuide.howToPlay.infoList.item5') }}</li>
              <li>{{ t('newcomersGuide.howToPlay.infoList.item6') }}</li>
              <li>{{ t('newcomersGuide.howToPlay.infoList.item7') }}</li>
              <li>{{ t('newcomersGuide.howToPlay.infoList.item8') }}</li>
            </ul>
          </div>
        </div>

        <!-- Action Types -->
        <div class="subsection">
          <h3 class="subsection-title">{{ t('newcomersGuide.howToPlay.actionTypes.title') }}</h3>
          <div class="action-grid">
            <div class="action-card">
              <h4>{{ t('newcomersGuide.howToPlay.actionTypes.immediate.title') }}</h4>
              <p>{{ t('newcomersGuide.howToPlay.actionTypes.immediate.description') }}</p>
            </div>
            <div class="action-card">
              <h4>{{ t('newcomersGuide.howToPlay.actionTypes.scheduled.title') }}</h4>
              <p>{{ t('newcomersGuide.howToPlay.actionTypes.scheduled.description') }}</p>
            </div>
            <div class="action-card">
              <h4>{{ t('newcomersGuide.howToPlay.actionTypes.finite.title') }}</h4>
              <p>{{ t('newcomersGuide.howToPlay.actionTypes.finite.description') }}</p>
            </div>
          </div>
        </div>

        <!-- Important Notes -->
        <div class="subsection">
          <h3 class="subsection-title">{{ t('newcomersGuide.howToPlay.importantNotes.title') }}</h3>
          <div class="notes-grid">
            <div class="note-item">
              <strong>{{ t('newcomersGuide.howToPlay.importantNotes.items.itemsCartography.title') }}</strong> {{ t('newcomersGuide.howToPlay.importantNotes.items.itemsCartography.description') }}
            </div>
            <div class="note-item">
              <strong>{{ t('newcomersGuide.howToPlay.importantNotes.items.deathSystem.title') }}</strong> {{ t('newcomersGuide.howToPlay.importantNotes.items.deathSystem.description') }}
            </div>
            <div class="note-item">
              <strong>{{ t('newcomersGuide.howToPlay.importantNotes.items.teamPlay.title') }}</strong> {{ t('newcomersGuide.howToPlay.importantNotes.items.teamPlay.description') }}
            </div>
            <div class="note-item">
              <strong>{{ t('newcomersGuide.howToPlay.importantNotes.items.npcs.title') }}</strong> {{ t('newcomersGuide.howToPlay.importantNotes.items.npcs.description') }}
            </div>
            <div class="note-item">
              <strong>{{ t('newcomersGuide.howToPlay.importantNotes.items.rolePlaying.title') }}</strong> {{ t('newcomersGuide.howToPlay.importantNotes.items.rolePlaying.description') }}
            </div>
            <div class="note-item">
              <strong>{{ t('newcomersGuide.howToPlay.importantNotes.items.turnTime.title') }}</strong> {{ t('newcomersGuide.howToPlay.importantNotes.items.turnTime.description') }}
            </div>
          </div>
        </div>

        <!-- Dimensions -->
        <div class="subsection">
          <h3 class="subsection-title">{{ t('newcomersGuide.howToPlay.dimensions.title') }}</h3>
          <div class="dimensions-grid">
            <div class="dimension-item">
              <img
                src="@/assets/images/dx-1.webp"
                alt="1st Dimension"
                class="dimension-image zoomable-image"
                @click="toggleZoom($event)"
              />
              <div class="dimension-info">
                <h4>{{ t('newcomersGuide.howToPlay.dimensions.first.title') }}</h4>
                <p>{{ t('newcomersGuide.howToPlay.dimensions.first.description') }}</p>
              </div>
            </div>
            <div class="dimension-item">
              <img
                src="@/assets/images/dx-2.webp"
                alt="2nd Dimension"
                class="dimension-image zoomable-image"
                @click="toggleZoom($event)"
              />
              <div class="dimension-info">
                <h4>{{ t('newcomersGuide.howToPlay.dimensions.second.title') }}</h4>
                <p>{{ t('newcomersGuide.howToPlay.dimensions.second.description') }}</p>
              </div>
            </div>
            <div class="dimension-item">
              <img
                src="@/assets/images/dx-3.webp"
                alt="3rd Dimension"
                class="dimension-image zoomable-image"
                @click="toggleZoom($event)"
              />
              <div class="dimension-info">
                <h4>{{ t('newcomersGuide.howToPlay.dimensions.third.title') }}</h4>
                <p>{{ t('newcomersGuide.howToPlay.dimensions.third.description') }}</p>
              </div>
            </div>
            <div class="dimension-item">
              <img
                src="@/assets/images/dx-4.webp"
                alt="4th Dimension"
                class="dimension-image zoomable-image"
                @click="toggleZoom($event)"
              />
              <div class="dimension-info">
                <h4>{{ t('newcomersGuide.howToPlay.dimensions.fourth.title') }}</h4>
                <p>{{ t('newcomersGuide.howToPlay.dimensions.fourth.description') }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- How To Play (For GameMaster) -->
      <section class="content-section">
        <h2 class="section-title">{{ t('newcomersGuide.howToPlayGM.title') }}</h2>
        <div class="content-grid">
          <div class="text-content">
            <div class="coming-soon">
              <p>{{ t('newcomersGuide.howToPlayGM.comingSoon') }}</p>
            </div>
          </div>
          <div class="image-content">
            <img
                src="@/assets/images/faq/faq-gm-dashboard.png"
                alt="Game Master interface dashboard"
                class="section-image zoomable-image"
                @click="toggleZoom($event)"
            />
            <p class="image-caption">{{ t('newcomersGuide.howToPlayGM.imageCaption') }}</p>
          </div>
        </div>
      </section>

      <!-- Rules -->
      <section class="content-section rules-section">
        <h2 class="section-title">{{ t('newcomersGuide.rules.title') }}</h2>
        <div class="rules-content">
          <div class="rules-list">
            <div class="rule-item">
              <span class="rule-number">1</span>
              <span class="rule-text">{{ t('newcomersGuide.rules.rule1') }}</span>
            </div>
            <div class="rule-item">
              <span class="rule-number">2</span>
              <span class="rule-text">{{ t('newcomersGuide.rules.rule2') }}</span>
            </div>
            <div class="rule-item">
              <span class="rule-number">3</span>
              <span class="rule-text">{{ t('newcomersGuide.rules.rule3') }}</span>
            </div>
            <div class="rule-item">
              <span class="rule-number">4</span>
              <span class="rule-text">{{ t('newcomersGuide.rules.rule4') }}</span>
            </div>
          </div>
          <img
              src="@/assets/images/faq/faq-arbitor-rules.png"
              alt="Group of players enjoying the game"
              class="rules-image zoomable-image"
              @click="toggleZoom($event)"
          />
        </div>
      </section>

      <!-- Footer -->
      <div class="footer-section">
        <p>{{ t('newcomersGuide.footer.readyToBegin') }}</p>
        <a href="https://discord.gg/vC3TvVzK" target="_blank" class="discord-link">
          {{ t('newcomersGuide.footer.joinDiscord') }}
        </a>
        <div class="additional-links">
          <router-link to="/faq/player-cheatsheet" class="additional-link">{{ t('newcomersGuide.footer.playerCheatSheet') }}</router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import TitleComponent from '@/components/TitleComponent.vue'
import HeroBackground from '@/components/WhatIsIt/HeroBackground.vue'
import ZoomModal from '@/components/WhatIsIt/ZoomModal.vue'

const { t } = useI18n()

const isZoomed = ref(false)
const currentZoomedImage = ref('')
const scrollPosition = ref(0)

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
  background-image: url('@/assets/images/backgrounds/common/moaddib_Desolate_corrupted_wasteland_with_twisted_terrain_jag_072aff1a-d29b-4f13-a8a6-57bab975d17b_0.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.newcomers-guide {
  max-width: 1400px;
  width: 100%;
  padding: 1rem;
  color: #b7f9ff;
  position: relative;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(1px);
  margin: 0 auto;
}

.subtitle {
  font-size: 1.2rem;
  color: #9feaff;
  font-style: italic;
  text-align: center;
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

/* Content Sections */
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

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
}

.text-content {
  font-size: 1rem;
}

.image-content {
  text-align: center;
}

.section-image {
  width: 100%;
  max-width: 450px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  position: relative;
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

/* Lists */
.step-list {
  counter-reset: step-counter;
  list-style: none;
  padding: 0;
}

.step-list li {
  counter-increment: step-counter;
  margin-bottom: 0.75rem;
  padding: 0.75rem;
  padding-left: 2.5rem;
  background: rgba(10, 18, 32, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(99, 247, 255, 0.3);
  position: relative;
}

.step-list li::before {
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

.info-list {
  list-style: none;
  padding: 0;
}

.info-list li {
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: rgba(10, 18, 32, 0.6);
  border-radius: 6px;
  border: 1px solid rgba(99, 247, 255, 0.3);
  font-size: 0.95rem;
}

/* Subsections */
.subsection {
  margin-top: 2rem;
}

.subsection-title {
  font-size: 1.5rem;
  color: #bdf9ff;
  margin-bottom: 1rem;
  font-weight: 600;
  letter-spacing: 0.15em;
}

/* Action Cards */
.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.action-card {
  padding: 0.75rem;
  background: rgba(6, 14, 24, 0.55);
  border-radius: 8px;
  border: 1px solid rgba(99, 247, 255, 0.3);
  text-align: center;
}

.action-card h4 {
  color: #bdf9ff;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.action-card p {
  color: #9feaff;
  font-size: 0.9rem;
}

/* Notes Grid */
.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.note-item {
  padding: 0.75rem;
  background: rgba(10, 18, 32, 0.6);
  border-radius: 6px;
  border: 1px solid rgba(99, 247, 255, 0.3);
  font-size: 0.9rem;
}

.note-item strong {
  color: #bdf9ff;
  display: block;
  margin-bottom: 0.25rem;
}

/* Dimensions */
.dimensions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.dimension-item {
  background: rgba(10, 18, 32, 0.6);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.dimension-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  position: relative;
}

.dimension-info {
  padding: 1rem;
  text-align: center;
}

.dimension-info h4 {
  color: #bdf9ff;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.dimension-info p {
  color: #9feaff;
  font-size: 0.85rem;
}

/* Coming Soon */
.coming-soon {
  text-align: center;
  padding: 2rem;
  background: rgba(10, 18, 32, 0.5);
  border-radius: 8px;
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.coming-soon p {
  font-size: 1.1rem;
  color: #9feaff;
  font-style: italic;
  opacity: 0.9;
}

/* Rules Section */
.rules-section {
  background: linear-gradient(135deg, rgba(99, 247, 255, 0.08), rgba(34, 211, 238, 0.05));
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.rules-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: center;
}

.rules-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.rule-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: rgba(10, 18, 32, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(99, 247, 255, 0.3);
}

.rule-number {
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

.rule-text {
  font-size: 1rem;
  color: #b7f9ff;
}

.rules-image {
  width: 100%;
  max-width: 450px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  position: relative;
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
  .newcomers-guide {
    max-width: 100%;
    padding: 1rem;
    padding-top: 70px;
  }

  .content-section {
    padding: 1.5rem;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .subsection-title {
    font-size: 1.4rem;
  }
}

@media (max-width: 768px) {
  .newcomers-guide {
    padding: 1rem;
    padding-top: 60px;
  }

  .subtitle {
    font-size: 1.1rem;
    margin-bottom: 1rem;
  }

  .content-grid,
  .rules-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

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

  .section-image,
  .rules-image {
    max-width: 100%;
  }

  .dimension-image {
    height: 130px;
  }

  .action-grid,
  .notes-grid,
  .dimensions-grid {
    grid-template-columns: 1fr;
  }

  .additional-links {
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .newcomers-guide {
    padding: 1rem 0.75rem;
    padding-top: 50px;
  }

  .subtitle {
    font-size: 1rem;
    margin-bottom: 1rem;
  }

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

  .dimension-image {
    height: 110px;
  }

  .zoomable-image:hover {
    transform: scale(1.02);
  }

  .step-list li {
    padding: 0.75rem;
    padding-left: 2rem;
  }

  .step-list li::before {
    width: 20px;
    height: 20px;
    font-size: 0.8rem;
    left: 0.5rem;
  }

  .discord-link {
    padding: 0.6rem 1.5rem;
    font-size: 0.9rem;
  }
}
</style>