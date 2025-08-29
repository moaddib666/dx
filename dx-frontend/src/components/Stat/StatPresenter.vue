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

<script>
import StatsGameService from "@/services/statService.js";
import DiceNRolls from "@/components/Dice/DiceNRolls.vue";
import SwapIcon from "@/components/icons/Swap.vue";

export default {
  name: "StatPresenter",
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

<style scoped>
.stat-presenter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(43, 43, 43, 0.9);
  padding: 0.5em 1em;
  border-radius: 0.5em;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  gap: 1em;
}

.stat-icon {
  width: 2.5em;
  height: 2.5em;
  border-radius: 50%;
  object-fit: contain;
}

.stat-name {
  flex: 1;
  color: white;
  font-weight: bold;
  font-size: 1.2em;
  text-transform: capitalize;
}

.stat-value {
  display: flex;
  align-items: center;
  gap: 0.5em;
}

.adjust-button {
  background: rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 0.2em;
  padding: 0.2em 0.5em;
  font-size: 0.9em;
  cursor: pointer;
  transition: background 0.2s ease;
}

.adjust-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.adjust-button:not(:disabled):hover {
  background: rgba(255, 255, 255, 0.4);
}

.value {
  font-size: 1.2em;
  font-weight: bold;
  color: white;
  width: 3rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.3rem;
  padding: 0.2em 0.5em;
}

.swap-icon {
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  color: rgba(255, 255, 255, 0.8);
}
</style>
