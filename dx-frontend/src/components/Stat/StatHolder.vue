<template xmlns="http://www.w3.org/1999/html">
  <div class="stat-holder">
    <h2 v-if="title" class="header">{{ title }}</h2>
    <div class="stat-list">
      <div v-for="stat in stats">
        <StatPresenter
            :key="stat.id"
            :stat="stat"
            :stats="stats"
            :editable="editable"
            :allowResetBaseStats="allowResetBaseStats"
            @increment="incrementStat"
            @decrement="decrementStat"
            @switchBaseStats="requestStatSwitch"
        />
      </div>
    </div>
    <!-- Modal to show the dice rolls -->
    <div>
      <SwitchBaseValuesModal
          :stats="stats"
          :isOpen="showModal && allowResetBaseStats"
          :initialFromStatId="preSelectedStat?.id"
          @switchBaseValues="handleSwitch"
          @closeModal="closeModal"
      />
    </div>
  </div>
</template>

<script>

import StatPresenter from "@/components/Stat/StatPresenter.vue";
import DiceNRolls from "@/components/Dice/DiceNRolls.vue";
import SwapResults from "@/components/Selectors/DiceStatsResults.vue";
import SwitchBaseValuesModal from "@/components/Modal/SwitchBaseValuesModal.vue";

export default {
  name: "StatHolder",
  components: {
    SwitchBaseValuesModal,
    SwapResults,
    DiceNRolls,
    StatPresenter,
  },
  data() {
    return {
      showModal: false,
      preSelectedStat: null,
    };
  },
  props: {
    allowResetBaseStats: {
      type: Boolean,
      required: false,
    },
    stats: {
      type: Array,
      required: true,
    },
    title: {
      type: String,
      required: false,
    },
    editable: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    requestStatSwitch(statId) {
      this.preSelectedStat = this.stats.find((stat) => stat.id === statId);
      this.openModal();
    },
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    handleSwitch({fromStatId, toStatId}) {
      this.$emit("switchBaseStats", {fromStatId, toStatId});
      this.closeModal();
    },
    incrementStat(id) {
      this.$emit("updateStat", {id, change: 1});
    },
    decrementStat(id) {
      this.$emit("updateStat", {id, change: -1});
    },
  },
};
</script>

<style scoped>
.stat-holder {
  display: flex;
  flex-direction: column;
  gap: 1em;
  margin: auto;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 0.5rem;
  padding: 1em;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
}

.header {
  color: white;
  font-size: 1.2em;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1em;
}

.stat-list {
  display: flex;
  flex-direction: column;
  gap: 1em;
}
</style>
