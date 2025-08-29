<template>
  <div class="character-review">
    <div class="background-image">
      <div class="gradient-overlay"></div>
    </div>
    <div v-if="isCharacterValid" class="review-content">
      <!-- Left Section: Avatar and Info -->
      <div class="left-section">
        <div class="avatar-wrapper">
          <!-- Avatar Image -->
          <div class="avatar-container">
            <img :src="avatar" alt="Character Avatar" class="avatar-image"/>
            <div class="avatar-overlay"></div>
          </div>
          <!-- Path Icon -->
          <div class="path-icon-wrapper">
            <img :src="path.icon" alt="Path Icon" class="path-icon" />
          </div>
        </div>
        <div class="character-info">
          <h2 class="character-name">{{ character.name }}</h2>
          <p class="rank">{{ t('playerComponents.characterReview.rank') }}{{ rank }}</p>
        </div>
      </div>

      <!-- Right Section: Details -->
      <div class="right-section">
        <div class="details-wrapper">
          <!-- Modificators -->
          <div class="modificators-section">
            <h3>{{ t('playerComponents.characterReview.modificators') }}</h3>
            <ul>
              <li v-for="mod in selectedModificators" :key="mod.id">{{ mod.name }}</li>
            </ul>
          </div>

<!--          &lt;!&ndash; Stats &ndash;&gt;-->
<!--          <div class="stats-section">-->
<!--            <h3>Stats</h3>-->
<!--            <ul>-->
<!--              <li v-for="stat in stats" :key="stat.name">-->
<!--                <strong>{{ stat.name }}</strong>: {{ stat.value }}-->
<!--              </li>-->
<!--            </ul>-->
<!--          </div>-->

          <!-- Spells -->
          <div class="spells-section">
            <h3>{{ t('playerComponents.characterReview.spells') }}</h3>
            <ul>
              <li v-for="spell in selectedSpells" :key="spell.id">{{ spell.name }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Validation Error -->
    <div v-else class="error-message">
      <div class="error-container">
        <h2>{{ t('playerComponents.characterReview.errorTitle') }}</h2>
        <p>{{ t('playerComponents.characterReview.errorDescription') }}</p>
        <ul>
          <li v-for="error in validationErrors" :key="error">{{ error }}</li>
        </ul>
        <p>{{ t('playerComponents.characterReview.errorAction') }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import avatarPlaceholderPath from "@/assets/images/avatar/placeholder.webp";
import { useI18n } from 'vue-i18n';

export default {
  name: "CharacterReview",
  props: {
    character: {
      type: Object,
      required: true,
    },
    spellsRegistry: {
      type: Array,
      required: true,
    },
    schoolsRegistry: {
      type: Array,
      required: true,
    },
    modificatorsRegistry: {
      type: Array,
      required: true,
    },
    statsRegistry: {
      type: Array,
      required: true,
    },
    pathRegistry: {
      type: Array,
      required: true,
    },
  },
  setup() {
    const { t } = useI18n();
    return { t };
  },
  data() {
    return {
      validationErrors: [],
    };
  },
  computed: {
    isCharacterValid() {
      this.validationErrors = [];
      if (!this.character) this.validationErrors.push(this.t('playerComponents.characterReview.validationErrors.missingCharacter'));
      else {
        if (!this.character.name) this.validationErrors.push(this.t('playerComponents.characterReview.validationErrors.missingName'));
        if (!this.character.bio || !this.character.bio.age)
          this.validationErrors.push(this.t('playerComponents.characterReview.validationErrors.missingAge'));
        if (!this.character.bio || !this.character.bio.gender)
          this.validationErrors.push(this.t('playerComponents.characterReview.validationErrors.missingGender'));
        if (!this.character.path)
          this.validationErrors.push(this.t('playerComponents.characterReview.validationErrors.missingPath'));
        if (this.character.rank === undefined) this.validationErrors.push(this.t('playerComponents.characterReview.validationErrors.missingRank'));
        // if (!this.character.modificators || this.character.modificators.length === 0)
        //   this.validationErrors.push("No modificators selected.");
        if (!this.character.stats || this.character.stats.length === 0)
          this.validationErrors.push(this.t('playerComponents.characterReview.validationErrors.missingStats'));
        if (!this.character.spells || this.character.spells.length === 0)
          this.validationErrors.push(this.t('playerComponents.characterReview.validationErrors.missingSpells'));
      }
      return this.validationErrors.length === 0;
    },
    avatar() {
      return this.character.avatar ? this.character.avatar : avatarPlaceholderPath;
    },
    backgroundImage() {
        const path = this.pathRegistry.find((p) => p.id === this.character.path);
        return path.backgroundImage
            ? path.backgroundImage
            : require("@/assets/images/backgrounds/preview-background.webp");
      },
    path() {
      return this.pathRegistry.find((path) => path.id === this.character.path) || {};
    },
    rank() {
      return this.character.rank || this.t('playerComponents.characterReview.unranked');
    },
    selectedModificators() {
      return this.character.modificators.map((id) =>
          this.modificatorsRegistry.find((mod) => mod.id === id)
      );
    },
    stats() {
      return this.character.stats.map((stat) => ({
        name: this.statsRegistry.find((s) => s.name === stat.name)?.name || stat.name,
        value: stat.value,
      }));
    },
    selectedSpells() {
      return this.character.spells.map((id) =>
          this.spellsRegistry.find((spell) => spell.id === id)
      );
    },
  },
};
</script>

<style scoped>
/* Character Review - Responsive */
.character-review {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  min-height: 60vh;
  max-height: 80vh;
  padding: 1rem;
  border-radius: 0.5rem;
  background: transparent;
  overflow-y: auto;
  width: 100%;
  box-sizing: border-box;
}

/* Responsive padding */
@media (min-width: 768px) {
  .character-review {
    padding: 1.5rem;
    max-height: 75vh;
  }
}

@media (min-width: 1024px) {
  .character-review {
    padding: 2rem;
    max-height: 80vh;
  }
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/images/backgrounds/preview-background.webp') center/cover no-repeat;
  z-index: -2;
  border-radius: 0.5rem;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8));
  z-index: -1;
  border-radius: 0.5rem;
}

.review-content {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-top: 1rem;
  gap: 1rem;
  position: relative;
  z-index: 2;
}

/* Responsive layout - two columns on larger screens */
@media (min-width: 768px) {
  .review-content {
    flex-direction: row;
    gap: 1.5rem;
    margin-top: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .review-content {
    gap: 2rem;
    margin-top: 2rem;
  }
}

/* Left Section - Responsive */
.left-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background: rgba(0, 0, 0, 0.2);
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(127, 255, 22, 0.2);
  box-sizing: border-box;
}

/* Responsive left section padding */
@media (min-width: 768px) {
  .left-section {
    padding: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .left-section {
    padding: 2rem;
  }
}

.avatar-wrapper {
  position: relative;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

/* Responsive avatar wrapper */
@media (min-width: 768px) {
  .avatar-wrapper {
    margin-bottom: 1.25rem;
    gap: 1rem;
  }
}

@media (min-width: 1024px) {
  .avatar-wrapper {
    margin-bottom: 1.5rem;
  }
}

.avatar-container {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(127, 255, 22, 0.3);
}

/* Responsive avatar sizing */
@media (min-width: 768px) {
  .avatar-container {
    width: 120px;
    height: 120px;
  }
}

@media (min-width: 1024px) {
  .avatar-container {
    width: 150px;
    height: 150px;
  }
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.path-icon-wrapper {
  background: rgba(0, 0, 0, 0.6);
  padding: 0.4rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(127, 255, 22, 0.3);
}

.path-icon {
  width: 24px;
  height: 24px;
}

/* Responsive path icon */
@media (min-width: 768px) {
  .path-icon-wrapper {
    padding: 0.5rem;
  }

  .path-icon {
    width: 28px;
    height: 28px;
  }
}

@media (min-width: 1024px) {
  .path-icon {
    width: 32px;
    height: 32px;
  }
}

.character-info {
  margin-top: 0.75rem;
}

/* Responsive character info */
@media (min-width: 768px) {
  .character-info {
    margin-top: 1rem;
  }
}

.character-name {
  font-size: 1.5rem;
  font-weight: 600;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  margin-bottom: 0.5rem;
}

/* Responsive character name */
@media (min-width: 768px) {
  .character-name {
    font-size: 1.75rem;
  }
}

@media (min-width: 1024px) {
  .character-name {
    font-size: 2rem;
  }
}

.rank {
  font-size: 1rem;
  color: rgba(250, 218, 149, 0.8);
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

/* Responsive rank */
@media (min-width: 768px) {
  .rank {
    font-size: 1.1rem;
  }
}

@media (min-width: 1024px) {
  .rank {
    font-size: 1.2rem;
  }
}

/* Right Section - Responsive */
.right-section {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: rgba(0, 0, 0, 0.2);
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(127, 255, 22, 0.2);
  box-sizing: border-box;
}

/* Responsive right section */
@media (min-width: 768px) {
  .right-section {
    gap: 1.25rem;
    padding: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .right-section {
    gap: 1.5rem;
    padding: 2rem;
  }
}

.details-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Responsive details wrapper */
@media (min-width: 768px) {
  .details-wrapper {
    gap: 1.25rem;
  }
}

@media (min-width: 1024px) {
  .details-wrapper {
    gap: 1.5rem;
  }
}

.modificators-section,
.spells-section {
  background: rgba(0, 0, 0, 0.1);
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(127, 255, 22, 0.2);
  box-sizing: border-box;
}

/* Responsive sections */
@media (min-width: 768px) {
  .modificators-section,
  .spells-section {
    padding: 1.25rem;
  }
}

@media (min-width: 1024px) {
  .modificators-section,
  .spells-section {
    padding: 1.5rem;
  }
}

h3 {
  font-size: 1.2rem;
  margin-bottom: 0.75rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

/* Responsive headings */
@media (min-width: 768px) {
  h3 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
  }
}

@media (min-width: 1024px) {
  h3 {
    font-size: 1.4rem;
  }
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin: 0.4rem 0;
  padding: 0.5rem;
  background: rgba(127, 255, 22, 0.1);
  border-radius: 0.25rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.9rem;
}

/* Responsive list items */
@media (min-width: 768px) {
  li {
    margin: 0.5rem 0;
    padding: 0.6rem;
    font-size: 0.95rem;
  }
}

@media (min-width: 1024px) {
  li {
    padding: 0.75rem;
    font-size: 1rem;
  }
}

li:hover {
  background: rgba(127, 255, 22, 0.15);
}

.error-message {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  color: #ff6b6b;
  text-align: center;
  padding: 2rem;
  position: relative;
  z-index: 2;
}

.error-container {
  background: rgba(0, 0, 0, 0.4);
  padding: 2rem;
  border-radius: 0.5rem;
  width: 80%;
  border: 2px solid rgba(255, 107, 107, 0.3);
  backdrop-filter: blur(2px);
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.error-container h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #ff6b6b;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

.error-container p {
  font-size: 1rem;
  margin: 1rem 0;
  color: rgba(255, 107, 107, 0.8);
  line-height: 1.5;
}

.error-container ul {
  text-align: left;
  margin: 1rem 0;
}

.error-container li {
  background: rgba(255, 107, 107, 0.1);
  border-color: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.error-container li:hover {
  background: rgba(255, 107, 107, 0.2);
  border-color: rgba(255, 107, 107, 0.4);
}
</style>
