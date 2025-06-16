<template>
  <div :class="{ 'is-loading': isLoading }" class="game-master-character-card">
    <!-- Loading overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <div class="loading-text">Loading character data...</div>
    </div>

    <!-- Card content -->
    <div v-else-if="character" class="card-content">
      <!-- Top Section -->
      <div class="top-section">
        <!-- Character header with avatar as background -->
        <div :style="getHeaderBackgroundStyle()"
             class="character-header">
          <!-- Character name overlay -->
          <div class="character-name-overlay">
            <h2 class="character-name">{{ character.name }}</h2>
            <span class="character-type">{{ character.npc ? 'NPC' : 'Player' }}</span>
          </div>

          <!-- Left side: Shield icons -->
          <div class="shields-container">
            <div v-for="shield in character.shields" :key="shield.id" class="shield-icon-container">
              <img v-if="getShieldIconUrl(shield)"
                   :alt="`${getShieldName(shield)} - Health: ${getShieldHealth(shield)}, Efficiency: ${formatEfficiency(getShieldEfficiency(shield))}, ${getShieldCycles(shield) ? getShieldCycles(shield) + ' cycles' : 'Permanent'}`"
                   :src="getShieldIconUrl(shield)"
                   class="shield-icon">
              <div v-else class="shield-icon-placeholder">🛡️</div>

              <!-- Cycles count overlay -->
              <div v-if="getShieldCycles(shield)" class="shield-cycles-overlay">{{ getShieldCycles(shield) }}</div>
            </div>
            <div v-if="character.shields.length === 0" class="no-shields">No shields</div>
          </div>

          <!-- Right side: Effect icons -->
          <div class="effects-container">
            <div v-for="effect in character.effects" :key="effect.id" class="effect-icon-container">
              <div class="effect-icon">{{ getEffectIcon(effect) }}</div>

              <!-- Effect details on hover -->
              <div class="effect-details">
                <div class="effect-name">{{ effect.name }}</div>
                <div class="effect-duration">
                  {{ effect.is_permanent ? 'Permanent' : `${effect.remaining_cycles} cycles` }}
                </div>
                <div v-if="effect.description" class="effect-description">{{ effect.description }}</div>
              </div>
            </div>
            <div v-if="character.effects.length === 0" class="no-effects">No effects</div>
          </div>
        </div>
      </div>

      <!-- Bottom Section -->
      <div class="bottom-section">
        <!-- Character attributes -->
        <div class="attributes-section">
          <h3>Attributes</h3>
          <div class="attributes-list">
            <div v-for="attr in character.attributes" :key="attr.id" class="attribute-item">
              <div class="attribute-name">{{ attr.name }}</div>
              <div class="attribute-bar-container">
                <div :style="{ width: `${calculateAttributePercentage(attr)}%` }" class="attribute-bar"></div>
              </div>
              <div class="attribute-value">{{ attr.current_value }} / {{ attr.max_value }}</div>
            </div>
          </div>
        </div>

        <!-- Biography toggle button -->
        <button v-if="character.biography"
                :title="showBio ? 'Hide Biography' : 'Show Biography'"
                class="toggle-button bio-toggle"
                @click="showBio = !showBio">
          <span class="toggle-icon">📜</span>
        </button>

        <!-- Biography Section (hidden by default) -->
        <div v-if="character.biography && showBio" class="biography-section">
          <div class="biography-content">
            <div v-if="character.biography.name" class="bio-field">
              <span class="bio-label">Full Name:</span>
              <span class="bio-value">{{ character.biography.name }}</span>
            </div>
            <div v-if="character.biography.age" class="bio-field">
              <span class="bio-label">Age:</span>
              <span class="bio-value">{{ character.biography.age }}</span>
            </div>
            <div v-if="character.biography.gender" class="bio-field">
              <span class="bio-label">Gender:</span>
              <span class="bio-value">{{ character.biography.gender }}</span>
            </div>
            <div v-if="character.biography.appearance" class="bio-field">
              <span class="bio-label">Appearance:</span>
              <span class="bio-value">{{ character.biography.appearance }}</span>
            </div>
            <div v-if="character.biography.personality" class="bio-field">
              <span class="bio-label">Personality:</span>
              <span class="bio-value">{{ character.biography.personality }}</span>
            </div>
            <div v-if="character.biography.background" class="bio-field bio-background">
              <span class="bio-label">Background:</span>
              <div class="bio-background-text">{{ character.biography.background }}</div>
            </div>
          </div>
        </div>

        <!-- External Sections -->
        <div class="external-sections">
          <!-- Inventory items -->
          <div class="inventory-section">
            <h3>Equipped Items</h3>
            <div class="items-grid">
              <div v-for="item in character.equipped_items" :key="item.id" class="item-card"
                   @click="emitItemSelected(item)">
                <div class="item-icon">{{ getItemIcon(item) }}</div>
                <div class="item-info">
                  <div class="item-name">{{ item.name }}</div>
                  <div class="item-type">{{ formatItemType(item.type) }}</div>
                </div>
              </div>
              <div v-if="character.equipped_items.length === 0" class="no-items">No equipped items</div>
            </div>
          </div>

          <!-- Currency information -->
          <div class="currency-section">
            <h3>Currency</h3>
            <div class="currency-list">
              <div v-for="currency in character.tokens" :key="currency.id" class="currency-item">
                <div class="currency-icon">{{ getCurrencyIcon(currency) }}</div>
                <div class="currency-info">
                  <div class="currency-name">{{ currency.name }}</div>
                  <div class="currency-amount">{{ currency.amount }}</div>
                </div>
              </div>
              <div v-if="character.tokens.length === 0" class="no-currency">No currency</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Close button -->
      <button class="close-button" @click="closeCard">×</button>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <div class="error-message">{{ error }}</div>
      <button class="retry-button" @click="loadCharacter">Retry</button>
    </div>
  </div>
</template>

<script>
import {gameMasterCharacterService} from '@/services/GameMasterCharacterService.js';

export default {
  name: 'GameMasterCharacterCard',
  props: {
    characterId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      character: null,
      isLoading: false,
      error: null,
      showTags: false,
      showBio: false
    };
  },
  async created() {
    // Set up event listeners
    gameMasterCharacterService.on('loadingStarted', this.onLoadingStarted);
    gameMasterCharacterService.on('characterLoaded', this.onCharacterLoaded);
    gameMasterCharacterService.on('loadingFailed', this.onLoadingFailed);

    // Load character data
    await this.loadCharacter();
  },
  beforeUnmount() {
    // Clean up event listeners
    gameMasterCharacterService.off('loadingStarted', this.onLoadingStarted);
    gameMasterCharacterService.off('characterLoaded', this.onCharacterLoaded);
    gameMasterCharacterService.off('loadingFailed', this.onLoadingFailed);
  },
  methods: {
    // Event handlers
    onLoadingStarted(characterId) {
      if (characterId === this.characterId) {
        this.isLoading = true;
        this.error = null;
      }
    },

    onCharacterLoaded(character) {
      if (character && character.id === this.characterId) {
        this.character = character;
        this.isLoading = false;
      }
    },

    onLoadingFailed({characterId, error}) {
      if (characterId === this.characterId) {
        this.error = error.message || 'Failed to load character data';
        this.isLoading = false;
      }
    },

    // Get background style for the header
    getHeaderBackgroundStyle() {
      if (this.character?.biography?.avatar) {
        return {
          backgroundImage: `url(${this.character.biography.avatar})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        };
      } else {
        // Fallback gradient background if no avatar
        return {
          background: 'linear-gradient(to bottom, #1E90FF, #000)'
        };
      }
    },

    // Load character data
    async loadCharacter() {
      try {
        this.isLoading = true;
        this.error = null;
        this.character = await gameMasterCharacterService.getCharacter(this.characterId);
      } catch (error) {
        console.error('Error loading character:', error);
        this.error = error.message || 'Failed to load character data';
      } finally {
        this.isLoading = false;
      }
    },

    // Close the card
    closeCard() {
      gameMasterCharacterService.closeCharacter(this.characterId);
      this.$emit('close');
    },

    // Emit item selected event
    emitItemSelected(item) {
      this.$emit('item-selected', item);
    },

    // Helper methods
    getCharacterInitials(name) {
      if (!name) return '??';
      return name.substring(0, 2).toUpperCase();
    },

    calculateShieldPercentage(shield) {
      if (!shield) return 0;

      // If we have the new shield data structure
      if (shield.health !== undefined && shield.shield && shield.shield.base_health) {
        return (shield.health / shield.shield.base_health) * 100;
      }

      // Fallback to the old structure
      if (shield.current_value !== undefined && shield.max_value) {
        return (shield.current_value / shield.max_value) * 100;
      }

      return 0;
    },

    calculateAttributePercentage(attribute) {
      if (!attribute || !attribute.max_value) return 0;
      return (attribute.current_value / attribute.max_value) * 100;
    },

    getEffectIcon(effect) {
      // Simple mapping of effect types to icons
      const icons = {
        'buff': '⬆️',
        'debuff': '⬇️',
        'damage': '🔥',
        'heal': '💚',
        'shield': '🛡️',
        'stun': '💫',
        'poison': '☠️'
      };

      // Try to determine effect type from name or description
      const effectType = effect.effect_type || this.guessEffectType(effect);
      return icons[effectType] || '✨';
    },

    guessEffectType(effect) {
      const name = (effect.name || '').toLowerCase();
      const description = (effect.description || '').toLowerCase();

      if (name.includes('buff') || description.includes('increase') || description.includes('boost')) return 'buff';
      if (name.includes('debuff') || description.includes('decrease') || description.includes('reduce')) return 'debuff';
      if (name.includes('damage') || description.includes('damage')) return 'damage';
      if (name.includes('heal') || description.includes('heal')) return 'heal';
      if (name.includes('shield') || description.includes('shield')) return 'shield';
      if (name.includes('stun') || description.includes('stun')) return 'stun';
      if (name.includes('poison') || description.includes('poison')) return 'poison';

      return 'buff'; // Default
    },

    getItemIcon(item) {
      // Simple mapping of item types to icons
      const icons = {
        'weapon': '⚔️',
        'armor': '🛡️',
        'potion': '🧪',
        'scroll': '📜',
        'food': '🍖',
        'key': '🔑',
        'tool': '🔧',
        'gem': '💎',
        'book': '📚'
      };

      const itemType = (item.type || '').toLowerCase();
      return icons[itemType] || '📦';
    },

    getCurrencyIcon(currency) {
      // Simple mapping of currency types to icons
      const icons = {
        'gold': '💰',
        'silver': '🥈',
        'copper': '🥉',
        'gem': '💎',
        'token': '🪙'
      };

      const currencyType = (currency.name || '').toLowerCase();
      for (const [type, icon] of Object.entries(icons)) {
        if (currencyType.includes(type)) return icon;
      }

      return '💰'; // Default
    },

    formatItemType(type) {
      if (!type) return 'Item';

      // Convert camelCase or snake_case to Title Case with spaces
      return type
          // Insert a space before all uppercase letters
          .replace(/([A-Z])/g, ' $1')
          // Replace underscores with spaces
          .replace(/_/g, ' ')
          // Capitalize first letter
          .replace(/^./, str => str.toUpperCase())
          // Trim any extra spaces
          .trim();
    },

    parseTags(tags) {
      if (!tags) return [];
      if (Array.isArray(tags)) return tags;
      if (typeof tags === 'string') return tags.split(',').map(tag => tag.trim());
      if (typeof tags === 'object') return Object.values(tags);
      return [];
    },

    getShieldName(shield) {
      if (!shield) return 'Shield';

      // Check for name in different possible locations
      if (shield.name) return shield.name;
      if (shield.shield && shield.shield.id) return shield.shield.id;

      return 'Shield';
    },

    getShieldIconUrl(shield) {
      if (!shield) return null;

      // Check for icon in different possible locations
      if (shield.icon) return shield.icon;
      if (shield.shield && shield.shield.icon) return shield.shield.icon;

      return null;
    },

    getShieldHealth(shield) {
      if (!shield) return 0;

      // Check for health in different possible locations
      if (shield.health !== undefined) return shield.health;
      if (shield.current_value !== undefined) return shield.current_value;

      return 0;
    },

    getShieldEfficiency(shield) {
      if (!shield) return 0;

      // Check for efficiency in different possible locations
      if (shield.efficiency !== undefined) return shield.efficiency;
      if (shield.shield && shield.shield.base_efficiency !== undefined) {
        return shield.shield.base_efficiency;
      }

      return 1; // Default efficiency is 1 (100%)
    },

    getShieldCycles(shield) {
      if (!shield) return null;

      // Check for cycles in different possible locations
      if (shield.cycles_left !== undefined) return shield.cycles_left;
      if (shield.remaining_cycles !== undefined) return shield.remaining_cycles;

      return null;
    },

    formatEfficiency(efficiency) {
      if (efficiency === undefined || efficiency === null) return '0%';

      // Convert to percentage and round to nearest integer
      const percentage = Math.round(efficiency * 100);
      return `${percentage}%`;
    },

    handleAvatarError(event) {
      // Replace the broken image with the avatar placeholder
      event.target.style.display = 'none';
      event.target.parentNode.querySelector('.avatar-placeholder').style.display = 'flex';
    }
  }
};
</script>

<style scoped>
.game-master-character-card {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 300px;
  max-height: calc(100vh - 40px);
  background: rgba(30, 30, 30, 0.95);
  border: 2px solid #1E90FF;
  border-radius: 12px;
  color: #ffffff;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.7);
  overflow-y: auto;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

/* Loading state */
.loading-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  height: 300px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #1E90FF;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

.loading-text {
  font-size: 1rem;
  color: #ccc;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Card content */
.card-content {
  display: flex;
  flex-direction: column;
  padding: 0.75rem;
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
  padding-top: 175%; /* 7/4 = 1.75 or 175% */
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
  align-items: center;
  padding: 3.5rem 0.2rem 0.5rem;
  overflow-y: auto; /* Allow scrolling if many shields */
}

.shield-icon-container {
  position: relative;
  width: 30px; /* Reduced to 0.75 of original size (40px * 0.75 = 30px) */
  height: 30px; /* Reduced to 0.75 of original size (40px * 0.75 = 30px) */
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.shield-icon-container:hover {
  transform: scale(1.05);
}

.shield-icon {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.shield-icon-placeholder {
  font-size: 0.9rem; /* Reduced from 1.2rem to match smaller container */
}

/* Cycles count overlay */
.shield-cycles-overlay {
  position: absolute;
  top: -5px;
  right: -5px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 50%;
  min-width: 16px;
  height: 16px;
  font-size: 0.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 2px;
  z-index: 5;
}

.no-shields {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  text-align: center;
  font-size: 0.7rem;
  color: #888;
  font-style: italic;
  transform: translateY(-50%);
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
  align-items: center;
  padding: 3.5rem 0.2rem 0.5rem;
  overflow-y: auto; /* Allow scrolling if many effects */
}

.effect-icon-container {
  position: relative;
  width: 40px;
  height: 40px;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.effect-icon-container:hover {
  transform: scale(1.05);
}

.effect-icon {
  font-size: 1.2rem;
  color: #fff;
}

/* Effect details on hover */
.effect-details {
  position: absolute;
  right: 45px;
  top: 0;
  width: 150px;
  background: rgba(0, 0, 0, 0.7);
  padding: 0.3rem;
  z-index: 10;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s ease;
  pointer-events: none;
}

.effect-icon-container:hover .effect-details {
  opacity: 1;
  visibility: visible;
}

.effect-name {
  font-weight: bold;
  font-size: 0.7rem;
  margin-bottom: 0.2rem;
  color: #fff;
}

.effect-duration {
  font-size: 0.6rem;
  color: #ccc;
  margin-bottom: 0.1rem;
}

.effect-description {
  font-size: 0.6rem;
  color: #aaa;
  line-height: 1.2;
}

.no-effects {
  position: absolute;
  top: 50%;
  right: 0;
  width: 100%;
  text-align: center;
  font-size: 0.7rem;
  color: #888;
  font-style: italic;
  transform: translateY(-50%);
}

/* Bottom Section */
.bottom-section {
  display: flex;
  flex-direction: column;
  padding-top: 0.5rem;
}

/* Attributes section */
.attributes-section {
  margin-bottom: 1rem;
  background: rgba(20, 20, 20, 0.5);
  border-radius: 8px;
  padding: 0.75rem;
  border: 1px solid rgba(30, 144, 255, 0.2);
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
}

.attributes-section h3 {
  font-size: 0.9rem;
  margin: 0 0 0.75rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #1E90FF;
  text-align: center;
  border-bottom: 1px solid rgba(30, 144, 255, 0.2);
  padding-bottom: 0.5rem;
}

.attributes-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.attribute-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.attribute-name {
  width: 70px;
  font-size: 0.8rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
}

.attribute-bar-container {
  flex: 1;
  height: 10px;
  background: transparent;
  overflow: hidden;
}

.attribute-bar {
  height: 100%;
  background: #1E90FF;
  transition: width 0.3s ease;
}

.attribute-value {
  width: 60px;
  font-size: 0.75rem;
  text-align: right;
  color: rgba(255, 255, 255, 0.8);
  font-family: monospace;
}

/* Biography section */
.biography-section {
  margin: 0.5rem 0;
  background: rgba(20, 20, 20, 0.5);
  border-radius: 6px;
  padding: 0.5rem;
  border: 1px solid rgba(30, 144, 255, 0.2);
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.3);
}

.biography-content {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.bio-field {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  font-size: 0.75rem;
  line-height: 1.3;
}

.bio-label {
  color: #aaa;
  font-weight: 500;
  min-width: 70px;
}

.bio-value {
  color: #fff;
  flex: 1;
}

.bio-background {
  flex-direction: column;
}

.bio-background-text {
  margin-top: 0.2rem;
  color: #ddd;
  font-size: 0.7rem;
  line-height: 1.4;
  background: rgba(0, 0, 0, 0.2);
  padding: 0.4rem;
  border-radius: 3px;
  max-height: 80px;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* External sections */
.external-sections {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Common section styling */
.inventory-section,
.currency-section {
  background: rgba(20, 20, 20, 0.5);
  border-radius: 8px;
  padding: 0.75rem;
  border: 1px solid rgba(30, 144, 255, 0.2);
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
}

.inventory-section h3,
.currency-section h3 {
  font-size: 0.9rem;
  margin: 0 0 0.75rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #1E90FF;
  text-align: center;
  border-bottom: 1px solid rgba(30, 144, 255, 0.2);
  padding-bottom: 0.5rem;
}

/* Items grid */
.items-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.item-card {
  background: rgba(30, 30, 30, 0.7);
  border-radius: 6px;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.item-card:hover {
  background: rgba(40, 40, 40, 0.8);
  border-color: rgba(30, 144, 255, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.item-icon {
  font-size: 1.3rem;
  color: #1E90FF;
}

.item-info {
  flex: 1;
  overflow: hidden;
}

.item-name {
  font-weight: bold;
  font-size: 0.8rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: rgba(255, 255, 255, 0.9);
}

.item-type {
  font-size: 0.7rem;
  color: #aaa;
}

.no-items {
  grid-column: span 2;
  text-align: center;
  padding: 0.75rem;
  color: #888;
  font-style: italic;
  background: rgba(30, 30, 30, 0.3);
  border-radius: 6px;
  border: 1px dashed rgba(255, 255, 255, 0.1);
}

/* Currency list */
.currency-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.currency-item {
  background: rgba(30, 30, 30, 0.7);
  border-radius: 6px;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 100px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.currency-item:hover {
  background: rgba(40, 40, 40, 0.8);
  border-color: rgba(255, 215, 0, 0.4); /* Gold color for currency */
}

.currency-icon {
  font-size: 1.1rem;
  color: gold;
}

.currency-info {
  flex: 1;
}

.currency-name {
  font-size: 0.75rem;
  color: #ccc;
}

.currency-amount {
  font-weight: bold;
  font-size: 0.85rem;
  color: gold;
}

.no-currency {
  width: 100%;
  text-align: center;
  padding: 0.75rem;
  color: #888;
  font-style: italic;
  background: rgba(30, 30, 30, 0.3);
  border-radius: 6px;
  border: 1px dashed rgba(255, 255, 255, 0.1);
}

/* Close button */
.close-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  z-index: 10;
}

.close-button:hover {
  background: rgba(255, 50, 50, 0.8);
  border-color: rgba(255, 255, 255, 0.4);
  transform: scale(1.1);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.4);
}

/* Error state */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  height: 300px;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-message {
  text-align: center;
  margin-bottom: 1rem;
  color: #ff6b6b;
}

.retry-button {
  padding: 0.5rem 1rem;
  background: #1E90FF;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s ease;
}

.retry-button:hover {
  background: #1a7fd1;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .game-master-character-card {
    width: 300px;
  }

  .items-grid {
    grid-template-columns: 1fr;
  }

  .no-items {
    grid-column: span 1;
  }
}
</style>
