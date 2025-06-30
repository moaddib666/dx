<template>
  <div class="page-container">
    <div class="hero-background" @click="toggleZoom($event)"></div>
    <main class="newcomers-guide">
      <TitleComponent>Newcomer's Guide</TitleComponent>
      <p class="subtitle">Welcome to a world where magic and technology collide</p>

      <!-- Zoom Modal -->
      <div v-if="isZoomed" class="zoom-modal" @click="closeZoom">
        <div class="zoomed-image" :style="zoomedImageStyle"></div>
      </div>

      <!-- How To Start -->
      <section class="content-section">
        <h2 class="section-title">How To Start</h2>
        <div class="content-grid">
          <div class="text-content">
            <ol class="step-list">
              <li>Register on <a href="https://dx.awesome.live/" target="_blank">https://dx.awesome.live/</a></li>
              <li>Connect our Discord and reach any of game masters so that add you to a campaign</li>
              <li>When you added to a campaign you can see the campaign in the site and able to create a new character for it</li>
              <li>When your character ready ping game master for validation</li>
              <li>When all done you are good to go to join game session on selected date and time</li>
            </ol>
          </div>
          <div class="image-content">
            <img
                src="@/assets/images/faq/faq-creation-path.png"
                alt="Character creation interface"
                class="section-image zoomable-image"
                @click="toggleZoom($event)"
            />
            <p class="image-caption">Character creation process</p>
          </div>
        </div>
      </section>

      <!-- How To Play (For Player) -->
      <section class="content-section">
        <h2 class="section-title">How To Play (For Player)</h2>
        <div class="content-grid">
          <div class="image-content">
            <img
                src="@/assets/images/faq/faq-gameplay-example.png"
                alt="Game interface showing combat and character stats"
                class="section-image zoomable-image"
                @click="toggleZoom($event)"
            />
            <p class="image-caption">Game interface overview</p>
          </div>
          <div class="text-content">
            <ul class="info-list">
              <li>Learn backstory (optional) - use Discord or chat with AI to understand lore and main game rules</li>
              <li>The game is divided by cycles where each cycle is a turn</li>
              <li>The character have characteristics and attributes</li>
              <li>The characteristics influence any action and attributes of your character</li>
              <li>On any action the dice been thrown and the result influenced by number of the dice result</li>
              <li>To perform actions you spend ActionPoints and Flow or Stamina depends on your path</li>
              <li>In general by the cycle you can make an action, use item, move, do dialog, act - acting and dialog is not taken the action points but moderated by GM</li>
              <li>Please find the order of your character by check your speed - in case you have same speed with other characters it's best to roll the dice to find who is faster</li>
            </ul>
          </div>
        </div>

        <!-- Action Types -->
        <div class="subsection">
          <h3 class="subsection-title">Action Types</h3>
          <div class="action-grid">
            <div class="action-card">
              <h4>Immediate Actions</h4>
              <p>Executed right after apply (gift, inspect)</p>
            </div>
            <div class="action-card">
              <h4>Scheduled Actions</h4>
              <p>Ordered and executed on turn end (attack, defense)</p>
            </div>
            <div class="action-card">
              <h4>Finite Actions</h4>
              <p>Complete instantly (move)</p>
            </div>
          </div>
        </div>

        <!-- Important Notes -->
        <div class="subsection">
          <h3 class="subsection-title">Important Notes</h3>
          <div class="notes-grid">
            <div class="note-item">
              <strong>Items & Cartography:</strong> Some items give you great advantage like cartograph that allow you and your guild draw the map and use it. It's better to communicate with person who have cartograph and report to him your position as it will not automatically mapped.
            </div>
            <div class="note-item">
              <strong>Death System:</strong> When you die you not actually died unless you don't have status death mark or through death, this is dimensional curse that would kill and wipe your character from the world. In other cases you would be respawned in safe place with penalties statuses coma.
            </div>
            <div class="note-item">
              <strong>Team Play:</strong> The first status is knocked out and you can been rescued by your team mates in this status.
            </div>
            <div class="note-item">
              <strong>NPCs:</strong> Not all NPC aggressive by default but you and your team mate could make guild aggressive against your guild so be cautious.
            </div>
            <div class="note-item">
              <strong>Role Playing:</strong> Don't forget to act when you performing something or want to participate in something - it's role play all in all.
            </div>
            <div class="note-item">
              <strong>Turn Time:</strong> Don't over act or make 5 minutes turns - you are not alone here!
            </div>
          </div>
        </div>

        <!-- Dimensions -->
        <div class="subsection">
          <h3 class="subsection-title">Dimensions</h3>
          <div class="dimensions-grid">
            <div class="dimension-item">
              <img
                src="@/assets/images/dx-1.webp"
                alt="1st Dimension"
                class="dimension-image zoomable-image"
                @click="toggleZoom($event)"
              />
              <div class="dimension-info">
                <h4>1st Dimension</h4>
                <p>Safe real world, energy regenerates</p>
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
                <h4>2nd Dimension</h4>
                <p>Faster time, energy drains slowly</p>
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
                <h4>3rd Dimension</h4>
                <p>Dangerous shadows, heavy energy drain</p>
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
                <h4>4th Dimension</h4>
                <p>Brutal storms, extreme energy cost</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- How To Play (For GameMaster) -->
      <section class="content-section">
        <h2 class="section-title">How To Play (For GameMaster)</h2>
        <div class="content-grid">
          <div class="text-content">
            <div class="coming-soon">
              <p>Come soon - not fully implemented due to permissions separations</p>
            </div>
          </div>
          <div class="image-content">
            <img
                src="@/assets/images/faq/faq-gm-dashboard.png"
                alt="Game Master interface dashboard"
                class="section-image zoomable-image"
                @click="toggleZoom($event)"
            />
            <p class="image-caption">GM Dashboard (Coming Soon)</p>
          </div>
        </div>
      </section>

      <!-- Rules -->
      <section class="content-section rules-section">
        <h2 class="section-title">Rules</h2>
        <div class="rules-content">
          <div class="rules-list">
            <div class="rule-item">
              <span class="rule-number">1</span>
              <span class="rule-text">Make fun</span>
            </div>
            <div class="rule-item">
              <span class="rule-number">2</span>
              <span class="rule-text">Do not blame each other or argue</span>
            </div>
            <div class="rule-item">
              <span class="rule-number">3</span>
              <span class="rule-text">Respect each other</span>
            </div>
            <div class="rule-item">
              <span class="rule-number">4</span>
              <span class="rule-text">Role play - be a character not yourself</span>
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
        <p>Ready to begin your adventure in Dimension-X?</p>
        <a href="https://discord.gg/32dwT8EP" target="_blank" class="discord-link">
          Join Our Discord
        </a>
        <div class="additional-links">
          <router-link to="/faq/player-cheatsheet" class="additional-link">Player Cheat Sheet</router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import TitleComponent from '@/components/TitleComponent.vue';

export default {
  name: 'NewcomersGuide',
  components: {
    TitleComponent
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
.newcomers-guide {
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
  background-image: url('@/assets/images/faq/faq-hero-section.png');
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

/* Zoom Modal */
.zoom-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.9);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: zoom-out;
}

.zoomed-image {
  width: 90%;
  height: 90%;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 8px;
  box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
  animation: zoomIn 0.3s ease;
}

@keyframes borderPulse {
  0% {
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.3), inset 0 0 15px rgba(255, 215, 0, 0.2);
  }
  100% {
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.6), inset 0 0 20px rgba(255, 215, 0, 0.4);
  }
}

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

/* Content Sections */
.content-section {
  margin-bottom: 4rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.section-title {
  font-size: 24px;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 600;
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
  color: #b0c4de;
  font-style: italic;
}

/* Lists */
.step-list {
  counter-reset: step-counter;
  list-style: none;
  padding: 0;
}

.step-list li {
  counter-increment: step-counter;
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border-left: 4px solid var(--cyber-yellow, #ffd700);
  position: relative;
}

.step-list li::before {
  content: counter(step-counter);
  position: absolute;
  left: -15px;
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

.info-list {
  list-style: none;
  padding: 0;
}

.info-list li {
  margin-bottom: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 6px;
  border-left: 3px solid #00ffff;
  font-size: 0.95rem;
}

/* Subsections */
.subsection {
  margin-top: 2rem;
}

.subsection-title {
  font-size: 1.5rem;
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 1rem;
  font-weight: 600;
}

/* Action Cards */
.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.action-card {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 215, 0, 0.3);
  text-align: center;
}

.action-card h4 {
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.action-card p {
  color: #b0c4de;
  font-size: 0.9rem;
}

/* Notes Grid */
.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.note-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 6px;
  border-left: 3px solid #00ffff;
  font-size: 0.9rem;
}

.note-item strong {
  color: var(--cyber-yellow, #ffd700);
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
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(255, 215, 0, 0.2);
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
  color: var(--cyber-yellow, #ffd700);
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.dimension-info p {
  color: #b0c4de;
  font-size: 0.85rem;
}

/* Coming Soon */
.coming-soon {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 165, 0, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(255, 165, 0, 0.3);
}

.coming-soon p {
  font-size: 1.1rem;
  color: #ffa500;
  font-style: italic;
}

/* Rules Section */
.rules-section {
  background: rgba(255, 215, 0, 0.05);
  border-color: var(--cyber-yellow, #ffd700);
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
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.rule-number {
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

.rule-text {
  font-size: 1rem;
  color: white;
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

/* Links */
a {
  color: var(--cyber-yellow, #ffd700);
  text-decoration: none;
  transition: color 0.3s ease;
}

a:hover {
  color: white;
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 768px) {
  .newcomers-guide {
    padding: 30px;
    margin-top: 40px;
  }

  .hero-background {
    background-attachment: scroll; /* Fixed attachment can cause issues on mobile */
  }

  .zoomed-image {
    width: 95%;
    height: 80%;
  }

  .content-grid,
  .rules-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .content-section {
    padding: 1.5rem;
  }

  .section-title {
    font-size: 20px;
  }

  .section-image,
  .rules-image {
    max-width: 100%;
  }

  .dimension-image {
    height: 130px;
  }

  .zoomable-image::before {
    border-width: 1px;
  }

  .action-grid,
  .notes-grid,
  .dimensions-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .newcomers-guide {
    padding: 20px;
    margin-top: 30px;
  }

  .subtitle {
    font-size: 1rem;
  }

  .content-section {
    padding: 1rem;
  }

  .section-title {
    font-size: 18px;
  }

  .dimension-image {
    height: 110px;
  }

  .zoomable-image:hover {
    transform: scale(1.02);
  }

  .zoomed-image {
    width: 98%;
    height: 70%;
  }

  .step-list li {
    padding: 0.75rem;
    margin-left: 20px;
  }
}
</style>