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
.character-review {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  max-height: 100vh;
  padding: 2rem;
  border-radius: 0.5rem;
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(127, 255, 22, 0.3);
  backdrop-filter: blur(2px);
  overflow: hidden;
}

/* Flow border effect */
.character-review::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 0.5rem;
  background: linear-gradient(45deg,
    transparent,
    rgba(127, 255, 22, 0.05),
    transparent,
    rgba(127, 255, 22, 0.05),
    transparent
  );
  background-size: 300% 300%;
  animation: flowBorder 8s ease-in-out infinite;
  opacity: 0.3;
  pointer-events: none;
}

@keyframes flowBorder {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
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
  width: 100%;
  margin-top: 2rem;
  gap: 2rem;
  position: relative;
  z-index: 2;
}

.left-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background: rgba(0, 0, 0, 0.3);
  padding: 2rem;
  border-radius: 0.5rem;
  border: 2px solid rgba(127, 255, 22, 0.2);
  backdrop-filter: blur(2px);
}

.avatar-wrapper {
  position: relative;
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.avatar-container {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgba(127, 255, 22, 0.4);
  box-shadow: 0 4px 15px rgba(127, 255, 22, 0.2);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.avatar-container:hover .avatar-image {
  transform: scale(1.05);
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(127, 255, 22, 0.1) 0%, transparent 70%);
  pointer-events: none;
}

.path-icon-wrapper {
  background: rgba(0, 0, 0, 0.8);
  padding: 0.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(127, 255, 22, 0.4);
  backdrop-filter: blur(2px);
}

.path-icon {
  width: 32px;
  height: 32px;
}

.character-info {
  margin-top: 1rem;
}

.character-name {
  font-size: 2rem;
  font-weight: 600;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  margin-bottom: 0.5rem;
}

.rank {
  font-size: 1.2rem;
  color: rgba(250, 218, 149, 0.8);
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.right-section {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: rgba(0, 0, 0, 0.3);
  padding: 2rem;
  border-radius: 0.5rem;
  border: 2px solid rgba(127, 255, 22, 0.2);
  backdrop-filter: blur(2px);
}

.details-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.modificators-section,
.spells-section {
  background: rgba(0, 0, 0, 0.2);
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 2px solid rgba(127, 255, 22, 0.2);
  backdrop-filter: blur(2px);
}

h3 {
  font-size: 1.4rem;
  margin-bottom: 1rem;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-weight: 600;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin: 0.5rem 0;
  padding: 0.75rem;
  background: rgba(127, 255, 22, 0.1);
  border-radius: 0.25rem;
  transition: all 0.3s ease;
  color: #fada95;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  border: 1px solid rgba(127, 255, 22, 0.2);
}

li:hover {
  background: rgba(127, 255, 22, 0.2);
  transform: translateX(4px);
  border-color: rgba(127, 255, 22, 0.4);
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
