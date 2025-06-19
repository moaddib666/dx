<template>
  <div
      :class="{ 'is-loading': isLoading, 'is-dragging': isDragging, 'is-selected': isSelected }"
      :style="{ top: positionY + 'px', right: 'auto', left: positionX + 'px' }"
      class="game-master-character-card"
  >
    <!-- Top Tab for Drag and Drop -->
    <div
        class="top-drag-tab"
        title="Drag items here"
        @dragover.prevent
        @drop.prevent="handleItemDrop"
    >
      <span class="tab-text">Drop Items Here</span>
    </div>

    <!-- Card Header with Tab and Close Button - Always visible -->
    <div class="card-header">
      <div
          class="drag-tab"
          title="Drag to move"
          @mousedown="startDrag"
      >
        <span class="drag-handle">≡</span>
      </div>
      <h3 class="card-title" title="Click to copy character ID" @click="copyCharacterId">Character Info</h3>
      <button class="close-button" @click="closeCard">×</button>
    </div>

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

          <!-- Character Stats Radar Chart -->
          <div class="character-stats-chart">
            <CharacterStatsRadarChart :character-id="character.id"/>
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
              <img v-if="getEffectIconUrl(effect)"
                   :alt="`${effect.effect?.id || 'Effect'} - ${effect.is_permanent ? 'Permanent' : `${effect.cycle_left || effect.ends_in || 0} cycles`}${effect.description ? ` - ${effect.description}` : ''}`"
                   :src="getEffectIconUrl(effect)"
                   class="effect-icon">
              <div v-else class="effect-icon-placeholder">{{ getEffectIcon(effect) }}</div>

              <!-- Cycles count overlay -->
              <div v-if="!effect.is_permanent && (effect.cycle_left || effect.ends_in)" class="effect-cycles-overlay">
                {{ effect.cycle_left || effect.ends_in }}
              </div>
            </div>
            <div v-if="character.effects.length === 0" class="no-effects">No effects</div>
          </div>

          <!-- Attribute bars at the bottom of the avatar -->
          <div class="card-bars">
            <AttributeBar
                v-for="(attr, index) in mainAttributes"
                :key="index"
                :current="attr.current"
                :max="attr.max"
                :type="attr.name"
                class="header-attribute-bar"
            />
          </div>
        </div>
      </div>

      <!-- Bottom Section -->
      <div class="bottom-section">

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
            <h3>Inventory</h3>
            <GameMasterInventoryGrid
                :items="character.equipped_items"
                @world-item-selected="handleWorldItemSelected"
            />
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

    </div>

    <!-- Error state - Close button is still accessible -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <div class="error-message">{{ error }}</div>
      <button class="retry-button" @click="loadCharacter">Retry</button>
    </div>
  </div>
</template>

<script>
import {gameMasterCharacterService} from '@/services/GameMasterCharacterService.js';
import AttributeBar from '@/components/GameMaster/Character/AttributeBar.vue';
import GameMasterInventoryGrid from '@/components/GameMaster/Character/GameMasterInventoryGrid.vue';
import CharacterStatsRadarChart from '@/components/CharacterStatsRadarChart.vue';

export default {
  name: 'GameMasterCharacterCard',
  components: {
    AttributeBar,
    GameMasterInventoryGrid,
    CharacterStatsRadarChart
  },
  props: {
    characterId: {
      type: String,
      required: true
    },
    isSelected: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      character: null,
      isLoading: false,
      error: null,
      showTags: false,
      showBio: false,
      isUnmounted: false,
      // Position tracking for draggable functionality
      isDragging: false,
      dragStartX: 0,
      dragStartY: 0,
      positionX: 0, // Will be set to center in created hook
      positionY: 0  // Will be set to center in created hook
    };
  },
  computed: {
    // Filter attributes to only show main ones (Health, Energy, Action Points)
    mainAttributes() {
      if (!this.character || !this.character.attributes) return [];

      const mainAttributeNames = ['Health', 'Energy', 'Action Points'];
      return this.character.attributes.filter(attr =>
          mainAttributeNames.includes(attr.name)
      );
    }
  },
  async created() {
    // Set up event listeners
    gameMasterCharacterService.on('loadingStarted', this.onLoadingStarted);
    gameMasterCharacterService.on('characterLoaded', this.onCharacterLoaded);
    gameMasterCharacterService.on('loadingFailed', this.onLoadingFailed);

    // Center the card on the screen
    this.centerCard();

    // Load character data
    await this.loadCharacter();
  },
  beforeUnmount() {
    // Set the unmounted flag to prevent further updates
    this.isUnmounted = true;

    // Clean up event listeners
    gameMasterCharacterService.off('loadingStarted', this.onLoadingStarted);
    gameMasterCharacterService.off('characterLoaded', this.onCharacterLoaded);
    gameMasterCharacterService.off('loadingFailed', this.onLoadingFailed);
  },
  methods: {
    // Event handlers
    onLoadingStarted(characterId) {
      if (this.isUnmounted) return;

      if (characterId === this.characterId) {
        this.isLoading = true;
        this.error = null;
      }
    },

    onCharacterLoaded(character) {
      if (this.isUnmounted) return;

      if (character && character.id === this.characterId) {
        this.character = character;
        this.isLoading = false;
      }
    },

    onLoadingFailed({characterId, error}) {
      if (this.isUnmounted) return;

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
        if (this.isUnmounted) return;

        this.isLoading = true;
        this.error = null;

        const character = await gameMasterCharacterService.getCharacter(this.characterId);

        // Check again if component was unmounted during the async operation
        if (this.isUnmounted) return;

        this.character = character;
      } catch (error) {
        if (this.isUnmounted) return;

        console.error('Error loading character:', error);
        this.error = error.message || 'Failed to load character data';
      } finally {
        if (this.isUnmounted) return;

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

    // Handle world item selected from inventory grid
    handleWorldItemSelected(worldItemId) {
      if (!worldItemId) return;

      // Find the item with the matching world item ID
      const selectedItem = this.character.equipped_items.find(
          item => item.world_item && item.world_item.id === worldItemId
      );

      if (selectedItem) {
        this.$emit('item-selected', selectedItem);
      }
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
      if (!attribute) return 0;

      // Check for current and max properties (new data structure)
      if (attribute.current !== undefined && attribute.max) {
        return (attribute.current / attribute.max) * 100;
      }

      // Fallback to current_value and max_value (old data structure)
      if (attribute.current_value !== undefined && attribute.max_value) {
        return (attribute.current_value / attribute.max_value) * 100;
      }

      return 0;
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

    getEffectIconUrl(effect) {
      if (!effect) return null;

      // Check for icon in different possible locations
      if (effect.effect && effect.effect.icon) return effect.effect.icon;
      if (effect.icon) return effect.icon;

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
    },

    // Handle item drop from drag and drop operation
    handleItemDrop(event) {
      try {
        // Get the dropped data
        const itemData = event.dataTransfer.getData('text/plain');

        if (!itemData) {
          console.warn('No data received from drop event');
          return;
        }

        // Try to parse the item data
        const item = JSON.parse(itemData);

        if (!item || !item.id) {
          console.warn('Invalid item data received:', itemData);
          return;
        }

        console.log('Item dropped:', item);

        // Emit an event to notify parent components
        this.$emit('item-dropped', item, this.characterId);

        // Show a visual feedback
        const tab = event.currentTarget;
        tab.classList.add('drop-success');

        // Remove the visual feedback after a short delay
        setTimeout(() => {
          tab.classList.remove('drop-success');
        }, 500);
      } catch (error) {
        console.error('Error handling dropped item:', error);
      }
    },

    // Dragging functionality
    startDrag(event) {
      // Only handle left mouse button
      if (event.button !== 0) return;

      // Set dragging flag
      this.isDragging = true;

      // Store the initial mouse position
      this.dragStartX = event.clientX;
      this.dragStartY = event.clientY;

      // Add event listeners for drag and drop
      document.addEventListener('mousemove', this.drag);
      document.addEventListener('mouseup', this.stopDrag);

      // Prevent text selection during drag
      event.preventDefault();
    },

    drag(event) {
      if (!this.isDragging) return;

      // Calculate the new position
      const deltaX = event.clientX - this.dragStartX;
      const deltaY = event.clientY - this.dragStartY;

      // Update the position
      this.positionX += deltaX;
      this.positionY += deltaY;

      // Keep the card within the viewport
      this.positionX = Math.max(0, Math.min(window.innerWidth - 300, this.positionX));
      this.positionY = Math.max(0, Math.min(window.innerHeight - 100, this.positionY));

      // Update the starting position for the next move
      this.dragStartX = event.clientX;
      this.dragStartY = event.clientY;
    },

    stopDrag() {
      // Reset dragging flag
      this.isDragging = false;

      // Remove event listeners
      document.removeEventListener('mousemove', this.drag);
      document.removeEventListener('mouseup', this.stopDrag);
    },

    // Center the card on the screen
    centerCard() {
      // Card width is 300px as defined in CSS
      const cardWidth = 300;
      const cardHeight = 400; // Approximate height, adjust as needed

      // Calculate center position
      this.positionX = Math.max(0, (window.innerWidth - cardWidth) / 2);
      this.positionY = Math.max(0, (window.innerHeight - cardHeight) / 2);
    },

    // Copy character ID to clipboard
    copyCharacterId() {
      if (!this.characterId) return;

      // Copy to clipboard
      navigator.clipboard.writeText(this.characterId)
          .then(() => {
            // Show feedback
            const cardTitle = document.querySelector('.card-title');
            if (cardTitle) {
              // Store original text
              const originalText = cardTitle.textContent;

              // Change text to show feedback
              cardTitle.textContent = 'ID Copied!';
              cardTitle.classList.add('copied');

              // Restore original text after a delay
              setTimeout(() => {
                cardTitle.textContent = originalText;
                cardTitle.classList.remove('copied');
              }, 1500);
            }
          })
          .catch(err => {
            console.error('Failed to copy character ID:', err);
          });
    }
  }
};
</script>

<style scoped>
.game-master-character-card {
  position: absolute;
  /* Position is now controlled by inline style */
  width: 300px;
  max-height: calc(100vh - 40px);
  background: rgba(30, 30, 30, 0.95);
  border: 2px solid #555;
  border-radius: 12px;
  color: #ffffff;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.7);
  z-index: 900; /* Lower z-index to prevent interference with underlying menus */
  display: flex;
  flex-direction: column;
  overflow: hidden;
  /* Add transition for smoother movement */
  transition: box-shadow 0.2s ease;
}

/* Add a subtle shadow effect when dragging */
.game-master-character-card.is-dragging {
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.8);
}

/* Apply blue border only to selected character */
.game-master-character-card.is-selected {
  border: 2px solid #1E90FF;
}

/* Top Tab for Drag and Drop */
.top-drag-tab {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: #1E90FF;
  color: white;
  padding: 5px 15px;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  z-index: 999;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
}

.top-drag-tab:hover {
  background: #4FC3F7;
  padding-top: 8px;
}

.tab-text {
  font-size: 0.8rem;
  font-weight: bold;
}

/* Visual feedback for successful drop */
.top-drag-tab.drop-success {
  background: #4CAF50;
  transform: translateX(-50%) scale(1.05);
  box-shadow: 0 -2px 8px rgba(76, 175, 80, 0.5);
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  background: #333;
  border-bottom: 1px solid #555;
  z-index: 10;
}

.drag-tab {
  cursor: grab;
  padding: 0.25rem 0.5rem;
  margin-right: 0.5rem;
  border-radius: 4px;
  background: #444;
  transition: background 0.2s ease;
}

/* Change cursor when actively dragging */
.is-dragging .drag-tab {
  cursor: grabbing;
}

.drag-tab:hover {
  background: #555;
}

.drag-handle {
  color: #aaa;
  font-size: 1rem;
  font-weight: bold;
}

.card-title {
  flex: 1;
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: #1E90FF;
  cursor: pointer;
  transition: all 0.2s ease;
}

.card-title:hover {
  color: #4FC3F7;
}

.card-title.copied {
  color: #4CAF50;
  font-weight: bold;
  transform: scale(1.05);
}

/* Loading state */
.loading-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  height: 300px;
  overflow-y: auto;
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
  overflow-y: auto;
  max-height: calc(100vh - 120px);
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

.header-attribute-bar {
  margin: 0;
  height: 0.7rem;
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
  width: 30px; /* Reduced to 0.75 of original size (40px * 0.75 = 30px) */
  height: 30px; /* Reduced to 0.75 of original size (40px * 0.75 = 30px) */
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.effect-icon-container:hover {
  transform: scale(1.05);
}

.effect-icon {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.effect-icon-placeholder {
  font-size: 0.9rem; /* Reduced from 1.2rem to match smaller container */
}

/* Cycles count overlay */
.effect-cycles-overlay {
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
  gap: 0.5rem;
}

/* Common section styling */
.currency-section {
  background: rgba(20, 20, 20, 0.5);
  border-radius: 8px;
  padding: 0.75rem;
  border: 1px solid rgba(30, 144, 255, 0.2);
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
}

/* Minimalistic inventory section */
.inventory-section {
  background: rgba(20, 20, 20, 0.5);
  border-radius: 4px;
  padding: 0.25rem;
  border: 1px solid rgba(30, 144, 255, 0.2);
  margin-bottom: 0.5rem;
}

.inventory-section h3,
.currency-section h3 {
  font-size: 0.8rem;
  margin: 0 0 0.25rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #1E90FF;
  text-align: center;
  border-bottom: 1px solid rgba(30, 144, 255, 0.2);
  padding-bottom: 0.25rem;
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
  overflow-y: auto;
  /* Ensure content doesn't overlap with header where close button is */
  margin-top: 10px;
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

/* Scrollbar Styling - Aligned with other scrolls on the page */
.card-content::-webkit-scrollbar,
.loading-overlay::-webkit-scrollbar,
.error-state::-webkit-scrollbar,
.bio-background-text::-webkit-scrollbar,
.shields-container::-webkit-scrollbar,
.effects-container::-webkit-scrollbar {
  width: 6px;
}

.card-content::-webkit-scrollbar-track,
.loading-overlay::-webkit-scrollbar-track,
.error-state::-webkit-scrollbar-track,
.bio-background-text::-webkit-scrollbar-track,
.shields-container::-webkit-scrollbar-track,
.effects-container::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.card-content::-webkit-scrollbar-thumb,
.loading-overlay::-webkit-scrollbar-thumb,
.error-state::-webkit-scrollbar-thumb,
.bio-background-text::-webkit-scrollbar-thumb,
.shields-container::-webkit-scrollbar-thumb,
.effects-container::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}

.card-content::-webkit-scrollbar-thumb:hover,
.loading-overlay::-webkit-scrollbar-thumb:hover,
.error-state::-webkit-scrollbar-thumb:hover,
.bio-background-text::-webkit-scrollbar-thumb:hover,
.shields-container::-webkit-scrollbar-thumb:hover,
.effects-container::-webkit-scrollbar-thumb:hover {
  background: #666;
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
