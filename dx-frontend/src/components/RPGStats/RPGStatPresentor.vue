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
};
</script>

<template>
  <div class="stat-presenter">
    <img
        class="stat-icon"
        :src="statsService.getCachedStatImage(stat.name)"
        :alt="stat.name"
        :title="stat.name"
    />
    <span class="stat-name">{{ stat.name }}</span>
    <DiceNRolls  :dice-rolls="stat.dice_rolls" :stat="stat.name" class="base-value"/>
    <SwipeIcon @click="$emit('switchBaseStats', stat.id)" class="swap-icon" v-if="allowResetBaseStats"/>

    <div class="stat-value">
<!--      <button-->
<!--          class="adjust-button"-->
<!--          :disabled="!editable"-->
<!--          @click="$emit('decrement', stat.id)"-->
<!--      >-->
<!--        &lt;-->
<!--      </button>-->
      <span class="value"> + {{ stat.additional_value }}</span>
<!--      <button-->
<!--          class="adjust-button"-->
<!--          :disabled="!editable"-->
<!--          @click="$emit('increment', stat.id)"-->
<!--      >-->
<!--        &gt;-->
<!--      </button>-->
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
  border-radius: 0.4rem;
  padding: 0.4rem;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.stat-presenter:hover {
  border-color: rgba(127, 255, 22, 0.5);
  background: rgba(0, 0, 0, 0.6);
}

.stat-icon {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  object-fit: contain;
  border: 2px solid rgba(127, 255, 22, 0.3);
  flex-shrink: 0;
}

.stat-name {
  flex: 1;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
  font-size: 0.85rem;
  font-weight: 600;
  color: #fada95;
  text-transform: capitalize;
  max-width: 10rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.stat-value {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.adjust-button {
  background: rgba(127, 255, 22, 0.2);
  color: #7fff16;
  border: 1px solid rgba(127, 255, 22, 0.3);
  border-radius: 0.3rem;
  padding: 0.2rem 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}

.adjust-button:disabled {
  cursor: not-allowed;
  opacity: 0.3;
  border-color: rgba(127, 255, 22, 0.1);
}

.adjust-button:not(:disabled):hover {
  background: rgba(127, 255, 22, 0.4);
  border-color: #7fff16;
}

.value {
  font-size: 1rem;
  font-weight: 600;
  color: #fada95;
  min-width: 2.5rem;
  text-align: center;
  background: rgba(250, 218, 149, 0.1);
  border: 1px solid rgba(250, 218, 149, 0.3);
  border-radius: 0.3rem;
  padding: 0.2rem 0.4rem;
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
}


.base-value {
  font-family: 'Cinzel', 'Times New Roman', 'Georgia', serif;
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