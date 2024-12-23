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
          <p class="rank">Rank: {{ rank }}</p>
        </div>
      </div>

      <!-- Right Section: Details -->
      <div class="right-section">
        <div class="details-wrapper">
          <!-- Modificators -->
          <div class="modificators-section">
            <h3>Modificators</h3>
            <ul>
              <li v-for="mod in selectedModificators" :key="mod.id">{{ mod.name }}</li>
            </ul>
          </div>

          <!-- Stats -->
          <div class="stats-section">
            <h3>Stats</h3>
            <ul>
              <li v-for="stat in stats" :key="stat.name">
                <strong>{{ stat.name }}</strong>: {{ stat.value }}
              </li>
            </ul>
          </div>

          <!-- Spells -->
          <div class="spells-section">
            <h3>Spells</h3>
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
        <h2>Character Data Incomplete</h2>
        <p>The following required data is missing or incomplete:</p>
        <ul>
          <li v-for="error in validationErrors" :key="error">{{ error }}</li>
        </ul>
        <p>Please complete the character creation process to view the review.</p>
      </div>
    </div>
  </div>
</template>

<script>
import avatarPlaceholderPath from "@/assets/images/avatar/placeholder.webp";
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
  data() {
    return {
      validationErrors: [],
    };
  },
  computed: {
    isCharacterValid() {
      this.validationErrors = [];
      if (!this.character) this.validationErrors.push("Character data is missing.");
      else {
        if (!this.character.name) this.validationErrors.push("Character name is missing.");
        if (!this.character.bio || !this.character.bio.age)
          this.validationErrors.push("Character age is missing.");
        if (!this.character.bio || !this.character.bio.gender)
          this.validationErrors.push("Character gender is missing.");
        if (!this.character.path)
          this.validationErrors.push("Character path is not selected.");
        if (this.character.rank === undefined) this.validationErrors.push("Character rank is missing.");
        if (!this.character.modificators || this.character.modificators.length === 0)
          this.validationErrors.push("No modificators selected.");
        if (!this.character.stats || this.character.stats.length === 0)
          this.validationErrors.push("No stats allocated.");
        if (!this.character.spells || this.character.spells.length === 0)
          this.validationErrors.push("No spells selected.");
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
      return this.character.rank || "Unranked";
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
  color: #fff;
  font-family: Arial, sans-serif;
  max-height: 100vh;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/images/backgrounds/preview-background.webp') center/cover no-repeat;
  z-index: -1;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.9));
  z-index: -1;
}

.review-content {
  display: flex;
  width: 90%;
  margin-top: 40px;
  gap: 30px;
}

.left-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.avatar-wrapper {
  position: relative;
  margin-bottom: 20px;
}

.avatar-image {
  width: 150px;
  height: 150px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}

.character-info {
  margin-top: 10px;
}

.character-name {
  font-size: 1.6rem;
  font-weight: bold;
}

.rank {
  font-size: 1.2rem;
  color: #bbb;
}

.right-section {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.details-wrapper {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

h3 {
  font-size: 1.3rem;
  margin-bottom: 5px;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin: 5px 0;
  padding: 5px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  transition: all 0.3s;
}

li:hover {
  background: rgba(255, 255, 255, 0.2);
}

.error-message {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  color: #f44336;
  text-align: center;
  padding: 20px;
}

.error-container {
  background-color: #222;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
}

.error-container h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.error-container p {
  font-size: 1rem;
  margin: 0;
}

   /* Avatar Section */
 .avatar-wrapper {
   display: flex;
   flex-direction: column;
   align-items: center;
   gap: 10px;
 }

.avatar-container {
  position: relative;
  width: 150px;
  height: 150px;
}

.avatar-image {
  width: 100%;
  height: 100%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 0, 0, 0) 60%, rgba(0, 0, 0, 0.3));
  pointer-events: none;
}

.path-icon-wrapper {
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  padding: 5px 10px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.path-icon {
  width: 24px;
  height: 24px;
}

/* Background and Overall Layout */
.character-review {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  color: #fff;
  font-family: Arial, sans-serif;
  max-height: 100vh;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('@/assets/images/backgrounds/preview-background.webp') center/cover no-repeat;
  z-index: -1;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.9));
  z-index: -1;
}
</style>
