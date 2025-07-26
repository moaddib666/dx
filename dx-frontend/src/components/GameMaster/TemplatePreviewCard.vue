<template>
  <div class="template-preview-card">
    <!-- Card content -->
    <div class="card-content">
      <!-- Top Section -->
      <div class="top-section">
        <!-- Character header with avatar as background -->
        <div :style="getHeaderBackgroundStyle()" class="character-header">
          <!-- Character name overlay -->
          <div class="character-name-overlay">
            <h2 class="character-name">{{ template.data.name || 'Unnamed Template' }}</h2>
            <span class="character-type">Template</span>
          </div>

          <!-- Character Stats Radar Chart -->
          <div class="character-stats-chart">
            <TemplateStatsRadarChart v-if="template && template.data.stats" :stats="template.data.stats"/>
          </div>

          <!-- Left side: Shield icons -->
          <div class="shields-container">
            <div v-for="shield in getShields()" :key="shield.id" class="shield-icon-container">
              <img v-if="shield.icon"
                   :alt="`${shield.name} - ${shield.efficiency}% efficiency`"
                   :src="shield.icon"
                   class="shield-icon">
              <div v-else class="shield-icon-placeholder">🛡️</div>
            </div>
            <div v-if="getShields().length === 0" class="no-shields">No shields</div>
          </div>

          <!-- Right side: Effect icons -->
          <div class="effects-container">
            <div v-for="effect in getEffects()" :key="effect.id" class="effect-icon-container">
              <img v-if="effect.icon"
                   :alt="`${effect.name} - ${effect.description || 'Effect'}`"
                   :src="effect.icon"
                   class="effect-icon">
              <div v-else class="effect-icon-placeholder">✨</div>
            </div>
            <div v-if="getEffects().length === 0" class="no-effects">No effects</div>
          </div>

          <!-- Attribute bars at the bottom of the avatar -->
          <div class="card-bars">
            <div class="attribute-bar">
              <div class="attribute-label">Health</div>
              <div class="attribute-value">100/100</div>
            </div>
            <div class="attribute-bar">
              <div class="attribute-label">Energy</div>
              <div class="attribute-value">100/100</div>
            </div>
            <div class="attribute-bar">
              <div class="attribute-label">Action Points</div>
              <div class="attribute-value">3/3</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Section -->
      <div class="bottom-section">
        <!-- Biography toggle button -->
        <button v-if="template.data.bio && hasBiographyData()"
                :title="showBio ? 'Hide Biography' : 'Show Biography'"
                class="toggle-button bio-toggle"
                @click="showBio = !showBio">
          <span class="toggle-icon">📜</span>
        </button>

        <!-- Biography Section (hidden by default) -->
        <div v-if="template.data.bio && showBio && hasBiographyData()" class="biography-section">
          <div class="biography-content">
            <div v-if="template.data.bio.name" class="bio-field">
              <span class="bio-label">Full Name:</span>
              <span class="bio-value">{{ template.data.bio.name }}</span>
            </div>
            <div v-if="template.data.bio.age" class="bio-field">
              <span class="bio-label">Age:</span>
              <span class="bio-value">{{ template.data.bio.age }}</span>
            </div>
            <div v-if="template.data.bio.gender" class="bio-field">
              <span class="bio-label">Gender:</span>
              <span class="bio-value">{{ template.data.bio.gender }}</span>
            </div>
            <div v-if="template.data.bio.origin" class="bio-field">
              <span class="bio-label">Origin:</span>
              <span class="bio-value">{{ template.data.bio.origin }}</span>
            </div>
            <div v-if="template.data.bio.background" class="bio-field bio-background">
              <span class="bio-label">Background:</span>
              <div class="bio-background-text">{{ template.data.bio.background }}</div>
            </div>
          </div>
        </div>

        <!-- External Sections -->
        <div class="external-sections">
          <!-- Path and Rank Information -->
          <div class="path-rank-section" v-if="template.data.path || template.data.rank">
            <h3>Path & Rank</h3>
            <div class="path-rank-content">
              <div v-if="template.data.path" class="info-item">
                <span class="info-label">Path:</span>
                <span class="info-value">{{ template.data.path }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Rank:</span>
                <span class="info-value">{{ template.data.rank }} ({{ getRankDescription() }})</span>
              </div>
            </div>
          </div>

          <!-- Schools & Spells Section -->
          <div class="abilities-section" v-if="template.data.schools.length > 0 || template.data.spells.length > 0">
            <h3>Schools & Spells</h3>
            <div class="abilities-grid">
              <div v-if="template.data.schools.length > 0" class="schools-display">
                <h4>Schools ({{ template.data.schools.length }})</h4>
                <div class="schools-list">
                  <div v-for="schoolId in template.data.schools" :key="schoolId" class="school-item">
                    <img v-if="getSchoolById(schoolId)?.icon"
                         :src="getSchoolById(schoolId).icon"
                         :alt="getSchoolById(schoolId)?.name"
                         class="school-icon">
                    <span class="school-name">{{ getSchoolById(schoolId)?.name || schoolId }}</span>
                  </div>
                </div>
              </div>
              <div v-if="template.data.spells.length > 0" class="spells-display">
                <h4>Spells ({{ template.data.spells.length }})</h4>
                <div class="spells-list">
                  <div v-for="spellId in template.data.spells" :key="spellId" class="spell-item">
                    <SkillIcon :skill="getSpellById(spellId)" v-if="getSpellById(spellId)" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Inventory items -->
          <div class="inventory-section" v-if="template.data.items.length > 0">
            <h3>Inventory</h3>
            <div class="inventory-grid">
              <div v-for="itemId in template.data.items" :key="itemId" class="inventory-item">
                <div class="item-placeholder">{{ itemId }}</div>
              </div>
            </div>
          </div>

          <!-- Tags Section -->
          <div class="tags-section" v-if="template.data.tags.length > 0">
            <h3>Tags</h3>
            <div class="tags-list">
              <span v-for="(tag, index) in template.data.tags" :key="index" class="tag-item">
                {{ tag }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SkillIcon from "@/components/Action/ActionIcon.vue";
import skillService from "@/services/skillService";

export default {
  name: 'TemplatePreviewCard',
  components: {
    SkillIcon,
    TemplateStatsRadarChart: () => import('@/components/GameMaster/TemplateStatsRadarChart.vue')
  },
  props: {
    template: {
      type: Object,
      required: true
    },
    service: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      skillService: skillService,
      showBio: false
    };
  },
  computed: {
    previewData() {
      return this.service?.getPreviewData() || null;
    },
    isPreviewGenerating() {
      return this.service?.isPreviewGenerating() || false;
    },
    displayData() {
      // Use preview data if available, otherwise fall back to template data
      return this.previewData || this.template;
    }
  },
  methods: {
    getHeaderBackgroundStyle() {
      // Use a default avatar background or template image
      const backgroundImage = this.template.data.avatar || '/api/placeholder/400/200';
      return {
        backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.7)), url('${backgroundImage}')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      };
    },

    getSchoolById(schoolId) {
      return this.skillService.getSchool(schoolId);
    },

    getSpellById(spellId) {
      return this.skillService.getSkill(spellId);
    },

    getRankDescription() {
      const rank = this.template.data.rank;
      if (rank === 0) return "Top Dog";
      if (rank <= 2) return "Elite";
      if (rank <= 5) return "Experienced";
      if (rank <= 7) return "Competent";
      return "Beginner";
    },

    getShields() {
      // For template preview, we can show some default shields or empty
      return [];
    },

    getEffects() {
      // For template preview, we can show some default effects or empty
      return [];
    },

    hasBiographyData() {
      if (!this.template.data.bio) return false;
      return !!(this.template.data.bio.name ||
                this.template.data.bio.age ||
                this.template.data.bio.gender ||
                this.template.data.bio.origin ||
                this.template.data.bio.background);
    }
  }
};
</script>

<style scoped>
.template-preview-card {
  background: rgba(30, 30, 30, 0.95);
  border: 2px solid #555;
  border-radius: 12px;
  color: #ffffff;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: 'Roboto', sans-serif;
}

/* Card content */
.card-content {
  display: flex;
  flex-direction: column;
  position: relative;
  background: rgba(30, 30, 30, 0.9);
}

/* Top Section */
.top-section {
  position: relative;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(30, 144, 255, 0.3);
  margin-bottom: 0.75rem;
}

/* Character header with avatar background */
.character-header {
  position: relative;
  width: 100%;
  /* 4:7 aspect ratio - vertical orientation */
  padding-top: 145%; /* 7/4 = 1.75 or 175% */
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1rem;
  /* Default background if no avatar */
  background: #1E90FF;
  background-size: cover;
  background-position: center;
}

/* Character name overlay */
.character-name-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 0.5rem;
  text-align: center;
}

/* Character Stats Chart */
.character-stats-chart {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70%;
  height: 60%;
  z-index: 5;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 8px;
  padding: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

/* Attribute bars at the bottom of the avatar */
.card-bars {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.5rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.attribute-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 0.7rem;
  font-size: 0.7rem;
  color: #fff;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 3px;
  padding: 0 0.5rem;
}

.attribute-label {
  font-size: 0.7rem;
  font-weight: bold;
}

.attribute-value {
  font-size: 0.7rem;
  color: #4CAF50;
}

.character-name {
  font-size: 1.2rem;
  margin: 0;
  font-weight: bold;
  color: #fff;
}

.character-type {
  font-size: 0.8rem;
  color: #ccc;
  margin-top: 0.1rem;
}

/* Left side: Shield icons */
.shields-container {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 50px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: 0.5rem 0.2rem;
  gap: 0.3rem;
  z-index: 3;
}

.shield-icon-container {
  position: relative;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.shield-icon {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  object-fit: cover;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.shield-icon-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  font-size: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Right side: Effect icons */
.effects-container {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 50px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: 0.5rem 0.2rem;
  gap: 0.3rem;
  z-index: 3;
}

.effect-icon-container {
  position: relative;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.effect-icon {
  width: 100%;
  height: 100%;
  border-radius: 4px;
  object-fit: cover;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.effect-icon-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  font-size: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.no-shields, .no-effects {
  color: rgba(255, 255, 255, 0.3);
  font-size: 0.6rem;
  text-align: center;
  writing-mode: vertical-lr;
  text-orientation: mixed;
  margin-top: 0.5rem;
}

/* Bottom Section */
.bottom-section {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Biography toggle button */
.toggle-button {
  position: absolute;
  top: -0.5rem;
  right: 0;
  background: rgba(30, 144, 255, 0.8);
  color: white;
  border: none;
  border-radius: 50%;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
}

.toggle-button:hover {
  background: rgba(30, 144, 255, 1);
  transform: scale(1.1);
}

.toggle-icon {
  font-size: 1rem;
}

/* Biography Section */
.biography-section {
  background: rgba(40, 40, 40, 0.8);
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 0.75rem;
  border: 1px solid rgba(30, 144, 255, 0.3);
}

.biography-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.bio-field {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  font-size: 0.8rem;
  line-height: 1.3;
}

.bio-label {
  color: rgba(30, 144, 255, 0.9);
  font-weight: bold;
  min-width: 4rem;
}

.bio-value {
  color: #ccc;
  flex: 1;
}

.bio-background {
  flex-direction: column;
  align-items: flex-start;
}

.bio-background-text {
  color: #ccc;
  font-size: 0.8rem;
  line-height: 1.4;
  margin-top: 0.25rem;
  text-align: justify;
}

/* External Sections */
.external-sections {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.external-sections h3 {
  font-size: 0.9rem;
  color: rgba(30, 144, 255, 0.9);
  margin: 0 0 0.5rem 0;
  padding-bottom: 0.25rem;
  border-bottom: 1px solid rgba(30, 144, 255, 0.3);
}

/* Path and Rank Section */
.path-rank-section {
  background: rgba(40, 40, 40, 0.5);
  border-radius: 6px;
  padding: 0.5rem;
}

.path-rank-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
}

.info-label {
  color: #aaa;
  font-weight: 500;
}

.info-value {
  color: #fff;
  font-weight: bold;
}

/* Schools & Spells Section */
.abilities-section {
  background: rgba(40, 40, 40, 0.5);
  border-radius: 6px;
  padding: 0.5rem;
}

.abilities-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.schools-display h4, .spells-display h4 {
  font-size: 0.8rem;
  color: #ccc;
  margin: 0 0 0.5rem 0;
}

.schools-list, .spells-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
  gap: 0.25rem;
}

.school-item, .spell-item {
  background: rgba(60, 60, 60, 0.8);
  border-radius: 4px;
  padding: 0.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.school-icon {
  width: 24px;
  height: 24px;
  border-radius: 3px;
  margin-bottom: 0.25rem;
  object-fit: cover;
}

.school-name {
  font-size: 0.6rem;
  color: #ccc;
  line-height: 1.1;
  word-break: break-word;
}

/* Inventory Section */
.inventory-section {
  background: rgba(40, 40, 40, 0.5);
  border-radius: 6px;
  padding: 0.5rem;
}

.inventory-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  gap: 0.25rem;
  margin-top: 0.5rem;
}

.inventory-item {
  aspect-ratio: 1;
  background: rgba(60, 60, 60, 0.8);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.item-placeholder {
  font-size: 0.6rem;
  color: #888;
  text-align: center;
  word-break: break-all;
  padding: 0.125rem;
}

/* Tags Section */
.tags-section {
  background: rgba(40, 40, 40, 0.5);
  border-radius: 6px;
  padding: 0.5rem;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-top: 0.5rem;
}

.tag-item {
  background: rgba(30, 144, 255, 0.2);
  color: #1E90FF;
  padding: 0.125rem 0.375rem;
  border-radius: 3px;
  font-size: 0.7rem;
  border: 1px solid rgba(30, 144, 255, 0.4);
}

/* Responsive adjustments */
@media (max-width: 350px) {
  .template-preview-card {
    width: 280px;
  }

  .character-header {
    padding-top: 160%;
  }

  .character-stats-chart {
    width: 60%;
    height: 50%;
  }

  .schools-list, .spells-list {
    grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  }

  .inventory-grid {
    grid-template-columns: repeat(auto-fill, minmax(35px, 1fr));
  }
}
</style>