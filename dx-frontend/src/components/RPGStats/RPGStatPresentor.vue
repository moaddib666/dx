<script>
import StatsGameService from "@/services/statService.js";
import DiceNRolls from "@/components/Dice/DiceNRolls.vue";
import SwapIcon from "@/components/icons/Swap.vue";

export default {
  name: "RPGStatPresentor",
  components: {SwipeIcon: SwapIcon, DiceNRolls},
  props: {
    allowResetBaseStats: {
      type: Boolean,
      required: false,
    },
    stat: {
      type: Object,
      required: true,
    },
    editable: {
      type: Boolean,
      default: false, // Enable or disable value editing
    },
  },
  data() {
    return {
      statsService: StatsGameService,
    };
  },
  computed: {
    // Calculate the base value from dice rolls
    baseValue() {
      if (!this.stat.dice_rolls || this.stat.dice_rolls.length === 0) {
        return this.stat.base_value || 0;
      }
      // Use the same calculation as DiceNRolls component
      const fadeCount = 1; // Assuming 1 dice is faded out
      const sorted = [...this.stat.dice_rolls.map(d => d.dice_side)].sort((a, b) => a - b);
      return sorted.slice(fadeCount).reduce((sum, roll) => sum + roll, 0);
    },

    // Calculate the total value (base + modifier)
    totalValue() {
      return this.baseValue + (this.stat.additional_value || 0);
    },

    // Get modifier value
    modifierValue() {
      return this.stat.additional_value || 0;
    },

    // Format the modifier with appropriate color class
    modifierText() {
      const additional = this.stat.additional_value || 0;
      if (additional === 0) {
        return '';
      }
      return additional > 0 ? `+${additional}` : `${additional}`;
    },

    // Get modifier color class
    modifierColorClass() {
      const additional = this.stat.additional_value || 0;
      if (additional > 0) return 'modifier-positive';
      if (additional < 0) return 'modifier-negative';
      return '';
    }
  },
};
</script>

<template>
  <div class="stat-presenter">
    <div class="left-section">
      <img
          class="stat-icon"
          :src="statsService.getCachedStatImage(stat.name)"
          :alt="stat.name"
          :title="stat.name"
      />
      <span class="stat-name">{{ stat.name }}</span>
    </div>
    <div class="right-section">
      <span v-if="modifierText" class="modifier" :class="modifierColorClass">{{ modifierText }}</span>
      <DiceNRolls :dice-rolls="stat.dice_rolls" :stat="stat.name" class="dice-results"/>
      <SwipeIcon @click="$emit('switchBaseStats', stat.id)" class="swap-icon" v-if="allowResetBaseStats"/>
    </div>
  </div>
</template>

<style scoped>
.stat-presenter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.3rem;
  padding: 0.3rem;
  gap: 0.25rem;
  transition: all 0.3s ease;
}

.stat-presenter:hover {
  border-color: rgba(127, 255, 22, 0.5);
  background: rgba(0, 0, 0, 0.6);
}

.left-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.right-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-left: auto;
}

.stat-icon {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  object-fit: contain;
  border: 2px solid rgba(127, 255, 22, 0.3);
  flex-shrink: 0;
}

.stat-name {
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.64rem;
  font-weight: 600;
  color: #fada95;
  text-transform: capitalize;
  max-width: 7.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dice-results {
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.modifier {
  font-size: 0.7rem;
  font-weight: 600;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  border-radius: 0.2rem;
  padding: 0.1rem 0.25rem;
  border: 1px solid;
}

.modifier-positive {
  color: #22c55e;
  background: rgba(34, 197, 94, 0.1);
  border-color: rgba(34, 197, 94, 0.3);
}

.modifier-negative {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
}

.swap-icon {
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  color: rgba(127, 255, 22, 0.8);
}

.swap-icon:hover {
  color: #7fff16;
  transform: scale(1.1);
}
</style>